# FreeRTOS Task Synchronization Patterns

**Purpose:** Inter-task communication and synchronization primitives for PRISM.k1 firmware real-time constraints

**Auto-activation keywords:** `FreeRTOS`, `queue`, `semaphore`, `mutex`, `task synchronization`, `deadlock`, `race condition`, `real-time`

---

## Quick Start

Use this skill for:
- Safe communication between tasks (queues)
- Protecting shared resources (mutexes)
- Signaling completion of work (semaphores)
- Avoiding deadlocks and race conditions
- Meeting real-time deadlines (120 FPS = 8.33ms)

---

## Task Fundamentals

### Task Creation

```c
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// Task function signature
void my_task(void *arg) {
    while (1) {
        // Do work
        printf("Task running\n");
        vTaskDelay(pdMS_TO_TICKS(100));  // Yield for 100ms
    }
}

// Create task
void setup_task() {
    xTaskCreatePinnedToCore(
        my_task,              // Task function
        "my_task",            // Task name (for debugging)
        2048,                 // Stack size (bytes)
        NULL,                 // Parameter
        1,                    // Priority (0=idle, higher=more priority)
        NULL,                 // Task handle (for later reference)
        0);                   // Core affinity (0=Core 0, 1=Core 1)
}
```

### PRISM.k1 Task Organization

```c
// Priority levels for PRISM firmware
#define PRIORITY_IDLE           0
#define PRIORITY_LOGGING        1
#define PRIORITY_NETWORK        2  // WebSocket, WiFi
#define PRIORITY_LED_CONTROL    3  // Pattern playback (MUST be high)
#define PRIORITY_AUDIO_DSP      2  // Same as network
```

---

## Queues: Inter-Task Communication

### Basic Queue Usage

```c
#include "freertos/queue.h"

// Define message structure
typedef struct {
    uint32_t command;
    uint8_t data[64];
} CommandMessage;

// Create queue (capacity for 10 messages)
QueueHandle_t cmd_queue = xQueueCreate(10, sizeof(CommandMessage));

// Task 1: Producer (sends commands)
void producer_task(void *arg) {
    while (1) {
        CommandMessage msg = {
            .command = 0x01,
            .data = {0x12, 0x34, 0x56},
        };

        // Send message (blocking, timeout 100ms)
        if (xQueueSend(cmd_queue, &msg, pdMS_TO_TICKS(100)) != pdPASS) {
            printf("Queue full, message dropped\n");
        }

        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

// Task 2: Consumer (receives commands)
void consumer_task(void *arg) {
    CommandMessage msg;

    while (1) {
        // Wait for message (blocking, indefinite timeout)
        if (xQueueReceive(cmd_queue, &msg, portMAX_DELAY)) {
            printf("Received command: 0x%02X\n", msg.command);
            // Process message
        }
    }
}
```

### Queue with Timeout (Non-Blocking)

```c
// Try to receive, wait max 50ms, don't block forever
CommandMessage msg;
BaseType_t result = xQueueReceive(cmd_queue, &msg, pdMS_TO_TICKS(50));

if (result == pdPASS) {
    // Message received
} else if (result == pdFAIL) {
    // Timeout - do something else
    printf("No message available\n");
}
```

### PRISM LED Control Queue

```c
// Queue for LED patterns to upload
typedef struct {
    uint8_t pattern_id;
    uint32_t duration_ms;
    bool loop;
} LEDCommand;

QueueHandle_t led_queue = xQueueCreate(5, sizeof(LEDCommand));

// WebSocket task sends LED commands
void websocket_task(void *arg) {
    LEDCommand cmd = {
        .pattern_id = 42,
        .duration_ms = 5000,
        .loop = true,
    };

    xQueueSend(led_queue, &cmd, pdMS_TO_TICKS(100));
}

// LED control task receives and processes
void led_control_task(void *arg) {
    LEDCommand cmd;

    while (1) {
        // Receive with 8.33ms timeout (120 FPS deadline)
        if (xQueueReceive(led_queue, &cmd, pdMS_TO_TICKS(8))) {
            start_led_pattern(cmd.pattern_id, cmd.duration_ms, cmd.loop);
        }

        // Continue current pattern playback
        update_led_frame();
        vTaskDelay(pdMS_TO_TICKS(8));  // ~120 FPS
    }
}
```

### Peek at Queue Without Removing

```c
// Look at next message without removing it
LEDCommand cmd;
if (xQueuePeek(led_queue, &cmd, 0) == pdPASS) {
    printf("Next command is pattern %d\n", cmd.pattern_id);
    // Still in queue, consumer can still receive it
}
```

---

## Semaphores: Signaling

### Binary Semaphore (0 or 1)

```c
#include "freertos/semphr.h"

// Create binary semaphore (initially empty/0)
SemaphoreHandle_t button_pressed = xSemaphoreCreateBinary();

// ISR: Signal that button was pressed
void button_isr(void) {
    BaseType_t higher_priority_woken = pdFALSE;
    xSemaphoreGiveFromISR(button_pressed, &higher_priority_woken);

    if (higher_priority_woken) {
        portYIELD_FROM_ISR();
    }
}

// Task: Wait for button press
void button_handler_task(void *arg) {
    while (1) {
        // Block until semaphore is given
        if (xSemaphoreTake(button_pressed, portMAX_DELAY) == pdPASS) {
            printf("Button was pressed!\n");
            handle_button_press();
        }
    }
}
```

### Counting Semaphore

```c
// Semaphore with initial count of 3 (e.g., 3 buffers available)
SemaphoreHandle_t buffer_semaphore = xSemaphoreCreateCounting(3, 3);

// Task 1: Allocate buffer
void allocate_buffer(void) {
    if (xSemaphoreTake(buffer_semaphore, pdMS_TO_TICKS(100)) == pdPASS) {
        // Got a buffer, count is now 2
        process_buffer();

        // Return buffer when done
        xSemaphoreGive(buffer_semaphore);
        // Count is now 3 again
    } else {
        printf("No buffers available\n");
    }
}
```

### PRISM Audio-to-LED Synchronization

```c
// Signal that new audio frame is ready for LED processing
SemaphoreHandle_t audio_frame_ready = xSemaphoreCreateBinary();

// Audio DSP task: Signal when FFT is complete
void audio_dsp_task(void *arg) {
    while (1) {
        read_audio_samples();
        compute_fft();

        // Signal LED task that new analysis is ready
        xSemaphoreGive(audio_frame_ready);

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

// LED task: Wait for audio analysis, update LEDs
void led_audio_reactive_task(void *arg) {
    while (1) {
        // Block until audio frame is ready
        if (xSemaphoreTake(audio_frame_ready, pdMS_TO_TICKS(100)) == pdPASS) {
            // Audio analysis is fresh
            update_leds_from_audio();
        } else {
            // Timeout - keep last pattern alive
            hold_pattern();
        }

        send_to_led_driver();
        vTaskDelay(pdMS_TO_TICKS(8));  // 120 FPS
    }
}
```

---

## Mutexes: Protecting Shared Resources

### Basic Mutex Usage

```c
#include "freertos/semphr.h"

// Shared resource
typedef struct {
    uint8_t data[256];
    uint16_t length;
} SharedBuffer;

SharedBuffer shared_data;

// Create mutex to protect access
SemaphoreHandle_t data_mutex = xSemaphoreCreateMutex();

// Task 1: Write to shared resource
void writer_task(void *arg) {
    while (1) {
        // Acquire lock
        if (xSemaphoreTake(data_mutex, pdMS_TO_TICKS(100)) == pdPASS) {
            // Safely access shared_data
            shared_data.data[0] = 0x42;
            shared_data.length = 1;

            // Critical section ends here
            xSemaphoreGive(data_mutex);
        } else {
            printf("Mutex timeout\n");
        }

        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

// Task 2: Read from shared resource
void reader_task(void *arg) {
    while (1) {
        if (xSemaphoreTake(data_mutex, pdMS_TO_TICKS(100)) == pdPASS) {
            // Safely read shared_data
            printf("Data[0] = 0x%02X, Length = %d\n",
                   shared_data.data[0],
                   shared_data.length);

            xSemaphoreGive(data_mutex);
        }

        vTaskDelay(pdMS_TO_TICKS(500));
    }
}
```

### PRISM LED Pattern Storage Protection

```c
// Shared LED pattern storage
typedef struct {
    uint8_t pattern_data[4096];
    uint16_t pattern_size;
    uint32_t crc32;
} LEDPattern;

LEDPattern current_pattern;
SemaphoreHandle_t pattern_mutex = xSemaphoreCreateMutex();

// WebSocket task: Receive and store pattern
void websocket_pattern_upload_task(void *arg) {
    uint8_t incoming_pattern[4096];

    while (1) {
        receive_pattern_from_ws(incoming_pattern);

        // Lock pattern storage
        if (xSemaphoreTake(pattern_mutex, pdMS_TO_TICKS(500)) == pdPASS) {
            // Safely update pattern
            memcpy(current_pattern.pattern_data, incoming_pattern, 4096);
            current_pattern.pattern_size = 4096;
            current_pattern.crc32 = calculate_crc32(incoming_pattern, 4096);

            xSemaphoreGive(pattern_mutex);
            printf("Pattern updated\n");
        }
    }
}

// LED playback task: Read and render pattern
void led_playback_task(void *arg) {
    while (1) {
        // Lock pattern storage (short timeout - must not block frame timing)
        if (xSemaphoreTake(pattern_mutex, 0) == pdPASS) {
            // Safe to read current_pattern
            render_pattern_frame(&current_pattern);
            xSemaphoreGive(pattern_mutex);
        } else {
            // Couldn't acquire lock - keep last rendered frame
            repeat_last_frame();
        }

        send_to_leds();
        vTaskDelay(pdMS_TO_TICKS(8));  // 120 FPS
    }
}
```

---

## Avoiding Deadlocks

### ❌ DEADLOCK SCENARIO

```c
// Two mutexes
SemaphoreHandle_t mutex_a = xSemaphoreCreateMutex();
SemaphoreHandle_t mutex_b = xSemaphoreCreateMutex();

// Task 1: Takes A, then tries to take B
void task_1(void *arg) {
    xSemaphoreTake(mutex_a, portMAX_DELAY);
    // ... do work ...
    xSemaphoreTake(mutex_b, portMAX_DELAY);  // Blocks waiting for B
    // ... more work ...
    xSemaphoreGive(mutex_b);
    xSemaphoreGive(mutex_a);
}

// Task 2: Takes B, then tries to take A
void task_2(void *arg) {
    xSemaphoreTake(mutex_b, portMAX_DELAY);
    // ... do work ...
    xSemaphoreTake(mutex_a, portMAX_DELAY);  // Blocks waiting for A
    // Task 1 holds A, waiting for B that Task 2 holds
    // Task 2 holds B, waiting for A that Task 1 holds
    // DEADLOCK!
}
```

### ✓ FIX: Consistent Lock Ordering

```c
// ALWAYS take in same order: A before B
void task_1(void *arg) {
    xSemaphoreTake(mutex_a, portMAX_DELAY);
    xSemaphoreTake(mutex_b, portMAX_DELAY);
    // ... work ...
    xSemaphoreGive(mutex_b);
    xSemaphoreGive(mutex_a);
}

void task_2(void *arg) {
    xSemaphoreTake(mutex_a, portMAX_DELAY);  // Same order!
    xSemaphoreTake(mutex_b, portMAX_DELAY);
    // ... work ...
    xSemaphoreGive(mutex_b);
    xSemaphoreGive(mutex_a);
}
```

### ✓ BETTER: Use Timeouts to Detect Deadlock

```c
void safe_task(void *arg) {
    if (xSemaphoreTake(mutex_a, pdMS_TO_TICKS(100)) != pdPASS) {
        printf("ERROR: Could not acquire mutex_a within 100ms\n");
        return;  // Abort instead of hanging forever
    }

    if (xSemaphoreTake(mutex_b, pdMS_TO_TICKS(100)) != pdPASS) {
        printf("ERROR: Could not acquire mutex_b within 100ms\n");
        xSemaphoreGive(mutex_a);  // Release first lock
        return;
    }

    // Safe to proceed
    xSemaphoreGive(mutex_b);
    xSemaphoreGive(mutex_a);
}
```

---

## Race Conditions: Multi-Writer Safety

### ❌ RACE CONDITION

```c
uint32_t frame_counter = 0;

// Task 1: Increment counter
void increment_task(void *arg) {
    while (1) {
        frame_counter++;  // NOT ATOMIC! 3+ operations:
        // 1. Read frame_counter
        // 2. Increment
        // 3. Write back
        // Task 2 might interrupt between steps!
        vTaskDelay(pdMS_TO_TICKS(1));
    }
}

// Task 2: Also increments
void increment_task_2(void *arg) {
    while (1) {
        frame_counter++;  // Race condition!
        vTaskDelay(pdMS_TO_TICKS(1));
    }
}
```

### ✓ FIX: Protect with Mutex

```c
SemaphoreHandle_t counter_mutex = xSemaphoreCreateMutex();

void safe_increment_task(void *arg) {
    while (1) {
        xSemaphoreTake(counter_mutex, portMAX_DELAY);
        frame_counter++;  // Now atomic
        xSemaphoreGive(counter_mutex);

        vTaskDelay(pdMS_TO_TICKS(1));
    }
}
```

### ✓ ATOMIC ALTERNATIVE: Use Atomic Operations

```c
// ESP32 supports atomic operations for single variables
volatile uint32_t atomic_counter = 0;

void atomic_increment_task(void *arg) {
    while (1) {
        // Single atomic instruction - no mutex needed
        __atomic_fetch_add(&atomic_counter, 1, __ATOMIC_SEQ_CST);
        vTaskDelay(pdMS_TO_TICKS(1));
    }
}
```

---

## Event Groups: Multiple Conditions

```c
#include "freertos/event_groups.h"

// Define event bits
#define WIFI_CONNECTED_BIT  (1 << 0)  // Bit 0
#define DEVICE_READY_BIT    (1 << 1)  // Bit 1
#define PATTERN_LOADED_BIT  (1 << 2)  // Bit 2

EventGroupHandle_t system_events = xEventGroupCreate();

// WiFi task: Signal when connected
void wifi_task(void *arg) {
    while (1) {
        if (connect_to_wifi()) {
            xEventGroupSetBits(system_events, WIFI_CONNECTED_BIT);
        }
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

// Pattern loader: Wait for both WiFi AND device ready
void pattern_loader_task(void *arg) {
    EventBits_t bits;

    while (1) {
        // Wait for BOTH bits to be set (max 5 second timeout)
        bits = xEventGroupWaitBits(
            system_events,
            WIFI_CONNECTED_BIT | DEVICE_READY_BIT,
            pdFALSE,  // Don't clear bits
            pdTRUE,   // Wait for ALL bits
            pdMS_TO_TICKS(5000));

        if (bits & (WIFI_CONNECTED_BIT | DEVICE_READY_BIT)) {
            load_pattern_from_cloud();
        } else {
            printf("System not ready\n");
        }

        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
```

---

## Real-Time Constraints: Meeting 120 FPS Deadline

### Task Timing Analysis

```c
// PRISM.k1 timing budget (8.33ms per frame = 120 FPS)
void led_frame_task(void *arg) {
    uint32_t last_wake_time = xTaskGetTickCount();

    while (1) {
        uint32_t start = esp_timer_get_time();

        // 1. Acquire pattern data (0.5ms max)
        xSemaphoreTake(pattern_mutex, pdMS_TO_TICKS(1));
        memcpy(&local_pattern, &current_pattern, sizeof(LEDPattern));
        xSemaphoreGive(pattern_mutex);

        // 2. Check for new WebSocket commands (0.2ms max)
        LEDCommand cmd;
        while (xQueueReceive(led_queue, &cmd, 0) == pdPASS) {
            apply_command(&cmd);
        }

        // 3. Render frame (3-4ms)
        render_frame(&local_pattern);

        // 4. Send to LED driver (2-3ms)
        send_to_leds();

        uint32_t elapsed = (esp_timer_get_time() - start) / 1000;  // Convert to ms

        if (elapsed > 8) {
            printf("WARN: Frame took %ldms, deadline missed!\n", elapsed);
        }

        // Wait for next frame slot (periodic task)
        vTaskDelayUntil(&last_wake_time, pdMS_TO_TICKS(8));
    }
}
```

### Priority Inversion Prevention

```c
// If high-priority LED task waits for mutex held by low-priority task,
// it gets delayed. Solution: Priority inheritance (automatic in FreeRTOS)

// Create mutex with priority inheritance (enabled by default)
SemaphoreHandle_t protected_resource = xSemaphoreCreateMutex();

// HIGH priority task
void high_priority_task(void *arg) {
    while (1) {
        // Even if this waits for mutex, priority inheritance ensures
        // the lower-priority holder temporarily runs at high priority
        xSemaphoreTake(protected_resource, portMAX_DELAY);
        // ... work ...
        xSemaphoreGive(protected_resource);
    }
}

// LOW priority task
void low_priority_task(void *arg) {
    while (1) {
        xSemaphoreTake(protected_resource, portMAX_DELAY);
        // While holding mutex, runs at inherited high priority!
        // ... work ...
        xSemaphoreGive(protected_resource);
    }
}
```

---

## Debugging Task Synchronization

### Monitor Task Status

```c
void debug_task_status(void) {
    TaskStatus_t tasks[10];
    uint32_t count = uxTaskGetSystemState(tasks, 10, NULL);

    for (uint32_t i = 0; i < count; i++) {
        printf("Task: %s, Priority: %d, State: %d, Stack: %d\n",
               tasks[i].pcTaskName,
               tasks[i].uxCurrentPriority,
               tasks[i].eCurrentState,
               tasks[i].usStackHighWaterMark);
    }
}
```

### Check Semaphore Count

```c
UBaseType_t semaphore_count = uxSemaphoreGetCount(my_semaphore);
printf("Semaphore count: %d\n", semaphore_count);
```

---

## Related Skills

- **FreeRTOS Documentation** — Official API reference
- **PRISM.k1-Firmware** — Real-time requirements and constraints
- **Audio DSP Patterns** — Audio-to-LED synchronization example

---

**Last Updated:** 2025-10-22
**Author:** Claude (FreeRTOS Synchronization)
**Status:** Production Ready
