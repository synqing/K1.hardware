# React - Api

**Pages:** 51

---

## React DOM APIs

**URL:** https://react.dev/reference/react-dom#apis

**Contents:**
- React DOM APIs
- APIs
- Resource Preloading APIs
- Entry points
- Removed APIs

The react-dom package contains methods that are only supported for the web applications (which run in the browser DOM environment). They are not supported for React Native.

These APIs can be imported from your components. They are rarely used:

These APIs can be used to make apps faster by pre-loading resources such as scripts, stylesheets, and fonts as soon as you know you need them, for example before navigating to another page where the resources will be used.

React-based frameworks frequently handle resource loading for you, so you might not have to call these APIs yourself. Consult your framework’s documentation for details.

The react-dom package provides two additional entry points:

These APIs were removed in React 19:

---

## Directives

**URL:** https://react.dev/reference/react-compiler/directives

**Contents:**
- Directives
- Overview
  - Available directives
  - Quick comparison
- Usage
  - Function-level directives
  - Module-level directives
  - Compilation modes interaction
- Best practices
  - Use directives sparingly

React Compiler directives are special string literals that control whether specific functions are compiled.

React Compiler directives provide fine-grained control over which functions are optimized by the compiler. They are string literals placed at the beginning of a function body or at the top of a module.

Place directives at the beginning of a function to control its compilation:

Place directives at the top of a file to affect all functions in that module:

Directives behave differently depending on your compilationMode:

Directives are escape hatches. Prefer configuring the compiler at the project level:

Always explain why a directive is used:

Opt-out directives should be temporary:

When adopting the React Compiler in a large codebase:

For specific issues with directives, see the troubleshooting sections in:

**Examples:**

Example 1 (unknown):
```unknown
function MyComponent() {  "use memo"; // Opt this component into compilation  return <div>{/* ... */}</div>;}
```

Example 2 (unknown):
```unknown
// Opt into compilationfunction OptimizedComponent() {  "use memo";  return <div>This will be optimized</div>;}// Opt out of compilationfunction UnoptimizedComponent() {  "use no memo";  return <div>This won't be optimized</div>;}
```

Example 3 (unknown):
```unknown
// At the very top of the file"use memo";// All functions in this file will be compiledfunction Component1() {  return <div>Compiled</div>;}function Component2() {  return <div>Also compiled</div>;}// Can be overridden at function levelfunction Component3() {  "use no memo"; // This overrides the module directive  return <div>Not compiled</div>;}
```

Example 4 (unknown):
```unknown
// ✅ Good - project-wide configuration{  plugins: [    ['babel-plugin-react-compiler', {      compilationMode: 'infer'    }]  ]}// ⚠️ Use directives only when neededfunction SpecialCase() {  "use no memo"; // Document why this is needed  // ...}
```

---

## React DOM APIs

**URL:** https://react.dev/reference/react-dom

**Contents:**
- React DOM APIs
- APIs
- Resource Preloading APIs
- Entry points
- Removed APIs

The react-dom package contains methods that are only supported for the web applications (which run in the browser DOM environment). They are not supported for React Native.

These APIs can be imported from your components. They are rarely used:

These APIs can be used to make apps faster by pre-loading resources such as scripts, stylesheets, and fonts as soon as you know you need them, for example before navigating to another page where the resources will be used.

React-based frameworks frequently handle resource loading for you, so you might not have to call these APIs yourself. Consult your framework’s documentation for details.

The react-dom package provides two additional entry points:

These APIs were removed in React 19:

---

## React DOM APIs

**URL:** https://react.dev/reference/react-dom#undefined

**Contents:**
- React DOM APIs
- APIs
- Resource Preloading APIs
- Entry points
- Removed APIs

The react-dom package contains methods that are only supported for the web applications (which run in the browser DOM environment). They are not supported for React Native.

These APIs can be imported from your components. They are rarely used:

These APIs can be used to make apps faster by pre-loading resources such as scripts, stylesheets, and fonts as soon as you know you need them, for example before navigating to another page where the resources will be used.

React-based frameworks frequently handle resource loading for you, so you might not have to call these APIs yourself. Consult your framework’s documentation for details.

The react-dom package provides two additional entry points:

These APIs were removed in React 19:

---

## preloadModule

**URL:** https://react.dev/reference/react-dom/preloadModule

**Contents:**
- preloadModule
  - Note
- Reference
  - preloadModule(href, options)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Preloading when rendering
  - Preloading in an event handler

React-based frameworks frequently handle resource loading for you, so you might not have to call this API yourself. Consult your framework’s documentation for details.

preloadModule lets you eagerly fetch an ESM module that you expect to use.

To preload an ESM module, call the preloadModule function from react-dom.

See more examples below.

The preloadModule function provides the browser with a hint that it should start downloading the given module, which can save time.

preloadModule returns nothing.

Call preloadModule when rendering a component if you know that it or its children will use a specific module.

If you want the browser to start executing the module immediately (rather than just downloading it), use preinitModule instead. If you want to load a script that isn’t an ESM module, use preload.

Call preloadModule in an event handler before transitioning to a page or state where the module will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

**Examples:**

Example 1 (unknown):
```unknown
preloadModule("https://example.com/module.js", {as: "script"});
```

Example 2 (python):
```python
import { preloadModule } from 'react-dom';function AppRoot() {  preloadModule("https://example.com/module.js", {as: "script"});  // ...}
```

Example 3 (python):
```python
import { preloadModule } from 'react-dom';function AppRoot() {  preloadModule("https://example.com/module.js", {as: "script"});  return ...;}
```

Example 4 (python):
```python
import { preloadModule } from 'react-dom';function CallToAction() {  const onClick = () => {    preloadModule("https://example.com/module.js", {as: "script"});    startWizard();  }  return (    <button onClick={onClick}>Start Wizard</button>  );}
```

---

## <Suspense>

**URL:** https://react.dev/reference/react/Suspense

**Contents:**
- <Suspense>
- Reference
  - <Suspense>
    - Props
    - Caveats
- Usage
  - Displaying a fallback while content is loading
  - Note
  - Revealing content together at once
  - Revealing nested content as it loads

<Suspense> lets you display a fallback until its children have finished loading.

You can wrap any part of your application with a Suspense boundary:

React will display your loading fallback until all the code and data needed by the children has been loaded.

In the example below, the Albums component suspends while fetching the list of albums. Until it’s ready to render, React switches the closest Suspense boundary above to show the fallback—your Loading component. Then, when the data loads, React hides the Loading fallback and renders the Albums component with data.

Only Suspense-enabled data sources will activate the Suspense component. They include:

Suspense does not detect when data is fetched inside an Effect or event handler.

The exact way you would load data in the Albums component above depends on your framework. If you use a Suspense-enabled framework, you’ll find the details in its data fetching documentation.

Suspense-enabled data fetching without the use of an opinionated framework is not yet supported. The requirements for implementing a Suspense-enabled data source are unstable and undocumented. An official API for integrating data sources with Suspense will be released in a future version of React.

By default, the whole tree inside Suspense is treated as a single unit. For example, even if only one of these components suspends waiting for some data, all of them together will be replaced by the loading indicator:

Then, after all of them are ready to be displayed, they will all appear together at once.

In the example below, both Biography and Albums fetch some data. However, because they are grouped under a single Suspense boundary, these components always “pop in” together at the same time.

Components that load data don’t have to be direct children of the Suspense boundary. For example, you can move Biography and Albums into a new Details component. This doesn’t change the behavior. Biography and Albums share the same closest parent Suspense boundary, so their reveal is coordinated together.

When a component suspends, the closest parent Suspense component shows the fallback. This lets you nest multiple Suspense components to create a loading sequence. Each Suspense boundary’s fallback will be filled in as the next level of content becomes available. For example, you can give the album list its own fallback:

With this change, displaying the Biography doesn’t need to “wait” for the Albums to load.

The sequence will be:

Suspense bo

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<Suspense fallback={<Loading />}>  <SomeComponent /></Suspense>
```

Example 2 (unknown):
```unknown
<Suspense fallback={<Loading />}>  <Albums /></Suspense>
```

Example 3 (unknown):
```unknown
<Suspense fallback={<Loading />}>  <Biography />  <Panel>    <Albums />  </Panel></Suspense>
```

Example 4 (unknown):
```unknown
<Suspense fallback={<Loading />}>  <Details artistId={artist.id} /></Suspense>function Details({ artistId }) {  return (    <>      <Biography artistId={artistId} />      <Panel>        <Albums artistId={artistId} />      </Panel>    </>  );}
```

---

## React Reference Overview

**URL:** https://react.dev/reference/react#react-compiler

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

## <Fragment> (<>...</>)

**URL:** https://react.dev/reference/react/Fragment

**Contents:**
- <Fragment> (<>...</>)
  - Canary
- Reference
  - <Fragment>
    - Props
  - Canary only FragmentInstance
    - Caveats
- Usage
  - Returning multiple elements
      - Deep Dive

<Fragment>, often used via <>...</> syntax, lets you group elements without a wrapper node.

Wrap elements in <Fragment> to group them together in situations where you need a single element. Grouping elements in Fragment has no effect on the resulting DOM; it is the same as if the elements were not grouped. The empty JSX tag <></> is shorthand for <Fragment></Fragment> in most cases.

When you pass a ref to a fragment, React provides a FragmentInstance object with methods for interacting with the DOM nodes wrapped by the fragment:

Event handling methods:

Focus management methods:

If you want to pass key to a Fragment, you can’t use the <>...</> syntax. You have to explicitly import Fragment from 'react' and render <Fragment key={yourKey}>...</Fragment>.

React does not reset state when you go from rendering <><Child /></> to [<Child />] or back, or when you go from rendering <><Child /></> to <Child /> and back. This only works a single level deep: for example, going from <><><Child /></></> to <Child /> resets the state. See the precise semantics here.

Canary only If you want to pass ref to a Fragment, you can’t use the <>...</> syntax. You have to explicitly import Fragment from 'react' and render <Fragment ref={yourRef}>...</Fragment>.

Use Fragment, or the equivalent <>...</> syntax, to group multiple elements together. You can use it to put multiple elements in any place where a single element can go. For example, a component can only return one element, but by using a Fragment you can group multiple elements together and then return them as a group:

Fragments are useful because grouping elements with a Fragment has no effect on layout or styles, unlike if you wrapped the elements in another container like a DOM element. If you inspect this example with the browser tools, you’ll see that all <h1> and <article> DOM nodes appear as siblings without wrappers around them:

The example above is equivalent to importing Fragment from React:

Usually you won’t need this unless you need to pass a key to your Fragment.

Like any other element, you can assign Fragment elements to variables, pass them as props, and so on:

You can use Fragment to group text together with components:

Here’s a situation where you need to write Fragment explicitly instead of using the <></> syntax. When you render multiple elements in a loop, you need to assign a key to each element. If the elements within the loop are Fragments, you need to use the normal JSX element syntax i

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<>  <OneChild />  <AnotherChild /></>
```

Example 2 (unknown):
```unknown
function Post() {  return (    <>      <PostTitle />      <PostBody />    </>  );}
```

Example 3 (python):
```python
import { Fragment } from 'react';function Post() {  return (    <Fragment>      <PostTitle />      <PostBody />    </Fragment>  );}
```

Example 4 (javascript):
```javascript
function CloseDialog() {  const buttons = (    <>      <OKButton />      <CancelButton />    </>  );  return (    <AlertDialog buttons={buttons}>      Are you sure you want to leave this page?    </AlertDialog>  );}
```

---

## React DOM APIs

**URL:** https://react.dev/reference/react-dom#entry-points

**Contents:**
- React DOM APIs
- APIs
- Resource Preloading APIs
- Entry points
- Removed APIs

The react-dom package contains methods that are only supported for the web applications (which run in the browser DOM environment). They are not supported for React Native.

These APIs can be imported from your components. They are rarely used:

These APIs can be used to make apps faster by pre-loading resources such as scripts, stylesheets, and fonts as soon as you know you need them, for example before navigating to another page where the resources will be used.

React-based frameworks frequently handle resource loading for you, so you might not have to call these APIs yourself. Consult your framework’s documentation for details.

The react-dom package provides two additional entry points:

These APIs were removed in React 19:

---

## <Activity>

**URL:** https://react.dev/reference/react/Activity

**Contents:**
- <Activity>
- Reference
  - <Activity>
    - Props
    - Caveats
- Usage
  - Restoring the state of hidden components
  - Restoring the DOM of hidden components
  - Pre-rendering content that’s likely to become visible
  - Note

<Activity> lets you hide and restore the UI and internal state of its children.

You can use Activity to hide part of your application:

When an Activity boundary is hidden, React will visually hide its children using the display: "none" CSS property. It will also destroy their Effects, cleaning up any active subscriptions.

While hidden, children still re-render in response to new props, albeit at a lower priority than the rest of the content.

When the boundary becomes visible again, React will reveal the children with their previous state restored, and re-create their Effects.

In this way, Activity can be thought of as a mechanism for rendering “background activity”. Rather than completely discarding content that’s likely to become visible again, you can use Activity to maintain and restore that content’s UI and internal state, while ensuring that your hidden content has no unwanted side effects.

See more examples below.

In React, when you want to conditionally show or hide a component, you typically mount or unmount it based on that condition:

But unmounting a component destroys its internal state, which is not always what you want.

When you hide a component using an Activity boundary instead, React will “save” its state for later:

This makes it possible to hide and then later restore components in the state they were previously in.

The following example has a sidebar with an expandable section. You can press “Overview” to reveal the three subitems below it. The main app area also has a button that hides and shows the sidebar.

Try expanding the Overview section, and then toggling the sidebar closed then open:

The Overview section always starts out collapsed. Because we unmount the sidebar when isShowingSidebar flips to false, all its internal state is lost.

This is a perfect use case for Activity. We can preserve the internal state of our sidebar, even when visually hiding it.

Let’s replace the conditional rendering of our sidebar with an Activity boundary:

and check out the new behavior:

Our sidebar’s internal state is now restored, without any changes to its implementation.

Since Activity boundaries hide their children using display: none, their children’s DOM is also preserved when hidden. This makes them great for maintaining ephemeral state in parts of the UI that the user is likely to interact with again.

In this example, the Contact tab has a <textarea> where the user can enter a message. If you enter some text, change to the Home

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<Activity mode={visibility}>  <Sidebar /></Activity>
```

Example 2 (unknown):
```unknown
<Activity mode={isShowingSidebar ? "visible" : "hidden"}>  <Sidebar /></Activity>
```

Example 3 (unknown):
```unknown
{isShowingSidebar && (  <Sidebar />)}
```

Example 4 (unknown):
```unknown
<Activity mode={isShowingSidebar ? "visible" : "hidden"}>  <Sidebar /></Activity>
```

---

## Client React DOM APIs

**URL:** https://react.dev/reference/react-dom/client

**Contents:**
- Client React DOM APIs
- Client APIs
- Browser support

The react-dom/client APIs let you render React components on the client (in the browser). These APIs are typically used at the top level of your app to initialize your React tree. A framework may call them for you. Most of your components don’t need to import or use them.

React supports all popular browsers, including Internet Explorer 9 and above. Some polyfills are required for older browsers such as IE 9 and IE 10.

---

## React Reference Overview

**URL:** https://react.dev/reference/react#rules-of-react

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

## Configuration

**URL:** https://react.dev/reference/react-compiler/configuration

**Contents:**
- Configuration
  - Note
- Compilation Control
- Version Compatibility
- Error Handling
- Debugging
- Feature Flags
- Common Configuration Patterns
  - Default configuration
  - React 17/18 projects

This page lists all configuration options available in React Compiler.

For most apps, the default options should work out of the box. If you have a special need, you can use these advanced options.

These options control what the compiler optimizes and how it selects components and hooks to compile.

React version configuration ensures the compiler generates code compatible with your React version.

target specifies which React version you’re using (17, 18, or 19).

These options control how the compiler responds to code that doesn’t follow the Rules of React.

panicThreshold determines whether to fail the build or skip problematic components.

Logging and analysis options help you understand what the compiler is doing.

logger provides custom logging for compilation events.

Conditional compilation lets you control when optimized code is used.

gating enables runtime feature flags for A/B testing or gradual rollouts.

For most React 19 applications, the compiler works without configuration:

Older React versions need the runtime package and target configuration:

Start with specific directories and expand gradually:

**Examples:**

Example 1 (unknown):
```unknown
// babel.config.jsmodule.exports = {  plugins: [    [      'babel-plugin-react-compiler', {        // compiler options      }    ]  ]};
```

Example 2 (unknown):
```unknown
{  compilationMode: 'annotation' // Only compile "use memo" functions}
```

Example 3 (unknown):
```unknown
// For React 18 projects{  target: '18' // Also requires react-compiler-runtime package}
```

Example 4 (unknown):
```unknown
// Recommended for production{  panicThreshold: 'none' // Skip components with errors instead of failing the build}
```

---

## preinit

**URL:** https://react.dev/reference/react-dom/preinit

**Contents:**
- preinit
  - Note
- Reference
  - preinit(href, options)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Preiniting when rendering
    - Examples of preiniting

React-based frameworks frequently handle resource loading for you, so you might not have to call this API yourself. Consult your framework’s documentation for details.

preinit lets you eagerly fetch and evaluate a stylesheet or external script.

To preinit a script or stylesheet, call the preinit function from react-dom.

See more examples below.

The preinit function provides the browser with a hint that it should start downloading and executing the given resource, which can save time. Scripts that you preinit are executed when they finish downloading. Stylesheets that you preinit are inserted into the document, which causes them to go into effect right away.

preinit returns nothing.

Call preinit when rendering a component if you know that it or its children will use a specific resource, and you’re OK with the resource being evaluated and thereby taking effect immediately upon being downloaded.

If you want the browser to download the script but not to execute it right away, use preload instead. If you want to load an ESM module, use preinitModule.

Call preinit in an event handler before transitioning to a page or state where external resources will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

**Examples:**

Example 1 (unknown):
```unknown
preinit("https://example.com/script.js", {as: "script"});
```

Example 2 (python):
```python
import { preinit } from 'react-dom';function AppRoot() {  preinit("https://example.com/script.js", {as: "script"});  // ...}
```

Example 3 (python):
```python
import { preinit } from 'react-dom';function AppRoot() {  preinit("https://example.com/script.js", {as: "script"});  return ...;}
```

Example 4 (python):
```python
import { preinit } from 'react-dom';function CallToAction() {  const onClick = () => {    preinit("https://example.com/wizardStyles.css", {as: "style"});    startWizard();  }  return (    <button onClick={onClick}>Start Wizard</button>  );}
```

---

## useSyncExternalStore

**URL:** https://react.dev/reference/react/useSyncExternalStore

**Contents:**
- useSyncExternalStore
- Reference
  - useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot?)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Subscribing to an external store
  - Note
  - Subscribing to a browser API

useSyncExternalStore is a React Hook that lets you subscribe to an external store.

Call useSyncExternalStore at the top level of your component to read a value from an external data store.

It returns the snapshot of the data in the store. You need to pass two functions as arguments:

See more examples below.

subscribe: A function that takes a single callback argument and subscribes it to the store. When the store changes, it should invoke the provided callback, which will cause React to re-call getSnapshot and (if needed) re-render the component. The subscribe function should return a function that cleans up the subscription.

getSnapshot: A function that returns a snapshot of the data in the store that’s needed by the component. While the store has not changed, repeated calls to getSnapshot must return the same value. If the store changes and the returned value is different (as compared by Object.is), React re-renders the component.

optional getServerSnapshot: A function that returns the initial snapshot of the data in the store. It will be used only during server rendering and during hydration of server-rendered content on the client. The server snapshot must be the same between the client and the server, and is usually serialized and passed from the server to the client. If you omit this argument, rendering the component on the server will throw an error.

The current snapshot of the store which you can use in your rendering logic.

The store snapshot returned by getSnapshot must be immutable. If the underlying store has mutable data, return a new immutable snapshot if the data has changed. Otherwise, return a cached last snapshot.

If a different subscribe function is passed during a re-render, React will re-subscribe to the store using the newly passed subscribe function. You can prevent this by declaring subscribe outside the component.

If the store is mutated during a non-blocking Transition update, React will fall back to performing that update as blocking. Specifically, for every Transition update, React will call getSnapshot a second time just before applying changes to the DOM. If it returns a different value than when it was called originally, React will restart the update from scratch, this time applying it as a blocking update, to ensure that every component on screen is reflecting the same version of the store.

It’s not recommended to suspend a render based on a store value returned by useSyncExternalStore. The reason is that mutations

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const snapshot = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot?)
```

Example 2 (python):
```python
import { useSyncExternalStore } from 'react';import { todosStore } from './todoStore.js';function TodosApp() {  const todos = useSyncExternalStore(todosStore.subscribe, todosStore.getSnapshot);  // ...}
```

Example 3 (javascript):
```javascript
const LazyProductDetailPage = lazy(() => import('./ProductDetailPage.js'));function ShoppingApp() {  const selectedProductId = useSyncExternalStore(...);  // ❌ Calling `use` with a Promise dependent on `selectedProductId`  const data = use(fetchItem(selectedProductId))  // ❌ Conditionally rendering a lazy component based on `selectedProductId`  return selectedProductId != null ? <LazyProductDetailPage /> : <FeaturedProducts />;}
```

Example 4 (python):
```python
import { useSyncExternalStore } from 'react';import { todosStore } from './todoStore.js';function TodosApp() {  const todos = useSyncExternalStore(todosStore.subscribe, todosStore.getSnapshot);  // ...}
```

---

## 'use server'

**URL:** https://react.dev/reference/rsc/use-server

**Contents:**
- 'use server'
  - React Server Components
- Reference
  - 'use server'
    - Caveats
  - Security considerations
  - Under Construction
  - Serializable arguments and return values
- Usage
  - Server Functions in forms

'use server' is for use with using React Server Components.

'use server' marks server-side functions that can be called from client-side code.

Add 'use server' at the top of an async function body to mark the function as callable by the client. We call these functions Server Functions.

When calling a Server Function on the client, it will make a network request to the server that includes a serialized copy of any arguments passed. If the Server Function returns a value, that value will be serialized and returned to the client.

Instead of individually marking functions with 'use server', you can add the directive to the top of a file to mark all exports within that file as Server Functions that can be used anywhere, including imported in client code.

Arguments to Server Functions are fully client-controlled. For security, always treat them as untrusted input, and make sure to validate and escape arguments as appropriate.

In any Server Function, make sure to validate that the logged-in user is allowed to perform that action.

To prevent sending sensitive data from a Server Function, there are experimental taint APIs to prevent unique values and objects from being passed to client code.

See experimental_taintUniqueValue and experimental_taintObjectReference.

Since client code calls the Server Function over the network, any arguments passed will need to be serializable.

Here are supported types for Server Function arguments:

Notably, these are not supported:

Supported serializable return values are the same as serializable props for a boundary Client Component.

The most common use case of Server Functions will be calling functions that mutate data. On the browser, the HTML form element is the traditional approach for a user to submit a mutation. With React Server Components, React introduces first-class support for Server Functions as Actions in forms.

Here is a form that allows a user to request a username.

In this example requestUsername is a Server Function passed to a <form>. When a user submits this form, there is a network request to the server function requestUsername. When calling a Server Function in a form, React will supply the form’s FormData as the first argument to the Server Function.

By passing a Server Function to the form action, React can progressively enhance the form. This means that forms can be submitted before the JavaScript bundle is loaded.

In the username request form, there might be the chance that a username is not 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
async function addToCart(data) {  'use server';  // ...}
```

Example 2 (javascript):
```javascript
// App.jsasync function requestUsername(formData) {  'use server';  const username = formData.get('username');  // ...}export default function App() {  return (    <form action={requestUsername}>      <input type="text" name="username" />      <button type="submit">Request</button>    </form>  );}
```

Example 3 (javascript):
```javascript
// requestUsername.js'use server';export default async function requestUsername(formData) {  const username = formData.get('username');  if (canRequest(username)) {    // ...    return 'successful';  }  return 'failed';}
```

Example 4 (python):
```python
// UsernameForm.js'use client';import { useActionState } from 'react';import requestUsername from './requestUsername';function UsernameForm() {  const [state, action] = useActionState(requestUsername, null, 'n/a');  return (    <>      <form action={action}>        <input type="text" name="username" />        <button type="submit">Request</button>      </form>      <p>Last submission request returned: {state}</p>    </>  );}
```

---

## useDeferredValue

**URL:** https://react.dev/reference/react/useDeferredValue

**Contents:**
- useDeferredValue
- Reference
  - useDeferredValue(value, initialValue?)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Showing stale content while fresh content is loading
  - Note
      - Deep Dive

useDeferredValue is a React Hook that lets you defer updating a part of the UI.

Call useDeferredValue at the top level of your component to get a deferred version of that value.

See more examples below.

When an update is inside a Transition, useDeferredValue always returns the new value and does not spawn a deferred render, since the update is already deferred.

The values you pass to useDeferredValue should either be primitive values (like strings and numbers) or objects created outside of rendering. If you create a new object during rendering and immediately pass it to useDeferredValue, it will be different on every render, causing unnecessary background re-renders.

When useDeferredValue receives a different value (compared with Object.is), in addition to the current render (when it still uses the previous value), it schedules a re-render in the background with the new value. The background re-render is interruptible: if there’s another update to the value, React will restart the background re-render from scratch. For example, if the user is typing into an input faster than a chart receiving its deferred value can re-render, the chart will only re-render after the user stops typing.

useDeferredValue is integrated with <Suspense>. If the background update caused by a new value suspends the UI, the user will not see the fallback. They will see the old deferred value until the data loads.

useDeferredValue does not by itself prevent extra network requests.

There is no fixed delay caused by useDeferredValue itself. As soon as React finishes the original re-render, React will immediately start working on the background re-render with the new deferred value. Any updates caused by events (like typing) will interrupt the background re-render and get prioritized over it.

The background re-render caused by useDeferredValue does not fire Effects until it’s committed to the screen. If the background re-render suspends, its Effects will run after the data loads and the UI updates.

Call useDeferredValue at the top level of your component to defer updating some part of your UI.

During the initial render, the deferred value will be the same as the value you provided.

During updates, the deferred value will “lag behind” the latest value. In particular, React will first re-render without updating the deferred value, and then try to re-render with the newly received value in the background.

Let’s walk through an example to see when this is useful.

This example 

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const deferredValue = useDeferredValue(value)
```

Example 2 (python):
```python
import { useState, useDeferredValue } from 'react';function SearchPage() {  const [query, setQuery] = useState('');  const deferredQuery = useDeferredValue(query);  // ...}
```

Example 3 (python):
```python
import { useState, useDeferredValue } from 'react';function SearchPage() {  const [query, setQuery] = useState('');  const deferredQuery = useDeferredValue(query);  // ...}
```

Example 4 (javascript):
```javascript
export default function App() {  const [query, setQuery] = useState('');  const deferredQuery = useDeferredValue(query);  return (    <>      <label>        Search albums:        <input value={query} onChange={e => setQuery(e.target.value)} />      </label>      <Suspense fallback={<h2>Loading...</h2>}>        <SearchResults query={deferredQuery} />      </Suspense>    </>  );}
```

---

## useInsertionEffect

**URL:** https://react.dev/reference/react/useInsertionEffect

**Contents:**
- useInsertionEffect
  - Pitfall
- Reference
  - useInsertionEffect(setup, dependencies?)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Injecting dynamic styles from CSS-in-JS libraries
      - Deep Dive

useInsertionEffect is for CSS-in-JS library authors. Unless you are working on a CSS-in-JS library and need a place to inject the styles, you probably want useEffect or useLayoutEffect instead.

useInsertionEffect allows inserting elements into the DOM before any layout Effects fire.

Call useInsertionEffect to insert styles before any Effects fire that may need to read layout:

See more examples below.

setup: The function with your Effect’s logic. Your setup function may also optionally return a cleanup function. When your component is added to the DOM, but before any layout Effects fire, React will run your setup function. After every re-render with changed dependencies, React will first run the cleanup function (if you provided it) with the old values, and then run your setup function with the new values. When your component is removed from the DOM, React will run your cleanup function.

optional dependencies: The list of all reactive values referenced inside of the setup code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is configured for React, it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like [dep1, dep2, dep3]. React will compare each dependency with its previous value using the Object.is comparison algorithm. If you don’t specify the dependencies at all, your Effect will re-run after every re-render of the component.

useInsertionEffect returns undefined.

Traditionally, you would style React components using plain CSS.

Some teams prefer to author styles directly in JavaScript code instead of writing CSS files. This usually requires using a CSS-in-JS library or a tool. There are three common approaches to CSS-in-JS:

If you use CSS-in-JS, we recommend a combination of the first two approaches (CSS files for static styles, inline styles for dynamic styles). We don’t recommend runtime <style> tag injection for two reasons:

The first problem is not solvable, but useInsertionEffect helps you solve the second problem.

Call useInsertionEffect to insert the styles before any layout Effects fire:

Similarly to useEffect, useInsertionEffect does not run on the server. If you need to collect which CSS rules have been used on the server, you can do it during rendering:

Read more about upgrading CSS-in-JS libraries with runtime injection to useInser

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
useInsertionEffect(setup, dependencies?)
```

Example 2 (python):
```python
import { useInsertionEffect } from 'react';// Inside your CSS-in-JS libraryfunction useCSS(rule) {  useInsertionEffect(() => {    // ... inject <style> tags here ...  });  return rule;}
```

Example 3 (unknown):
```unknown
// In your JS file:<button className="success" />// In your CSS file:.success { color: green; }
```

Example 4 (javascript):
```javascript
// Inside your CSS-in-JS librarylet isInserted = new Set();function useCSS(rule) {  useInsertionEffect(() => {    // As explained earlier, we don't recommend runtime injection of <style> tags.    // But if you have to do it, then it's important to do in useInsertionEffect.    if (!isInserted.has(rule)) {      isInserted.add(rule);      document.head.appendChild(getStyleForRule(rule));    }  });  return rule;}function Button() {  const className = useCSS('...');  return <div className={className} />;}
```

---

## Directives

**URL:** https://react.dev/reference/rsc/directives#source-code-directives

**Contents:**
- Directives
  - React Server Components
- Source code directives

Directives are for use in React Server Components.

Directives provide instructions to bundlers compatible with React Server Components.

---

## Legacy React APIs

**URL:** https://react.dev/reference/react/legacy

**Contents:**
- Legacy React APIs
- Legacy APIs
- Removed APIs

These APIs are exported from the react package, but they are not recommended for use in newly written code. See the linked individual API pages for the suggested alternatives.

These APIs were removed in React 19:

---

## Client React DOM APIs

**URL:** https://react.dev/reference/react-dom/client#undefined

**Contents:**
- Client React DOM APIs
- Client APIs
- Browser support

The react-dom/client APIs let you render React components on the client (in the browser). These APIs are typically used at the top level of your app to initialize your React tree. A framework may call them for you. Most of your components don’t need to import or use them.

React supports all popular browsers, including Internet Explorer 9 and above. Some polyfills are required for older browsers such as IE 9 and IE 10.

---

## React Reference Overview

**URL:** https://react.dev/reference/react#react-dom

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

## useLayoutEffect

**URL:** https://react.dev/reference/react/useLayoutEffect

**Contents:**
- useLayoutEffect
  - Pitfall
- Reference
  - useLayoutEffect(setup, dependencies?)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Measuring layout before the browser repaints the screen
    - useLayoutEffect vs useEffect

useLayoutEffect can hurt performance. Prefer useEffect when possible.

useLayoutEffect is a version of useEffect that fires before the browser repaints the screen.

Call useLayoutEffect to perform the layout measurements before the browser repaints the screen:

See more examples below.

setup: The function with your Effect’s logic. Your setup function may also optionally return a cleanup function. Before your component is added to the DOM, React will run your setup function. After every re-render with changed dependencies, React will first run the cleanup function (if you provided it) with the old values, and then run your setup function with the new values. Before your component is removed from the DOM, React will run your cleanup function.

optional dependencies: The list of all reactive values referenced inside of the setup code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is configured for React, it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like [dep1, dep2, dep3]. React will compare each dependency with its previous value using the Object.is comparison. If you omit this argument, your Effect will re-run after every re-render of the component.

useLayoutEffect returns undefined.

useLayoutEffect is a Hook, so you can only call it at the top level of your component or your own Hooks. You can’t call it inside loops or conditions. If you need that, extract a component and move the Effect there.

When Strict Mode is on, React will run one extra development-only setup+cleanup cycle before the first real setup. This is a stress-test that ensures that your cleanup logic “mirrors” your setup logic and that it stops or undoes whatever the setup is doing. If this causes a problem, implement the cleanup function.

If some of your dependencies are objects or functions defined inside the component, there is a risk that they will cause the Effect to re-run more often than needed. To fix this, remove unnecessary object and function dependencies. You can also extract state updates and non-reactive logic outside of your Effect.

Effects only run on the client. They don’t run during server rendering.

The code inside useLayoutEffect and all state updates scheduled from it block the browser from repainting the screen. When used excessively, this makes your app slo

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
useLayoutEffect(setup, dependencies?)
```

Example 2 (python):
```python
import { useState, useRef, useLayoutEffect } from 'react';function Tooltip() {  const ref = useRef(null);  const [tooltipHeight, setTooltipHeight] = useState(0);  useLayoutEffect(() => {    const { height } = ref.current.getBoundingClientRect();    setTooltipHeight(height);  }, []);  // ...
```

Example 3 (javascript):
```javascript
function Tooltip() {  const ref = useRef(null);  const [tooltipHeight, setTooltipHeight] = useState(0); // You don't know real height yet  useLayoutEffect(() => {    const { height } = ref.current.getBoundingClientRect();    setTooltipHeight(height); // Re-render now that you know the real height  }, []);  // ...use tooltipHeight in the rendering logic below...}
```

---

## act

**URL:** https://react.dev/reference/react/act

**Contents:**
- act
  - Note
- Reference
  - await act(async actFn)
  - Note
    - Parameters
    - Returns
- Usage
  - Rendering components in tests
  - Dispatching events in tests

act is a test helper to apply pending React updates before making assertions.

To prepare a component for assertions, wrap the code rendering it and performing updates inside an await act() call. This makes your test run closer to how React works in the browser.

You might find using act() directly a bit too verbose. To avoid some of the boilerplate, you could use a library like React Testing Library, whose helpers are wrapped with act().

When writing UI tests, tasks like rendering, user events, or data fetching can be considered as “units” of interaction with a user interface. React provides a helper called act() that makes sure all updates related to these “units” have been processed and applied to the DOM before you make any assertions.

The name act comes from the Arrange-Act-Assert pattern.

We recommend using act with await and an async function. Although the sync version works in many cases, it doesn’t work in all cases and due to the way React schedules updates internally, it’s difficult to predict when you can use the sync version.

We will deprecate and remove the sync version in the future.

act does not return anything.

When testing a component, you can use act to make assertions about its output.

For example, let’s say we have this Counter component, the usage examples below show how to test it:

To test the render output of a component, wrap the render inside act():

Here, we create a container, append it to the document, and render the Counter component inside act(). This ensures that the component is rendered and its effects are applied before making assertions.

Using act ensures that all updates have been applied before we make assertions.

To test events, wrap the event dispatch inside act():

Here, we render the component with act, and then dispatch the event inside another act(). This ensures that all updates from the event are applied before making assertions.

Don’t forget that dispatching DOM events only works when the DOM container is added to the document. You can use a library like React Testing Library to reduce the boilerplate code.

Using act requires setting global.IS_REACT_ACT_ENVIRONMENT=true in your test environment. This is to ensure that act is only used in the correct environment.

If you don’t set the global, you will see an error like this:

To fix, add this to your global setup file for React tests:

In testing frameworks like React Testing Library, IS_REACT_ACT_ENVIRONMENT is already set for you.

**Examples:**

Example 1 (unknown):
```unknown
await act(async actFn)
```

Example 2 (javascript):
```javascript
it ('renders with button disabled', async () => {  await act(async () => {    root.render(<TestComponent />)  });  expect(container.querySelector('button')).toBeDisabled();});
```

Example 3 (javascript):
```javascript
function Counter() {  const [count, setCount] = useState(0);  const handleClick = () => {    setCount(prev => prev + 1);  }  useEffect(() => {    document.title = `You clicked ${count} times`;  }, [count]);  return (    <div>      <p>You clicked {count} times</p>      <button onClick={handleClick}>        Click me      </button>    </div>  )}
```

Example 4 (python):
```python
import {act} from 'react';import ReactDOMClient from 'react-dom/client';import Counter from './Counter';it('can render and update a counter', async () => {  container = document.createElement('div');  document.body.appendChild(container);    // ✅ Render the component inside act().  await act(() => {    ReactDOMClient.createRoot(container).render(<Counter />);  });    const button = container.querySelector('button');  const label = container.querySelector('p');  expect(label.textContent).toBe('You clicked 0 times');  expect(document.title).toBe('You clicked 0 times');});
```

---

## preinitModule

**URL:** https://react.dev/reference/react-dom/preinitModule

**Contents:**
- preinitModule
  - Note
- Reference
  - preinitModule(href, options)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Preloading when rendering
  - Preloading in an event handler

React-based frameworks frequently handle resource loading for you, so you might not have to call this API yourself. Consult your framework’s documentation for details.

preinitModule lets you eagerly fetch and evaluate an ESM module.

To preinit an ESM module, call the preinitModule function from react-dom.

See more examples below.

The preinitModule function provides the browser with a hint that it should start downloading and executing the given module, which can save time. Modules that you preinit are executed when they finish downloading.

preinitModule returns nothing.

Call preinitModule when rendering a component if you know that it or its children will use a specific module and you’re OK with the module being evaluated and thereby taking effect immediately upon being downloaded.

If you want the browser to download the module but not to execute it right away, use preloadModule instead. If you want to preinit a script that isn’t an ESM module, use preinit.

Call preinitModule in an event handler before transitioning to a page or state where the module will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

**Examples:**

Example 1 (unknown):
```unknown
preinitModule("https://example.com/module.js", {as: "script"});
```

Example 2 (python):
```python
import { preinitModule } from 'react-dom';function AppRoot() {  preinitModule("https://example.com/module.js", {as: "script"});  // ...}
```

Example 3 (python):
```python
import { preinitModule } from 'react-dom';function AppRoot() {  preinitModule("https://example.com/module.js", {as: "script"});  return ...;}
```

Example 4 (python):
```python
import { preinitModule } from 'react-dom';function CallToAction() {  const onClick = () => {    preinitModule("https://example.com/module.js", {as: "script"});    startWizard();  }  return (    <button onClick={onClick}>Start Wizard</button>  );}
```

---

## React Reference Overview

**URL:** https://react.dev/reference/react

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

## useDebugValue

**URL:** https://react.dev/reference/react/useDebugValue

**Contents:**
- useDebugValue
- Reference
  - useDebugValue(value, format?)
    - Parameters
    - Returns
- Usage
  - Adding a label to a custom Hook
  - Note
  - Deferring formatting of a debug value

useDebugValue is a React Hook that lets you add a label to a custom Hook in React DevTools.

Call useDebugValue at the top level of your custom Hook to display a readable debug value:

See more examples below.

useDebugValue does not return anything.

Call useDebugValue at the top level of your custom Hook to display a readable debug value for React DevTools.

This gives components calling useOnlineStatus a label like OnlineStatus: "Online" when you inspect them:

Without the useDebugValue call, only the underlying data (in this example, true) would be displayed.

Don’t add debug values to every custom Hook. It’s most valuable for custom Hooks that are part of shared libraries and that have a complex internal data structure that’s difficult to inspect.

You can also pass a formatting function as the second argument to useDebugValue:

Your formatting function will receive the debug value as a parameter and should return a formatted display value. When your component is inspected, React DevTools will call this function and display its result.

This lets you avoid running potentially expensive formatting logic unless the component is actually inspected. For example, if date is a Date value, this avoids calling toDateString() on it for every render.

**Examples:**

Example 1 (unknown):
```unknown
useDebugValue(value, format?)
```

Example 2 (python):
```python
import { useDebugValue } from 'react';function useOnlineStatus() {  // ...  useDebugValue(isOnline ? 'Online' : 'Offline');  // ...}
```

Example 3 (python):
```python
import { useDebugValue } from 'react';function useOnlineStatus() {  // ...  useDebugValue(isOnline ? 'Online' : 'Offline');  // ...}
```

Example 4 (javascript):
```javascript
useDebugValue(date, date => date.toDateString());
```

---

## Directives

**URL:** https://react.dev/reference/rsc/directives#undefined

**Contents:**
- Directives
  - React Server Components
- Source code directives

Directives are for use in React Server Components.

Directives provide instructions to bundlers compatible with React Server Components.

---

## Server React DOM APIs

**URL:** https://react.dev/reference/react-dom/server

**Contents:**
- Server React DOM APIs
- Server APIs for Web Streams
  - Note
- Server APIs for Node.js Streams
- Legacy Server APIs for non-streaming environments

The react-dom/server APIs let you server-side render React components to HTML. These APIs are only used on the server at the top level of your app to generate the initial HTML. A framework may call them for you. Most of your components don’t need to import or use them.

These methods are only available in the environments with Web Streams, which includes browsers, Deno, and some modern edge runtimes:

Node.js also includes these methods for compatibility, but they are not recommended due to worse performance. Use the dedicated Node.js APIs instead.

These methods are only available in the environments with Node.js Streams:

These methods can be used in the environments that don’t support streams:

They have limited functionality compared to the streaming APIs.

---

## Server Functions

**URL:** https://react.dev/reference/rsc/server-functions

**Contents:**
- Server Functions
  - React Server Components
  - Note
    - How do I build support for Server Functions?
- Usage
  - Creating a Server Function from a Server Component
  - Importing Server Functions from Client Components
  - Server Functions with Actions
  - Server Functions with Form Actions
  - Server Functions with useActionState

Server Functions are for use in React Server Components.

Note: Until September 2024, we referred to all Server Functions as “Server Actions”. If a Server Function is passed to an action prop or called from inside an action then it is a Server Action, but not all Server Functions are Server Actions. The naming in this documentation has been updated to reflect that Server Functions can be used for multiple purposes.

Server Functions allow Client Components to call async functions executed on the server.

While Server Functions in React 19 are stable and will not break between minor versions, the underlying APIs used to implement Server Functions in a React Server Components bundler or framework do not follow semver and may break between minors in React 19.x.

To support Server Functions as a bundler or framework, we recommend pinning to a specific React version, or using the Canary release. We will continue working with bundlers and frameworks to stabilize the APIs used to implement Server Functions in the future.

When a Server Function is defined with the "use server" directive, your framework will automatically create a reference to the Server Function, and pass that reference to the Client Component. When that function is called on the client, React will send a request to the server to execute the function, and return the result.

Server Functions can be created in Server Components and passed as props to Client Components, or they can be imported and used in Client Components.

Server Components can define Server Functions with the "use server" directive:

When React renders the EmptyNote Server Component, it will create a reference to the createNoteAction function, and pass that reference to the Button Client Component. When the button is clicked, React will send a request to the server to execute the createNoteAction function with the reference provided:

For more, see the docs for "use server".

Client Components can import Server Functions from files that use the "use server" directive:

When the bundler builds the EmptyNote Client Component, it will create a reference to the createNote function in the bundle. When the button is clicked, React will send a request to the server to execute the createNote function using the reference provided:

For more, see the docs for "use server".

Server Functions can be called from Actions on the client:

This allows you to access the isPending state of the Server Function by wrapping it in an Action on the cli

*[Content truncated]*

**Examples:**

Example 1 (python):
```python
// Server Componentimport Button from './Button';function EmptyNote () {  async function createNoteAction() {    // Server Function    'use server';        await db.notes.create();  }  return <Button onClick={createNoteAction}/>;}
```

Example 2 (javascript):
```javascript
"use client";export default function Button({onClick}) {   console.log(onClick);   // {$$typeof: Symbol.for("react.server.reference"), $$id: 'createNoteAction'}  return <button onClick={() => onClick()}>Create Empty Note</button>}
```

Example 3 (unknown):
```unknown
"use server";export async function createNote() {  await db.notes.create();}
```

Example 4 (python):
```python
"use client";import {createNote} from './actions';function EmptyNote() {  console.log(createNote);  // {$$typeof: Symbol.for("react.server.reference"), $$id: 'createNote'}  <button onClick={() => createNote()} />}
```

---

## React Reference Overview

**URL:** https://react.dev/reference/react#undefined

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

## React Reference Overview

**URL:** https://react.dev/reference/react#react

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

## useId

**URL:** https://react.dev/reference/react/useId

**Contents:**
- useId
- Reference
  - useId()
    - Parameters
    - Returns
    - Caveats
- Usage
  - Pitfall
  - Generating unique IDs for accessibility attributes
  - Pitfall

useId is a React Hook for generating unique IDs that can be passed to accessibility attributes.

Call useId at the top level of your component to generate a unique ID:

See more examples below.

useId does not take any parameters.

useId returns a unique ID string associated with this particular useId call in this particular component.

useId is a Hook, so you can only call it at the top level of your component or your own Hooks. You can’t call it inside loops or conditions. If you need that, extract a new component and move the state into it.

useId should not be used to generate keys in a list. Keys should be generated from your data.

useId currently cannot be used in async Server Components.

Do not call useId to generate keys in a list. Keys should be generated from your data.

Call useId at the top level of your component to generate a unique ID:

You can then pass the generated ID to different attributes:

Let’s walk through an example to see when this is useful.

HTML accessibility attributes like aria-describedby let you specify that two tags are related to each other. For example, you can specify that an element (like an input) is described by another element (like a paragraph).

In regular HTML, you would write it like this:

However, hardcoding IDs like this is not a good practice in React. A component may be rendered more than once on the page—but IDs have to be unique! Instead of hardcoding an ID, generate a unique ID with useId:

Now, even if PasswordField appears multiple times on the screen, the generated IDs won’t clash.

Watch this video to see the difference in the user experience with assistive technologies.

With server rendering, useId requires an identical component tree on the server and the client. If the trees you render on the server and the client don’t match exactly, the generated IDs won’t match.

You might be wondering why useId is better than incrementing a global variable like nextId++.

The primary benefit of useId is that React ensures that it works with server rendering. During server rendering, your components generate HTML output. Later, on the client, hydration attaches your event handlers to the generated HTML. For hydration to work, the client output must match the server HTML.

This is very difficult to guarantee with an incrementing counter because the order in which the Client Components are hydrated may not match the order in which the server HTML was emitted. By calling useId, you ensure that hydration will wo

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const id = useId()
```

Example 2 (python):
```python
import { useId } from 'react';function PasswordField() {  const passwordHintId = useId();  // ...
```

Example 3 (python):
```python
import { useId } from 'react';function PasswordField() {  const passwordHintId = useId();  // ...
```

Example 4 (unknown):
```unknown
<>  <input type="password" aria-describedby={passwordHintId} />  <p id={passwordHintId}></>
```

---

## flushSync

**URL:** https://react.dev/reference/react-dom/flushSync

**Contents:**
- flushSync
  - Pitfall
- Reference
  - flushSync(callback)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Flushing updates for third-party integrations
  - Pitfall

Using flushSync is uncommon and can hurt the performance of your app.

flushSync lets you force React to flush any updates inside the provided callback synchronously. This ensures that the DOM is updated immediately.

Call flushSync to force React to flush any pending work and update the DOM synchronously.

Most of the time, flushSync can be avoided. Use flushSync as last resort.

See more examples below.

flushSync returns undefined.

When integrating with third-party code such as browser APIs or UI libraries, it may be necessary to force React to flush updates. Use flushSync to force React to flush any state updates inside the callback synchronously:

This ensures that, by the time the next line of code runs, React has already updated the DOM.

Using flushSync is uncommon, and using it often can significantly hurt the performance of your app. If your app only uses React APIs, and does not integrate with third-party libraries, flushSync should be unnecessary.

However, it can be helpful for integrating with third-party code like browser APIs.

Some browser APIs expect results inside of callbacks to be written to the DOM synchronously, by the end of the callback, so the browser can do something with the rendered DOM. In most cases, React handles this for you automatically. But in some cases it may be necessary to force a synchronous update.

For example, the browser onbeforeprint API allows you to change the page immediately before the print dialog opens. This is useful for applying custom print styles that allow the document to display better for printing. In the example below, you use flushSync inside of the onbeforeprint callback to immediately “flush” the React state to the DOM. Then, by the time the print dialog opens, isPrinting displays “yes”:

Without flushSync, the print dialog will display isPrinting as “no”. This is because React batches the updates asynchronously and the print dialog is displayed before the state is updated.

flushSync can significantly hurt performance, and may unexpectedly force pending Suspense boundaries to show their fallback state.

Most of the time, flushSync can be avoided, so use flushSync as a last resort.

React cannot flushSync in the middle of a render. If you do, it will noop and warn:

This includes calling flushSync inside:

For example, calling flushSync in an Effect will noop and warn:

To fix this, you usually want to move the flushSync call to an event:

If it’s difficult to move to an event, you can defer f

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
flushSync(callback)
```

Example 2 (python):
```python
import { flushSync } from 'react-dom';flushSync(() => {  setSomething(123);});
```

Example 3 (javascript):
```javascript
flushSync(() => {  setSomething(123);});// By this line, the DOM is updated.
```

Example 4 (python):
```python
import { useEffect } from 'react';import { flushSync } from 'react-dom';function MyComponent() {  useEffect(() => {    // 🚩 Wrong: calling flushSync inside an effect    flushSync(() => {      setSomething(newValue);    });  }, []);  return <div>{/* ... */}</div>;}
```

---

## startTransition

**URL:** https://react.dev/reference/react/startTransition

**Contents:**
- startTransition
- Reference
  - startTransition(action)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Marking a state update as a non-blocking Transition
  - Note

startTransition lets you render a part of the UI in the background.

The startTransition function lets you mark a state update as a Transition.

See more examples below.

startTransition does not return anything.

startTransition does not provide a way to track whether a Transition is pending. To show a pending indicator while the Transition is ongoing, you need useTransition instead.

You can wrap an update into a Transition only if you have access to the set function of that state. If you want to start a Transition in response to some prop or a custom Hook return value, try useDeferredValue instead.

The function you pass to startTransition is called immediately, marking all state updates that happen while it executes as Transitions. If you try to perform state updates in a setTimeout, for example, they won’t be marked as Transitions.

You must wrap any state updates after any async requests in another startTransition to mark them as Transitions. This is a known limitation that we will fix in the future (see Troubleshooting).

A state update marked as a Transition will be interrupted by other state updates. For example, if you update a chart component inside a Transition, but then start typing into an input while the chart is in the middle of a re-render, React will restart the rendering work on the chart component after handling the input state update.

Transition updates can’t be used to control text inputs.

If there are multiple ongoing Transitions, React currently batches them together. This is a limitation that may be removed in a future release.

You can mark a state update as a Transition by wrapping it in a startTransition call:

Transitions let you keep the user interface updates responsive even on slow devices.

With a Transition, your UI stays responsive in the middle of a re-render. For example, if the user clicks a tab but then change their mind and click another tab, they can do that without waiting for the first re-render to finish.

startTransition is very similar to useTransition, except that it does not provide the isPending flag to track whether a Transition is ongoing. You can call startTransition when useTransition is not available. For example, startTransition works outside components, such as from a data library.

Learn about Transitions and see examples on the useTransition page.

**Examples:**

Example 1 (unknown):
```unknown
startTransition(action)
```

Example 2 (python):
```python
import { startTransition } from 'react';function TabContainer() {  const [tab, setTab] = useState('about');  function selectTab(nextTab) {    startTransition(() => {      setTab(nextTab);    });  }  // ...}
```

Example 3 (python):
```python
import { startTransition } from 'react';function TabContainer() {  const [tab, setTab] = useState('about');  function selectTab(nextTab) {    startTransition(() => {      setTab(nextTab);    });  }  // ...}
```

---

## Directives

**URL:** https://react.dev/reference/rsc/directives

**Contents:**
- Directives
  - React Server Components
- Source code directives

Directives are for use in React Server Components.

Directives provide instructions to bundlers compatible with React Server Components.

---

## lazy

**URL:** https://react.dev/reference/react/lazy

**Contents:**
- lazy
- Reference
  - lazy(load)
    - Parameters
    - Returns
  - load function
    - Parameters
    - Returns
- Usage
  - Lazy-loading components with Suspense

lazy lets you defer loading component’s code until it is rendered for the first time.

Call lazy outside your components to declare a lazy-loaded React component:

See more examples below.

lazy returns a React component you can render in your tree. While the code for the lazy component is still loading, attempting to render it will suspend. Use <Suspense> to display a loading indicator while it’s loading.

load receives no parameters.

You need to return a Promise or some other thenable (a Promise-like object with a then method). It needs to eventually resolve to an object whose .default property is a valid React component type, such as a function, memo, or a forwardRef component.

Usually, you import components with the static import declaration:

To defer loading this component’s code until it’s rendered for the first time, replace this import with:

This code relies on dynamic import(), which might require support from your bundler or framework. Using this pattern requires that the lazy component you’re importing was exported as the default export.

Now that your component’s code loads on demand, you also need to specify what should be displayed while it is loading. You can do this by wrapping the lazy component or any of its parents into a <Suspense> boundary:

In this example, the code for MarkdownPreview won’t be loaded until you attempt to render it. If MarkdownPreview hasn’t loaded yet, Loading will be shown in its place. Try ticking the checkbox:

This demo loads with an artificial delay. The next time you untick and tick the checkbox, Preview will be cached, so there will be no loading state. To see the loading state again, click “Reset” on the sandbox.

Learn more about managing loading states with Suspense.

Do not declare lazy components inside other components:

Instead, always declare them at the top level of your module:

**Examples:**

Example 1 (javascript):
```javascript
const SomeComponent = lazy(load)
```

Example 2 (python):
```python
import { lazy } from 'react';const MarkdownPreview = lazy(() => import('./MarkdownPreview.js'));
```

Example 3 (python):
```python
import MarkdownPreview from './MarkdownPreview.js';
```

Example 4 (python):
```python
import { lazy } from 'react';const MarkdownPreview = lazy(() => import('./MarkdownPreview.js'));
```

---

## Compiling Libraries

**URL:** https://react.dev/reference/react-compiler/compiling-libraries

**Contents:**
- Compiling Libraries
- Why Ship Compiled Code?
- Setting Up Compilation
- Backwards Compatibility
  - 1. Install the runtime package
  - 2. Configure the target version
- Testing Strategy
- Troubleshooting
  - Library doesn’t work with older React versions
  - Compilation conflicts with other Babel plugins

This guide helps library authors understand how to use React Compiler to ship optimized library code to their users.

As a library author, you can compile your library code before publishing to npm. This provides several benefits:

Add React Compiler to your library’s build process:

Configure your build tool to compile your library. For example, with Babel:

If your library supports React versions below 19, you’ll need additional configuration:

We recommend installing react-compiler-runtime as a direct dependency:

Set the minimum React version your library supports:

Test your library both with and without compilation to ensure compatibility. Run your existing test suite against the compiled code, and also create a separate test configuration that bypasses the compiler. This helps catch any issues that might arise from the compilation process and ensures your library works correctly in all scenarios.

If your compiled library throws errors in React 17 or 18:

Some Babel plugins may conflict with React Compiler:

If users see “Cannot find module ‘react-compiler-runtime’“:

**Examples:**

Example 1 (unknown):
```unknown
// babel.config.jsmodule.exports = {  plugins: [    'babel-plugin-react-compiler',  ],  // ... other config};
```

Example 2 (unknown):
```unknown
{  "dependencies": {    "react-compiler-runtime": "^1.0.0"  },  "peerDependencies": {    "react": "^17.0.0 || ^18.0.0 || ^19.0.0"  }}
```

Example 3 (unknown):
```unknown
{  target: '17', // Minimum supported React version}
```

---

## <ViewTransition> - This feature is available in the latest Canary version of React

**URL:** https://react.dev/reference/react/ViewTransition

**Contents:**
- <ViewTransition> - This feature is available in the latest Canary version of React
  - Canary
- Reference
  - <ViewTransition>
      - Deep Dive
    - How does <ViewTransition> work?
    - Props
    - Callback
  - View Transition Class
  - Styling View Transitions

The <ViewTransition /> API is currently only available in React’s Canary and Experimental channels.

Learn more about React’s release channels here.

<ViewTransition> lets you animate elements that update inside a Transition.

Wrap elements in <ViewTransition> to animate them when they update inside a Transition. React uses the following heuristics to determine if a View Transition activates for an animation:

By default, <ViewTransition> animates with a smooth cross-fade (the browser default view transition). You can customize the animation by providing a View Transition Class to the <ViewTransition> component. You can customize animations for each kind of trigger (see Styling View Transitions).

Under the hood, React applies view-transition-name to inline styles of the nearest DOM node nested inside the <ViewTransition> component. If there are multiple sibling DOM nodes like <ViewTransition><div /><div /></ViewTransition> then React adds a suffix to the name to make each unique but conceptually they’re part of the same one. React doesn’t apply these eagerly but only at the time that boundary should participate in an animation.

React automatically calls startViewTransition itself behind the scenes so you should never do that yourself. In fact, if you have something else on the page running a ViewTransition React will interrupt it. So it’s recommended that you use React itself to coordinate these. If you had other ways of trigger ViewTransitions in the past, we recommend that you migrate to the built-in way.

If there are other React ViewTransitions already running then React will wait for them to finish before starting the next one. However, importantly if there are multiple updates happening while the first one is running, those will all be batched into one. If you start A->B. Then in the meantime you get an update to go to C and then D. When the first A->B animation finishes the next one will animate from B->D.

The getSnapshotBeforeUpdate life-cycle will be called before startViewTransition and some view-transition-name will update at the same time.

Then React calls startViewTransition. Inside the updateCallback, React will:

After the ready Promise of the startViewTransition is resolved, React will then revert the view-transition-name. Then React will invoke the onEnter, onExit, onUpdate and onShare callbacks to allow for manual programmatic control over the Animations. This will be after the built-in default ones have already been computed.

If a f

*[Content truncated]*

**Examples:**

Example 1 (python):
```python
import {ViewTransition} from 'react';<ViewTransition>  <div>...</div></ViewTransition>
```

Example 2 (unknown):
```unknown
<ViewTransition enter="slide-in">
```

Example 3 (unknown):
```unknown
::view-transition-group(.slide-in) {  }::view-transition-old(.slide-in) {}::view-transition-new(.slide-in) {}
```

Example 4 (javascript):
```javascript
function Child() {  return (    <ViewTransition>      <div>Hi</div>    </ViewTransition>  );}function Parent() {  const [show, setShow] = useState();  if (show) {    return <Child />;  }  return null;}
```

---

## useImperativeHandle

**URL:** https://react.dev/reference/react/useImperativeHandle

**Contents:**
- useImperativeHandle
- Reference
  - useImperativeHandle(ref, createHandle, dependencies?)
    - Parameters
  - Note
    - Returns
- Usage
  - Exposing a custom ref handle to the parent component
  - Exposing your own imperative methods
  - Pitfall

useImperativeHandle is a React Hook that lets you customize the handle exposed as a ref.

Call useImperativeHandle at the top level of your component to customize the ref handle it exposes:

See more examples below.

ref: The ref you received as a prop to the MyInput component.

createHandle: A function that takes no arguments and returns the ref handle you want to expose. That ref handle can have any type. Usually, you will return an object with the methods you want to expose.

optional dependencies: The list of all reactive values referenced inside of the createHandle code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is configured for React, it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like [dep1, dep2, dep3]. React will compare each dependency with its previous value using the Object.is comparison. If a re-render resulted in a change to some dependency, or if you omitted this argument, your createHandle function will re-execute, and the newly created handle will be assigned to the ref.

Starting with React 19, ref is available as a prop. In React 18 and earlier, it was necessary to get the ref from forwardRef.

useImperativeHandle returns undefined.

To expose a DOM node to the parent element, pass in the ref prop to the node.

With the code above, a ref to MyInput will receive the <input> DOM node. However, you can expose a custom value instead. To customize the exposed handle, call useImperativeHandle at the top level of your component:

Note that in the code above, the ref is no longer passed to the <input>.

For example, suppose you don’t want to expose the entire <input> DOM node, but you want to expose two of its methods: focus and scrollIntoView. To do this, keep the real browser DOM in a separate ref. Then use useImperativeHandle to expose a handle with only the methods that you want the parent component to call:

Now, if the parent component gets a ref to MyInput, it will be able to call the focus and scrollIntoView methods on it. However, it will not have full access to the underlying <input> DOM node.

The methods you expose via an imperative handle don’t have to match the DOM methods exactly. For example, this Post component exposes a scrollAndFocusAddComment method via an imperative handle. This lets the parent Page scroll the list o

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
useImperativeHandle(ref, createHandle, dependencies?)
```

Example 2 (python):
```python
import { useImperativeHandle } from 'react';function MyInput({ ref }) {  useImperativeHandle(ref, () => {    return {      // ... your methods ...    };  }, []);  // ...
```

Example 3 (unknown):
```unknown
function MyInput({ ref }) {  return <input ref={ref} />;};
```

Example 4 (python):
```python
import { useImperativeHandle } from 'react';function MyInput({ ref }) {  useImperativeHandle(ref, () => {    return {      // ... your methods ...    };  }, []);  return <input />;};
```

---

## prefetchDNS

**URL:** https://react.dev/reference/react-dom/prefetchDNS

**Contents:**
- prefetchDNS
- Reference
  - prefetchDNS(href)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Prefetching DNS when rendering
  - Prefetching DNS in an event handler

prefetchDNS lets you eagerly look up the IP of a server that you expect to load resources from.

To look up a host, call the prefetchDNS function from react-dom.

See more examples below.

The prefetchDNS function provides the browser with a hint that it should look up the IP address of a given server. If the browser chooses to do so, this can speed up the loading of resources from that server.

prefetchDNS returns nothing.

Call prefetchDNS when rendering a component if you know that its children will load external resources from that host.

Call prefetchDNS in an event handler before transitioning to a page or state where external resources will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

**Examples:**

Example 1 (unknown):
```unknown
prefetchDNS("https://example.com");
```

Example 2 (python):
```python
import { prefetchDNS } from 'react-dom';function AppRoot() {  prefetchDNS("https://example.com");  // ...}
```

Example 3 (python):
```python
import { prefetchDNS } from 'react-dom';function AppRoot() {  prefetchDNS("https://example.com");  return ...;}
```

Example 4 (python):
```python
import { prefetchDNS } from 'react-dom';function CallToAction() {  const onClick = () => {    prefetchDNS('http://example.com');    startWizard();  }  return (    <button onClick={onClick}>Start Wizard</button>  );}
```

---

## useTransition

**URL:** https://react.dev/reference/react/useTransition

**Contents:**
- useTransition
- Reference
  - useTransition()
    - Parameters
    - Returns
  - startTransition(action)
  - Note
    - Functions called in startTransition are called “Actions”.
    - Parameters
    - Returns

useTransition is a React Hook that lets you render a part of the UI in the background.

Call useTransition at the top level of your component to mark some state updates as Transitions.

See more examples below.

useTransition does not take any parameters.

useTransition returns an array with exactly two items:

The startTransition function returned by useTransition lets you mark an update as a Transition.

The function passed to startTransition is called an “Action”. By convention, any callback called inside startTransition (such as a callback prop) should be named action or include the “Action” suffix:

startTransition does not return anything.

useTransition is a Hook, so it can only be called inside components or custom Hooks. If you need to start a Transition somewhere else (for example, from a data library), call the standalone startTransition instead.

You can wrap an update into a Transition only if you have access to the set function of that state. If you want to start a Transition in response to some prop or a custom Hook value, try useDeferredValue instead.

The function you pass to startTransition is called immediately, marking all state updates that happen while it executes as Transitions. If you try to perform state updates in a setTimeout, for example, they won’t be marked as Transitions.

You must wrap any state updates after any async requests in another startTransition to mark them as Transitions. This is a known limitation that we will fix in the future (see Troubleshooting).

The startTransition function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. Learn more about removing Effect dependencies.

A state update marked as a Transition will be interrupted by other state updates. For example, if you update a chart component inside a Transition, but then start typing into an input while the chart is in the middle of a re-render, React will restart the rendering work on the chart component after handling the input update.

Transition updates can’t be used to control text inputs.

If there are multiple ongoing Transitions, React currently batches them together. This is a limitation that may be removed in a future release.

Call useTransition at the top of your component to create Actions, and access the pending state:

useTransition returns an array with exactly two items:

To start 

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [isPending, startTransition] = useTransition()
```

Example 2 (python):
```python
import { useTransition } from 'react';function TabContainer() {  const [isPending, startTransition] = useTransition();  // ...}
```

Example 3 (javascript):
```javascript
function TabContainer() {  const [isPending, startTransition] = useTransition();  const [tab, setTab] = useState('about');  function selectTab(nextTab) {    startTransition(() => {      setTab(nextTab);    });  }  // ...}
```

Example 4 (javascript):
```javascript
function SubmitButton({ submitAction }) {  const [isPending, startTransition] = useTransition();  return (    <button      disabled={isPending}      onClick={() => {        startTransition(async () => {          await submitAction();        });      }}    >      Submit    </button>  );}
```

---

## createRoot

**URL:** https://react.dev/reference/react-dom/client/createRoot

**Contents:**
- createRoot
- Reference
  - createRoot(domNode, options?)
    - Parameters
    - Returns
    - Caveats
  - root.render(reactNode)
    - Parameters
    - Returns
    - Caveats

createRoot lets you create a root to display React components inside a browser DOM node.

Call createRoot to create a React root for displaying content inside a browser DOM element.

React will create a root for the domNode, and take over managing the DOM inside it. After you’ve created a root, you need to call root.render to display a React component inside of it:

An app fully built with React will usually only have one createRoot call for its root component. A page that uses “sprinkles” of React for parts of the page may have as many separate roots as needed.

See more examples below.

domNode: A DOM element. React will create a root for this DOM element and allow you to call functions on the root, such as render to display rendered React content.

optional options: An object with options for this React root.

createRoot returns an object with two methods: render and unmount.

Call root.render to display a piece of JSX (“React node”) into the React root’s browser DOM node.

React will display <App /> in the root, and take over managing the DOM inside it.

See more examples below.

root.render returns undefined.

The first time you call root.render, React will clear all the existing HTML content inside the React root before rendering the React component into it.

If your root’s DOM node contains HTML generated by React on the server or during the build, use hydrateRoot() instead, which attaches the event handlers to the existing HTML.

If you call render on the same root more than once, React will update the DOM as necessary to reflect the latest JSX you passed. React will decide which parts of the DOM can be reused and which need to be recreated by “matching it up” with the previously rendered tree. Calling render on the same root again is similar to calling the set function on the root component: React avoids unnecessary DOM updates.

Although rendering is synchronous once it starts, root.render(...) is not. This means code after root.render() may run before any effects (useLayoutEffect, useEffect) of that specific render are fired. This is usually fine and rarely needs adjustment. In rare cases where effect timing matters, you can wrap root.render(...) in flushSync to ensure the initial render runs fully synchronously.

Call root.unmount to destroy a rendered tree inside a React root.

An app fully built with React will usually not have any calls to root.unmount.

This is mostly useful if your React root’s DOM node (or any of its ancestors) may get re

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const root = createRoot(domNode, options?)
```

Example 2 (python):
```python
import { createRoot } from 'react-dom/client';const domNode = document.getElementById('root');const root = createRoot(domNode);
```

Example 3 (unknown):
```unknown
root.render(<App />);
```

Example 4 (unknown):
```unknown
root.render(<App />);
```

---

## React Reference Overview

**URL:** https://react.dev/reference/react#legacy-apis

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

## preconnect

**URL:** https://react.dev/reference/react-dom/preconnect

**Contents:**
- preconnect
- Reference
  - preconnect(href)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Preconnecting when rendering
  - Preconnecting in an event handler

preconnect lets you eagerly connect to a server that you expect to load resources from.

To preconnect to a host, call the preconnect function from react-dom.

See more examples below.

The preconnect function provides the browser with a hint that it should open a connection to the given server. If the browser chooses to do so, this can speed up the loading of resources from that server.

preconnect returns nothing.

Call preconnect when rendering a component if you know that its children will load external resources from that host.

Call preconnect in an event handler before transitioning to a page or state where external resources will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

**Examples:**

Example 1 (unknown):
```unknown
preconnect("https://example.com");
```

Example 2 (python):
```python
import { preconnect } from 'react-dom';function AppRoot() {  preconnect("https://example.com");  // ...}
```

Example 3 (python):
```python
import { preconnect } from 'react-dom';function AppRoot() {  preconnect("https://example.com");  return ...;}
```

Example 4 (python):
```python
import { preconnect } from 'react-dom';function CallToAction() {  const onClick = () => {    preconnect('http://example.com');    startWizard();  }  return (    <button onClick={onClick}>Start Wizard</button>  );}
```

---

## hydrateRoot

**URL:** https://react.dev/reference/react-dom/client/hydrateRoot

**Contents:**
- hydrateRoot
- Reference
  - hydrateRoot(domNode, reactNode, options?)
    - Parameters
    - Returns
    - Caveats
  - root.render(reactNode)
    - Parameters
    - Returns
    - Caveats

hydrateRoot lets you display React components inside a browser DOM node whose HTML content was previously generated by react-dom/server.

Call hydrateRoot to “attach” React to existing HTML that was already rendered by React in a server environment.

React will attach to the HTML that exists inside the domNode, and take over managing the DOM inside it. An app fully built with React will usually only have one hydrateRoot call with its root component.

See more examples below.

domNode: A DOM element that was rendered as the root element on the server.

reactNode: The “React node” used to render the existing HTML. This will usually be a piece of JSX like <App /> which was rendered with a ReactDOM Server method such as renderToPipeableStream(<App />).

optional options: An object with options for this React root.

hydrateRoot returns an object with two methods: render and unmount.

Call root.render to update a React component inside a hydrated React root for a browser DOM element.

React will update <App /> in the hydrated root.

See more examples below.

root.render returns undefined.

Call root.unmount to destroy a rendered tree inside a React root.

An app fully built with React will usually not have any calls to root.unmount.

This is mostly useful if your React root’s DOM node (or any of its ancestors) may get removed from the DOM by some other code. For example, imagine a jQuery tab panel that removes inactive tabs from the DOM. If a tab gets removed, everything inside it (including the React roots inside) would get removed from the DOM as well. You need to tell React to “stop” managing the removed root’s content by calling root.unmount. Otherwise, the components inside the removed root won’t clean up and free up resources like subscriptions.

Calling root.unmount will unmount all the components in the root and “detach” React from the root DOM node, including removing any event handlers or state in the tree.

root.unmount does not accept any parameters.

root.unmount returns undefined.

Calling root.unmount will unmount all the components in the tree and “detach” React from the root DOM node.

Once you call root.unmount you cannot call root.render again on the root. Attempting to call root.render on an unmounted root will throw a “Cannot update an unmounted root” error.

If your app’s HTML was generated by react-dom/server, you need to hydrate it on the client.

This will hydrate the server HTML inside the browser DOM node with the React component for y

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const root = hydrateRoot(domNode, reactNode, options?)
```

Example 2 (python):
```python
import { hydrateRoot } from 'react-dom/client';const domNode = document.getElementById('root');const root = hydrateRoot(domNode, reactNode);
```

Example 3 (unknown):
```unknown
root.render(<App />);
```

Example 4 (unknown):
```unknown
root.unmount();
```

---

## 'use client'

**URL:** https://react.dev/reference/rsc/use-client

**Contents:**
- 'use client'
  - React Server Components
- Reference
  - 'use client'
    - Caveats
  - How 'use client' marks client code
      - Deep Dive
    - How is FancyText both a Server and a Client Component?
      - Deep Dive
    - Why is Copyright a Server Component?

'use client' is for use with React Server Components.

'use client' lets you mark what code runs on the client.

Add 'use client' at the top of a file to mark the module and its transitive dependencies as client code.

When a file marked with 'use client' is imported from a Server Component, compatible bundlers will treat the module import as a boundary between server-run and client-run code.

As dependencies of RichTextEditor, formatDate and Button will also be evaluated on the client regardless of whether their modules contain a 'use client' directive. Note that a single module may be evaluated on the server when imported from server code and on the client when imported from client code.

In a React app, components are often split into separate files, or modules.

For apps that use React Server Components, the app is server-rendered by default. 'use client' introduces a server-client boundary in the module dependency tree, effectively creating a subtree of Client modules.

To better illustrate this, consider the following React Server Components app.

In the module dependency tree of this example app, the 'use client' directive in InspirationGenerator.js marks that module and all of its transitive dependencies as Client modules. The subtree starting at InspirationGenerator.js is now marked as Client modules.

'use client' segments the module dependency tree of the React Server Components app, marking InspirationGenerator.js and all of its dependencies as client-rendered.

During render, the framework will server-render the root component and continue through the render tree, opting-out of evaluating any code imported from client-marked code.

The server-rendered portion of the render tree is then sent to the client. The client, with its client code downloaded, then completes rendering the rest of the tree.

The render tree for the React Server Components app. InspirationGenerator and its child component FancyText are components exported from client-marked code and considered Client Components.

We introduce the following definitions:

Working through the example app, App, FancyText and Copyright are all server-rendered and considered Server Components. As InspirationGenerator.js and its transitive dependencies are marked as client code, the component InspirationGenerator and its child component FancyText are Client Components.

By the above definitions, the component FancyText is both a Server and Client Component, how can that be?

First, let’s clarify 

*[Content truncated]*

**Examples:**

Example 1 (python):
```python
'use client';import { useState } from 'react';import { formatDate } from './formatters';import Button from './button';export default function RichTextEditor({ timestamp, text }) {  const date = formatDate(timestamp);  // ...  const editButton = <Button />;  // ...}
```

Example 2 (unknown):
```unknown
// This is a definition of a componentfunction MyComponent() {  return <p>My Component</p>}
```

Example 3 (python):
```python
import MyComponent from './MyComponent';function App() {  // This is a usage of a component  return <MyComponent />;}
```

Example 4 (python):
```python
import { readFile } from 'node:fs/promises';import Counter from './Counter';export default async function CounterContainer() {  const initialValue = await readFile('/path/to/counter_value');  return <Counter initialValue={initialValue} />}
```

---

## React DOM APIs

**URL:** https://react.dev/reference/react-dom#resource-preloading-apis

**Contents:**
- React DOM APIs
- APIs
- Resource Preloading APIs
- Entry points
- Removed APIs

The react-dom package contains methods that are only supported for the web applications (which run in the browser DOM environment). They are not supported for React Native.

These APIs can be imported from your components. They are rarely used:

These APIs can be used to make apps faster by pre-loading resources such as scripts, stylesheets, and fonts as soon as you know you need them, for example before navigating to another page where the resources will be used.

React-based frameworks frequently handle resource loading for you, so you might not have to call these APIs yourself. Consult your framework’s documentation for details.

The react-dom package provides two additional entry points:

These APIs were removed in React 19:

---

## preload

**URL:** https://react.dev/reference/react-dom/preload

**Contents:**
- preload
  - Note
- Reference
  - preload(href, options)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Preloading when rendering
    - Examples of preloading

React-based frameworks frequently handle resource loading for you, so you might not have to call this API yourself. Consult your framework’s documentation for details.

preload lets you eagerly fetch a resource such as a stylesheet, font, or external script that you expect to use.

To preload a resource, call the preload function from react-dom.

See more examples below.

The preload function provides the browser with a hint that it should start downloading the given resource, which can save time.

preload returns nothing.

Call preload when rendering a component if you know that it or its children will use a specific resource.

If you want the browser to start executing the script immediately (rather than just downloading it), use preinit instead. If you want to load an ESM module, use preloadModule.

Call preload in an event handler before transitioning to a page or state where external resources will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

**Examples:**

Example 1 (unknown):
```unknown
preload("https://example.com/font.woff2", {as: "font"});
```

Example 2 (python):
```python
import { preload } from 'react-dom';function AppRoot() {  preload("https://example.com/font.woff2", {as: "font"});  // ...}
```

Example 3 (python):
```python
import { preload } from 'react-dom';function AppRoot() {  preload("https://example.com/script.js", {as: "script"});  return ...;}
```

Example 4 (python):
```python
import { preload } from 'react-dom';function CallToAction() {  const onClick = () => {    preload("https://example.com/wizardStyles.css", {as: "style"});    startWizard();  }  return (    <button onClick={onClick}>Start Wizard</button>  );}
```

---

## createRoot

**URL:** https://react.dev/reference/react-dom/client/createRoot#root-unmount

**Contents:**
- createRoot
- Reference
  - createRoot(domNode, options?)
    - Parameters
    - Returns
    - Caveats
  - root.render(reactNode)
    - Parameters
    - Returns
    - Caveats

createRoot lets you create a root to display React components inside a browser DOM node.

Call createRoot to create a React root for displaying content inside a browser DOM element.

React will create a root for the domNode, and take over managing the DOM inside it. After you’ve created a root, you need to call root.render to display a React component inside of it:

An app fully built with React will usually only have one createRoot call for its root component. A page that uses “sprinkles” of React for parts of the page may have as many separate roots as needed.

See more examples below.

domNode: A DOM element. React will create a root for this DOM element and allow you to call functions on the root, such as render to display rendered React content.

optional options: An object with options for this React root.

createRoot returns an object with two methods: render and unmount.

Call root.render to display a piece of JSX (“React node”) into the React root’s browser DOM node.

React will display <App /> in the root, and take over managing the DOM inside it.

See more examples below.

root.render returns undefined.

The first time you call root.render, React will clear all the existing HTML content inside the React root before rendering the React component into it.

If your root’s DOM node contains HTML generated by React on the server or during the build, use hydrateRoot() instead, which attaches the event handlers to the existing HTML.

If you call render on the same root more than once, React will update the DOM as necessary to reflect the latest JSX you passed. React will decide which parts of the DOM can be reused and which need to be recreated by “matching it up” with the previously rendered tree. Calling render on the same root again is similar to calling the set function on the root component: React avoids unnecessary DOM updates.

Although rendering is synchronous once it starts, root.render(...) is not. This means code after root.render() may run before any effects (useLayoutEffect, useEffect) of that specific render are fired. This is usually fine and rarely needs adjustment. In rare cases where effect timing matters, you can wrap root.render(...) in flushSync to ensure the initial render runs fully synchronously.

Call root.unmount to destroy a rendered tree inside a React root.

An app fully built with React will usually not have any calls to root.unmount.

This is mostly useful if your React root’s DOM node (or any of its ancestors) may get re

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const root = createRoot(domNode, options?)
```

Example 2 (python):
```python
import { createRoot } from 'react-dom/client';const domNode = document.getElementById('root');const root = createRoot(domNode);
```

Example 3 (unknown):
```unknown
root.render(<App />);
```

Example 4 (unknown):
```unknown
root.render(<App />);
```

---

## React DOM APIs

**URL:** https://react.dev/reference/react-dom#removed-apis

**Contents:**
- React DOM APIs
- APIs
- Resource Preloading APIs
- Entry points
- Removed APIs

The react-dom package contains methods that are only supported for the web applications (which run in the browser DOM environment). They are not supported for React Native.

These APIs can be imported from your components. They are rarely used:

These APIs can be used to make apps faster by pre-loading resources such as scripts, stylesheets, and fonts as soon as you know you need them, for example before navigating to another page where the resources will be used.

React-based frameworks frequently handle resource loading for you, so you might not have to call these APIs yourself. Consult your framework’s documentation for details.

The react-dom package provides two additional entry points:

These APIs were removed in React 19:

---
