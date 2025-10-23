# M5Stack Tab5 UI Components & Patterns

**Purpose:** Common patterns for M5Stack Tab5 applications (touch input, display management, UI components)

**Auto-activation keywords:** `M5Stack`, `Tab5`, `touch`, `gesture`, `display`, `UI components`, `LVGL`, `buttons`

---

## Quick Start

Use this skill when developing Tab5 apps:
- Handle touch input (tap, swipe, long press)
- Manage display updates and rendering
- Implement common UI components (buttons, cards, lists)
- Handle navigation and state transitions

---

## Touch Input Handling

### Basic Touch Detection

```cpp
#include "M5GFX.h"

M5GFX display;

void touch_example() {
    // Initialize M5Stack display
    display.begin();

    auto touch_point = display.getTouch();

    if (touch_point.x != -1) {  // -1 means no touch
        // Touch detected at (touch_point.x, touch_point.y)
        printf("Touch at: %d, %d\n", touch_point.x, touch_point.y);
    }
}
```

### Touch State Machine (Tap vs Long Press)

```cpp
#include "esp_timer.h"

typedef enum {
    TOUCH_IDLE = 0,
    TOUCH_DOWN = 1,
    TOUCH_PRESSED = 2,  // Long press
    TOUCH_RELEASED = 3,
} touch_state_t;

typedef struct {
    touch_state_t state;
    int32_t x, y;
    uint64_t press_time_us;
    bool is_long_press;
} touch_event_t;

#define LONG_PRESS_THRESHOLD_MS 500

touch_event_t detect_touch_event() {
    static touch_event_t event = {TOUCH_IDLE, 0, 0, 0, false};
    static bool was_touched = false;

    auto touch = display.getTouch();
    uint64_t current_time = esp_timer_get_time();

    if (touch.x != -1) {
        // Touch down
        if (!was_touched) {
            event.state = TOUCH_DOWN;
            event.x = touch.x;
            event.y = touch.y;
            event.press_time_us = current_time;
            event.is_long_press = false;
            was_touched = true;
        } else {
            // Still touching
            uint64_t press_duration_ms = (current_time - event.press_time_us) / 1000;

            if (press_duration_ms > LONG_PRESS_THRESHOLD_MS && !event.is_long_press) {
                event.state = TOUCH_PRESSED;
                event.is_long_press = true;
            }
        }
    } else {
        // Touch released
        if (was_touched) {
            event.state = TOUCH_RELEASED;
            was_touched = false;
        } else {
            event.state = TOUCH_IDLE;
        }
    }

    return event;
}
```

### Gesture Detection: Swipe

```cpp
typedef enum {
    GESTURE_NONE = 0,
    GESTURE_SWIPE_LEFT = 1,
    GESTURE_SWIPE_RIGHT = 2,
    GESTURE_SWIPE_UP = 3,
    GESTURE_SWIPE_DOWN = 4,
} gesture_t;

typedef struct {
    gesture_t gesture;
    int32_t start_x, start_y;
    int32_t end_x, end_y;
    uint64_t duration_ms;
} gesture_event_t;

#define SWIPE_THRESHOLD_PX 50
#define SWIPE_MIN_VELOCITY_PX_MS 100

gesture_event_t detect_swipe() {
    static int32_t touch_start_x = 0, touch_start_y = 0;
    static uint64_t touch_start_time = 0;
    static bool tracking = false;

    gesture_event_t result = {GESTURE_NONE, 0, 0, 0, 0, 0};

    auto touch = display.getTouch();
    uint64_t current_time = esp_timer_get_time();

    if (touch.x != -1) {
        if (!tracking) {
            // New touch
            touch_start_x = touch.x;
            touch_start_y = touch.y;
            touch_start_time = current_time;
            tracking = true;
        }
    } else {
        // Touch released - check if it was a swipe
        if (tracking) {
            uint64_t duration_ms = (current_time - touch_start_time) / 1000;
            int32_t dx = touch.x - touch_start_x;
            int32_t dy = touch.y - touch_start_y;
            int32_t distance = sqrt(dx*dx + dy*dy);

            if (distance > SWIPE_THRESHOLD_PX && duration_ms > 0) {
                int32_t velocity = distance / duration_ms;  // px/ms

                if (velocity > SWIPE_MIN_VELOCITY_PX_MS) {
                    // Determine swipe direction
                    if (abs(dx) > abs(dy)) {
                        // Horizontal swipe
                        result.gesture = dx > 0 ? GESTURE_SWIPE_RIGHT : GESTURE_SWIPE_LEFT;
                    } else {
                        // Vertical swipe
                        result.gesture = dy > 0 ? GESTURE_SWIPE_DOWN : GESTURE_SWIPE_UP;
                    }

                    result.start_x = touch_start_x;
                    result.start_y = touch_start_y;
                    result.end_x = touch.x;
                    result.end_y = touch.y;
                    result.duration_ms = duration_ms;
                }
            }

            tracking = false;
        }
    }

    return result;
}
```

---

## Display Management

### M5Stack Tab5 Display Specs

```cpp
// M5Stack Tab5 (with ILI9341 or similar)
#define DISPLAY_WIDTH 320
#define DISPLAY_HEIGHT 240
#define DISPLAY_COLOR_DEPTH 16  // 16-bit RGB565
```

### Double Buffering Pattern

```cpp
#include <vector>

class DoubleBufferedDisplay {
private:
    std::vector<uint16_t> buffer1;
    std::vector<uint16_t> buffer2;
    std::vector<uint16_t>* front_buffer;
    std::vector<uint16_t>* back_buffer;

public:
    DoubleBufferedDisplay() {
        buffer1.resize(DISPLAY_WIDTH * DISPLAY_HEIGHT);
        buffer2.resize(DISPLAY_WIDTH * DISPLAY_HEIGHT);
        front_buffer = &buffer1;
        back_buffer = &buffer2;
    }

    void draw_on_back_buffer(int x, int y, uint16_t color) {
        if (x >= 0 && x < DISPLAY_WIDTH && y >= 0 && y < DISPLAY_HEIGHT) {
            (*back_buffer)[y * DISPLAY_WIDTH + x] = color;
        }
    }

    void swap_buffers() {
        std::swap(front_buffer, back_buffer);
        // Send front_buffer to display
        display.pushImage(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT,
                         (uint16_t*)front_buffer->data());
    }

    void clear_back_buffer(uint16_t color = 0x0000) {
        std::fill(back_buffer->begin(), back_buffer->end(), color);
    }
};
```

### Efficient Display Updates (Dirty Region)

```cpp
struct DirtyRegion {
    int x_min, y_min, x_max, y_max;
    bool is_dirty;
};

void update_only_dirty_region(DirtyRegion& region) {
    if (!region.is_dirty) return;

    int width = region.x_max - region.x_min;
    int height = region.y_max - region.y_min;

    uint16_t* line_buffer = (uint16_t*)malloc(width * sizeof(uint16_t));

    for (int y = region.y_min; y < region.y_max; y++) {
        // Prepare line data
        for (int x = region.x_min; x < region.x_max; x++) {
            line_buffer[x - region.x_min] = get_pixel_color(x, y);
        }

        // Send only this line to display
        display.pushImage(region.x_min, y, width, 1, line_buffer);
    }

    free(line_buffer);
    region.is_dirty = false;
}
```

---

## Common UI Components

### Button Component

```cpp
typedef struct {
    int x, y, width, height;
    const char* label;
    uint16_t bg_color;
    uint16_t text_color;
    bool pressed;
    bool hovered;
} Button;

bool button_is_clicked(Button& btn, touch_event_t touch) {
    // Check if touch is within button bounds
    bool in_bounds =
        touch.x >= btn.x &&
        touch.x < btn.x + btn.width &&
        touch.y >= btn.y &&
        touch.y < btn.y + btn.height;

    // Click = touch up within bounds
    if (touch.state == TOUCH_RELEASED && in_bounds) {
        return true;
    }

    // Update hover state
    btn.hovered = in_bounds && touch.state == TOUCH_DOWN;

    return false;
}

void button_draw(Button& btn) {
    uint16_t color = btn.hovered ? 0xFFFF : btn.bg_color;  // Lighten on hover

    // Draw background
    display.fillRect(btn.x, btn.y, btn.width, btn.height, color);

    // Draw border
    display.drawRect(btn.x, btn.y, btn.width, btn.height, 0x0000);

    // Draw text (centered)
    display.setTextColor(btn.text_color);
    display.setTextDatum(MC_DATUM);  // Middle-center
    display.drawString(btn.label,
                      btn.x + btn.width/2,
                      btn.y + btn.height/2);
}
```

### Card Component (Touchable List Item)

```cpp
typedef struct {
    int x, y, width, height;
    const char* title;
    const char* subtitle;
    uint32_t id;
    bool selected;
} Card;

void card_draw(Card& card) {
    uint16_t bg_color = card.selected ? 0x841F : 0xFFFF;  // Blue if selected

    // Background
    display.fillRect(card.x, card.y, card.width, card.height, bg_color);

    // Border
    display.drawRect(card.x, card.y, card.width, card.height, 0x0000);

    // Title
    display.setTextColor(0x0000);
    display.setTextSize(2);
    display.drawString(card.title, card.x + 10, card.y + 5);

    // Subtitle
    display.setTextSize(1);
    display.drawString(card.subtitle, card.x + 10, card.y + 25);
}

bool card_is_tapped(Card& card, touch_event_t touch) {
    return touch.state == TOUCH_RELEASED &&
           touch.x >= card.x && touch.x < card.x + card.width &&
           touch.y >= card.y && touch.y < card.y + card.height;
}
```

### Progress Bar

```cpp
typedef struct {
    int x, y, width, height;
    float progress;  // 0.0 to 1.0
    uint16_t fg_color, bg_color;
} ProgressBar;

void progress_bar_draw(ProgressBar& bar) {
    // Background
    display.fillRect(bar.x, bar.y, bar.width, bar.height, bar.bg_color);

    // Foreground (progress)
    int filled_width = (int)(bar.width * bar.progress);
    display.fillRect(bar.x, bar.y, filled_width, bar.height, bar.fg_color);

    // Border
    display.drawRect(bar.x, bar.y, bar.width, bar.height, 0x0000);
}

void progress_bar_set_progress(ProgressBar& bar, float progress) {
    bar.progress = progress < 0.0f ? 0.0f : (progress > 1.0f ? 1.0f : progress);
}
```

---

## Navigation Pattern: Modal Stack

```cpp
typedef enum {
    SCREEN_HOME = 0,
    SCREEN_SETTINGS = 1,
    SCREEN_DETAIL = 2,
} screen_t;

typedef struct {
    screen_t screen_stack[10];
    int stack_depth;
} NavigationStack;

NavigationStack nav;

void nav_push(screen_t screen) {
    if (nav.stack_depth < 10) {
        nav.screen_stack[nav.stack_depth++] = screen;
    }
}

void nav_pop() {
    if (nav.stack_depth > 0) {
        nav.stack_depth--;
    }
}

screen_t nav_current() {
    return nav.screen_depth > 0 ?
        nav.screen_stack[nav.stack_depth - 1] :
        SCREEN_HOME;
}

void nav_replace(screen_t screen) {
    if (nav.stack_depth > 0) {
        nav.screen_stack[nav.stack_depth - 1] = screen;
    }
}
```

---

## State Management: Screen States

```cpp
typedef enum {
    STATE_IDLE = 0,
    STATE_LOADING = 1,
    STATE_ERROR = 2,
    STATE_DISPLAYING = 3,
} app_state_t;

typedef struct {
    app_state_t state;
    const char* error_message;
    uint32_t last_state_change_ms;
    uint32_t state_duration_ms;
} AppContext;

void app_update_state(AppContext& ctx, app_state_t new_state) {
    ctx.state = new_state;
    ctx.last_state_change_ms = millis();
    ctx.state_duration_ms = 0;

    switch (new_state) {
        case STATE_LOADING:
            // Show loading spinner
            display_show_loading();
            break;
        case STATE_ERROR:
            // Show error message
            display_show_error(ctx.error_message);
            break;
        case STATE_DISPLAYING:
            // Show content
            display_show_content();
            break;
        default:
            break;
    }
}

void app_tick(AppContext& ctx) {
    ctx.state_duration_ms = millis() - ctx.last_state_change_ms;

    // Auto-transition from loading if timeout
    if (ctx.state == STATE_LOADING && ctx.state_duration_ms > 5000) {
        app_update_state(ctx, STATE_ERROR);
        ctx.error_message = "Timeout loading data";
    }
}
```

---

## Performance Optimizations

### Minimize Redraws

```cpp
class SmartDisplay {
private:
    bool needs_redraw = true;

public:
    void mark_dirty() {
        needs_redraw = true;
    }

    void render() {
        if (!needs_redraw) return;  // Skip if nothing changed

        // Perform expensive draw operations
        // ... render all components ...

        needs_redraw = false;
    }
};
```

### Memory-Efficient Image Loading

```cpp
// Instead of loading full image into RAM
// Stream image data in chunks
void draw_image_from_sd_card(const char* path, int x, int y) {
    File file = SD.open(path);
    uint16_t buffer[320];  // One line at a time

    for (int row = 0; row < 240; row++) {
        file.read((uint8_t*)buffer, 320 * 2);
        display.pushImage(x, y + row, 320, 1, buffer);
    }

    file.close();
}
```

---

## LVGL Integration (Modern Alternative)

M5Stack Tab5 can also use LVGL (Light and Versatile Graphics Library) for more advanced UIs:

```cpp
#include "lvgl.h"

void setup_lvgl_display() {
    lv_init();

    // Create display object
    static lv_disp_draw_buf_t draw_buf;
    static uint16_t buf[320 * 240];
    lv_disp_draw_buf_init(&draw_buf, buf, NULL, 320 * 240);

    static lv_disp_drv_t disp_drv;
    lv_disp_drv_init(&disp_drv);
    disp_drv.draw_buf = &draw_buf;
    disp_drv.hor_res = 320;
    disp_drv.ver_res = 240;
    disp_drv.flush_cb = display_flush_callback;
    lv_disp_drv_register(&disp_drv);

    // Create touchpad input
    static lv_indev_drv_t indev_drv;
    lv_indev_drv_init(&indev_drv);
    indev_drv.type = LV_INDEV_TYPE_POINTER;
    indev_drv.read_cb = touchpad_read_callback;
    lv_indev_drv_register(&indev_drv);
}

void create_simple_ui() {
    // Create container
    lv_obj_t* cont = lv_obj_create(lv_scr_act());
    lv_obj_set_size(cont, 300, 200);
    lv_obj_center(cont);

    // Create button
    lv_obj_t* btn = lv_btn_create(cont);
    lv_obj_add_event_cb(btn, button_event_handler, LV_EVENT_CLICKED, NULL);

    // Create label for button
    lv_obj_t* label = lv_label_create(btn);
    lv_label_set_text(label, "Click Me!");
}
```

---

## Common Patterns: Pull-to-Refresh

```cpp
struct PullToRefreshState {
    int pull_distance;
    int refresh_threshold;
    bool is_refreshing;
    int start_y;
};

bool handle_pull_to_refresh(touch_event_t touch, PullToRefreshState& state) {
    if (touch.state == TOUCH_DOWN && touch.y < 50) {
        state.start_y = touch.y;
        return false;
    }

    if (touch.state != TOUCH_IDLE && state.start_y != 0) {
        state.pull_distance = touch.y - state.start_y;

        if (state.pull_distance > state.refresh_threshold && !state.is_refreshing) {
            state.is_refreshing = true;
            return true;  // Trigger refresh
        }
    }

    if (touch.state == TOUCH_RELEASED) {
        state.start_y = 0;
        state.pull_distance = 0;
    }

    return false;
}
```

---

## Related Skills

- **React** — Web component patterns (similar concepts)
- **M5Stack Documentation** — Hardware reference
- **FreeRTOS** — Task management for responsive UI

---

**Last Updated:** 2025-10-22
**Author:** Claude (M5Stack UI Patterns)
**Status:** Production Ready
