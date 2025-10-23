# React - Hooks

**Pages:** 62

---

## useState

**URL:** https://react.dev/reference/react/useState#my-initializer-or-updater-function-runs-twice

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## Built-in React DOM Hooks

**URL:** https://react.dev/reference/react-dom/hooks#undefined

**Contents:**
- Built-in React DOM Hooks
- Form Hooks

The react-dom package contains Hooks that are only supported for web applications (which run in the browser DOM environment). These Hooks are not supported in non-browser environments like iOS, Android, or Windows applications. If you are looking for Hooks that are supported in web browsers and other environments see the React Hooks page. This page lists all the Hooks in the react-dom package.

Forms let you create interactive controls for submitting information. To manage forms in your components, use one of these Hooks:

**Examples:**

Example 1 (javascript):
```javascript
function Form({ action }) {  async function increment(n) {    return n + 1;  }  const [count, incrementFormAction] = useActionState(increment, 0);  return (    <form action={action}>      <button formAction={incrementFormAction}>Count: {count}</button>      <Button />    </form>  );}function Button() {  const { pending } = useFormStatus();  return (    <button disabled={pending} type="submit">      Submit    </button>  );}
```

---

## useState

**URL:** https://react.dev/reference/react/useState#examples-initializer

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#im-trying-to-set-state-to-a-function-but-it-gets-called-instead

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## Built-in React Hooks

**URL:** https://react.dev/reference/react/hooks#your-own-hooks

**Contents:**
- Built-in React Hooks
- State Hooks
- Context Hooks
- Ref Hooks
- Effect Hooks
- Performance Hooks
- Other Hooks
- Your own Hooks

Hooks let you use different React features from your components. You can either use the built-in Hooks or combine them to build your own. This page lists all built-in Hooks in React.

State lets a component “remember” information like user input. For example, a form component can use state to store the input value, while an image gallery component can use state to store the selected image index.

To add state to a component, use one of these Hooks:

Context lets a component receive information from distant parents without passing it as props. For example, your app’s top-level component can pass the current UI theme to all components below, no matter how deep.

Refs let a component hold some information that isn’t used for rendering, like a DOM node or a timeout ID. Unlike with state, updating a ref does not re-render your component. Refs are an “escape hatch” from the React paradigm. They are useful when you need to work with non-React systems, such as the built-in browser APIs.

Effects let a component connect to and synchronize with external systems. This includes dealing with network, browser DOM, animations, widgets written using a different UI library, and other non-React code.

Effects are an “escape hatch” from the React paradigm. Don’t use Effects to orchestrate the data flow of your application. If you’re not interacting with an external system, you might not need an Effect.

There are two rarely used variations of useEffect with differences in timing:

A common way to optimize re-rendering performance is to skip unnecessary work. For example, you can tell React to reuse a cached calculation or to skip a re-render if the data has not changed since the previous render.

To skip calculations and unnecessary re-rendering, use one of these Hooks:

Sometimes, you can’t skip re-rendering because the screen actually needs to update. In that case, you can improve performance by separating blocking updates that must be synchronous (like typing into an input) from non-blocking updates which don’t need to block the user interface (like updating a chart).

To prioritize rendering, use one of these Hooks:

These Hooks are mostly useful to library authors and aren’t commonly used in the application code.

You can also define your own custom Hooks as JavaScript functions.

**Examples:**

Example 1 (javascript):
```javascript
function ImageGallery() {  const [index, setIndex] = useState(0);  // ...
```

Example 2 (javascript):
```javascript
function Button() {  const theme = useContext(ThemeContext);  // ...
```

Example 3 (javascript):
```javascript
function Form() {  const inputRef = useRef(null);  // ...
```

Example 4 (javascript):
```javascript
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...
```

---

## useRef

**URL:** https://react.dev/reference/react/useRef

**Contents:**
- useRef
- Reference
  - useRef(initialValue)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Referencing a value with a ref
    - Examples of referencing a value with useRef
    - Example 1 of 2: Click counter

useRef is a React Hook that lets you reference a value that’s not needed for rendering.

Call useRef at the top level of your component to declare a ref.

See more examples below.

useRef returns an object with a single property:

On the next renders, useRef will return the same object.

Call useRef at the top level of your component to declare one or more refs.

useRef returns a ref object with a single current property initially set to the initial value you provided.

On the next renders, useRef will return the same object. You can change its current property to store information and read it later. This might remind you of state, but there is an important difference.

Changing a ref does not trigger a re-render. This means refs are perfect for storing information that doesn’t affect the visual output of your component. For example, if you need to store an interval ID and retrieve it later, you can put it in a ref. To update the value inside the ref, you need to manually change its current property:

Later, you can read that interval ID from the ref so that you can call clear that interval:

By using a ref, you ensure that:

Changing a ref does not trigger a re-render, so refs are not appropriate for storing information you want to display on the screen. Use state for that instead. Read more about choosing between useRef and useState.

This component uses a ref to keep track of how many times the button was clicked. Note that it’s okay to use a ref instead of state here because the click count is only read and written in an event handler.

If you show {ref.current} in the JSX, the number won’t update on click. This is because setting ref.current does not trigger a re-render. Information that’s used for rendering should be state instead.

Do not write or read ref.current during rendering.

React expects that the body of your component behaves like a pure function:

Reading or writing a ref during rendering breaks these expectations.

You can read or write refs from event handlers or effects instead.

If you have to read or write something during rendering, use state instead.

When you break these rules, your component might still work, but most of the newer features we’re adding to React will rely on these expectations. Read more about keeping your components pure.

It’s particularly common to use a ref to manipulate the DOM. React has built-in support for this.

First, declare a ref object with an initial value of null:

Then pass your ref object as the r

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const ref = useRef(initialValue)
```

Example 2 (python):
```python
import { useRef } from 'react';function MyComponent() {  const intervalRef = useRef(0);  const inputRef = useRef(null);  // ...
```

Example 3 (python):
```python
import { useRef } from 'react';function Stopwatch() {  const intervalRef = useRef(0);  // ...
```

Example 4 (javascript):
```javascript
function handleStartClick() {  const intervalId = setInterval(() => {    // ...  }, 1000);  intervalRef.current = intervalId;}
```

---

## useState

**URL:** https://react.dev/reference/react/useState#passing-the-updater-function

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#reference

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#troubleshooting

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useFormStatus

**URL:** https://react.dev/reference/react-dom/hooks/useFormStatus

**Contents:**
- useFormStatus
- Reference
  - useFormStatus()
    - Parameters
    - Returns
    - Caveats
- Usage
  - Display a pending state during form submission
  - Pitfall
      - useFormStatus will not return status information for a <form> rendered in the same component.

useFormStatus is a Hook that gives you status information of the last form submission.

The useFormStatus Hook provides status information of the last form submission.

To get status information, the Submit component must be rendered within a <form>. The Hook returns information like the pending property which tells you if the form is actively submitting.

In the above example, Submit uses this information to disable <button> presses while the form is submitting.

See more examples below.

useFormStatus does not take any parameters.

A status object with the following properties:

pending: A boolean. If true, this means the parent <form> is pending submission. Otherwise, false.

data: An object implementing the FormData interface that contains the data the parent <form> is submitting. If there is no active submission or no parent <form>, it will be null.

method: A string value of either 'get' or 'post'. This represents whether the parent <form> is submitting with either a GET or POST HTTP method. By default, a <form> will use the GET method and can be specified by the method property.

To display a pending state while a form is submitting, you can call the useFormStatus Hook in a component rendered in a <form> and read the pending property returned.

Here, we use the pending property to indicate the form is submitting.

The useFormStatus Hook only returns status information for a parent <form> and not for any <form> rendered in the same component calling the Hook, or child components.

Instead call useFormStatus from inside a component that is located inside <form>.

You can use the data property of the status information returned from useFormStatus to display what data is being submitted by the user.

Here, we have a form where users can request a username. We can use useFormStatus to display a temporary status message confirming what username they have requested.

useFormStatus will only return status information for a parent <form>.

If the component that calls useFormStatus is not nested in a <form>, status.pending will always return false. Verify useFormStatus is called in a component that is a child of a <form> element.

useFormStatus will not track the status of a <form> rendered in the same component. See Pitfall for more details.

**Examples:**

Example 1 (javascript):
```javascript
const { pending, data, method, action } = useFormStatus();
```

Example 2 (python):
```python
import { useFormStatus } from "react-dom";import action from './actions';function Submit() {  const status = useFormStatus();  return <button disabled={status.pending}>Submit</button>}export default function App() {  return (    <form action={action}>      <Submit />    </form>  );}
```

Example 3 (javascript):
```javascript
function Form() {  // 🚩 `pending` will never be true  // useFormStatus does not track the form rendered in this component  const { pending } = useFormStatus();  return <form action={submit}></form>;}
```

Example 4 (javascript):
```javascript
function Submit() {  // ✅ `pending` will be derived from the form that wraps the Submit component  const { pending } = useFormStatus();   return <button disabled={pending}>...</button>;}function Form() {  // This is the <form> `useFormStatus` tracks  return (    <form action={submit}>      <Submit />    </form>  );}
```

---

## useState

**URL:** https://react.dev/reference/react/useState#resetting-state-with-a-key

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#adding-state-to-a-component

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#passing-the-initializer-function

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#updating-objects-and-arrays-in-state

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useEffect

**URL:** https://react.dev/reference/react/useEffect

**Contents:**
- useEffect
- Reference
  - useEffect(setup, dependencies?)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Connecting to an external system
  - Note
    - Examples of connecting to an external system

useEffect is a React Hook that lets you synchronize a component with an external system.

Call useEffect at the top level of your component to declare an Effect:

See more examples below.

setup: The function with your Effect’s logic. Your setup function may also optionally return a cleanup function. When your component is added to the DOM, React will run your setup function. After every re-render with changed dependencies, React will first run the cleanup function (if you provided it) with the old values, and then run your setup function with the new values. After your component is removed from the DOM, React will run your cleanup function.

optional dependencies: The list of all reactive values referenced inside of the setup code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is configured for React, it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like [dep1, dep2, dep3]. React will compare each dependency with its previous value using the Object.is comparison. If you omit this argument, your Effect will re-run after every re-render of the component. See the difference between passing an array of dependencies, an empty array, and no dependencies at all.

useEffect returns undefined.

useEffect is a Hook, so you can only call it at the top level of your component or your own Hooks. You can’t call it inside loops or conditions. If you need that, extract a new component and move the state into it.

If you’re not trying to synchronize with some external system, you probably don’t need an Effect.

When Strict Mode is on, React will run one extra development-only setup+cleanup cycle before the first real setup. This is a stress-test that ensures that your cleanup logic “mirrors” your setup logic and that it stops or undoes whatever the setup is doing. If this causes a problem, implement the cleanup function.

If some of your dependencies are objects or functions defined inside the component, there is a risk that they will cause the Effect to re-run more often than needed. To fix this, remove unnecessary object and function dependencies. You can also extract state updates and non-reactive logic outside of your Effect.

If your Effect wasn’t caused by an interaction (like a click), React will generally let the browser paint the updated screen first before runn

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
useEffect(setup, dependencies?)
```

Example 2 (python):
```python
import { useState, useEffect } from 'react';import { createConnection } from './chat.js';function ChatRoom({ roomId }) {  const [serverUrl, setServerUrl] = useState('https://localhost:1234');  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => {      connection.disconnect();    };  }, [serverUrl, roomId]);  // ...}
```

Example 3 (python):
```python
import { useState, useEffect } from 'react';import { createConnection } from './chat.js';function ChatRoom({ roomId }) {  const [serverUrl, setServerUrl] = useState('https://localhost:1234');  useEffect(() => {  	const connection = createConnection(serverUrl, roomId);    connection.connect();  	return () => {      connection.disconnect();  	};  }, [serverUrl, roomId]);  // ...}
```

Example 4 (javascript):
```javascript
function useChatRoom({ serverUrl, roomId }) {  useEffect(() => {    const options = {      serverUrl: serverUrl,      roomId: roomId    };    const connection = createConnection(options);    connection.connect();    return () => connection.disconnect();  }, [roomId, serverUrl]);}
```

---

## Rules of Hooks

**URL:** https://react.dev/reference/rules/rules-of-hooks

**Contents:**
- Rules of Hooks
- Only call Hooks at the top level
  - Note
- Only call Hooks from React functions

Hooks are defined using JavaScript functions, but they represent a special type of reusable UI logic with restrictions on where they can be called.

Functions whose names start with use are called Hooks in React.

Don’t call Hooks inside loops, conditions, nested functions, or try/catch/finally blocks. Instead, always use Hooks at the top level of your React function, before any early returns. You can only call Hooks while React is rendering a function component:

It’s not supported to call Hooks (functions starting with use) in any other cases, for example:

If you break these rules, you might see this error.

You can use the eslint-plugin-react-hooks plugin to catch these mistakes.

Custom Hooks may call other Hooks (that’s their whole purpose). This works because custom Hooks are also supposed to only be called while a function component is rendering.

Don’t call Hooks from regular JavaScript functions. Instead, you can:

✅ Call Hooks from React function components. ✅ Call Hooks from custom Hooks.

By following this rule, you ensure that all stateful logic in a component is clearly visible from its source code.

**Examples:**

Example 1 (javascript):
```javascript
function Counter() {  // ✅ Good: top-level in a function component  const [count, setCount] = useState(0);  // ...}function useWindowWidth() {  // ✅ Good: top-level in a custom Hook  const [width, setWidth] = useState(window.innerWidth);  // ...}
```

Example 2 (javascript):
```javascript
function Bad({ cond }) {  if (cond) {    // 🔴 Bad: inside a condition (to fix, move it outside!)    const theme = useContext(ThemeContext);  }  // ...}function Bad() {  for (let i = 0; i < 10; i++) {    // 🔴 Bad: inside a loop (to fix, move it outside!)    const theme = useContext(ThemeContext);  }  // ...}function Bad({ cond }) {  if (cond) {    return;  }  // 🔴 Bad: after a conditional return (to fix, move it before the return!)  const theme = useContext(ThemeContext);  // ...}function Bad() {  function handleClick() {    // 🔴 Bad: inside an event handler (to fix, move it outside!)    const 
...
```

Example 3 (javascript):
```javascript
function FriendList() {  const [onlineStatus, setOnlineStatus] = useOnlineStatus(); // ✅}function setOnlineStatus() { // ❌ Not a component or custom Hook!  const [onlineStatus, setOnlineStatus] = useOnlineStatus();}
```

---

## useState

**URL:** https://react.dev/reference/react/useState#is-using-an-updater-always-preferred

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useMemo

**URL:** https://react.dev/reference/react/useMemo

**Contents:**
- useMemo
  - Note
- Reference
  - useMemo(calculateValue, dependencies)
    - Parameters
    - Returns
    - Caveats
  - Note
- Usage
  - Skipping expensive recalculations

useMemo is a React Hook that lets you cache the result of a calculation between re-renders.

React Compiler automatically memoizes values and functions, reducing the need for manual useMemo calls. You can use the compiler to handle memoization automatically.

Call useMemo at the top level of your component to cache a calculation between re-renders:

See more examples below.

calculateValue: The function calculating the value that you want to cache. It should be pure, should take no arguments, and should return a value of any type. React will call your function during the initial render. On next renders, React will return the same value again if the dependencies have not changed since the last render. Otherwise, it will call calculateValue, return its result, and store it so it can be reused later.

dependencies: The list of all reactive values referenced inside of the calculateValue code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is configured for React, it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like [dep1, dep2, dep3]. React will compare each dependency with its previous value using the Object.is comparison.

On the initial render, useMemo returns the result of calling calculateValue with no arguments.

During next renders, it will either return an already stored value from the last render (if the dependencies haven’t changed), or call calculateValue again, and return the result that calculateValue has returned.

Caching return values like this is also known as memoization, which is why this Hook is called useMemo.

To cache a calculation between re-renders, wrap it in a useMemo call at the top level of your component:

You need to pass two things to useMemo:

On the initial render, the value you’ll get from useMemo will be the result of calling your calculation.

On every subsequent render, React will compare the dependencies with the dependencies you passed during the last render. If none of the dependencies have changed (compared with Object.is), useMemo will return the value you already calculated before. Otherwise, React will re-run your calculation and return the new value.

In other words, useMemo caches a calculation result between re-renders until its dependencies change.

Let’s walk through an example to see when this is useful.

By 

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const cachedValue = useMemo(calculateValue, dependencies)
```

Example 2 (python):
```python
import { useMemo } from 'react';function TodoList({ todos, tab }) {  const visibleTodos = useMemo(    () => filterTodos(todos, tab),    [todos, tab]  );  // ...}
```

Example 3 (python):
```python
import { useMemo } from 'react';function TodoList({ todos, tab, theme }) {  const visibleTodos = useMemo(() => filterTodos(todos, tab), [todos, tab]);  // ...}
```

Example 4 (javascript):
```javascript
function TodoList({ todos, tab, theme }) {  const visibleTodos = filterTodos(todos, tab);  // ...}
```

---

## useState

**URL:** https://react.dev/reference/react/useState#usestate

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## Reusing Logic with Custom Hooks

**URL:** https://react.dev/learn/reusing-logic-with-custom-hooks

**Contents:**
- Reusing Logic with Custom Hooks
  - You will learn
- Custom Hooks: Sharing logic between components
  - Extracting your own custom Hook from a component
  - Hook names always start with use
  - Note
      - Deep Dive
    - Should all functions called during rendering start with the use prefix?
  - Custom Hooks let you share stateful logic, not state itself
- Passing reactive values between Hooks

React comes with several built-in Hooks like useState, useContext, and useEffect. Sometimes, you’ll wish that there was a Hook for some more specific purpose: for example, to fetch data, to keep track of whether the user is online, or to connect to a chat room. You might not find these Hooks in React, but you can create your own Hooks for your application’s needs.

Imagine you’re developing an app that heavily relies on the network (as most apps do). You want to warn the user if their network connection has accidentally gone off while they were using your app. How would you go about it? It seems like you’ll need two things in your component:

This will keep your component synchronized with the network status. You might start with something like this:

Try turning your network on and off, and notice how this StatusBar updates in response to your actions.

Now imagine you also want to use the same logic in a different component. You want to implement a Save button that will become disabled and show “Reconnecting…” instead of “Save” while the network is off.

To start, you can copy and paste the isOnline state and the Effect into SaveButton:

Verify that, if you turn off the network, the button will change its appearance.

These two components work fine, but the duplication in logic between them is unfortunate. It seems like even though they have different visual appearance, you want to reuse the logic between them.

Imagine for a moment that, similar to useState and useEffect, there was a built-in useOnlineStatus Hook. Then both of these components could be simplified and you could remove the duplication between them:

Although there is no such built-in Hook, you can write it yourself. Declare a function called useOnlineStatus and move all the duplicated code into it from the components you wrote earlier:

At the end of the function, return isOnline. This lets your components read that value:

Verify that switching the network on and off updates both components.

Now your components don’t have as much repetitive logic. More importantly, the code inside them describes what they want to do (use the online status!) rather than how to do it (by subscribing to the browser events).

When you extract logic into custom Hooks, you can hide the gnarly details of how you deal with some external system or a browser API. The code of your components expresses your intent, not the implementation.

React applications are built from components. Components are built from Hook

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
function StatusBar() {  const isOnline = useOnlineStatus();  return <h1>{isOnline ? '✅ Online' : '❌ Disconnected'}</h1>;}function SaveButton() {  const isOnline = useOnlineStatus();  function handleSaveClick() {    console.log('✅ Progress saved');  }  return (    <button disabled={!isOnline} onClick={handleSaveClick}>      {isOnline ? 'Save progress' : 'Reconnecting...'}    </button>  );}
```

Example 2 (javascript):
```javascript
function useOnlineStatus() {  const [isOnline, setIsOnline] = useState(true);  useEffect(() => {    function handleOnline() {      setIsOnline(true);    }    function handleOffline() {      setIsOnline(false);    }    window.addEventListener('online', handleOnline);    window.addEventListener('offline', handleOffline);    return () => {      window.removeEventListener('online', handleOnline);      window.removeEventListener('offline', handleOffline);    };  }, []);  return isOnline;}
```

Example 3 (unknown):
```unknown
// 🔴 Avoid: A Hook that doesn't use Hooksfunction useSorted(items) {  return items.slice().sort();}// ✅ Good: A regular function that doesn't use Hooksfunction getSorted(items) {  return items.slice().sort();}
```

Example 4 (javascript):
```javascript
function List({ items, shouldSort }) {  let displayedItems = items;  if (shouldSort) {    // ✅ It's ok to call getSorted() conditionally because it's not a Hook    displayedItems = getSorted(items);  }  // ...}
```

---

## Built-in React Hooks

**URL:** https://react.dev/reference/react/hooks#state-hooks

**Contents:**
- Built-in React Hooks
- State Hooks
- Context Hooks
- Ref Hooks
- Effect Hooks
- Performance Hooks
- Other Hooks
- Your own Hooks

Hooks let you use different React features from your components. You can either use the built-in Hooks or combine them to build your own. This page lists all built-in Hooks in React.

State lets a component “remember” information like user input. For example, a form component can use state to store the input value, while an image gallery component can use state to store the selected image index.

To add state to a component, use one of these Hooks:

Context lets a component receive information from distant parents without passing it as props. For example, your app’s top-level component can pass the current UI theme to all components below, no matter how deep.

Refs let a component hold some information that isn’t used for rendering, like a DOM node or a timeout ID. Unlike with state, updating a ref does not re-render your component. Refs are an “escape hatch” from the React paradigm. They are useful when you need to work with non-React systems, such as the built-in browser APIs.

Effects let a component connect to and synchronize with external systems. This includes dealing with network, browser DOM, animations, widgets written using a different UI library, and other non-React code.

Effects are an “escape hatch” from the React paradigm. Don’t use Effects to orchestrate the data flow of your application. If you’re not interacting with an external system, you might not need an Effect.

There are two rarely used variations of useEffect with differences in timing:

A common way to optimize re-rendering performance is to skip unnecessary work. For example, you can tell React to reuse a cached calculation or to skip a re-render if the data has not changed since the previous render.

To skip calculations and unnecessary re-rendering, use one of these Hooks:

Sometimes, you can’t skip re-rendering because the screen actually needs to update. In that case, you can improve performance by separating blocking updates that must be synchronous (like typing into an input) from non-blocking updates which don’t need to block the user interface (like updating a chart).

To prioritize rendering, use one of these Hooks:

These Hooks are mostly useful to library authors and aren’t commonly used in the application code.

You can also define your own custom Hooks as JavaScript functions.

**Examples:**

Example 1 (javascript):
```javascript
function ImageGallery() {  const [index, setIndex] = useState(0);  // ...
```

Example 2 (javascript):
```javascript
function Button() {  const theme = useContext(ThemeContext);  // ...
```

Example 3 (javascript):
```javascript
function Form() {  const inputRef = useRef(null);  // ...
```

Example 4 (javascript):
```javascript
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#ive-updated-the-state-but-logging-gives-me-the-old-value

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory#meet-your-first-hook

**Contents:**
- State: A Component's Memory
  - You will learn
- When a regular variable isn’t enough
- Adding a state variable
  - Meet your first Hook
  - Pitfall
  - Anatomy of useState
  - Note
- Giving a component multiple state variables
      - Deep Dive

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” should put a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

Here’s a component that renders a sculpture image. Clicking the “Next” button should show the next sculpture by changing the index to 1, then 2, and so on. However, this won’t work (you can try it!):

The handleClick event handler is updating a local variable, index. But two things prevent that change from being visible:

To update a component with new data, two things need to happen:

The useState Hook provides those two things:

To add a state variable, import useState from React at the top of the file:

Then, replace this line:

index is a state variable and setIndex is the setter function.

The [ and ] syntax here is called array destructuring and it lets you read values from an array. The array returned by useState always has exactly two items.

This is how they work together in handleClick:

Now clicking the “Next” button switches the current sculpture:

In React, useState, as well as any other function starting with “use”, is called a Hook.

Hooks are special functions that are only available while React is rendering (which we’ll get into in more detail on the next page). They let you “hook into” different React features.

State is just one of those features, but you will meet the other Hooks later.

Hooks—functions starting with use—can only be called at the top level of your components or your own Hooks. You can’t call Hooks inside conditions, loops, or other nested functions. Hooks are functions, but it’s helpful to think of them as unconditional declarations about your component’s needs. You “use” React features at the top of your component similar to how you “import” modules at the top of your file.

When you call useState, you are telling React that you want this component to remember something:

In this case, you want React to remember index.

The convention is to name this pair like const [something, setSomething]. You could name it anything you like, but conventions make things easier to understand across projects.

The only argument to useState is the initial value of your state variable. In this example, the

*[Content truncated]*

**Examples:**

Example 1 (python):
```python
import { useState } from 'react';
```

Example 2 (javascript):
```javascript
let index = 0;
```

Example 3 (javascript):
```javascript
const [index, setIndex] = useState(0);
```

Example 4 (unknown):
```unknown
function handleClick() {  setIndex(index + 1);}
```

---

## useState

**URL:** https://react.dev/reference/react/useState#counter-number

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#form-object

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#usage

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## Built-in React Hooks

**URL:** https://react.dev/reference/react/hooks#context-hooks

**Contents:**
- Built-in React Hooks
- State Hooks
- Context Hooks
- Ref Hooks
- Effect Hooks
- Performance Hooks
- Other Hooks
- Your own Hooks

Hooks let you use different React features from your components. You can either use the built-in Hooks or combine them to build your own. This page lists all built-in Hooks in React.

State lets a component “remember” information like user input. For example, a form component can use state to store the input value, while an image gallery component can use state to store the selected image index.

To add state to a component, use one of these Hooks:

Context lets a component receive information from distant parents without passing it as props. For example, your app’s top-level component can pass the current UI theme to all components below, no matter how deep.

Refs let a component hold some information that isn’t used for rendering, like a DOM node or a timeout ID. Unlike with state, updating a ref does not re-render your component. Refs are an “escape hatch” from the React paradigm. They are useful when you need to work with non-React systems, such as the built-in browser APIs.

Effects let a component connect to and synchronize with external systems. This includes dealing with network, browser DOM, animations, widgets written using a different UI library, and other non-React code.

Effects are an “escape hatch” from the React paradigm. Don’t use Effects to orchestrate the data flow of your application. If you’re not interacting with an external system, you might not need an Effect.

There are two rarely used variations of useEffect with differences in timing:

A common way to optimize re-rendering performance is to skip unnecessary work. For example, you can tell React to reuse a cached calculation or to skip a re-render if the data has not changed since the previous render.

To skip calculations and unnecessary re-rendering, use one of these Hooks:

Sometimes, you can’t skip re-rendering because the screen actually needs to update. In that case, you can improve performance by separating blocking updates that must be synchronous (like typing into an input) from non-blocking updates which don’t need to block the user interface (like updating a chart).

To prioritize rendering, use one of these Hooks:

These Hooks are mostly useful to library authors and aren’t commonly used in the application code.

You can also define your own custom Hooks as JavaScript functions.

**Examples:**

Example 1 (javascript):
```javascript
function ImageGallery() {  const [index, setIndex] = useState(0);  // ...
```

Example 2 (javascript):
```javascript
function Button() {  const theme = useContext(ThemeContext);  // ...
```

Example 3 (javascript):
```javascript
function Form() {  const inputRef = useRef(null);  // ...
```

Example 4 (javascript):
```javascript
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#parameters

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## React calls Components and Hooks

**URL:** https://react.dev/reference/rules/react-calls-components-and-hooks

**Contents:**
- React calls Components and Hooks
- Never call component functions directly
- Never pass around Hooks as regular values
  - Don’t dynamically mutate a Hook
  - Don’t dynamically use Hooks

React is responsible for rendering components and Hooks when necessary to optimize the user experience. It is declarative: you tell React what to render in your component’s logic, and React will figure out how best to display it to your user.

Components should only be used in JSX. Don’t call them as regular functions. React should call it.

React must decide when your component function is called during rendering. In React, you do this using JSX.

If a component contains Hooks, it’s easy to violate the Rules of Hooks when components are called directly in a loop or conditionally.

Letting React orchestrate rendering also allows a number of benefits:

Hooks should only be called inside of components or Hooks. Never pass it around as a regular value.

Hooks allow you to augment a component with React features. They should always be called as a function, and never passed around as a regular value. This enables local reasoning, or the ability for developers to understand everything a component can do by looking at that component in isolation.

Breaking this rule will cause React to not automatically optimize your component.

Hooks should be as “static” as possible. This means you shouldn’t dynamically mutate them. For example, this means you shouldn’t write higher order Hooks:

Hooks should be immutable and not be mutated. Instead of mutating a Hook dynamically, create a static version of the Hook with the desired functionality.

Hooks should also not be dynamically used: for example, instead of doing dependency injection in a component by passing a Hook as a value:

You should always inline the call of the Hook into that component and handle any logic in there.

This way, <Button /> is much easier to understand and debug. When Hooks are used in dynamic ways, it increases the complexity of your app greatly and inhibits local reasoning, making your team less productive in the long term. It also makes it easier to accidentally break the Rules of Hooks that Hooks should not be called conditionally. If you find yourself needing to mock components for tests, it’s better to mock the server instead to respond with canned data. If possible, it’s also usually more effective to test your app with end-to-end tests.

**Examples:**

Example 1 (unknown):
```unknown
function BlogPost() {  return <Layout><Article /></Layout>; // ✅ Good: Only use components in JSX}
```

Example 2 (unknown):
```unknown
function BlogPost() {  return <Layout>{Article()}</Layout>; // 🔴 Bad: Never call them directly}
```

Example 3 (javascript):
```javascript
function ChatInput() {  const useDataWithLogging = withLogging(useData); // 🔴 Bad: don't write higher order Hooks  const data = useDataWithLogging();}
```

Example 4 (javascript):
```javascript
function ChatInput() {  const data = useDataWithLogging(); // ✅ Good: Create a new version of the Hook}function useDataWithLogging() {  // ... Create a new version of the Hook and inline the logic here}
```

---

## useState

**URL:** https://react.dev/reference/react/useState#storing-information-from-previous-renders

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#ive-updated-the-state-but-the-screen-doesnt-update

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## Quick Start

**URL:** https://react.dev/learn#using-hooks

**Contents:**
- Quick Start
  - You will learn
- Creating and nesting components
- Writing markup with JSX
- Adding styles
- Displaying data
- Conditional rendering
- Rendering lists
- Responding to events
- Updating the screen

Welcome to the React documentation! This page will give you an introduction to 80% of the React concepts that you will use on a daily basis.

React apps are made out of components. A component is a piece of the UI (user interface) that has its own logic and appearance. A component can be as small as a button, or as large as an entire page.

React components are JavaScript functions that return markup:

Now that you’ve declared MyButton, you can nest it into another component:

Notice that <MyButton /> starts with a capital letter. That’s how you know it’s a React component. React component names must always start with a capital letter, while HTML tags must be lowercase.

Have a look at the result:

The export default keywords specify the main component in the file. If you’re not familiar with some piece of JavaScript syntax, MDN and javascript.info have great references.

The markup syntax you’ve seen above is called JSX. It is optional, but most React projects use JSX for its convenience. All of the tools we recommend for local development support JSX out of the box.

JSX is stricter than HTML. You have to close tags like <br />. Your component also can’t return multiple JSX tags. You have to wrap them into a shared parent, like a <div>...</div> or an empty <>...</> wrapper:

If you have a lot of HTML to port to JSX, you can use an online converter.

In React, you specify a CSS class with className. It works the same way as the HTML class attribute:

Then you write the CSS rules for it in a separate CSS file:

React does not prescribe how you add CSS files. In the simplest case, you’ll add a <link> tag to your HTML. If you use a build tool or a framework, consult its documentation to learn how to add a CSS file to your project.

JSX lets you put markup into JavaScript. Curly braces let you “escape back” into JavaScript so that you can embed some variable from your code and display it to the user. For example, this will display user.name:

You can also “escape into JavaScript” from JSX attributes, but you have to use curly braces instead of quotes. For example, className="avatar" passes the "avatar" string as the CSS class, but src={user.imageUrl} reads the JavaScript user.imageUrl variable value, and then passes that value as the src attribute:

You can put more complex expressions inside the JSX curly braces too, for example, string concatenation:

In the above example, style={{}} is not a special syntax, but a regular {} object inside the style={ } JSX 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
function MyButton() {  return (    <button>I'm a button</button>  );}
```

Example 2 (unknown):
```unknown
export default function MyApp() {  return (    <div>      <h1>Welcome to my app</h1>      <MyButton />    </div>  );}
```

Example 3 (unknown):
```unknown
function AboutPage() {  return (    <>      <h1>About</h1>      <p>Hello there.<br />How do you do?</p>    </>  );}
```

Example 4 (unknown):
```unknown
<img className="avatar" />
```

---

## useState

**URL:** https://react.dev/reference/react/useState#setstate-caveats

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## React Reference Overview

**URL:** https://react.dev/reference/react#eslint-plugin-react-hooks

**Contents:**
- React Reference Overview
- React
- React DOM
- React Compiler
- ESLint Plugin React Hooks
- Rules of React
- Legacy APIs

This section provides detailed reference documentation for working with React. For an introduction to React, please visit the Learn section.

The React reference documentation is broken down into functional subsections:

Programmatic React features:

React-dom contains features that are only supported for web applications (which run in the browser DOM environment). This section is broken into the following:

The React Compiler is a build-time optimization tool that automatically memoizes your React components and values:

The ESLint plugin for React Hooks helps enforce the Rules of React:

React has idioms — or rules — for how to express patterns in a way that is easy to understand and yields high-quality applications:

---

## useState

**URL:** https://react.dev/reference/react/useState#caveats

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## Built-in React Hooks

**URL:** https://react.dev/reference/react/hooks#ref-hooks

**Contents:**
- Built-in React Hooks
- State Hooks
- Context Hooks
- Ref Hooks
- Effect Hooks
- Performance Hooks
- Other Hooks
- Your own Hooks

Hooks let you use different React features from your components. You can either use the built-in Hooks or combine them to build your own. This page lists all built-in Hooks in React.

State lets a component “remember” information like user input. For example, a form component can use state to store the input value, while an image gallery component can use state to store the selected image index.

To add state to a component, use one of these Hooks:

Context lets a component receive information from distant parents without passing it as props. For example, your app’s top-level component can pass the current UI theme to all components below, no matter how deep.

Refs let a component hold some information that isn’t used for rendering, like a DOM node or a timeout ID. Unlike with state, updating a ref does not re-render your component. Refs are an “escape hatch” from the React paradigm. They are useful when you need to work with non-React systems, such as the built-in browser APIs.

Effects let a component connect to and synchronize with external systems. This includes dealing with network, browser DOM, animations, widgets written using a different UI library, and other non-React code.

Effects are an “escape hatch” from the React paradigm. Don’t use Effects to orchestrate the data flow of your application. If you’re not interacting with an external system, you might not need an Effect.

There are two rarely used variations of useEffect with differences in timing:

A common way to optimize re-rendering performance is to skip unnecessary work. For example, you can tell React to reuse a cached calculation or to skip a re-render if the data has not changed since the previous render.

To skip calculations and unnecessary re-rendering, use one of these Hooks:

Sometimes, you can’t skip re-rendering because the screen actually needs to update. In that case, you can improve performance by separating blocking updates that must be synchronous (like typing into an input) from non-blocking updates which don’t need to block the user interface (like updating a chart).

To prioritize rendering, use one of these Hooks:

These Hooks are mostly useful to library authors and aren’t commonly used in the application code.

You can also define your own custom Hooks as JavaScript functions.

**Examples:**

Example 1 (javascript):
```javascript
function ImageGallery() {  const [index, setIndex] = useState(0);  // ...
```

Example 2 (javascript):
```javascript
function Button() {  const theme = useContext(ThemeContext);  // ...
```

Example 3 (javascript):
```javascript
function Form() {  const inputRef = useRef(null);  // ...
```

Example 4 (javascript):
```javascript
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...
```

---

## useContext

**URL:** https://react.dev/reference/react/useContext

**Contents:**
- useContext
- Reference
  - useContext(SomeContext)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Passing data deeply into the tree
  - Pitfall
  - Updating data passed via context

useContext is a React Hook that lets you read and subscribe to context from your component.

Call useContext at the top level of your component to read and subscribe to context.

See more examples below.

useContext returns the context value for the calling component. It is determined as the value passed to the closest SomeContext above the calling component in the tree. If there is no such provider, then the returned value will be the defaultValue you have passed to createContext for that context. The returned value is always up-to-date. React automatically re-renders components that read some context if it changes.

Call useContext at the top level of your component to read and subscribe to context.

useContext returns the context value for the context you passed. To determine the context value, React searches the component tree and finds the closest context provider above for that particular context.

To pass context to a Button, wrap it or one of its parent components into the corresponding context provider:

It doesn’t matter how many layers of components there are between the provider and the Button. When a Button anywhere inside of Form calls useContext(ThemeContext), it will receive "dark" as the value.

useContext() always looks for the closest provider above the component that calls it. It searches upwards and does not consider providers in the component from which you’re calling useContext().

Often, you’ll want the context to change over time. To update context, combine it with state. Declare a state variable in the parent component, and pass the current state down as the context value to the provider.

Now any Button inside of the provider will receive the current theme value. If you call setTheme to update the theme value that you pass to the provider, all Button components will re-render with the new 'light' value.

In this example, the MyApp component holds a state variable which is then passed to the ThemeContext provider. Checking the “Dark mode” checkbox updates the state. Changing the provided value re-renders all the components using that context.

Note that value="dark" passes the "dark" string, but value={theme} passes the value of the JavaScript theme variable with JSX curly braces. Curly braces also let you pass context values that aren’t strings.

If React can’t find any providers of that particular context in the parent tree, the context value returned by useContext() will be equal to the default value that you specified when you

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const value = useContext(SomeContext)
```

Example 2 (python):
```python
import { useContext } from 'react';function MyComponent() {  const theme = useContext(ThemeContext);  // ...
```

Example 3 (python):
```python
import { useContext } from 'react';function Button() {  const theme = useContext(ThemeContext);  // ...
```

Example 4 (unknown):
```unknown
function MyPage() {  return (    <ThemeContext value="dark">      <Form />    </ThemeContext>  );}function Form() {  // ... renders buttons inside ...}
```

---

## useState

**URL:** https://react.dev/reference/react/useState#examples-basic

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#undefined

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#avoiding-recreating-the-initial-state

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## Built-in React Hooks

**URL:** https://react.dev/reference/react/hooks#other-hooks

**Contents:**
- Built-in React Hooks
- State Hooks
- Context Hooks
- Ref Hooks
- Effect Hooks
- Performance Hooks
- Other Hooks
- Your own Hooks

Hooks let you use different React features from your components. You can either use the built-in Hooks or combine them to build your own. This page lists all built-in Hooks in React.

State lets a component “remember” information like user input. For example, a form component can use state to store the input value, while an image gallery component can use state to store the selected image index.

To add state to a component, use one of these Hooks:

Context lets a component receive information from distant parents without passing it as props. For example, your app’s top-level component can pass the current UI theme to all components below, no matter how deep.

Refs let a component hold some information that isn’t used for rendering, like a DOM node or a timeout ID. Unlike with state, updating a ref does not re-render your component. Refs are an “escape hatch” from the React paradigm. They are useful when you need to work with non-React systems, such as the built-in browser APIs.

Effects let a component connect to and synchronize with external systems. This includes dealing with network, browser DOM, animations, widgets written using a different UI library, and other non-React code.

Effects are an “escape hatch” from the React paradigm. Don’t use Effects to orchestrate the data flow of your application. If you’re not interacting with an external system, you might not need an Effect.

There are two rarely used variations of useEffect with differences in timing:

A common way to optimize re-rendering performance is to skip unnecessary work. For example, you can tell React to reuse a cached calculation or to skip a re-render if the data has not changed since the previous render.

To skip calculations and unnecessary re-rendering, use one of these Hooks:

Sometimes, you can’t skip re-rendering because the screen actually needs to update. In that case, you can improve performance by separating blocking updates that must be synchronous (like typing into an input) from non-blocking updates which don’t need to block the user interface (like updating a chart).

To prioritize rendering, use one of these Hooks:

These Hooks are mostly useful to library authors and aren’t commonly used in the application code.

You can also define your own custom Hooks as JavaScript functions.

**Examples:**

Example 1 (javascript):
```javascript
function ImageGallery() {  const [index, setIndex] = useState(0);  // ...
```

Example 2 (javascript):
```javascript
function Button() {  const theme = useContext(ThemeContext);  // ...
```

Example 3 (javascript):
```javascript
function Form() {  const inputRef = useRef(null);  // ...
```

Example 4 (javascript):
```javascript
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#im-getting-an-error-too-many-re-renders

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## eslint-plugin-react-hooks - This feature is available in the latest RC version

**URL:** https://react.dev/reference/eslint-plugin-react-hooks

**Contents:**
- eslint-plugin-react-hooks - This feature is available in the latest RC version
  - Note
- Recommended Rules

eslint-plugin-react-hooks provides ESLint rules to enforce the Rules of React.

This plugin helps you catch violations of React’s rules at build time, ensuring your components and hooks follow React’s rules for correctness and performance. The lints cover both fundamental React patterns (exhaustive-deps and rules-of-hooks) and issues flagged by React Compiler. React Compiler diagnostics are automatically surfaced by this ESLint plugin, and can be used even if your app hasn’t adopted the compiler yet.

When the compiler reports a diagnostic, it means that the compiler was able to statically detect a pattern that is not supported or breaks the Rules of React. When it detects this, it automatically skips over those components and hooks, while keeping the rest of your app compiled. This ensures optimal coverage of safe optimizations that won’t break your app.

What this means for linting, is that you don’t need to fix all violations immediately. Address them at your own pace to gradually increase the number of optimized components.

These rules are included in the recommended preset in eslint-plugin-react-hooks:

---

## useState

**URL:** https://react.dev/reference/react/useState#setstate-returns

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useCallback

**URL:** https://react.dev/reference/react/useCallback

**Contents:**
- useCallback
  - Note
- Reference
  - useCallback(fn, dependencies)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Skipping re-rendering of components
  - Note

useCallback is a React Hook that lets you cache a function definition between re-renders.

React Compiler automatically memoizes values and functions, reducing the need for manual useCallback calls. You can use the compiler to handle memoization automatically.

Call useCallback at the top level of your component to cache a function definition between re-renders:

See more examples below.

fn: The function value that you want to cache. It can take any arguments and return any values. React will return (not call!) your function back to you during the initial render. On next renders, React will give you the same function again if the dependencies have not changed since the last render. Otherwise, it will give you the function that you have passed during the current render, and store it in case it can be reused later. React will not call your function. The function is returned to you so you can decide when and whether to call it.

dependencies: The list of all reactive values referenced inside of the fn code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is configured for React, it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like [dep1, dep2, dep3]. React will compare each dependency with its previous value using the Object.is comparison algorithm.

On the initial render, useCallback returns the fn function you have passed.

During subsequent renders, it will either return an already stored fn function from the last render (if the dependencies haven’t changed), or return the fn function you have passed during this render.

When you optimize rendering performance, you will sometimes need to cache the functions that you pass to child components. Let’s first look at the syntax for how to do this, and then see in which cases it’s useful.

To cache a function between re-renders of your component, wrap its definition into the useCallback Hook:

You need to pass two things to useCallback:

On the initial render, the returned function you’ll get from useCallback will be the function you passed.

On the following renders, React will compare the dependencies with the dependencies you passed during the previous render. If none of the dependencies have changed (compared with Object.is), useCallback will return the same function as before. Otherwise, useCallback will re

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const cachedFn = useCallback(fn, dependencies)
```

Example 2 (python):
```python
import { useCallback } from 'react';export default function ProductPage({ productId, referrer, theme }) {  const handleSubmit = useCallback((orderDetails) => {    post('/product/' + productId + '/buy', {      referrer,      orderDetails,    });  }, [productId, referrer]);
```

Example 3 (python):
```python
import { useCallback } from 'react';function ProductPage({ productId, referrer, theme }) {  const handleSubmit = useCallback((orderDetails) => {    post('/product/' + productId + '/buy', {      referrer,      orderDetails,    });  }, [productId, referrer]);  // ...
```

Example 4 (unknown):
```unknown
function ProductPage({ productId, referrer, theme }) {  // ...  return (    <div className={theme}>      <ShippingForm onSubmit={handleSubmit} />    </div>  );
```

---

## Built-in React DOM Hooks

**URL:** https://react.dev/reference/react-dom/hooks

**Contents:**
- Built-in React DOM Hooks
- Form Hooks

The react-dom package contains Hooks that are only supported for web applications (which run in the browser DOM environment). These Hooks are not supported in non-browser environments like iOS, Android, or Windows applications. If you are looking for Hooks that are supported in web browsers and other environments see the React Hooks page. This page lists all the Hooks in the react-dom package.

Forms let you create interactive controls for submitting information. To manage forms in your components, use one of these Hooks:

**Examples:**

Example 1 (javascript):
```javascript
function Form({ action }) {  async function increment(n) {    return n + 1;  }  const [count, incrementFormAction] = useActionState(increment, 0);  return (    <form action={action}>      <button formAction={incrementFormAction}>Count: {count}</button>      <Button />    </form>  );}function Button() {  const { pending } = useFormStatus();  return (    <button disabled={pending} type="submit">      Submit    </button>  );}
```

---

## Built-in React Hooks

**URL:** https://react.dev/reference/react/hooks#effect-hooks

**Contents:**
- Built-in React Hooks
- State Hooks
- Context Hooks
- Ref Hooks
- Effect Hooks
- Performance Hooks
- Other Hooks
- Your own Hooks

Hooks let you use different React features from your components. You can either use the built-in Hooks or combine them to build your own. This page lists all built-in Hooks in React.

State lets a component “remember” information like user input. For example, a form component can use state to store the input value, while an image gallery component can use state to store the selected image index.

To add state to a component, use one of these Hooks:

Context lets a component receive information from distant parents without passing it as props. For example, your app’s top-level component can pass the current UI theme to all components below, no matter how deep.

Refs let a component hold some information that isn’t used for rendering, like a DOM node or a timeout ID. Unlike with state, updating a ref does not re-render your component. Refs are an “escape hatch” from the React paradigm. They are useful when you need to work with non-React systems, such as the built-in browser APIs.

Effects let a component connect to and synchronize with external systems. This includes dealing with network, browser DOM, animations, widgets written using a different UI library, and other non-React code.

Effects are an “escape hatch” from the React paradigm. Don’t use Effects to orchestrate the data flow of your application. If you’re not interacting with an external system, you might not need an Effect.

There are two rarely used variations of useEffect with differences in timing:

A common way to optimize re-rendering performance is to skip unnecessary work. For example, you can tell React to reuse a cached calculation or to skip a re-render if the data has not changed since the previous render.

To skip calculations and unnecessary re-rendering, use one of these Hooks:

Sometimes, you can’t skip re-rendering because the screen actually needs to update. In that case, you can improve performance by separating blocking updates that must be synchronous (like typing into an input) from non-blocking updates which don’t need to block the user interface (like updating a chart).

To prioritize rendering, use one of these Hooks:

These Hooks are mostly useful to library authors and aren’t commonly used in the application code.

You can also define your own custom Hooks as JavaScript functions.

**Examples:**

Example 1 (javascript):
```javascript
function ImageGallery() {  const [index, setIndex] = useState(0);  // ...
```

Example 2 (javascript):
```javascript
function Button() {  const theme = useContext(ThemeContext);  // ...
```

Example 3 (javascript):
```javascript
function Form() {  const inputRef = useRef(null);  // ...
```

Example 4 (javascript):
```javascript
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#setstate

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## Components and Hooks must be pure

**URL:** https://react.dev/reference/rules/components-and-hooks-must-be-pure

**Contents:**
- Components and Hooks must be pure
  - Note
  - Why does purity matter?
    - How does React run your code?
      - Deep Dive
    - How to tell if code runs in render
- Components and Hooks must be idempotent
- Side effects must run outside of render
  - Note
  - When is it okay to have mutation?

Pure functions only perform a calculation and nothing more. It makes your code easier to understand, debug, and allows React to automatically optimize your components and Hooks correctly.

This reference page covers advanced topics and requires familiarity with the concepts covered in the Keeping Components Pure page.

One of the key concepts that makes React, React is purity. A pure component or hook is one that is:

When render is kept pure, React can understand how to prioritize which updates are most important for the user to see first. This is made possible because of render purity: since components don’t have side effects in render, React can pause rendering components that aren’t as important to update, and only come back to them later when it’s needed.

Concretely, this means that rendering logic can be run multiple times in a way that allows React to give your user a pleasant user experience. However, if your component has an untracked side effect – like modifying the value of a global variable during render – when React runs your rendering code again, your side effects will be triggered in a way that won’t match what you want. This often leads to unexpected bugs that can degrade how your users experience your app. You can see an example of this in the Keeping Components Pure page.

React is declarative: you tell React what to render, and React will figure out how best to display it to your user. To do this, React has a few phases where it runs your code. You don’t need to know about all of these phases to use React well. But at a high level, you should know about what code runs in render, and what runs outside of it.

Rendering refers to calculating what the next version of your UI should look like. After rendering, Effects are flushed (meaning they are run until there are no more left) and may update the calculation if the Effects have impacts on layout. React takes this new calculation and compares it to the calculation used to create the previous version of your UI, then commits just the minimum changes needed to the DOM (what your user actually sees) to catch it up to the latest version.

One quick heuristic to tell if code runs during render is to examine where it is: if it’s written at the top level like in the example below, there’s a good chance it runs during render.

Event handlers and Effects don’t run in render:

Components must always return the same output with respect to their inputs – props, state, and context. This is known as id

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
function Dropdown() {  const selectedItems = new Set(); // created during render  // ...}
```

Example 2 (javascript):
```javascript
function Dropdown() {  const selectedItems = new Set();  const onSelect = (item) => {    // this code is in an event handler, so it's only run when the user triggers this    selectedItems.add(item);  }}
```

Example 3 (javascript):
```javascript
function Dropdown() {  const selectedItems = new Set();  useEffect(() => {    // this code is inside of an Effect, so it only runs after rendering    logForAnalytics(selectedItems);  }, [selectedItems]);}
```

Example 4 (javascript):
```javascript
function Clock() {  const time = new Date(); // 🔴 Bad: always returns a different result!  return <span>{time.toLocaleString()}</span>}
```

---

## Built-in React Hooks

**URL:** https://react.dev/reference/react/hooks#performance-hooks

**Contents:**
- Built-in React Hooks
- State Hooks
- Context Hooks
- Ref Hooks
- Effect Hooks
- Performance Hooks
- Other Hooks
- Your own Hooks

Hooks let you use different React features from your components. You can either use the built-in Hooks or combine them to build your own. This page lists all built-in Hooks in React.

State lets a component “remember” information like user input. For example, a form component can use state to store the input value, while an image gallery component can use state to store the selected image index.

To add state to a component, use one of these Hooks:

Context lets a component receive information from distant parents without passing it as props. For example, your app’s top-level component can pass the current UI theme to all components below, no matter how deep.

Refs let a component hold some information that isn’t used for rendering, like a DOM node or a timeout ID. Unlike with state, updating a ref does not re-render your component. Refs are an “escape hatch” from the React paradigm. They are useful when you need to work with non-React systems, such as the built-in browser APIs.

Effects let a component connect to and synchronize with external systems. This includes dealing with network, browser DOM, animations, widgets written using a different UI library, and other non-React code.

Effects are an “escape hatch” from the React paradigm. Don’t use Effects to orchestrate the data flow of your application. If you’re not interacting with an external system, you might not need an Effect.

There are two rarely used variations of useEffect with differences in timing:

A common way to optimize re-rendering performance is to skip unnecessary work. For example, you can tell React to reuse a cached calculation or to skip a re-render if the data has not changed since the previous render.

To skip calculations and unnecessary re-rendering, use one of these Hooks:

Sometimes, you can’t skip re-rendering because the screen actually needs to update. In that case, you can improve performance by separating blocking updates that must be synchronous (like typing into an input) from non-blocking updates which don’t need to block the user interface (like updating a chart).

To prioritize rendering, use one of these Hooks:

These Hooks are mostly useful to library authors and aren’t commonly used in the application code.

You can also define your own custom Hooks as JavaScript functions.

**Examples:**

Example 1 (javascript):
```javascript
function ImageGallery() {  const [index, setIndex] = useState(0);  // ...
```

Example 2 (javascript):
```javascript
function Button() {  const theme = useContext(ThemeContext);  // ...
```

Example 3 (javascript):
```javascript
function Form() {  const inputRef = useRef(null);  // ...
```

Example 4 (javascript):
```javascript
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...
```

---

## Built-in React Hooks

**URL:** https://react.dev/reference/react/hooks

**Contents:**
- Built-in React Hooks
- State Hooks
- Context Hooks
- Ref Hooks
- Effect Hooks
- Performance Hooks
- Other Hooks
- Your own Hooks

Hooks let you use different React features from your components. You can either use the built-in Hooks or combine them to build your own. This page lists all built-in Hooks in React.

State lets a component “remember” information like user input. For example, a form component can use state to store the input value, while an image gallery component can use state to store the selected image index.

To add state to a component, use one of these Hooks:

Context lets a component receive information from distant parents without passing it as props. For example, your app’s top-level component can pass the current UI theme to all components below, no matter how deep.

Refs let a component hold some information that isn’t used for rendering, like a DOM node or a timeout ID. Unlike with state, updating a ref does not re-render your component. Refs are an “escape hatch” from the React paradigm. They are useful when you need to work with non-React systems, such as the built-in browser APIs.

Effects let a component connect to and synchronize with external systems. This includes dealing with network, browser DOM, animations, widgets written using a different UI library, and other non-React code.

Effects are an “escape hatch” from the React paradigm. Don’t use Effects to orchestrate the data flow of your application. If you’re not interacting with an external system, you might not need an Effect.

There are two rarely used variations of useEffect with differences in timing:

A common way to optimize re-rendering performance is to skip unnecessary work. For example, you can tell React to reuse a cached calculation or to skip a re-render if the data has not changed since the previous render.

To skip calculations and unnecessary re-rendering, use one of these Hooks:

Sometimes, you can’t skip re-rendering because the screen actually needs to update. In that case, you can improve performance by separating blocking updates that must be synchronous (like typing into an input) from non-blocking updates which don’t need to block the user interface (like updating a chart).

To prioritize rendering, use one of these Hooks:

These Hooks are mostly useful to library authors and aren’t commonly used in the application code.

You can also define your own custom Hooks as JavaScript functions.

**Examples:**

Example 1 (javascript):
```javascript
function ImageGallery() {  const [index, setIndex] = useState(0);  // ...
```

Example 2 (javascript):
```javascript
function Button() {  const theme = useContext(ThemeContext);  // ...
```

Example 3 (javascript):
```javascript
function Form() {  const inputRef = useRef(null);  // ...
```

Example 4 (javascript):
```javascript
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#setstate-parameters

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#returns

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#updating-state-based-on-the-previous-state

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#examples-objects

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## Built-in React Hooks

**URL:** https://react.dev/reference/react/hooks#undefined

**Contents:**
- Built-in React Hooks
- State Hooks
- Context Hooks
- Ref Hooks
- Effect Hooks
- Performance Hooks
- Other Hooks
- Your own Hooks

Hooks let you use different React features from your components. You can either use the built-in Hooks or combine them to build your own. This page lists all built-in Hooks in React.

State lets a component “remember” information like user input. For example, a form component can use state to store the input value, while an image gallery component can use state to store the selected image index.

To add state to a component, use one of these Hooks:

Context lets a component receive information from distant parents without passing it as props. For example, your app’s top-level component can pass the current UI theme to all components below, no matter how deep.

Refs let a component hold some information that isn’t used for rendering, like a DOM node or a timeout ID. Unlike with state, updating a ref does not re-render your component. Refs are an “escape hatch” from the React paradigm. They are useful when you need to work with non-React systems, such as the built-in browser APIs.

Effects let a component connect to and synchronize with external systems. This includes dealing with network, browser DOM, animations, widgets written using a different UI library, and other non-React code.

Effects are an “escape hatch” from the React paradigm. Don’t use Effects to orchestrate the data flow of your application. If you’re not interacting with an external system, you might not need an Effect.

There are two rarely used variations of useEffect with differences in timing:

A common way to optimize re-rendering performance is to skip unnecessary work. For example, you can tell React to reuse a cached calculation or to skip a re-render if the data has not changed since the previous render.

To skip calculations and unnecessary re-rendering, use one of these Hooks:

Sometimes, you can’t skip re-rendering because the screen actually needs to update. In that case, you can improve performance by separating blocking updates that must be synchronous (like typing into an input) from non-blocking updates which don’t need to block the user interface (like updating a chart).

To prioritize rendering, use one of these Hooks:

These Hooks are mostly useful to library authors and aren’t commonly used in the application code.

You can also define your own custom Hooks as JavaScript functions.

**Examples:**

Example 1 (javascript):
```javascript
function ImageGallery() {  const [index, setIndex] = useState(0);  // ...
```

Example 2 (javascript):
```javascript
function Button() {  const theme = useContext(ThemeContext);  // ...
```

Example 3 (javascript):
```javascript
function Form() {  const inputRef = useRef(null);  // ...
```

Example 4 (javascript):
```javascript
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...
```

---

## useState

**URL:** https://react.dev/reference/react/useState#examples-updater

**Contents:**
- useState
- Reference
  - useState(initialState)
    - Parameters
    - Returns
    - Caveats
  - set functions, like setSomething(nextState)
    - Parameters
    - Returns
    - Caveats

useState is a React Hook that lets you add a state variable to your component.

Call useState at the top level of your component to declare a state variable.

The convention is to name state variables like [something, setSomething] using array destructuring.

See more examples below.

useState returns an array with exactly two values:

The set function returned by useState lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

set functions do not have a return value.

The set function only updates the state variable for the next render. If you read the state variable after calling the set function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

The set function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

Calling the set function during rendering is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to store information from the previous renders. See an example below.

In Strict Mode, React will call your updater function twice in order to help you find accidental impurities. This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

Call useState at the top level of your component to declare one or more state variables.

The convention is to name state variables like [something, setSomething

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, setState] = useState(initialState)
```

Example 2 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

Example 3 (javascript):
```javascript
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

Example 4 (python):
```python
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

---

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory#anatomy-of-usestate

**Contents:**
- State: A Component's Memory
  - You will learn
- When a regular variable isn’t enough
- Adding a state variable
  - Meet your first Hook
  - Pitfall
  - Anatomy of useState
  - Note
- Giving a component multiple state variables
      - Deep Dive

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” should put a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

Here’s a component that renders a sculpture image. Clicking the “Next” button should show the next sculpture by changing the index to 1, then 2, and so on. However, this won’t work (you can try it!):

The handleClick event handler is updating a local variable, index. But two things prevent that change from being visible:

To update a component with new data, two things need to happen:

The useState Hook provides those two things:

To add a state variable, import useState from React at the top of the file:

Then, replace this line:

index is a state variable and setIndex is the setter function.

The [ and ] syntax here is called array destructuring and it lets you read values from an array. The array returned by useState always has exactly two items.

This is how they work together in handleClick:

Now clicking the “Next” button switches the current sculpture:

In React, useState, as well as any other function starting with “use”, is called a Hook.

Hooks are special functions that are only available while React is rendering (which we’ll get into in more detail on the next page). They let you “hook into” different React features.

State is just one of those features, but you will meet the other Hooks later.

Hooks—functions starting with use—can only be called at the top level of your components or your own Hooks. You can’t call Hooks inside conditions, loops, or other nested functions. Hooks are functions, but it’s helpful to think of them as unconditional declarations about your component’s needs. You “use” React features at the top of your component similar to how you “import” modules at the top of your file.

When you call useState, you are telling React that you want this component to remember something:

In this case, you want React to remember index.

The convention is to name this pair like const [something, setSomething]. You could name it anything you like, but conventions make things easier to understand across projects.

The only argument to useState is the initial value of your state variable. In this example, the

*[Content truncated]*

**Examples:**

Example 1 (python):
```python
import { useState } from 'react';
```

Example 2 (javascript):
```javascript
let index = 0;
```

Example 3 (javascript):
```javascript
const [index, setIndex] = useState(0);
```

Example 4 (unknown):
```unknown
function handleClick() {  setIndex(index + 1);}
```

---

## Reusing Logic with Custom Hooks

**URL:** https://react.dev/learn/reusing-logic-with-custom-hooks#extracting-your-own-custom-hook-from-a-component

**Contents:**
- Reusing Logic with Custom Hooks
  - You will learn
- Custom Hooks: Sharing logic between components
  - Extracting your own custom Hook from a component
  - Hook names always start with use
  - Note
      - Deep Dive
    - Should all functions called during rendering start with the use prefix?
  - Custom Hooks let you share stateful logic, not state itself
- Passing reactive values between Hooks

React comes with several built-in Hooks like useState, useContext, and useEffect. Sometimes, you’ll wish that there was a Hook for some more specific purpose: for example, to fetch data, to keep track of whether the user is online, or to connect to a chat room. You might not find these Hooks in React, but you can create your own Hooks for your application’s needs.

Imagine you’re developing an app that heavily relies on the network (as most apps do). You want to warn the user if their network connection has accidentally gone off while they were using your app. How would you go about it? It seems like you’ll need two things in your component:

This will keep your component synchronized with the network status. You might start with something like this:

Try turning your network on and off, and notice how this StatusBar updates in response to your actions.

Now imagine you also want to use the same logic in a different component. You want to implement a Save button that will become disabled and show “Reconnecting…” instead of “Save” while the network is off.

To start, you can copy and paste the isOnline state and the Effect into SaveButton:

Verify that, if you turn off the network, the button will change its appearance.

These two components work fine, but the duplication in logic between them is unfortunate. It seems like even though they have different visual appearance, you want to reuse the logic between them.

Imagine for a moment that, similar to useState and useEffect, there was a built-in useOnlineStatus Hook. Then both of these components could be simplified and you could remove the duplication between them:

Although there is no such built-in Hook, you can write it yourself. Declare a function called useOnlineStatus and move all the duplicated code into it from the components you wrote earlier:

At the end of the function, return isOnline. This lets your components read that value:

Verify that switching the network on and off updates both components.

Now your components don’t have as much repetitive logic. More importantly, the code inside them describes what they want to do (use the online status!) rather than how to do it (by subscribing to the browser events).

When you extract logic into custom Hooks, you can hide the gnarly details of how you deal with some external system or a browser API. The code of your components expresses your intent, not the implementation.

React applications are built from components. Components are built from Hook

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
function StatusBar() {  const isOnline = useOnlineStatus();  return <h1>{isOnline ? '✅ Online' : '❌ Disconnected'}</h1>;}function SaveButton() {  const isOnline = useOnlineStatus();  function handleSaveClick() {    console.log('✅ Progress saved');  }  return (    <button disabled={!isOnline} onClick={handleSaveClick}>      {isOnline ? 'Save progress' : 'Reconnecting...'}    </button>  );}
```

Example 2 (javascript):
```javascript
function useOnlineStatus() {  const [isOnline, setIsOnline] = useState(true);  useEffect(() => {    function handleOnline() {      setIsOnline(true);    }    function handleOffline() {      setIsOnline(false);    }    window.addEventListener('online', handleOnline);    window.addEventListener('offline', handleOffline);    return () => {      window.removeEventListener('online', handleOnline);      window.removeEventListener('offline', handleOffline);    };  }, []);  return isOnline;}
```

Example 3 (unknown):
```unknown
// 🔴 Avoid: A Hook that doesn't use Hooksfunction useSorted(items) {  return items.slice().sort();}// ✅ Good: A regular function that doesn't use Hooksfunction getSorted(items) {  return items.slice().sort();}
```

Example 4 (javascript):
```javascript
function List({ items, shouldSort }) {  let displayedItems = items;  if (shouldSort) {    // ✅ It's ok to call getSorted() conditionally because it's not a Hook    displayedItems = getSorted(items);  }  // ...}
```

---

## Referencing Values with Refs

**URL:** https://react.dev/learn/referencing-values-with-refs

**Contents:**
- Referencing Values with Refs
  - You will learn
- Adding a ref to your component
- Example: building a stopwatch
- Differences between refs and state
      - Deep Dive
    - How does useRef work inside?
- When to use refs
- Best practices for refs
- Refs and the DOM

When you want a component to “remember” some information, but you don’t want that information to trigger new renders, you can use a ref.

You can add a ref to your component by importing the useRef Hook from React:

Inside your component, call the useRef Hook and pass the initial value that you want to reference as the only argument. For example, here is a ref to the value 0:

useRef returns an object like this:

Illustrated by Rachel Lee Nabors

You can access the current value of that ref through the ref.current property. This value is intentionally mutable, meaning you can both read and write to it. It’s like a secret pocket of your component that React doesn’t track. (This is what makes it an “escape hatch” from React’s one-way data flow—more on that below!)

Here, a button will increment ref.current on every click:

The ref points to a number, but, like state, you could point to anything: a string, an object, or even a function. Unlike state, ref is a plain JavaScript object with the current property that you can read and modify.

Note that the component doesn’t re-render with every increment. Like state, refs are retained by React between re-renders. However, setting state re-renders a component. Changing a ref does not!

You can combine refs and state in a single component. For example, let’s make a stopwatch that the user can start or stop by pressing a button. In order to display how much time has passed since the user pressed “Start”, you will need to keep track of when the Start button was pressed and what the current time is. This information is used for rendering, so you’ll keep it in state:

When the user presses “Start”, you’ll use setInterval in order to update the time every 10 milliseconds:

When the “Stop” button is pressed, you need to cancel the existing interval so that it stops updating the now state variable. You can do this by calling clearInterval, but you need to give it the interval ID that was previously returned by the setInterval call when the user pressed Start. You need to keep the interval ID somewhere. Since the interval ID is not used for rendering, you can keep it in a ref:

When a piece of information is used for rendering, keep it in state. When a piece of information is only needed by event handlers and changing it doesn’t require a re-render, using a ref may be more efficient.

Perhaps you’re thinking refs seem less “strict” than state—you can mutate them instead of always having to use a state setting function, for

*[Content truncated]*

**Examples:**

Example 1 (python):
```python
import { useRef } from 'react';
```

Example 2 (javascript):
```javascript
const ref = useRef(0);
```

Example 3 (unknown):
```unknown
{   current: 0 // The value you passed to useRef}
```

Example 4 (javascript):
```javascript
const [startTime, setStartTime] = useState(null);const [now, setNow] = useState(null);
```

---

## Built-in React DOM Hooks

**URL:** https://react.dev/reference/react-dom/hooks#form-hooks

**Contents:**
- Built-in React DOM Hooks
- Form Hooks

The react-dom package contains Hooks that are only supported for web applications (which run in the browser DOM environment). These Hooks are not supported in non-browser environments like iOS, Android, or Windows applications. If you are looking for Hooks that are supported in web browsers and other environments see the React Hooks page. This page lists all the Hooks in the react-dom package.

Forms let you create interactive controls for submitting information. To manage forms in your components, use one of these Hooks:

**Examples:**

Example 1 (javascript):
```javascript
function Form({ action }) {  async function increment(n) {    return n + 1;  }  const [count, incrementFormAction] = useActionState(increment, 0);  return (    <form action={action}>      <button formAction={incrementFormAction}>Count: {count}</button>      <Button />    </form>  );}function Button() {  const { pending } = useFormStatus();  return (    <button disabled={pending} type="submit">      Submit    </button>  );}
```

---
