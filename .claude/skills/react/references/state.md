# React - State

**Pages:** 18

---

## Managing State

**URL:** https://react.dev/learn/managing-state

**Contents:**
- Managing State
  - In this chapter
- Reacting to input with state
- Ready to learn this topic?
- Choosing the state structure
- Ready to learn this topic?
- Sharing state between components
- Ready to learn this topic?
- Preserving and resetting state
- Ready to learn this topic?

As your application grows, it helps to be more intentional about how your state is organized and how the data flows between your components. Redundant or duplicate state is a common source of bugs. In this chapter, you’ll learn how to structure your state well, how to keep your state update logic maintainable, and how to share state between distant components.

With React, you won’t modify the UI from code directly. For example, you won’t write commands like “disable the button”, “enable the button”, “show the success message”, etc. Instead, you will describe the UI you want to see for the different visual states of your component (“initial state”, “typing state”, “success state”), and then trigger the state changes in response to user input. This is similar to how designers think about UI.

Here is a quiz form built using React. Note how it uses the status state variable to determine whether to enable or disable the submit button, and whether to show the success message instead.

Read Reacting to Input with State to learn how to approach interactions with a state-driven mindset.

Structuring state well can make a difference between a component that is pleasant to modify and debug, and one that is a constant source of bugs. The most important principle is that state shouldn’t contain redundant or duplicated information. If there’s unnecessary state, it’s easy to forget to update it, and introduce bugs!

For example, this form has a redundant fullName state variable:

You can remove it and simplify the code by calculating fullName while the component is rendering:

This might seem like a small change, but many bugs in React apps are fixed this way.

Read Choosing the State Structure to learn how to design the state shape to avoid bugs.

Sometimes, you want the state of two components to always change together. To do it, remove state from both of them, move it to their closest common parent, and then pass it down to them via props. This is known as “lifting state up”, and it’s one of the most common things you will do writing React code.

In this example, only one panel should be active at a time. To achieve this, instead of keeping the active state inside each individual panel, the parent component holds the state and specifies the props for its children.

Read Sharing State Between Components to learn how to lift state up and keep components in sync.

When you re-render a component, React needs to decide which parts of the tree to keep (and update), and wh

*[Content truncated]*

---

## useReducer

**URL:** https://react.dev/reference/react/useReducer

**Contents:**
- useReducer
- Reference
  - useReducer(reducer, initialArg, init?)
    - Parameters
    - Returns
    - Caveats
  - dispatch function
    - Parameters
    - Returns
    - Caveats

useReducer is a React Hook that lets you add a reducer to your component.

Call useReducer at the top level of your component to manage its state with a reducer.

See more examples below.

useReducer returns an array with exactly two values:

The dispatch function returned by useReducer lets you update the state to a different value and trigger a re-render. You need to pass the action as the only argument to the dispatch function:

React will set the next state to the result of calling the reducer function you’ve provided with the current state and the action you’ve passed to dispatch.

dispatch functions do not have a return value.

The dispatch function only updates the state variable for the next render. If you read the state variable after calling the dispatch function, you will still get the old value that was on the screen before your call.

If the new value you provide is identical to the current state, as determined by an Object.is comparison, React will skip re-rendering the component and its children. This is an optimization. React may still need to call your component before ignoring the result, but it shouldn’t affect your code.

React batches state updates. It updates the screen after all the event handlers have run and have called their set functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use flushSync.

Call useReducer at the top level of your component to manage state with a reducer.

useReducer returns an array with exactly two items:

To update what’s on the screen, call dispatch with an object representing what the user did, called an action:

React will pass the current state and the action to your reducer function. Your reducer will calculate and return the next state. React will store that next state, render your component with it, and update the UI.

useReducer is very similar to useState, but it lets you move the state update logic from event handlers into a single function outside of your component. Read more about choosing between useState and useReducer.

A reducer function is declared like this:

Then you need to fill in the code that will calculate and return the next state. By convention, it is common to write it as a switch statement. For each case in the switch, calculate and return some next state.

Actions can have any shape. By convention, it’s common to pass objects with a type property id

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [state, dispatch] = useReducer(reducer, initialArg, init?)
```

Example 2 (python):
```python
import { useReducer } from 'react';function reducer(state, action) {  // ...}function MyComponent() {  const [state, dispatch] = useReducer(reducer, { age: 42 });  // ...
```

Example 3 (javascript):
```javascript
const [state, dispatch] = useReducer(reducer, { age: 42 });function handleClick() {  dispatch({ type: 'incremented_age' });  // ...
```

Example 4 (python):
```python
import { useReducer } from 'react';function reducer(state, action) {  // ...}function MyComponent() {  const [state, dispatch] = useReducer(reducer, { age: 42 });  // ...
```

---

## State as a Snapshot

**URL:** https://react.dev/learn/state-as-a-snapshot

**Contents:**
- State as a Snapshot
  - You will learn
- Setting state triggers renders
- Rendering takes a snapshot in time
- State over time
- Recap
- Try out some challenges
    - Challenge 1 of 1: Implement a traffic light

State variables might look like regular JavaScript variables that you can read and write to. However, state behaves more like a snapshot. Setting it does not change the state variable you already have, but instead triggers a re-render.

You might think of your user interface as changing directly in response to the user event like a click. In React, it works a little differently from this mental model. On the previous page, you saw that setting state requests a re-render from React. This means that for an interface to react to the event, you need to update the state.

In this example, when you press “send”, setIsSent(true) tells React to re-render the UI:

Here’s what happens when you click the button:

Let’s take a closer look at the relationship between state and rendering.

“Rendering” means that React is calling your component, which is a function. The JSX you return from that function is like a snapshot of the UI in time. Its props, event handlers, and local variables were all calculated using its state at the time of the render.

Unlike a photograph or a movie frame, the UI “snapshot” you return is interactive. It includes logic like event handlers that specify what happens in response to inputs. React updates the screen to match this snapshot and connects the event handlers. As a result, pressing a button will trigger the click handler from your JSX.

When React re-renders a component:

Illustrated by Rachel Lee Nabors

As a component’s memory, state is not like a regular variable that disappears after your function returns. State actually “lives” in React itself—as if on a shelf!—outside of your function. When React calls your component, it gives you a snapshot of the state for that particular render. Your component returns a snapshot of the UI with a fresh set of props and event handlers in its JSX, all calculated using the state values from that render!

Illustrated by Rachel Lee Nabors

Here’s a little experiment to show you how this works. In this example, you might expect that clicking the “+3” button would increment the counter three times because it calls setNumber(number + 1) three times.

See what happens when you click the “+3” button:

Notice that number only increments once per click!

Setting state only changes it for the next render. During the first render, number was 0. This is why, in that render’s onClick handler, the value of number is still 0 even after setNumber(number + 1) was called:

Here is what this button’s click handler t

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
<button onClick={() => {  setNumber(number + 1);  setNumber(number + 1);  setNumber(number + 1);}}>+3</button>
```

Example 2 (javascript):
```javascript
<button onClick={() => {  setNumber(0 + 1);  setNumber(0 + 1);  setNumber(0 + 1);}}>+3</button>
```

Example 3 (javascript):
```javascript
<button onClick={() => {  setNumber(1 + 1);  setNumber(1 + 1);  setNumber(1 + 1);}}>+3</button>
```

Example 4 (unknown):
```unknown
setNumber(0 + 5);alert(0);
```

---

## Queueing a Series of State Updates

**URL:** https://react.dev/learn/queueing-a-series-of-state-updates

**Contents:**
- Queueing a Series of State Updates
  - You will learn
- React batches state updates
- Updating the same state multiple times before the next render
  - What happens if you update state after replacing it
  - Note
  - What happens if you replace state after updating it
  - Naming conventions
- Recap
- Try out some challenges

Setting a state variable will queue another render. But sometimes you might want to perform multiple operations on the value before queueing the next render. To do this, it helps to understand how React batches state updates.

You might expect that clicking the “+3” button will increment the counter three times because it calls setNumber(number + 1) three times:

However, as you might recall from the previous section, each render’s state values are fixed, so the value of number inside the first render’s event handler is always 0, no matter how many times you call setNumber(1):

But there is one other factor at play here. React waits until all code in the event handlers has run before processing your state updates. This is why the re-render only happens after all these setNumber() calls.

This might remind you of a waiter taking an order at the restaurant. A waiter doesn’t run to the kitchen at the mention of your first dish! Instead, they let you finish your order, let you make changes to it, and even take orders from other people at the table.

Illustrated by Rachel Lee Nabors

This lets you update multiple state variables—even from multiple components—without triggering too many re-renders. But this also means that the UI won’t be updated until after your event handler, and any code in it, completes. This behavior, also known as batching, makes your React app run much faster. It also avoids dealing with confusing “half-finished” renders where only some of the variables have been updated.

React does not batch across multiple intentional events like clicks—each click is handled separately. Rest assured that React only does batching when it’s generally safe to do. This ensures that, for example, if the first button click disables a form, the second click would not submit it again.

It is an uncommon use case, but if you would like to update the same state variable multiple times before the next render, instead of passing the next state value like setNumber(number + 1), you can pass a function that calculates the next state based on the previous one in the queue, like setNumber(n => n + 1). It is a way to tell React to “do something with the state value” instead of just replacing it.

Try incrementing the counter now:

Here, n => n + 1 is called an updater function. When you pass it to a state setter:

Here’s how React works through these lines of code while executing the event handler:

When you call useState during the next render, React goes through the 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
setNumber(0 + 1);setNumber(0 + 1);setNumber(0 + 1);
```

Example 2 (javascript):
```javascript
setNumber(n => n + 1);setNumber(n => n + 1);setNumber(n => n + 1);
```

Example 3 (javascript):
```javascript
<button onClick={() => {  setNumber(number + 5);  setNumber(n => n + 1);}}>
```

Example 4 (javascript):
```javascript
<button onClick={() => {  setNumber(number + 5);  setNumber(n => n + 1);  setNumber(42);}}>
```

---

## Thinking in React

**URL:** https://react.dev/learn/thinking-in-react#step-4-identify-where-your-state-should-live

**Contents:**
- Thinking in React
- Start with the mockup
- Step 1: Break the UI into a component hierarchy
- Step 2: Build a static version in React
  - Pitfall
- Step 3: Find the minimal but complete representation of UI state
      - Deep Dive
    - Props vs State
- Step 4: Identify where your state should live
- Step 5: Add inverse data flow

React can change how you think about the designs you look at and the apps you build. When you build a user interface with React, you will first break it apart into pieces called components. Then, you will describe the different visual states for each of your components. Finally, you will connect your components together so that the data flows through them. In this tutorial, we’ll guide you through the thought process of building a searchable product data table with React.

Imagine that you already have a JSON API and a mockup from a designer.

The JSON API returns some data that looks like this:

The mockup looks like this:

To implement a UI in React, you will usually follow the same five steps.

Start by drawing boxes around every component and subcomponent in the mockup and naming them. If you work with a designer, they may have already named these components in their design tool. Ask them!

Depending on your background, you can think about splitting up a design into components in different ways:

If your JSON is well-structured, you’ll often find that it naturally maps to the component structure of your UI. That’s because UI and data models often have the same information architecture—that is, the same shape. Separate your UI into components, where each component matches one piece of your data model.

There are five components on this screen:

If you look at ProductTable (lavender), you’ll see that the table header (containing the “Name” and “Price” labels) isn’t its own component. This is a matter of preference, and you could go either way. For this example, it is a part of ProductTable because it appears inside the ProductTable’s list. However, if this header grows to be complex (e.g., if you add sorting), you can move it into its own ProductTableHeader component.

Now that you’ve identified the components in the mockup, arrange them into a hierarchy. Components that appear within another component in the mockup should appear as a child in the hierarchy:

Now that you have your component hierarchy, it’s time to implement your app. The most straightforward approach is to build a version that renders the UI from your data model without adding any interactivity… yet! It’s often easier to build the static version first and add interactivity later. Building a static version requires a lot of typing and no thinking, but adding interactivity requires a lot of thinking and not a lot of typing.

To build a static version of your app that renders your data mod

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
[  { category: "Fruits", price: "$1", stocked: true, name: "Apple" },  { category: "Fruits", price: "$1", stocked: true, name: "Dragonfruit" },  { category: "Fruits", price: "$2", stocked: false, name: "Passionfruit" },  { category: "Vegetables", price: "$2", stocked: true, name: "Spinach" },  { category: "Vegetables", price: "$4", stocked: false, name: "Pumpkin" },  { category: "Vegetables", price: "$1", stocked: true, name: "Peas" }]
```

Example 2 (javascript):
```javascript
function FilterableProductTable({ products }) {  const [filterText, setFilterText] = useState('');  const [inStockOnly, setInStockOnly] = useState(false);
```

Example 3 (unknown):
```unknown
<div>  <SearchBar     filterText={filterText}     inStockOnly={inStockOnly} />  <ProductTable     products={products}    filterText={filterText}    inStockOnly={inStockOnly} /></div>
```

Example 4 (unknown):
```unknown
function SearchBar({ filterText, inStockOnly }) {  return (    <form>      <input         type="text"         value={filterText}         placeholder="Search..."/>
```

---

## Choosing the State Structure

**URL:** https://react.dev/learn/choosing-the-state-structure

**Contents:**
- Choosing the State Structure
  - You will learn
- Principles for structuring state
- Group related state
  - Pitfall
- Avoid contradictions in state
- Avoid redundant state
      - Deep Dive
    - Don’t mirror props in state
- Avoid duplication in state

Structuring state well can make a difference between a component that is pleasant to modify and debug, and one that is a constant source of bugs. Here are some tips you should consider when structuring state.

When you write a component that holds some state, you’ll have to make choices about how many state variables to use and what the shape of their data should be. While it’s possible to write correct programs even with a suboptimal state structure, there are a few principles that can guide you to make better choices:

The goal behind these principles is to make state easy to update without introducing mistakes. Removing redundant and duplicate data from state helps ensure that all its pieces stay in sync. This is similar to how a database engineer might want to “normalize” the database structure to reduce the chance of bugs. To paraphrase Albert Einstein, “Make your state as simple as it can be—but no simpler.”

Now let’s see how these principles apply in action.

You might sometimes be unsure between using a single or multiple state variables.

Technically, you can use either of these approaches. But if some two state variables always change together, it might be a good idea to unify them into a single state variable. Then you won’t forget to always keep them in sync, like in this example where moving the cursor updates both coordinates of the red dot:

Another case where you’ll group data into an object or an array is when you don’t know how many pieces of state you’ll need. For example, it’s helpful when you have a form where the user can add custom fields.

If your state variable is an object, remember that you can’t update only one field in it without explicitly copying the other fields. For example, you can’t do setPosition({ x: 100 }) in the above example because it would not have the y property at all! Instead, if you wanted to set x alone, you would either do setPosition({ ...position, x: 100 }), or split them into two state variables and do setX(100).

Here is a hotel feedback form with isSending and isSent state variables:

While this code works, it leaves the door open for “impossible” states. For example, if you forget to call setIsSent and setIsSending together, you may end up in a situation where both isSending and isSent are true at the same time. The more complex your component is, the harder it is to understand what happened.

Since isSending and isSent should never be true at the same time, it is better to replace them with one status

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [x, setX] = useState(0);const [y, setY] = useState(0);
```

Example 2 (javascript):
```javascript
const [position, setPosition] = useState({ x: 0, y: 0 });
```

Example 3 (javascript):
```javascript
const isSending = status === 'sending';const isSent = status === 'sent';
```

Example 4 (javascript):
```javascript
const fullName = firstName + ' ' + lastName;
```

---

## Built-in React APIs

**URL:** https://react.dev/reference/react/apis

**Contents:**
- Built-in React APIs
- Resource APIs

In addition to Hooks and Components, the react package exports a few other APIs that are useful for defining components. This page lists all the remaining modern React APIs.

Resources can be accessed by a component without having them as part of their state. For example, a component can read a message from a Promise or read styling information from a context.

To read a value from a resource, use this API:

**Examples:**

Example 1 (javascript):
```javascript
function MessageComponent({ messagePromise }) {  const message = use(messagePromise);  const theme = use(ThemeContext);  // ...}
```

---

## Built-in React APIs

**URL:** https://react.dev/reference/react/apis#resource-apis

**Contents:**
- Built-in React APIs
- Resource APIs

In addition to Hooks and Components, the react package exports a few other APIs that are useful for defining components. This page lists all the remaining modern React APIs.

Resources can be accessed by a component without having them as part of their state. For example, a component can read a message from a Promise or read styling information from a context.

To read a value from a resource, use this API:

**Examples:**

Example 1 (javascript):
```javascript
function MessageComponent({ messagePromise }) {  const message = use(messagePromise);  const theme = use(ThemeContext);  // ...}
```

---

## useActionState

**URL:** https://react.dev/reference/react/useActionState

**Contents:**
- useActionState
  - Note
- Reference
  - useActionState(action, initialState, permalink?)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Using information returned by a form action
    - Display information after submitting a form

useActionState is a Hook that allows you to update state based on the result of a form action.

In earlier React Canary versions, this API was part of React DOM and called useFormState.

Call useActionState at the top level of your component to create component state that is updated when a form action is invoked. You pass useActionState an existing form action function as well as an initial state, and it returns a new action that you use in your form, along with the latest form state and whether the Action is still pending. The latest form state is also passed to the function that you provided.

The form state is the value returned by the action when the form was last submitted. If the form has not yet been submitted, it is the initial state that you pass.

If used with a Server Function, useActionState allows the server’s response from submitting the form to be shown even before hydration has completed.

See more examples below.

useActionState returns an array with the following values:

Call useActionState at the top level of your component to access the return value of an action from the last time a form was submitted.

useActionState returns an array with the following items:

When the form is submitted, the action function that you provided will be called. Its return value will become the new current state of the form.

The action that you provide will also receive a new first argument, namely the current state of the form. The first time the form is submitted, this will be the initial state you provided, while with subsequent submissions, it will be the return value from the last time the action was called. The rest of the arguments are the same as if useActionState had not been used.

To display messages such as an error message or toast that’s returned by a Server Function, wrap the action in a call to useActionState.

When you wrap an action with useActionState, it gets an extra argument as its first argument. The submitted form data is therefore its second argument instead of its first as it would usually be. The new first argument that gets added is the current state of the form.

**Examples:**

Example 1 (javascript):
```javascript
const [state, formAction, isPending] = useActionState(fn, initialState, permalink?);
```

Example 2 (python):
```python
import { useActionState } from "react";async function increment(previousState, formData) {  return previousState + 1;}function StatefulForm({}) {  const [state, formAction] = useActionState(increment, 0);  return (    <form>      {state}      <button formAction={formAction}>Increment</button>    </form>  )}
```

Example 3 (python):
```python
import { useActionState } from 'react';import { action } from './actions.js';function MyComponent() {  const [state, formAction] = useActionState(action, null);  // ...  return (    <form action={formAction}>      {/* ... */}    </form>  );}
```

Example 4 (unknown):
```unknown
function action(currentState, formData) {  // ...  return 'next state';}
```

---

## use

**URL:** https://react.dev/reference/react/use

**Contents:**
- use
- Reference
  - use(resource)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Reading context with use
  - Pitfall
  - Streaming data from the server to the client

use is a React API that lets you read the value of a resource like a Promise or context.

Call use in your component to read the value of a resource like a Promise or context.

Unlike React Hooks, use can be called within loops and conditional statements like if. Like React Hooks, the function that calls use must be a Component or Hook.

When called with a Promise, the use API integrates with Suspense and Error Boundaries. The component calling use suspends while the Promise passed to use is pending. If the component that calls use is wrapped in a Suspense boundary, the fallback will be displayed. Once the Promise is resolved, the Suspense fallback is replaced by the rendered components using the data returned by the use API. If the Promise passed to use is rejected, the fallback of the nearest Error Boundary will be displayed.

See more examples below.

The use API returns the value that was read from the resource like the resolved value of a Promise or context.

When a context is passed to use, it works similarly to useContext. While useContext must be called at the top level of your component, use can be called inside conditionals like if and loops like for. use is preferred over useContext because it is more flexible.

use returns the context value for the context you passed. To determine the context value, React searches the component tree and finds the closest context provider above for that particular context.

To pass context to a Button, wrap it or one of its parent components into the corresponding context provider.

It doesn’t matter how many layers of components there are between the provider and the Button. When a Button anywhere inside of Form calls use(ThemeContext), it will receive "dark" as the value.

Unlike useContext, use can be called in conditionals and loops like if.

use is called from inside a if statement, allowing you to conditionally read values from a Context.

Like useContext, use(context) always looks for the closest context provider above the component that calls it. It searches upwards and does not consider context providers in the component from which you’re calling use(context).

Data can be streamed from the server to the client by passing a Promise as a prop from a Server Component to a Client Component.

The Client Component then takes the Promise it received as a prop and passes it to the use API. This allows the Client Component to read the value from the Promise that was initially created by the Server Component.

B

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const value = use(resource);
```

Example 2 (python):
```python
import { use } from 'react';function MessageComponent({ messagePromise }) {  const message = use(messagePromise);  const theme = use(ThemeContext);  // ...
```

Example 3 (python):
```python
import { use } from 'react';function Button() {  const theme = use(ThemeContext);  // ...
```

Example 4 (unknown):
```unknown
function MyPage() {  return (    <ThemeContext value="dark">      <Form />    </ThemeContext>  );}function Form() {  // ... renders buttons inside ...}
```

---

## Thinking in React

**URL:** https://react.dev/learn/thinking-in-react#step-3-find-the-minimal-but-complete-representation-of-ui-state

**Contents:**
- Thinking in React
- Start with the mockup
- Step 1: Break the UI into a component hierarchy
- Step 2: Build a static version in React
  - Pitfall
- Step 3: Find the minimal but complete representation of UI state
      - Deep Dive
    - Props vs State
- Step 4: Identify where your state should live
- Step 5: Add inverse data flow

React can change how you think about the designs you look at and the apps you build. When you build a user interface with React, you will first break it apart into pieces called components. Then, you will describe the different visual states for each of your components. Finally, you will connect your components together so that the data flows through them. In this tutorial, we’ll guide you through the thought process of building a searchable product data table with React.

Imagine that you already have a JSON API and a mockup from a designer.

The JSON API returns some data that looks like this:

The mockup looks like this:

To implement a UI in React, you will usually follow the same five steps.

Start by drawing boxes around every component and subcomponent in the mockup and naming them. If you work with a designer, they may have already named these components in their design tool. Ask them!

Depending on your background, you can think about splitting up a design into components in different ways:

If your JSON is well-structured, you’ll often find that it naturally maps to the component structure of your UI. That’s because UI and data models often have the same information architecture—that is, the same shape. Separate your UI into components, where each component matches one piece of your data model.

There are five components on this screen:

If you look at ProductTable (lavender), you’ll see that the table header (containing the “Name” and “Price” labels) isn’t its own component. This is a matter of preference, and you could go either way. For this example, it is a part of ProductTable because it appears inside the ProductTable’s list. However, if this header grows to be complex (e.g., if you add sorting), you can move it into its own ProductTableHeader component.

Now that you’ve identified the components in the mockup, arrange them into a hierarchy. Components that appear within another component in the mockup should appear as a child in the hierarchy:

Now that you have your component hierarchy, it’s time to implement your app. The most straightforward approach is to build a version that renders the UI from your data model without adding any interactivity… yet! It’s often easier to build the static version first and add interactivity later. Building a static version requires a lot of typing and no thinking, but adding interactivity requires a lot of thinking and not a lot of typing.

To build a static version of your app that renders your data mod

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
[  { category: "Fruits", price: "$1", stocked: true, name: "Apple" },  { category: "Fruits", price: "$1", stocked: true, name: "Dragonfruit" },  { category: "Fruits", price: "$2", stocked: false, name: "Passionfruit" },  { category: "Vegetables", price: "$2", stocked: true, name: "Spinach" },  { category: "Vegetables", price: "$4", stocked: false, name: "Pumpkin" },  { category: "Vegetables", price: "$1", stocked: true, name: "Peas" }]
```

Example 2 (javascript):
```javascript
function FilterableProductTable({ products }) {  const [filterText, setFilterText] = useState('');  const [inStockOnly, setInStockOnly] = useState(false);
```

Example 3 (unknown):
```unknown
<div>  <SearchBar     filterText={filterText}     inStockOnly={inStockOnly} />  <ProductTable     products={products}    filterText={filterText}    inStockOnly={inStockOnly} /></div>
```

Example 4 (unknown):
```unknown
function SearchBar({ filterText, inStockOnly }) {  return (    <form>      <input         type="text"         value={filterText}         placeholder="Search..."/>
```

---

## Preserving and Resetting State

**URL:** https://react.dev/learn/preserving-and-resetting-state

**Contents:**
- Preserving and Resetting State
  - You will learn
- State is tied to a position in the render tree
- Same component at the same position preserves state
  - Pitfall
- Different components at the same position reset state
  - Pitfall
- Resetting state at the same position
  - Option 1: Rendering a component in different positions
  - Option 2: Resetting state with a key

State is isolated between components. React keeps track of which state belongs to which component based on their place in the UI tree. You can control when to preserve state and when to reset it between re-renders.

React builds render trees for the component structure in your UI.

When you give a component state, you might think the state “lives” inside the component. But the state is actually held inside React. React associates each piece of state it’s holding with the correct component by where that component sits in the render tree.

Here, there is only one <Counter /> JSX tag, but it’s rendered at two different positions:

Here’s how these look as a tree:

These are two separate counters because each is rendered at its own position in the tree. You don’t usually have to think about these positions to use React, but it can be useful to understand how it works.

In React, each component on the screen has fully isolated state. For example, if you render two Counter components side by side, each of them will get its own, independent, score and hover states.

Try clicking both counters and notice they don’t affect each other:

As you can see, when one counter is updated, only the state for that component is updated:

React will keep the state around for as long as you render the same component at the same position in the tree. To see this, increment both counters, then remove the second component by unchecking “Render the second counter” checkbox, and then add it back by ticking it again:

Notice how the moment you stop rendering the second counter, its state disappears completely. That’s because when React removes a component, it destroys its state.

When you tick “Render the second counter”, a second Counter and its state are initialized from scratch (score = 0) and added to the DOM.

React preserves a component’s state for as long as it’s being rendered at its position in the UI tree. If it gets removed, or a different component gets rendered at the same position, React discards its state.

In this example, there are two different <Counter /> tags:

When you tick or clear the checkbox, the counter state does not get reset. Whether isFancy is true or false, you always have a <Counter /> as the first child of the div returned from the root App component:

Updating the App state does not reset the Counter because Counter stays in the same position

It’s the same component at the same position, so from React’s perspective, it’s the same counter.

Remember t

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
{isPlayerA ? (  <Counter key="Taylor" person="Taylor" />) : (  <Counter key="Sarah" person="Sarah" />)}
```

Example 2 (unknown):
```unknown
<Chat key={to.id} contact={to} />
```

---

## createContext

**URL:** https://react.dev/reference/react/createContext

**Contents:**
- createContext
- Reference
  - createContext(defaultValue)
    - Parameters
    - Returns
  - SomeContext Provider
  - Note
    - Props
  - SomeContext.Consumer
    - Props

createContext lets you create a context that components can provide or read.

Call createContext outside of any components to create a context.

See more examples below.

createContext returns a context object.

The context object itself does not hold any information. It represents which context other components read or provide. Typically, you will use SomeContext in components above to specify the context value, and call useContext(SomeContext) in components below to read it. The context object has a few properties:

Wrap your components into a context provider to specify the value of this context for all components inside:

Starting in React 19, you can render <SomeContext> as a provider.

In older versions of React, use <SomeContext.Provider>.

Before useContext existed, there was an older way to read context:

Although this older way still works, newly written code should read context with useContext() instead:

Context lets components pass information deep down without explicitly passing props.

Call createContext outside any components to create one or more contexts.

createContext returns a context object. Components can read context by passing it to useContext():

By default, the values they receive will be the default values you have specified when creating the contexts. However, by itself this isn’t useful because the default values never change.

Context is useful because you can provide other, dynamic values from your components:

Now the Page component and any components inside it, no matter how deep, will “see” the passed context values. If the passed context values change, React will re-render the components reading the context as well.

Read more about reading and providing context and see examples.

Often, components in different files will need access to the same context. This is why it’s common to declare contexts in a separate file. Then you can use the export statement to make context available for other files:

Components declared in other files can then use the import statement to read or provide this context:

This works similar to importing and exporting components.

Code like this specifies the default context value:

This value never changes. React only uses this value as a fallback if it can’t find a matching provider above.

To make context change over time, add state and wrap components in a context provider.

**Examples:**

Example 1 (javascript):
```javascript
const SomeContext = createContext(defaultValue)
```

Example 2 (python):
```python
import { createContext } from 'react';const ThemeContext = createContext('light');
```

Example 3 (javascript):
```javascript
function App() {  const [theme, setTheme] = useState('light');  // ...  return (    <ThemeContext value={theme}>      <Page />    </ThemeContext>  );}
```

Example 4 (javascript):
```javascript
function Button() {  // 🟡 Legacy way (not recommended)  return (    <ThemeContext.Consumer>      {theme => (        <button className={theme} />      )}    </ThemeContext.Consumer>  );}
```

---

## Updating Arrays in State

**URL:** https://react.dev/learn/updating-arrays-in-state

**Contents:**
- Updating Arrays in State
  - You will learn
- Updating arrays without mutation
  - Pitfall
  - Adding to an array
  - Removing from an array
  - Transforming an array
  - Replacing items in an array
  - Inserting into an array
  - Making other changes to an array

Arrays are mutable in JavaScript, but you should treat them as immutable when you store them in state. Just like with objects, when you want to update an array stored in state, you need to create a new one (or make a copy of an existing one), and then set state to use the new array.

In JavaScript, arrays are just another kind of object. Like with objects, you should treat arrays in React state as read-only. This means that you shouldn’t reassign items inside an array like arr[0] = 'bird', and you also shouldn’t use methods that mutate the array, such as push() and pop().

Instead, every time you want to update an array, you’ll want to pass a new array to your state setting function. To do that, you can create a new array from the original array in your state by calling its non-mutating methods like filter() and map(). Then you can set your state to the resulting new array.

Here is a reference table of common array operations. When dealing with arrays inside React state, you will need to avoid the methods in the left column, and instead prefer the methods in the right column:

Alternatively, you can use Immer which lets you use methods from both columns.

Unfortunately, slice and splice are named similarly but are very different:

In React, you will be using slice (no p!) a lot more often because you don’t want to mutate objects or arrays in state. Updating Objects explains what mutation is and why it’s not recommended for state.

push() will mutate an array, which you don’t want:

Instead, create a new array which contains the existing items and a new item at the end. There are multiple ways to do this, but the easiest one is to use the ... array spread syntax:

Now it works correctly:

The array spread syntax also lets you prepend an item by placing it before the original ...artists:

In this way, spread can do the job of both push() by adding to the end of an array and unshift() by adding to the beginning of an array. Try it in the sandbox above!

The easiest way to remove an item from an array is to filter it out. In other words, you will produce a new array that will not contain that item. To do this, use the filter method, for example:

Click the “Delete” button a few times, and look at its click handler.

Here, artists.filter(a => a.id !== artist.id) means “create an array that consists of those artists whose IDs are different from artist.id”. In other words, each artist’s “Delete” button will filter that artist out of the array, and then request a

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
setArtists( // Replace the state  [ // with a new array    ...artists, // that contains all the old items    { id: nextId++, name: name } // and one new item at the end  ]);
```

Example 2 (unknown):
```unknown
setArtists([  { id: nextId++, name: name },  ...artists // Put old items at the end]);
```

Example 3 (javascript):
```javascript
setArtists(  artists.filter(a => a.id !== artist.id));
```

Example 4 (javascript):
```javascript
const nextList = [...list];nextList[0].seen = true; // Problem: mutates list[0]setList(nextList);
```

---

## Choosing the State Structure

**URL:** https://react.dev/learn/choosing-the-state-structure#avoid-redundant-state

**Contents:**
- Choosing the State Structure
  - You will learn
- Principles for structuring state
- Group related state
  - Pitfall
- Avoid contradictions in state
- Avoid redundant state
      - Deep Dive
    - Don’t mirror props in state
- Avoid duplication in state

Structuring state well can make a difference between a component that is pleasant to modify and debug, and one that is a constant source of bugs. Here are some tips you should consider when structuring state.

When you write a component that holds some state, you’ll have to make choices about how many state variables to use and what the shape of their data should be. While it’s possible to write correct programs even with a suboptimal state structure, there are a few principles that can guide you to make better choices:

The goal behind these principles is to make state easy to update without introducing mistakes. Removing redundant and duplicate data from state helps ensure that all its pieces stay in sync. This is similar to how a database engineer might want to “normalize” the database structure to reduce the chance of bugs. To paraphrase Albert Einstein, “Make your state as simple as it can be—but no simpler.”

Now let’s see how these principles apply in action.

You might sometimes be unsure between using a single or multiple state variables.

Technically, you can use either of these approaches. But if some two state variables always change together, it might be a good idea to unify them into a single state variable. Then you won’t forget to always keep them in sync, like in this example where moving the cursor updates both coordinates of the red dot:

Another case where you’ll group data into an object or an array is when you don’t know how many pieces of state you’ll need. For example, it’s helpful when you have a form where the user can add custom fields.

If your state variable is an object, remember that you can’t update only one field in it without explicitly copying the other fields. For example, you can’t do setPosition({ x: 100 }) in the above example because it would not have the y property at all! Instead, if you wanted to set x alone, you would either do setPosition({ ...position, x: 100 }), or split them into two state variables and do setX(100).

Here is a hotel feedback form with isSending and isSent state variables:

While this code works, it leaves the door open for “impossible” states. For example, if you forget to call setIsSent and setIsSending together, you may end up in a situation where both isSending and isSent are true at the same time. The more complex your component is, the harder it is to understand what happened.

Since isSending and isSent should never be true at the same time, it is better to replace them with one status

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [x, setX] = useState(0);const [y, setY] = useState(0);
```

Example 2 (javascript):
```javascript
const [position, setPosition] = useState({ x: 0, y: 0 });
```

Example 3 (javascript):
```javascript
const isSending = status === 'sending';const isSent = status === 'sent';
```

Example 4 (javascript):
```javascript
const fullName = firstName + ' ' + lastName;
```

---

## Extracting State Logic into a Reducer

**URL:** https://react.dev/learn/extracting-state-logic-into-a-reducer

**Contents:**
- Extracting State Logic into a Reducer
  - You will learn
- Consolidate state logic with a reducer
  - Step 1: Move from setting state to dispatching actions
  - Note
  - Step 2: Write a reducer function
  - Note
      - Deep Dive
    - Why are reducers called this way?
  - Step 3: Use the reducer from your component

Components with many state updates spread across many event handlers can get overwhelming. For these cases, you can consolidate all the state update logic outside your component in a single function, called a reducer.

As your components grow in complexity, it can get harder to see at a glance all the different ways in which a component’s state gets updated. For example, the TaskApp component below holds an array of tasks in state and uses three different event handlers to add, remove, and edit tasks:

Each of its event handlers calls setTasks in order to update the state. As this component grows, so does the amount of state logic sprinkled throughout it. To reduce this complexity and keep all your logic in one easy-to-access place, you can move that state logic into a single function outside your component, called a “reducer”.

Reducers are a different way to handle state. You can migrate from useState to useReducer in three steps:

Your event handlers currently specify what to do by setting state:

Remove all the state setting logic. What you are left with are three event handlers:

Managing state with reducers is slightly different from directly setting state. Instead of telling React “what to do” by setting state, you specify “what the user just did” by dispatching “actions” from your event handlers. (The state update logic will live elsewhere!) So instead of “setting tasks” via an event handler, you’re dispatching an “added/changed/deleted a task” action. This is more descriptive of the user’s intent.

The object you pass to dispatch is called an “action”:

It is a regular JavaScript object. You decide what to put in it, but generally it should contain the minimal information about what happened. (You will add the dispatch function itself in a later step.)

An action object can have any shape.

By convention, it is common to give it a string type that describes what happened, and pass any additional information in other fields. The type is specific to a component, so in this example either 'added' or 'added_task' would be fine. Choose a name that says what happened!

A reducer function is where you will put your state logic. It takes two arguments, the current state and the action object, and it returns the next state:

React will set the state to what you return from the reducer.

To move your state setting logic from your event handlers to a reducer function in this example, you will:

Here is all the state setting logic migrated to a reducer functi

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
function handleAddTask(text) {  setTasks([    ...tasks,    {      id: nextId++,      text: text,      done: false,    },  ]);}function handleChangeTask(task) {  setTasks(    tasks.map((t) => {      if (t.id === task.id) {        return task;      } else {        return t;      }    })  );}function handleDeleteTask(taskId) {  setTasks(tasks.filter((t) => t.id !== taskId));}
```

Example 2 (unknown):
```unknown
function handleAddTask(text) {  dispatch({    type: 'added',    id: nextId++,    text: text,  });}function handleChangeTask(task) {  dispatch({    type: 'changed',    task: task,  });}function handleDeleteTask(taskId) {  dispatch({    type: 'deleted',    id: taskId,  });}
```

Example 3 (unknown):
```unknown
function handleDeleteTask(taskId) {  dispatch(    // "action" object:    {      type: 'deleted',      id: taskId,    }  );}
```

Example 4 (unknown):
```unknown
dispatch({  // specific to component  type: 'what_happened',  // other fields go here});
```

---

## Built-in React APIs

**URL:** https://react.dev/reference/react/apis#undefined

**Contents:**
- Built-in React APIs
- Resource APIs

In addition to Hooks and Components, the react package exports a few other APIs that are useful for defining components. This page lists all the remaining modern React APIs.

Resources can be accessed by a component without having them as part of their state. For example, a component can read a message from a Promise or read styling information from a context.

To read a value from a resource, use this API:

**Examples:**

Example 1 (javascript):
```javascript
function MessageComponent({ messagePromise }) {  const message = use(messagePromise);  const theme = use(ThemeContext);  // ...}
```

---

## Updating Objects in State

**URL:** https://react.dev/learn/updating-objects-in-state

**Contents:**
- Updating Objects in State
  - You will learn
- What’s a mutation?
- Treat state as read-only
      - Deep Dive
    - Local mutation is fine
- Copying objects with the spread syntax
      - Deep Dive
    - Using a single event handler for multiple fields
- Updating a nested object

State can hold any kind of JavaScript value, including objects. But you shouldn’t change objects that you hold in the React state directly. Instead, when you want to update an object, you need to create a new one (or make a copy of an existing one), and then set the state to use that copy.

You can store any kind of JavaScript value in state.

So far you’ve been working with numbers, strings, and booleans. These kinds of JavaScript values are “immutable”, meaning unchangeable or “read-only”. You can trigger a re-render to replace a value:

The x state changed from 0 to 5, but the number 0 itself did not change. It’s not possible to make any changes to the built-in primitive values like numbers, strings, and booleans in JavaScript.

Now consider an object in state:

Technically, it is possible to change the contents of the object itself. This is called a mutation:

However, although objects in React state are technically mutable, you should treat them as if they were immutable—like numbers, booleans, and strings. Instead of mutating them, you should always replace them.

In other words, you should treat any JavaScript object that you put into state as read-only.

This example holds an object in state to represent the current pointer position. The red dot is supposed to move when you touch or move the cursor over the preview area. But the dot stays in the initial position:

The problem is with this bit of code.

This code modifies the object assigned to position from the previous render. But without using the state setting function, React has no idea that object has changed. So React does not do anything in response. It’s like trying to change the order after you’ve already eaten the meal. While mutating state can work in some cases, we don’t recommend it. You should treat the state value you have access to in a render as read-only.

To actually trigger a re-render in this case, create a new object and pass it to the state setting function:

With setPosition, you’re telling React:

Notice how the red dot now follows your pointer when you touch or hover over the preview area:

Code like this is a problem because it modifies an existing object in state:

But code like this is absolutely fine because you’re mutating a fresh object you have just created:

In fact, it is completely equivalent to writing this:

Mutation is only a problem when you change existing objects that are already in state. Mutating an object you’ve just created is okay because no other code

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [x, setX] = useState(0);
```

Example 2 (javascript):
```javascript
const [position, setPosition] = useState({ x: 0, y: 0 });
```

Example 3 (unknown):
```unknown
position.x = 5;
```

Example 4 (javascript):
```javascript
onPointerMove={e => {  position.x = e.clientX;  position.y = e.clientY;}}
```

---
