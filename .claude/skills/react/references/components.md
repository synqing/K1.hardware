# React - Components

**Pages:** 101

---

## Writing Markup with JSX

**URL:** https://react.dev/learn/writing-markup-with-jsx

**Contents:**
- Writing Markup with JSX
  - You will learn
- JSX: Putting markup into JavaScript
  - Note
- Converting HTML to JSX
  - Note
- The Rules of JSX
  - 1. Return a single root element
      - Deep Dive
    - Why do multiple JSX tags need to be wrapped?

JSX is a syntax extension for JavaScript that lets you write HTML-like markup inside a JavaScript file. Although there are other ways to write components, most React developers prefer the conciseness of JSX, and most codebases use it.

The Web has been built on HTML, CSS, and JavaScript. For many years, web developers kept content in HTML, design in CSS, and logic in JavaScript—often in separate files! Content was marked up inside HTML while the page’s logic lived separately in JavaScript:

But as the Web became more interactive, logic increasingly determined content. JavaScript was in charge of the HTML! This is why in React, rendering logic and markup live together in the same place—components.

Sidebar.js React component

Form.js React component

Keeping a button’s rendering logic and markup together ensures that they stay in sync with each other on every edit. Conversely, details that are unrelated, such as the button’s markup and a sidebar’s markup, are isolated from each other, making it safer to change either of them on their own.

Each React component is a JavaScript function that may contain some markup that React renders into the browser. React components use a syntax extension called JSX to represent that markup. JSX looks a lot like HTML, but it is a bit stricter and can display dynamic information. The best way to understand this is to convert some HTML markup to JSX markup.

JSX and React are two separate things. They’re often used together, but you can use them independently of each other. JSX is a syntax extension, while React is a JavaScript library.

Suppose that you have some (perfectly valid) HTML:

And you want to put it into your component:

If you copy and paste it as is, it will not work:

This is because JSX is stricter and has a few more rules than HTML! If you read the error messages above, they’ll guide you to fix the markup, or you can follow the guide below.

Most of the time, React’s on-screen error messages will help you find where the problem is. Give them a read if you get stuck!

To return multiple elements from a component, wrap them with a single parent tag.

For example, you can use a <div>:

If you don’t want to add an extra <div> to your markup, you can write <> and </> instead:

This empty tag is called a Fragment. Fragments let you group things without leaving any trace in the browser HTML tree.

JSX looks like HTML, but under the hood it is transformed into plain JavaScript objects. You can’t return two objects fr

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<h1>Hedy Lamarr's Todos</h1><img   src="https://i.imgur.com/yXOvdOSs.jpg"   alt="Hedy Lamarr"   class="photo"><ul>    <li>Invent new traffic lights    <li>Rehearse a movie scene    <li>Improve the spectrum technology</ul>
```

Example 2 (unknown):
```unknown
export default function TodoList() {  return (    // ???  )}
```

Example 3 (unknown):
```unknown
<div>  <h1>Hedy Lamarr's Todos</h1>  <img     src="https://i.imgur.com/yXOvdOSs.jpg"     alt="Hedy Lamarr"     class="photo"  >  <ul>    ...  </ul></div>
```

Example 4 (unknown):
```unknown
<>  <h1>Hedy Lamarr's Todos</h1>  <img     src="https://i.imgur.com/yXOvdOSs.jpg"     alt="Hedy Lamarr"     class="photo"  >  <ul>    ...  </ul></>
```

---

## React DOM Components

**URL:** https://react.dev/reference/react-dom/components#all-html-components

**Contents:**
- React DOM Components
- Common components
- Form components
- Resource and Metadata Components
- All HTML components
  - Note
  - Custom HTML elements
    - Setting values on custom elements
    - Listening for events on custom elements
  - Note

React supports all of the browser built-in HTML and SVG components.

All of the built-in browser components support some props and events.

This includes React-specific props like ref and dangerouslySetInnerHTML.

These built-in browser components accept user input:

They are special in React because passing the value prop to them makes them controlled.

These built-in browser components let you load external resources or annotate the document with metadata:

They are special in React because React can render them into the document head, suspend while resources are loading, and enact other behaviors that are described on the reference page for each specific component.

React supports all built-in browser HTML components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing HTML to JSX with an online converter.

If you render a tag with a dash, like <my-element>, React will assume you want to render a custom HTML element.

If you render a built-in browser HTML element with an is attribute, it will also be treated as a custom element.

Custom elements have two methods of passing data into them:

By default, React will pass values bound in JSX as attributes:

Non-string JavaScript values passed to custom elements will be serialized by default:

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

A common pattern when using custom elements is that they may dispatch CustomEvents rather than accept a function to call when an event occur. You can listen for these events using an on prefix when binding to the event via JSX.

Events are case-sensitive and support dashes (-). Preserve the casing of the event and include all dashes when listening for custom element’s events:

React supports all built-in browser SVG components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing SVG to JSX with an online converter.

Namespaced attributes also have to be written without the colon:

**Examples:**

Example 1 (unknown):
```unknown
<my-element value="Hello, world!"></my-element>
```

Example 2 (unknown):
```unknown
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`<my-element value={[1,2,3]}></my-element>
```

Example 3 (unknown):
```unknown
// Listens for `say-hi` events<my-element onsay-hi={console.log}></my-element>// Listens for `sayHi` events<my-element onsayHi={console.log}></my-element>
```

---

## Thinking in React

**URL:** https://react.dev/learn/thinking-in-react#step-1-break-the-ui-into-a-component-hierarchy

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

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component#step-1-pass-props-to-the-child-component

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## Adding Interactivity

**URL:** https://react.dev/learn/adding-interactivity#render-and-commit

**Contents:**
- Adding Interactivity
  - In this chapter
- Responding to events
- Ready to learn this topic?
- State: a component’s memory
- Ready to learn this topic?
- Render and commit
- Ready to learn this topic?
- State as a snapshot
- Ready to learn this topic?

Some things on the screen update in response to user input. For example, clicking an image gallery switches the active image. In React, data that changes over time is called state. You can add state to any component, and update it as needed. In this chapter, you’ll learn how to write components that handle interactions, update their state, and display different output over time.

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to user interactions like clicking, hovering, focusing on form inputs, and so on.

Built-in components like <button> only support built-in browser events like onClick. However, you can also create your own components, and give their event handler props any application-specific names that you like.

Read Responding to Events to learn how to add event handlers.

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” puts a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

You can add state to a component with a useState Hook. Hooks are special functions that let your components use React features (state is one of those features). The useState Hook lets you declare a state variable. It takes the initial state and returns a pair of values: the current state, and a state setter function that lets you update it.

Here is how an image gallery uses and updates state on click:

Read State: A Component’s Memory to learn how to remember a value and update it on interaction.

Before your components are displayed on the screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

Read Render and Commit to learn the lifecycle of a UI update.

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already ha

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

Example 2 (unknown):
```unknown
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

Example 3 (unknown):
```unknown
console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0
```

---

## Your First Component

**URL:** https://react.dev/learn/your-first-component#step-2-define-the-function

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## Built-in React Components

**URL:** https://react.dev/reference/react/components#undefined

**Contents:**
- Built-in React Components
- Built-in components
- Your own components

React exposes a few built-in components that you can use in your JSX.

You can also define your own components as JavaScript functions.

---

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory#when-a-regular-variable-isnt-enough

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

## Your First Component

**URL:** https://react.dev/learn/your-first-component

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## Your First Component

**URL:** https://react.dev/learn/your-first-component#step-1-export-the-component

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui#javascript-in-jsx-with-curly-braces

**Contents:**
- Describing the UI
  - In this chapter
- Your first component
- Ready to learn this topic?
- Importing and exporting components
- Ready to learn this topic?
- Writing markup with JSX
- Ready to learn this topic?
- JavaScript in JSX with curly braces
- Ready to learn this topic?

React is a JavaScript library for rendering user interfaces (UI). UI is built from small units like buttons, text, and images. React lets you combine them into reusable, nestable components. From web sites to phone apps, everything on the screen can be broken down into components. In this chapter, you’ll learn to create, customize, and conditionally display React components.

React applications are built from isolated pieces of UI called components. A React component is a JavaScript function that you can sprinkle with markup. Components can be as small as a button, or as large as an entire page. Here is a Gallery component rendering three Profile components:

Read Your First Component to learn how to declare and use React components.

You can declare many components in one file, but large files can get difficult to navigate. To solve this, you can export a component into its own file, and then import that component from another file:

Read Importing and Exporting Components to learn how to split components into their own files.

Each React component is a JavaScript function that may contain some markup that React renders into the browser. React components use a syntax extension called JSX to represent that markup. JSX looks a lot like HTML, but it is a bit stricter and can display dynamic information.

If we paste existing HTML markup into a React component, it won’t always work:

If you have existing HTML like this, you can fix it using a converter:

Read Writing Markup with JSX to learn how to write valid JSX.

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to “open a window” to JavaScript:

Read JavaScript in JSX with Curly Braces to learn how to access JavaScript data from JSX.

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, functions, and even JSX!

Read Passing Props to a Component to learn how to pass and read props.

Your components will often need to display different things depending on different conditions. In React, you can conditionally render JSX using JavaScript syntax like if statement

*[Content truncated]*

---

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component#passing-props-to-a-component

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## <select>

**URL:** https://react.dev/reference/react-dom/components/select

**Contents:**
- <select>
- Reference
  - <select>
    - Props
    - Caveats
- Usage
  - Displaying a select box with options
  - Providing a label for a select box
  - Providing an initially selected option
  - Pitfall

The built-in browser <select> component lets you render a select box with options.

To display a select box, render the built-in browser <select> component.

See more examples below.

<select> supports all common element props.

You can make a select box controlled by passing a value prop:

When you pass value, you must also pass an onChange handler that updates the passed value.

If your <select> is uncontrolled, you may pass the defaultValue prop instead:

These <select> props are relevant both for uncontrolled and controlled select boxes:

Render a <select> with a list of <option> components inside to display a select box. Give each <option> a value representing the data to be submitted with the form.

Typically, you will place every <select> inside a <label> tag. This tells the browser that this label is associated with that select box. When the user clicks the label, the browser will automatically focus the select box. It’s also essential for accessibility: a screen reader will announce the label caption when the user focuses the select box.

If you can’t nest <select> into a <label>, associate them by passing the same ID to <select id> and <label htmlFor>. To avoid conflicts between multiple instances of one component, generate such an ID with useId.

By default, the browser will select the first <option> in the list. To select a different option by default, pass that <option>’s value as the defaultValue to the <select> element.

Unlike in HTML, passing a selected attribute to an individual <option> is not supported.

Pass multiple={true} to the <select> to let the user select multiple options. In that case, if you also specify defaultValue to choose the initially selected options, it must be an array.

Add a <form> around your select box with a <button type="submit"> inside. It will call your <form onSubmit> event handler. By default, the browser will send the form data to the current URL and refresh the page. You can override that behavior by calling e.preventDefault(). Read the form data with new FormData(e.target).

Give a name to your <select>, for example <select name="selectedFruit" />. The name you specified will be used as a key in the form data, for example { selectedFruit: "orange" }.

If you use <select multiple={true}>, the FormData you’ll read from the form will include each selected value as a separate name-value pair. Look closely at the console logs in the example above.

By default, any <button> inside a <form> will submit it. This 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<select>  <option value="someOption">Some option</option>  <option value="otherOption">Other option</option></select>
```

Example 2 (unknown):
```unknown
<select>  <option value="someOption">Some option</option>  <option value="otherOption">Other option</option></select>
```

Example 3 (javascript):
```javascript
function FruitPicker() {  const [selectedFruit, setSelectedFruit] = useState('orange'); // Declare a state variable...  // ...  return (    <select      value={selectedFruit} // ...force the select's value to match the state variable...      onChange={e => setSelectedFruit(e.target.value)} // ... and update the state variable on any change!    >      <option value="apple">Apple</option>      <option value="banana">Banana</option>      <option value="orange">Orange</option>    </select>  );}
```

---

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component#recap

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## React DOM Components

**URL:** https://react.dev/reference/react-dom/components#undefined

**Contents:**
- React DOM Components
- Common components
- Form components
- Resource and Metadata Components
- All HTML components
  - Note
  - Custom HTML elements
    - Setting values on custom elements
    - Listening for events on custom elements
  - Note

React supports all of the browser built-in HTML and SVG components.

All of the built-in browser components support some props and events.

This includes React-specific props like ref and dangerouslySetInnerHTML.

These built-in browser components accept user input:

They are special in React because passing the value prop to them makes them controlled.

These built-in browser components let you load external resources or annotate the document with metadata:

They are special in React because React can render them into the document head, suspend while resources are loading, and enact other behaviors that are described on the reference page for each specific component.

React supports all built-in browser HTML components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing HTML to JSX with an online converter.

If you render a tag with a dash, like <my-element>, React will assume you want to render a custom HTML element.

If you render a built-in browser HTML element with an is attribute, it will also be treated as a custom element.

Custom elements have two methods of passing data into them:

By default, React will pass values bound in JSX as attributes:

Non-string JavaScript values passed to custom elements will be serialized by default:

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

A common pattern when using custom elements is that they may dispatch CustomEvents rather than accept a function to call when an event occur. You can listen for these events using an on prefix when binding to the event via JSX.

Events are case-sensitive and support dashes (-). Preserve the casing of the event and include all dashes when listening for custom element’s events:

React supports all built-in browser SVG components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing SVG to JSX with an online converter.

Namespaced attributes also have to be written without the colon:

**Examples:**

Example 1 (unknown):
```unknown
<my-element value="Hello, world!"></my-element>
```

Example 2 (unknown):
```unknown
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`<my-element value={[1,2,3]}></my-element>
```

Example 3 (unknown):
```unknown
// Listens for `say-hi` events<my-element onsay-hi={console.log}></my-element>// Listens for `sayHi` events<my-element onsayHi={console.log}></my-element>
```

---

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## <input>

**URL:** https://react.dev/reference/react-dom/components/input

**Contents:**
- <input>
- Reference
  - <input>
    - Props
    - Caveats
- Usage
  - Displaying inputs of different types
  - Providing a label for an input
  - Providing an initial value for an input
  - Reading the input values when submitting a form

The built-in browser <input> component lets you render different kinds of form inputs.

To display an input, render the built-in browser <input> component.

See more examples below.

<input> supports all common element props.

You can make an input controlled by passing one of these props:

When you pass either of them, you must also pass an onChange handler that updates the passed value.

These <input> props are only relevant for uncontrolled inputs:

These <input> props are relevant both for uncontrolled and controlled inputs:

To display an input, render an <input> component. By default, it will be a text input. You can pass type="checkbox" for a checkbox, type="radio" for a radio button, or one of the other input types.

Typically, you will place every <input> inside a <label> tag. This tells the browser that this label is associated with that input. When the user clicks the label, the browser will automatically focus the input. It’s also essential for accessibility: a screen reader will announce the label caption when the user focuses the associated input.

If you can’t nest <input> into a <label>, associate them by passing the same ID to <input id> and <label htmlFor>. To avoid conflicts between multiple instances of one component, generate such an ID with useId.

You can optionally specify the initial value for any input. Pass it as the defaultValue string for text inputs. Checkboxes and radio buttons should specify the initial value with the defaultChecked boolean instead.

Add a <form> around your inputs with a <button type="submit"> inside. It will call your <form onSubmit> event handler. By default, the browser will send the form data to the current URL and refresh the page. You can override that behavior by calling e.preventDefault(). Read the form data with new FormData(e.target).

Give a name to every <input>, for example <input name="firstName" defaultValue="Taylor" />. The name you specified will be used as a key in the form data, for example { firstName: "Taylor" }.

By default, a <button> inside a <form> without a type attribute will submit it. This can be surprising! If you have your own custom Button React component, consider using <button type="button"> instead of <button> (with no type). Then, to be explicit, use <button type="submit"> for buttons that are supposed to submit the form.

An input like <input /> is uncontrolled. Even if you pass an initial value like <input defaultValue="Initial text" />, your JSX only specifies the init

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<input name="myInput" />
```

Example 2 (javascript):
```javascript
function Form() {  const [firstName, setFirstName] = useState(''); // Declare a state variable...  // ...  return (    <input      value={firstName} // ...force the input's value to match the state variable...      onChange={e => setFirstName(e.target.value)} // ... and update the state variable on any edits!    />  );}
```

Example 3 (javascript):
```javascript
function Form() {  const [firstName, setFirstName] = useState('');  return (    <>      <label>        First name:        <input value={firstName} onChange={e => setFirstName(e.target.value)} />      </label>      {firstName !== '' && <p>Your name is {firstName}.</p>}      ...
```

Example 4 (javascript):
```javascript
function Form() {  // ...  const [age, setAge] = useState('');  const ageAsNumber = Number(age);  return (    <>      <label>        Age:        <input          value={age}          onChange={e => setAge(e.target.value)}          type="number"        />        <button onClick={() => setAge(ageAsNumber + 10)}>          Add 10 years        </button>
```

---

## <script>

**URL:** https://react.dev/reference/react-dom/components/script

**Contents:**
- <script>
- Reference
  - <script>
    - Props
    - Special rendering behavior
- Usage
  - Rendering an external script
  - Note
  - Rendering an inline script

The built-in browser <script> component lets you add a script to your document.

To add inline or external scripts to your document, render the built-in browser <script> component. You can render <script> from any component and React will in certain cases place the corresponding DOM element in the document head and de-duplicate identical scripts.

See more examples below.

<script> supports all common element props.

It should have either children or a src prop.

Other supported props:

Props that disable React’s special treatment of scripts:

Props that are not recommended for use with React:

React can move <script> components to the document’s <head> and de-duplicate identical scripts.

To opt into this behavior, provide the src and async={true} props. React will de-duplicate scripts if they have the same src. The async prop must be true to allow scripts to be safely moved.

This special treatment comes with two caveats:

If a component depends on certain scripts in order to be displayed correctly, you can render a <script> within the component. However, the component might be committed before the script has finished loading. You can start depending on the script content once the load event is fired e.g. by using the onLoad prop.

React will de-duplicate scripts that have the same src, inserting only one of them into the DOM even if multiple components render it.

When you want to use a script, it can be beneficial to call the preinit function. Calling this function may allow the browser to start fetching the script earlier than if you just render a <script> component, for example by sending an HTTP Early Hints response.

To include an inline script, render the <script> component with the script source code as its children. Inline scripts are not de-duplicated or moved to the document <head>.

**Examples:**

Example 1 (unknown):
```unknown
<script> alert("hi!") </script>
```

Example 2 (unknown):
```unknown
<script> alert("hi!") </script><script src="script.js" />
```

---

## Adding Interactivity

**URL:** https://react.dev/learn/adding-interactivity#queueing-a-series-of-state-updates

**Contents:**
- Adding Interactivity
  - In this chapter
- Responding to events
- Ready to learn this topic?
- State: a component’s memory
- Ready to learn this topic?
- Render and commit
- Ready to learn this topic?
- State as a snapshot
- Ready to learn this topic?

Some things on the screen update in response to user input. For example, clicking an image gallery switches the active image. In React, data that changes over time is called state. You can add state to any component, and update it as needed. In this chapter, you’ll learn how to write components that handle interactions, update their state, and display different output over time.

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to user interactions like clicking, hovering, focusing on form inputs, and so on.

Built-in components like <button> only support built-in browser events like onClick. However, you can also create your own components, and give their event handler props any application-specific names that you like.

Read Responding to Events to learn how to add event handlers.

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” puts a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

You can add state to a component with a useState Hook. Hooks are special functions that let your components use React features (state is one of those features). The useState Hook lets you declare a state variable. It takes the initial state and returns a pair of values: the current state, and a state setter function that lets you update it.

Here is how an image gallery uses and updates state on click:

Read State: A Component’s Memory to learn how to remember a value and update it on interaction.

Before your components are displayed on the screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

Read Render and Commit to learn the lifecycle of a UI update.

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already ha

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

Example 2 (unknown):
```unknown
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

Example 3 (unknown):
```unknown
console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0
```

---

## Adding Interactivity

**URL:** https://react.dev/learn/adding-interactivity

**Contents:**
- Adding Interactivity
  - In this chapter
- Responding to events
- Ready to learn this topic?
- State: a component’s memory
- Ready to learn this topic?
- Render and commit
- Ready to learn this topic?
- State as a snapshot
- Ready to learn this topic?

Some things on the screen update in response to user input. For example, clicking an image gallery switches the active image. In React, data that changes over time is called state. You can add state to any component, and update it as needed. In this chapter, you’ll learn how to write components that handle interactions, update their state, and display different output over time.

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to user interactions like clicking, hovering, focusing on form inputs, and so on.

Built-in components like <button> only support built-in browser events like onClick. However, you can also create your own components, and give their event handler props any application-specific names that you like.

Read Responding to Events to learn how to add event handlers.

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” puts a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

You can add state to a component with a useState Hook. Hooks are special functions that let your components use React features (state is one of those features). The useState Hook lets you declare a state variable. It takes the initial state and returns a pair of values: the current state, and a state setter function that lets you update it.

Here is how an image gallery uses and updates state on click:

Read State: A Component’s Memory to learn how to remember a value and update it on interaction.

Before your components are displayed on the screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

Read Render and Commit to learn the lifecycle of a UI update.

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already ha

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

Example 2 (unknown):
```unknown
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

Example 3 (unknown):
```unknown
console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0
```

---

## Adding Interactivity

**URL:** https://react.dev/learn/adding-interactivity#updating-arrays-in-state

**Contents:**
- Adding Interactivity
  - In this chapter
- Responding to events
- Ready to learn this topic?
- State: a component’s memory
- Ready to learn this topic?
- Render and commit
- Ready to learn this topic?
- State as a snapshot
- Ready to learn this topic?

Some things on the screen update in response to user input. For example, clicking an image gallery switches the active image. In React, data that changes over time is called state. You can add state to any component, and update it as needed. In this chapter, you’ll learn how to write components that handle interactions, update their state, and display different output over time.

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to user interactions like clicking, hovering, focusing on form inputs, and so on.

Built-in components like <button> only support built-in browser events like onClick. However, you can also create your own components, and give their event handler props any application-specific names that you like.

Read Responding to Events to learn how to add event handlers.

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” puts a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

You can add state to a component with a useState Hook. Hooks are special functions that let your components use React features (state is one of those features). The useState Hook lets you declare a state variable. It takes the initial state and returns a pair of values: the current state, and a state setter function that lets you update it.

Here is how an image gallery uses and updates state on click:

Read State: A Component’s Memory to learn how to remember a value and update it on interaction.

Before your components are displayed on the screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

Read Render and Commit to learn the lifecycle of a UI update.

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already ha

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

Example 2 (unknown):
```unknown
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

Example 3 (unknown):
```unknown
console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0
```

---

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component#familiar-props

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## <meta>

**URL:** https://react.dev/reference/react-dom/components/meta

**Contents:**
- <meta>
- Reference
  - <meta>
    - Props
    - Special rendering behavior
- Usage
  - Annotating the document with metadata
  - Annotating specific items within the document with metadata

The built-in browser <meta> component lets you add metadata to the document.

To add document metadata, render the built-in browser <meta> component. You can render <meta> from any component and React will always place the corresponding DOM element in the document head.

See more examples below.

<meta> supports all common element props.

It should have exactly one of the following props: name, httpEquiv, charset, itemProp. The <meta> component does something different depending on which of these props is specified.

React will always place the DOM element corresponding to the <meta> component within the document’s <head>, regardless of where in the React tree it is rendered. The <head> is the only valid place for <meta> to exist within the DOM, yet it’s convenient and keeps things composable if a component representing a specific page can render <meta> components itself.

There is one exception to this: if <meta> has an itemProp prop, there is no special behavior, because in this case it doesn’t represent metadata about the document but rather metadata about a specific part of the page.

You can annotate the document with metadata such as keywords, a summary, or the author’s name. React will place this metadata within the document <head> regardless of where in the React tree it is rendered.

You can render the <meta> component from any component. React will put a <meta> DOM node in the document <head>.

You can use the <meta> component with the itemProp prop to annotate specific items within the document with metadata. In this case, React will not place these annotations within the document <head> but will place them like any other React component.

**Examples:**

Example 1 (unknown):
```unknown
<meta name="keywords" content="React, JavaScript, semantic markup, html" />
```

Example 2 (unknown):
```unknown
<meta name="keywords" content="React, JavaScript, semantic markup, html" />
```

Example 3 (unknown):
```unknown
<meta name="author" content="John Smith" /><meta name="keywords" content="React, JavaScript, semantic markup, html" /><meta name="description" content="API reference for the <meta> component in React DOM" />
```

Example 4 (unknown):
```unknown
<section itemScope>  <h3>Annotating specific items</h3>  <meta itemProp="description" content="API reference for using <meta> with itemProp" />  <p>...</p></section>
```

---

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory#complete-the-gallery

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

## Adding Interactivity

**URL:** https://react.dev/learn/adding-interactivity#undefined

**Contents:**
- Adding Interactivity
  - In this chapter
- Responding to events
- Ready to learn this topic?
- State: a component’s memory
- Ready to learn this topic?
- Render and commit
- Ready to learn this topic?
- State as a snapshot
- Ready to learn this topic?

Some things on the screen update in response to user input. For example, clicking an image gallery switches the active image. In React, data that changes over time is called state. You can add state to any component, and update it as needed. In this chapter, you’ll learn how to write components that handle interactions, update their state, and display different output over time.

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to user interactions like clicking, hovering, focusing on form inputs, and so on.

Built-in components like <button> only support built-in browser events like onClick. However, you can also create your own components, and give their event handler props any application-specific names that you like.

Read Responding to Events to learn how to add event handlers.

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” puts a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

You can add state to a component with a useState Hook. Hooks are special functions that let your components use React features (state is one of those features). The useState Hook lets you declare a state variable. It takes the initial state and returns a pair of values: the current state, and a state setter function that lets you update it.

Here is how an image gallery uses and updates state on click:

Read State: A Component’s Memory to learn how to remember a value and update it on interaction.

Before your components are displayed on the screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

Read Render and Commit to learn the lifecycle of a UI update.

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already ha

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

Example 2 (unknown):
```unknown
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

Example 3 (unknown):
```unknown
console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0
```

---

## Conditional Rendering

**URL:** https://react.dev/learn/conditional-rendering

**Contents:**
- Conditional Rendering
  - You will learn
- Conditionally returning JSX
  - Conditionally returning nothing with null
- Conditionally including JSX
  - Conditional (ternary) operator (? :)
      - Deep Dive
    - Are these two examples fully equivalent?
  - Logical AND operator (&&)
  - Pitfall

Your components will often need to display different things depending on different conditions. In React, you can conditionally render JSX using JavaScript syntax like if statements, &&, and ? : operators.

Let’s say you have a PackingList component rendering several Items, which can be marked as packed or not:

Notice that some of the Item components have their isPacked prop set to true instead of false. You want to add a checkmark (✅) to packed items if isPacked={true}.

You can write this as an if/else statement like so:

If the isPacked prop is true, this code returns a different JSX tree. With this change, some of the items get a checkmark at the end:

Try editing what gets returned in either case, and see how the result changes!

Notice how you’re creating branching logic with JavaScript’s if and return statements. In React, control flow (like conditions) is handled by JavaScript.

In some situations, you won’t want to render anything at all. For example, say you don’t want to show packed items at all. A component must return something. In this case, you can return null:

If isPacked is true, the component will return nothing, null. Otherwise, it will return JSX to render.

In practice, returning null from a component isn’t common because it might surprise a developer trying to render it. More often, you would conditionally include or exclude the component in the parent component’s JSX. Here’s how to do that!

In the previous example, you controlled which (if any!) JSX tree would be returned by the component. You may already have noticed some duplication in the render output:

Both of the conditional branches return <li className="item">...</li>:

While this duplication isn’t harmful, it could make your code harder to maintain. What if you want to change the className? You’d have to do it in two places in your code! In such a situation, you could conditionally include a little JSX to make your code more DRY.

JavaScript has a compact syntax for writing a conditional expression — the conditional operator or “ternary operator”.

You can read it as “if isPacked is true, then (?) render name + ' ✅', otherwise (:) render name”.

If you’re coming from an object-oriented programming background, you might assume that the two examples above are subtly different because one of them may create two different “instances” of <li>. But JSX elements aren’t “instances” because they don’t hold any internal state and aren’t real DOM nodes. They’re lightweight descriptio

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
if (isPacked) {  return <li className="item">{name} ✅</li>;}return <li className="item">{name}</li>;
```

Example 2 (unknown):
```unknown
if (isPacked) {  return null;}return <li className="item">{name}</li>;
```

Example 3 (unknown):
```unknown
<li className="item">{name} ✅</li>
```

Example 4 (unknown):
```unknown
<li className="item">{name}</li>
```

---

## Your First Component

**URL:** https://react.dev/learn/your-first-component#components-all-the-way-down

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## Adding Interactivity

**URL:** https://react.dev/learn/adding-interactivity#responding-to-events

**Contents:**
- Adding Interactivity
  - In this chapter
- Responding to events
- Ready to learn this topic?
- State: a component’s memory
- Ready to learn this topic?
- Render and commit
- Ready to learn this topic?
- State as a snapshot
- Ready to learn this topic?

Some things on the screen update in response to user input. For example, clicking an image gallery switches the active image. In React, data that changes over time is called state. You can add state to any component, and update it as needed. In this chapter, you’ll learn how to write components that handle interactions, update their state, and display different output over time.

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to user interactions like clicking, hovering, focusing on form inputs, and so on.

Built-in components like <button> only support built-in browser events like onClick. However, you can also create your own components, and give their event handler props any application-specific names that you like.

Read Responding to Events to learn how to add event handlers.

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” puts a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

You can add state to a component with a useState Hook. Hooks are special functions that let your components use React features (state is one of those features). The useState Hook lets you declare a state variable. It takes the initial state and returns a pair of values: the current state, and a state setter function that lets you update it.

Here is how an image gallery uses and updates state on click:

Read State: A Component’s Memory to learn how to remember a value and update it on interaction.

Before your components are displayed on the screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

Read Render and Commit to learn the lifecycle of a UI update.

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already ha

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

Example 2 (unknown):
```unknown
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

Example 3 (unknown):
```unknown
console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0
```

---

## Server Components

**URL:** https://react.dev/reference/rsc/server-components

**Contents:**
- Server Components
  - Note
    - How do I build support for Server Components?
  - Server Components without a Server
  - Note
  - Server Components with a Server
  - Adding interactivity to Server Components
  - Note
    - There is no directive for Server Components.
  - Async components with Server Components

Server Components are a new type of Component that renders ahead of time, before bundling, in an environment separate from your client app or SSR server.

This separate environment is the “server” in React Server Components. Server Components can run once at build time on your CI server, or they can be run for each request using a web server.

While React Server Components in React 19 are stable and will not break between minor versions, the underlying APIs used to implement a React Server Components bundler or framework do not follow semver and may break between minors in React 19.x.

To support React Server Components as a bundler or framework, we recommend pinning to a specific React version, or using the Canary release. We will continue working with bundlers and frameworks to stabilize the APIs used to implement React Server Components in the future.

Server components can run at build time to read from the filesystem or fetch static content, so a web server is not required. For example, you may want to read static data from a content management system.

Without Server Components, it’s common to fetch static data on the client with an Effect:

This pattern means users need to download and parse an additional 75K (gzipped) of libraries, and wait for a second request to fetch the data after the page loads, just to render static content that will not change for the lifetime of the page.

With Server Components, you can render these components once at build time:

The rendered output can then be server-side rendered (SSR) to HTML and uploaded to a CDN. When the app loads, the client will not see the original Page component, or the expensive libraries for rendering the markdown. The client will only see the rendered output:

This means the content is visible during first page load, and the bundle does not include the expensive libraries needed to render the static content.

You may notice that the Server Component above is an async function:

Async Components are a new feature of Server Components that allow you to await in render.

See Async components with Server Components below.

Server Components can also run on a web server during a request for a page, letting you access your data layer without having to build an API. They are rendered before your application is bundled, and can pass data and JSX as props to Client Components.

Without Server Components, it’s common to fetch dynamic data on the client in an Effect:

With Server Components, you can rea

*[Content truncated]*

**Examples:**

Example 1 (python):
```python
// bundle.jsimport marked from 'marked'; // 35.9K (11.2K gzipped)import sanitizeHtml from 'sanitize-html'; // 206K (63.3K gzipped)function Page({page}) {  const [content, setContent] = useState('');  // NOTE: loads *after* first page render.  useEffect(() => {    fetch(`/api/content/${page}`).then((data) => {      setContent(data.content);    });  }, [page]);  return <div>{sanitizeHtml(marked(content))}</div>;}
```

Example 2 (javascript):
```javascript
// api.jsapp.get(`/api/content/:page`, async (req, res) => {  const page = req.params.page;  const content = await file.readFile(`${page}.md`);  res.send({content});});
```

Example 3 (python):
```python
import marked from 'marked'; // Not included in bundleimport sanitizeHtml from 'sanitize-html'; // Not included in bundleasync function Page({page}) {  // NOTE: loads *during* render, when the app is built.  const content = await file.readFile(`${page}.md`);  return <div>{sanitizeHtml(marked(content))}</div>;}
```

Example 4 (unknown):
```unknown
<div><!-- html for markdown --></div>
```

---

## React DOM Components

**URL:** https://react.dev/reference/react-dom/components#custom-html-elements

**Contents:**
- React DOM Components
- Common components
- Form components
- Resource and Metadata Components
- All HTML components
  - Note
  - Custom HTML elements
    - Setting values on custom elements
    - Listening for events on custom elements
  - Note

React supports all of the browser built-in HTML and SVG components.

All of the built-in browser components support some props and events.

This includes React-specific props like ref and dangerouslySetInnerHTML.

These built-in browser components accept user input:

They are special in React because passing the value prop to them makes them controlled.

These built-in browser components let you load external resources or annotate the document with metadata:

They are special in React because React can render them into the document head, suspend while resources are loading, and enact other behaviors that are described on the reference page for each specific component.

React supports all built-in browser HTML components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing HTML to JSX with an online converter.

If you render a tag with a dash, like <my-element>, React will assume you want to render a custom HTML element.

If you render a built-in browser HTML element with an is attribute, it will also be treated as a custom element.

Custom elements have two methods of passing data into them:

By default, React will pass values bound in JSX as attributes:

Non-string JavaScript values passed to custom elements will be serialized by default:

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

A common pattern when using custom elements is that they may dispatch CustomEvents rather than accept a function to call when an event occur. You can listen for these events using an on prefix when binding to the event via JSX.

Events are case-sensitive and support dashes (-). Preserve the casing of the event and include all dashes when listening for custom element’s events:

React supports all built-in browser SVG components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing SVG to JSX with an online converter.

Namespaced attributes also have to be written without the colon:

**Examples:**

Example 1 (unknown):
```unknown
<my-element value="Hello, world!"></my-element>
```

Example 2 (unknown):
```unknown
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`<my-element value={[1,2,3]}></my-element>
```

Example 3 (unknown):
```unknown
// Listens for `say-hi` events<my-element onsay-hi={console.log}></my-element>// Listens for `sayHi` events<my-element onsayHi={console.log}></my-element>
```

---

## unmountComponentAtNode

**URL:** https://react.dev/reference/react-dom/unmountComponentAtNode

**Contents:**
- unmountComponentAtNode
  - Deprecated
- Reference
  - unmountComponentAtNode(domNode)
    - Parameters
    - Returns
- Usage
  - Removing a React app from a DOM element

This API will be removed in a future major version of React.

In React 18, unmountComponentAtNode was replaced by root.unmount().

unmountComponentAtNode removes a mounted React component from the DOM.

Call unmountComponentAtNode to remove a mounted React component from the DOM and clean up its event handlers and state.

See more examples below.

unmountComponentAtNode returns true if a component was unmounted and false otherwise.

Call unmountComponentAtNode to remove a mounted React component from a browser DOM node and clean up its event handlers and state.

Occasionally, you may want to “sprinkle” React on an existing page, or a page that is not fully written in React. In those cases, you may need to “stop” the React app, by removing all of the UI, state, and listeners from the DOM node it was rendered to.

In this example, clicking “Render React App” will render a React app. Click “Unmount React App” to destroy it:

**Examples:**

Example 1 (unknown):
```unknown
unmountComponentAtNode(domNode)
```

Example 2 (python):
```python
import { unmountComponentAtNode } from 'react-dom';const domNode = document.getElementById('root');render(<App />, domNode);unmountComponentAtNode(domNode);
```

Example 3 (python):
```python
import { render, unmountComponentAtNode } from 'react-dom';import App from './App.js';const rootNode = document.getElementById('root');render(<App />, rootNode);// ...unmountComponentAtNode(rootNode);
```

---

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory#adding-a-state-variable

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

## Built-in React Components

**URL:** https://react.dev/reference/react/components

**Contents:**
- Built-in React Components
- Built-in components
- Your own components

React exposes a few built-in components that you can use in your JSX.

You can also define your own components as JavaScript functions.

---

## Built-in React Components

**URL:** https://react.dev/reference/react/components#your-own-components

**Contents:**
- Built-in React Components
- Built-in components
- Your own components

React exposes a few built-in components that you can use in your JSX.

You can also define your own components as JavaScript functions.

---

## React DOM Components

**URL:** https://react.dev/reference/react-dom/components#all-svg-components

**Contents:**
- React DOM Components
- Common components
- Form components
- Resource and Metadata Components
- All HTML components
  - Note
  - Custom HTML elements
    - Setting values on custom elements
    - Listening for events on custom elements
  - Note

React supports all of the browser built-in HTML and SVG components.

All of the built-in browser components support some props and events.

This includes React-specific props like ref and dangerouslySetInnerHTML.

These built-in browser components accept user input:

They are special in React because passing the value prop to them makes them controlled.

These built-in browser components let you load external resources or annotate the document with metadata:

They are special in React because React can render them into the document head, suspend while resources are loading, and enact other behaviors that are described on the reference page for each specific component.

React supports all built-in browser HTML components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing HTML to JSX with an online converter.

If you render a tag with a dash, like <my-element>, React will assume you want to render a custom HTML element.

If you render a built-in browser HTML element with an is attribute, it will also be treated as a custom element.

Custom elements have two methods of passing data into them:

By default, React will pass values bound in JSX as attributes:

Non-string JavaScript values passed to custom elements will be serialized by default:

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

A common pattern when using custom elements is that they may dispatch CustomEvents rather than accept a function to call when an event occur. You can listen for these events using an on prefix when binding to the event via JSX.

Events are case-sensitive and support dashes (-). Preserve the casing of the event and include all dashes when listening for custom element’s events:

React supports all built-in browser SVG components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing SVG to JSX with an online converter.

Namespaced attributes also have to be written without the colon:

**Examples:**

Example 1 (unknown):
```unknown
<my-element value="Hello, world!"></my-element>
```

Example 2 (unknown):
```unknown
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`<my-element value={[1,2,3]}></my-element>
```

Example 3 (unknown):
```unknown
// Listens for `say-hi` events<my-element onsay-hi={console.log}></my-element>// Listens for `sayHi` events<my-element onsayHi={console.log}></my-element>
```

---

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory#state-is-isolated-and-private

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

## Thinking in React

**URL:** https://react.dev/learn/thinking-in-react#props-vs-state

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

## Common components (e.g. <div>)

**URL:** https://react.dev/reference/react-dom/components/common

**Contents:**
- Common components (e.g. <div>)
- Reference
  - Common components (e.g. <div>)
    - Props
    - Caveats
  - ref callback function
    - Parameters
  - Note
    - React 19 added cleanup functions for ref callbacks.
    - Returns

All built-in browser components, such as <div>, support some common props and events.

See more examples below.

These special React props are supported for all built-in components:

children: A React node (an element, a string, a number, a portal, an empty node like null, undefined and booleans, or an array of other React nodes). Specifies the content inside the component. When you use JSX, you will usually specify the children prop implicitly by nesting tags like <div><span /></div>.

dangerouslySetInnerHTML: An object of the form { __html: '<p>some html</p>' } with a raw HTML string inside. Overrides the innerHTML property of the DOM node and displays the passed HTML inside. This should be used with extreme caution! If the HTML inside isn’t trusted (for example, if it’s based on user data), you risk introducing an XSS vulnerability. Read more about using dangerouslySetInnerHTML.

ref: A ref object from useRef or createRef, or a ref callback function, or a string for legacy refs. Your ref will be filled with the DOM element for this node. Read more about manipulating the DOM with refs.

suppressContentEditableWarning: A boolean. If true, suppresses the warning that React shows for elements that both have children and contentEditable={true} (which normally do not work together). Use this if you’re building a text input library that manages the contentEditable content manually.

suppressHydrationWarning: A boolean. If you use server rendering, normally there is a warning when the server and the client render different content. In some rare cases (like timestamps), it is very hard or impossible to guarantee an exact match. If you set suppressHydrationWarning to true, React will not warn you about mismatches in the attributes and the content of that element. It only works one level deep, and is intended to be used as an escape hatch. Don’t overuse it. Read about suppressing hydration errors.

style: An object with CSS styles, for example { fontWeight: 'bold', margin: 20 }. Similarly to the DOM style property, the CSS property names need to be written as camelCase, for example fontWeight instead of font-weight. You can pass strings or numbers as values. If you pass a number, like width: 100, React will automatically append px (“pixels”) to the value unless it’s a unitless property. We recommend using style only for dynamic styles where you don’t know the style values ahead of time. In other cases, applying plain CSS classes with className is more efficient. R

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<div className="wrapper">Some content</div>
```

Example 2 (javascript):
```javascript
<div ref={(node) => {  console.log('Attached', node);  return () => {    console.log('Clean up', node)  }}}>
```

Example 3 (javascript):
```javascript
<button onClick={e => {  console.log(e); // React event object}} />
```

Example 4 (javascript):
```javascript
<div  onAnimationStart={e => console.log('onAnimationStart')}  onAnimationIteration={e => console.log('onAnimationIteration')}  onAnimationEnd={e => console.log('onAnimationEnd')}/>
```

---

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory#challenges

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

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui#importing-and-exporting-components

**Contents:**
- Describing the UI
  - In this chapter
- Your first component
- Ready to learn this topic?
- Importing and exporting components
- Ready to learn this topic?
- Writing markup with JSX
- Ready to learn this topic?
- JavaScript in JSX with curly braces
- Ready to learn this topic?

React is a JavaScript library for rendering user interfaces (UI). UI is built from small units like buttons, text, and images. React lets you combine them into reusable, nestable components. From web sites to phone apps, everything on the screen can be broken down into components. In this chapter, you’ll learn to create, customize, and conditionally display React components.

React applications are built from isolated pieces of UI called components. A React component is a JavaScript function that you can sprinkle with markup. Components can be as small as a button, or as large as an entire page. Here is a Gallery component rendering three Profile components:

Read Your First Component to learn how to declare and use React components.

You can declare many components in one file, but large files can get difficult to navigate. To solve this, you can export a component into its own file, and then import that component from another file:

Read Importing and Exporting Components to learn how to split components into their own files.

Each React component is a JavaScript function that may contain some markup that React renders into the browser. React components use a syntax extension called JSX to represent that markup. JSX looks a lot like HTML, but it is a bit stricter and can display dynamic information.

If we paste existing HTML markup into a React component, it won’t always work:

If you have existing HTML like this, you can fix it using a converter:

Read Writing Markup with JSX to learn how to write valid JSX.

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to “open a window” to JavaScript:

Read JavaScript in JSX with Curly Braces to learn how to access JavaScript data from JSX.

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, functions, and even JSX!

Read Passing Props to a Component to learn how to pass and read props.

Your components will often need to display different things depending on different conditions. In React, you can conditionally render JSX using JavaScript syntax like if statement

*[Content truncated]*

---

## JavaScript in JSX with Curly Braces

**URL:** https://react.dev/learn/javascript-in-jsx-with-curly-braces#using-double-curlies-css-and-other-objects-in-jsx

**Contents:**
- JavaScript in JSX with Curly Braces
  - You will learn
- Passing strings with quotes
- Using curly braces: A window into the JavaScript world
  - Where to use curly braces
- Using “double curlies”: CSS and other objects in JSX
  - Pitfall
- More fun with JavaScript objects and curly braces
- Recap
- Try out some challenges

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to open a window to JavaScript.

When you want to pass a string attribute to JSX, you put it in single or double quotes:

Here, "https://i.imgur.com/7vQD0fPs.jpg" and "Gregorio Y. Zara" are being passed as strings.

But what if you want to dynamically specify the src or alt text? You could use a value from JavaScript by replacing " and " with { and }:

Notice the difference between className="avatar", which specifies an "avatar" CSS class name that makes the image round, and src={avatar} that reads the value of the JavaScript variable called avatar. That’s because curly braces let you work with JavaScript right there in your markup!

JSX is a special way of writing JavaScript. That means it’s possible to use JavaScript inside it—with curly braces { }. The example below first declares a name for the scientist, name, then embeds it with curly braces inside the <h1>:

Try changing the name’s value from 'Gregorio Y. Zara' to 'Hedy Lamarr'. See how the list title changes?

Any JavaScript expression will work between curly braces, including function calls like formatDate():

You can only use curly braces in two ways inside JSX:

In addition to strings, numbers, and other JavaScript expressions, you can even pass objects in JSX. Objects are also denoted with curly braces, like { name: "Hedy Lamarr", inventions: 5 }. Therefore, to pass a JS object in JSX, you must wrap the object in another pair of curly braces: person={{ name: "Hedy Lamarr", inventions: 5 }}.

You may see this with inline CSS styles in JSX. React does not require you to use inline styles (CSS classes work great for most cases). But when you need an inline style, you pass an object to the style attribute:

Try changing the values of backgroundColor and color.

You can really see the JavaScript object inside the curly braces when you write it like this:

The next time you see {{ and }} in JSX, know that it’s nothing more than an object inside the JSX curlies!

Inline style properties are written in camelCase. For example, HTML <ul style="background-color: black"> would be written as <ul style={{ backgroundColor: 'black' }}> in your component.

You can move several expressions into one object, and reference them in your JS

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<ul style={  {    backgroundColor: 'black',    color: 'pink'  }}>
```

Example 2 (javascript):
```javascript
const person = {  name: 'Gregorio Y. Zara',  theme: {    backgroundColor: 'black',    color: 'pink'  }};
```

Example 3 (unknown):
```unknown
<div style={person.theme}>  <h1>{person.name}'s Todos</h1>
```

---

## You Might Not Need an Effect

**URL:** https://react.dev/learn/you-might-not-need-an-effect

**Contents:**
- You Might Not Need an Effect
  - You will learn
- How to remove unnecessary Effects
  - Updating state based on props or state
  - Caching expensive calculations
  - Note
      - Deep Dive
    - How to tell if a calculation is expensive?
  - Resetting all state when a prop changes
  - Adjusting some state when a prop changes

Effects are an escape hatch from the React paradigm. They let you “step outside” of React and synchronize your components with some external system like a non-React widget, network, or the browser DOM. If there is no external system involved (for example, if you want to update a component’s state when some props or state change), you shouldn’t need an Effect. Removing unnecessary Effects will make your code easier to follow, faster to run, and less error-prone.

There are two common cases in which you don’t need Effects:

You do need Effects to synchronize with external systems. For example, you can write an Effect that keeps a jQuery widget synchronized with the React state. You can also fetch data with Effects: for example, you can synchronize the search results with the current search query. Keep in mind that modern frameworks provide more efficient built-in data fetching mechanisms than writing Effects directly in your components.

To help you gain the right intuition, let’s look at some common concrete examples!

Suppose you have a component with two state variables: firstName and lastName. You want to calculate a fullName from them by concatenating them. Moreover, you’d like fullName to update whenever firstName or lastName change. Your first instinct might be to add a fullName state variable and update it in an Effect:

This is more complicated than necessary. It is inefficient too: it does an entire render pass with a stale value for fullName, then immediately re-renders with the updated value. Remove the state variable and the Effect:

When something can be calculated from the existing props or state, don’t put it in state. Instead, calculate it during rendering. This makes your code faster (you avoid the extra “cascading” updates), simpler (you remove some code), and less error-prone (you avoid bugs caused by different state variables getting out of sync with each other). If this approach feels new to you, Thinking in React explains what should go into state.

This component computes visibleTodos by taking the todos it receives by props and filtering them according to the filter prop. You might feel tempted to store the result in state and update it from an Effect:

Like in the earlier example, this is both unnecessary and inefficient. First, remove the state and the Effect:

Usually, this code is fine! But maybe getFilteredTodos() is slow or you have a lot of todos. In that case you don’t want to recalculate getFilteredTodos() if some unrelated 

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
function Form() {  const [firstName, setFirstName] = useState('Taylor');  const [lastName, setLastName] = useState('Swift');  // 🔴 Avoid: redundant state and unnecessary Effect  const [fullName, setFullName] = useState('');  useEffect(() => {    setFullName(firstName + ' ' + lastName);  }, [firstName, lastName]);  // ...}
```

Example 2 (javascript):
```javascript
function Form() {  const [firstName, setFirstName] = useState('Taylor');  const [lastName, setLastName] = useState('Swift');  // ✅ Good: calculated during rendering  const fullName = firstName + ' ' + lastName;  // ...}
```

Example 3 (javascript):
```javascript
function TodoList({ todos, filter }) {  const [newTodo, setNewTodo] = useState('');  // 🔴 Avoid: redundant state and unnecessary Effect  const [visibleTodos, setVisibleTodos] = useState([]);  useEffect(() => {    setVisibleTodos(getFilteredTodos(todos, filter));  }, [todos, filter]);  // ...}
```

Example 4 (javascript):
```javascript
function TodoList({ todos, filter }) {  const [newTodo, setNewTodo] = useState('');  // ✅ This is fine if getFilteredTodos() is not slow.  const visibleTodos = getFilteredTodos(todos, filter);  // ...}
```

---

## Your First Component

**URL:** https://react.dev/learn/your-first-component#defining-a-component

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## <style>

**URL:** https://react.dev/reference/react-dom/components/style

**Contents:**
- <style>
- Reference
  - <style>
    - Props
    - Special rendering behavior
- Usage
  - Rendering an inline CSS stylesheet

The built-in browser <style> component lets you add inline CSS stylesheets to your document.

To add inline styles to your document, render the built-in browser <style> component. You can render <style> from any component and React will in certain cases place the corresponding DOM element in the document head and de-duplicate identical styles.

See more examples below.

<style> supports all common element props.

Props that are not recommended for use with React:

React can move <style> components to the document’s <head>, de-duplicate identical stylesheets, and suspend while the stylesheet is loading.

To opt into this behavior, provide the href and precedence props. React will de-duplicate styles if they have the same href. The precedence prop tells React where to rank the <style> DOM node relative to others in the document <head>, which determines which stylesheet can override the other.

This special treatment comes with three caveats:

If a component depends on certain CSS styles in order to be displayed correctly, you can render an inline stylesheet within the component.

The href prop should uniquely identify the stylesheet, because React will de-duplicate stylesheets that have the same href. If you supply a precedence prop, React will reorder inline stylesheets based on the order these values appear in the component tree.

Inline stylesheets will not trigger Suspense boundaries while they’re loading. Even if they load async resources like fonts or images.

**Examples:**

Example 1 (unknown):
```unknown
<style>{` p { color: red; } `}</style>
```

Example 2 (unknown):
```unknown
<style>{` p { color: red; } `}</style>
```

---

## Your First Component

**URL:** https://react.dev/learn/your-first-component#undefined

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## <textarea>

**URL:** https://react.dev/reference/react-dom/components/textarea

**Contents:**
- <textarea>
- Reference
  - <textarea>
    - Props
    - Caveats
- Usage
  - Displaying a text area
  - Providing a label for a text area
  - Providing an initial value for a text area
  - Pitfall

The built-in browser <textarea> component lets you render a multiline text input.

To display a text area, render the built-in browser <textarea> component.

See more examples below.

<textarea> supports all common element props.

You can make a text area controlled by passing a value prop:

When you pass value, you must also pass an onChange handler that updates the passed value.

If your <textarea> is uncontrolled, you may pass the defaultValue prop instead:

These <textarea> props are relevant both for uncontrolled and controlled text areas:

Render <textarea> to display a text area. You can specify its default size with the rows and cols attributes, but by default the user will be able to resize it. To disable resizing, you can specify resize: none in the CSS.

Typically, you will place every <textarea> inside a <label> tag. This tells the browser that this label is associated with that text area. When the user clicks the label, the browser will focus the text area. It’s also essential for accessibility: a screen reader will announce the label caption when the user focuses the text area.

If you can’t nest <textarea> into a <label>, associate them by passing the same ID to <textarea id> and <label htmlFor>. To avoid conflicts between instances of one component, generate such an ID with useId.

You can optionally specify the initial value for the text area. Pass it as the defaultValue string.

Unlike in HTML, passing initial text like <textarea>Some content</textarea> is not supported.

Add a <form> around your textarea with a <button type="submit"> inside. It will call your <form onSubmit> event handler. By default, the browser will send the form data to the current URL and refresh the page. You can override that behavior by calling e.preventDefault(). Read the form data with new FormData(e.target).

Give a name to your <textarea>, for example <textarea name="postContent" />. The name you specified will be used as a key in the form data, for example { postContent: "Your post" }.

By default, any <button> inside a <form> will submit it. This can be surprising! If you have your own custom Button React component, consider returning <button type="button"> instead of <button>. Then, to be explicit, use <button type="submit"> for buttons that are supposed to submit the form.

A text area like <textarea /> is uncontrolled. Even if you pass an initial value like <textarea defaultValue="Initial text" />, your JSX only specifies the initial value, not the value 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<textarea />
```

Example 2 (unknown):
```unknown
<textarea name="postContent" />
```

Example 3 (javascript):
```javascript
function NewPost() {  const [postContent, setPostContent] = useState(''); // Declare a state variable...  // ...  return (    <textarea      value={postContent} // ...force the input's value to match the state variable...      onChange={e => setPostContent(e.target.value)} // ... and update the state variable on any edits!    />  );}
```

Example 4 (unknown):
```unknown
// 🔴 Bug: controlled text area with no onChange handler<textarea value={something} />
```

---

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory#recap

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

## Your First Component

**URL:** https://react.dev/learn/your-first-component#using-a-component

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## Your First Component

**URL:** https://react.dev/learn/your-first-component#step-3-add-markup

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## <input>

**URL:** https://react.dev/reference/react-dom/components/input#controlling-an-input-with-a-state-variable

**Contents:**
- <input>
- Reference
  - <input>
    - Props
    - Caveats
- Usage
  - Displaying inputs of different types
  - Providing a label for an input
  - Providing an initial value for an input
  - Reading the input values when submitting a form

The built-in browser <input> component lets you render different kinds of form inputs.

To display an input, render the built-in browser <input> component.

See more examples below.

<input> supports all common element props.

You can make an input controlled by passing one of these props:

When you pass either of them, you must also pass an onChange handler that updates the passed value.

These <input> props are only relevant for uncontrolled inputs:

These <input> props are relevant both for uncontrolled and controlled inputs:

To display an input, render an <input> component. By default, it will be a text input. You can pass type="checkbox" for a checkbox, type="radio" for a radio button, or one of the other input types.

Typically, you will place every <input> inside a <label> tag. This tells the browser that this label is associated with that input. When the user clicks the label, the browser will automatically focus the input. It’s also essential for accessibility: a screen reader will announce the label caption when the user focuses the associated input.

If you can’t nest <input> into a <label>, associate them by passing the same ID to <input id> and <label htmlFor>. To avoid conflicts between multiple instances of one component, generate such an ID with useId.

You can optionally specify the initial value for any input. Pass it as the defaultValue string for text inputs. Checkboxes and radio buttons should specify the initial value with the defaultChecked boolean instead.

Add a <form> around your inputs with a <button type="submit"> inside. It will call your <form onSubmit> event handler. By default, the browser will send the form data to the current URL and refresh the page. You can override that behavior by calling e.preventDefault(). Read the form data with new FormData(e.target).

Give a name to every <input>, for example <input name="firstName" defaultValue="Taylor" />. The name you specified will be used as a key in the form data, for example { firstName: "Taylor" }.

By default, a <button> inside a <form> without a type attribute will submit it. This can be surprising! If you have your own custom Button React component, consider using <button type="button"> instead of <button> (with no type). Then, to be explicit, use <button type="submit"> for buttons that are supposed to submit the form.

An input like <input /> is uncontrolled. Even if you pass an initial value like <input defaultValue="Initial text" />, your JSX only specifies the init

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<input name="myInput" />
```

Example 2 (javascript):
```javascript
function Form() {  const [firstName, setFirstName] = useState(''); // Declare a state variable...  // ...  return (    <input      value={firstName} // ...force the input's value to match the state variable...      onChange={e => setFirstName(e.target.value)} // ... and update the state variable on any edits!    />  );}
```

Example 3 (javascript):
```javascript
function Form() {  const [firstName, setFirstName] = useState('');  return (    <>      <label>        First name:        <input value={firstName} onChange={e => setFirstName(e.target.value)} />      </label>      {firstName !== '' && <p>Your name is {firstName}.</p>}      ...
```

Example 4 (javascript):
```javascript
function Form() {  // ...  const [age, setAge] = useState('');  const ageAsNumber = Number(age);  return (    <>      <label>        Age:        <input          value={age}          onChange={e => setAge(e.target.value)}          type="number"        />        <button onClick={() => setAge(ageAsNumber + 10)}>          Add 10 years        </button>
```

---

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui#keeping-components-pure

**Contents:**
- Describing the UI
  - In this chapter
- Your first component
- Ready to learn this topic?
- Importing and exporting components
- Ready to learn this topic?
- Writing markup with JSX
- Ready to learn this topic?
- JavaScript in JSX with curly braces
- Ready to learn this topic?

React is a JavaScript library for rendering user interfaces (UI). UI is built from small units like buttons, text, and images. React lets you combine them into reusable, nestable components. From web sites to phone apps, everything on the screen can be broken down into components. In this chapter, you’ll learn to create, customize, and conditionally display React components.

React applications are built from isolated pieces of UI called components. A React component is a JavaScript function that you can sprinkle with markup. Components can be as small as a button, or as large as an entire page. Here is a Gallery component rendering three Profile components:

Read Your First Component to learn how to declare and use React components.

You can declare many components in one file, but large files can get difficult to navigate. To solve this, you can export a component into its own file, and then import that component from another file:

Read Importing and Exporting Components to learn how to split components into their own files.

Each React component is a JavaScript function that may contain some markup that React renders into the browser. React components use a syntax extension called JSX to represent that markup. JSX looks a lot like HTML, but it is a bit stricter and can display dynamic information.

If we paste existing HTML markup into a React component, it won’t always work:

If you have existing HTML like this, you can fix it using a converter:

Read Writing Markup with JSX to learn how to write valid JSX.

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to “open a window” to JavaScript:

Read JavaScript in JSX with Curly Braces to learn how to access JavaScript data from JSX.

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, functions, and even JSX!

Read Passing Props to a Component to learn how to pass and read props.

Your components will often need to display different things depending on different conditions. In React, you can conditionally render JSX using JavaScript syntax like if statement

*[Content truncated]*

---

## Keeping Components Pure

**URL:** https://react.dev/learn/keeping-components-pure

**Contents:**
- Keeping Components Pure
  - You will learn
- Purity: Components as formulas
- Side Effects: (un)intended consequences
      - Deep Dive
    - Detecting impure calculations with StrictMode
  - Local mutation: Your component’s little secret
- Where you can cause side effects
      - Deep Dive
    - Why does React care about purity?

Some JavaScript functions are pure. Pure functions only perform a calculation and nothing more. By strictly only writing your components as pure functions, you can avoid an entire class of baffling bugs and unpredictable behavior as your codebase grows. To get these benefits, though, there are a few rules you must follow.

In computer science (and especially the world of functional programming), a pure function is a function with the following characteristics:

You might already be familiar with one example of pure functions: formulas in math.

Consider this math formula: y = 2x.

If x = 2 then y = 4. Always.

If x = 3 then y = 6. Always.

If x = 3, y won’t sometimes be 9 or –1 or 2.5 depending on the time of day or the state of the stock market.

If y = 2x and x = 3, y will always be 6.

If we made this into a JavaScript function, it would look like this:

In the above example, double is a pure function. If you pass it 3, it will return 6. Always.

React is designed around this concept. React assumes that every component you write is a pure function. This means that React components you write must always return the same JSX given the same inputs:

When you pass drinkers={2} to Recipe, it will return JSX containing 2 cups of water. Always.

If you pass drinkers={4}, it will return JSX containing 4 cups of water. Always.

Just like a math formula.

You could think of your components as recipes: if you follow them and don’t introduce new ingredients during the cooking process, you will get the same dish every time. That “dish” is the JSX that the component serves to React to render.

Illustrated by Rachel Lee Nabors

React’s rendering process must always be pure. Components should only return their JSX, and not change any objects or variables that existed before rendering—that would make them impure!

Here is a component that breaks this rule:

This component is reading and writing a guest variable declared outside of it. This means that calling this component multiple times will produce different JSX! And what’s more, if other components read guest, they will produce different JSX, too, depending on when they were rendered! That’s not predictable.

Going back to our formula y = 2x, now even if x = 2, we cannot trust that y = 4. Our tests could fail, our users would be baffled, planes would fall out of the sky—you can see how this would lead to confusing bugs!

You can fix this component by passing guest as a prop instead:

Now your component is pure, as the

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
function double(number) {  return 2 * number;}
```

---

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component#challenges

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## Importing and Exporting Components

**URL:** https://react.dev/learn/importing-and-exporting-components

**Contents:**
- Importing and Exporting Components
  - You will learn
- The root component file
- Exporting and importing a component
  - Note
      - Deep Dive
    - Default vs named exports
- Exporting and importing multiple components from the same file
  - Note
- Recap

The magic of components lies in their reusability: you can create components that are composed of other components. But as you nest more and more components, it often makes sense to start splitting them into different files. This lets you keep your files easy to scan and reuse components in more places.

In Your First Component, you made a Profile component and a Gallery component that renders it:

These currently live in a root component file, named App.js in this example. Depending on your setup, your root component could be in another file, though. If you use a framework with file-based routing, such as Next.js, your root component will be different for every page.

What if you want to change the landing screen in the future and put a list of science books there? Or place all the profiles somewhere else? It makes sense to move Gallery and Profile out of the root component file. This will make them more modular and reusable in other files. You can move a component in three steps:

Here both Profile and Gallery have been moved out of App.js into a new file called Gallery.js. Now you can change App.js to import Gallery from Gallery.js:

Notice how this example is broken down into two component files now:

You may encounter files that leave off the .js file extension like so:

Either './Gallery.js' or './Gallery' will work with React, though the former is closer to how native ES Modules work.

There are two primary ways to export values with JavaScript: default exports and named exports. So far, our examples have only used default exports. But you can use one or both of them in the same file. A file can have no more than one default export, but it can have as many named exports as you like.

How you export your component dictates how you must import it. You will get an error if you try to import a default export the same way you would a named export! This chart can help you keep track:

When you write a default import, you can put any name you want after import. For example, you could write import Banana from './Button.js' instead and it would still provide you with the same default export. In contrast, with named imports, the name has to match on both sides. That’s why they are called named imports!

People often use default exports if the file exports only one component, and use named exports if it exports multiple components and values. Regardless of which coding style you prefer, always give meaningful names to your component functions and the files tha

*[Content truncated]*

**Examples:**

Example 1 (python):
```python
import Gallery from './Gallery';
```

Example 2 (unknown):
```unknown
export function Profile() {  // ...}
```

Example 3 (python):
```python
import { Profile } from './Gallery.js';
```

Example 4 (unknown):
```unknown
export default function App() {  return <Profile />;}
```

---

## Your First Component

**URL:** https://react.dev/learn/your-first-component#components-ui-building-blocks

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## Quick Start

**URL:** https://react.dev/learn#writing-markup-with-jsx

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

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component#how-props-change-over-time

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component#undefined

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## Your First Component

**URL:** https://react.dev/learn/your-first-component#what-the-browser-sees

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component#forwarding-props-with-the-jsx-spread-syntax

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component#specifying-a-default-value-for-a-prop

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## <title>

**URL:** https://react.dev/reference/react-dom/components/title

**Contents:**
- <title>
- Reference
  - <title>
    - Props
    - Special rendering behavior
  - Pitfall
- Usage
  - Set the document title
  - Use variables in the title

The built-in browser <title> component lets you specify the title of the document.

To specify the title of the document, render the built-in browser <title> component. You can render <title> from any component and React will always place the corresponding DOM element in the document head.

See more examples below.

<title> supports all common element props.

React will always place the DOM element corresponding to the <title> component within the document’s <head>, regardless of where in the React tree it is rendered. The <head> is the only valid place for <title> to exist within the DOM, yet it’s convenient and keeps things composable if a component representing a specific page can render its <title> itself.

There are two exception to this:

Only render a single <title> at a time. If more than one component renders a <title> tag at the same time, React will place all of those titles in the document head. When this happens, the behavior of browsers and search engines is undefined.

Render the <title> component from any component with text as its children. React will put a <title> DOM node in the document <head>.

The children of the <title> component must be a single string of text. (Or a single number or a single object with a toString method.) It might not be obvious, but using JSX curly braces like this:

… actually causes the <title> component to get a two-element array as its children (the string "Results page" and the value of pageNumber). This will cause an error. Instead, use string interpolation to pass <title> a single string:

**Examples:**

Example 1 (unknown):
```unknown
<title>My Blog</title>
```

Example 2 (unknown):
```unknown
<title>My Blog</title>
```

Example 3 (unknown):
```unknown
<title>Results page {pageNumber}</title> // 🔴 Problem: This is not a single string
```

Example 4 (unknown):
```unknown
<title>{`Results page ${pageNumber}`}</title>
```

---

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui#your-first-component

**Contents:**
- Describing the UI
  - In this chapter
- Your first component
- Ready to learn this topic?
- Importing and exporting components
- Ready to learn this topic?
- Writing markup with JSX
- Ready to learn this topic?
- JavaScript in JSX with curly braces
- Ready to learn this topic?

React is a JavaScript library for rendering user interfaces (UI). UI is built from small units like buttons, text, and images. React lets you combine them into reusable, nestable components. From web sites to phone apps, everything on the screen can be broken down into components. In this chapter, you’ll learn to create, customize, and conditionally display React components.

React applications are built from isolated pieces of UI called components. A React component is a JavaScript function that you can sprinkle with markup. Components can be as small as a button, or as large as an entire page. Here is a Gallery component rendering three Profile components:

Read Your First Component to learn how to declare and use React components.

You can declare many components in one file, but large files can get difficult to navigate. To solve this, you can export a component into its own file, and then import that component from another file:

Read Importing and Exporting Components to learn how to split components into their own files.

Each React component is a JavaScript function that may contain some markup that React renders into the browser. React components use a syntax extension called JSX to represent that markup. JSX looks a lot like HTML, but it is a bit stricter and can display dynamic information.

If we paste existing HTML markup into a React component, it won’t always work:

If you have existing HTML like this, you can fix it using a converter:

Read Writing Markup with JSX to learn how to write valid JSX.

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to “open a window” to JavaScript:

Read JavaScript in JSX with Curly Braces to learn how to access JavaScript data from JSX.

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, functions, and even JSX!

Read Passing Props to a Component to learn how to pass and read props.

Your components will often need to display different things depending on different conditions. In React, you can conditionally render JSX using JavaScript syntax like if statement

*[Content truncated]*

---

## JavaScript in JSX with Curly Braces

**URL:** https://react.dev/learn/javascript-in-jsx-with-curly-braces

**Contents:**
- JavaScript in JSX with Curly Braces
  - You will learn
- Passing strings with quotes
- Using curly braces: A window into the JavaScript world
  - Where to use curly braces
- Using “double curlies”: CSS and other objects in JSX
  - Pitfall
- More fun with JavaScript objects and curly braces
- Recap
- Try out some challenges

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to open a window to JavaScript.

When you want to pass a string attribute to JSX, you put it in single or double quotes:

Here, "https://i.imgur.com/7vQD0fPs.jpg" and "Gregorio Y. Zara" are being passed as strings.

But what if you want to dynamically specify the src or alt text? You could use a value from JavaScript by replacing " and " with { and }:

Notice the difference between className="avatar", which specifies an "avatar" CSS class name that makes the image round, and src={avatar} that reads the value of the JavaScript variable called avatar. That’s because curly braces let you work with JavaScript right there in your markup!

JSX is a special way of writing JavaScript. That means it’s possible to use JavaScript inside it—with curly braces { }. The example below first declares a name for the scientist, name, then embeds it with curly braces inside the <h1>:

Try changing the name’s value from 'Gregorio Y. Zara' to 'Hedy Lamarr'. See how the list title changes?

Any JavaScript expression will work between curly braces, including function calls like formatDate():

You can only use curly braces in two ways inside JSX:

In addition to strings, numbers, and other JavaScript expressions, you can even pass objects in JSX. Objects are also denoted with curly braces, like { name: "Hedy Lamarr", inventions: 5 }. Therefore, to pass a JS object in JSX, you must wrap the object in another pair of curly braces: person={{ name: "Hedy Lamarr", inventions: 5 }}.

You may see this with inline CSS styles in JSX. React does not require you to use inline styles (CSS classes work great for most cases). But when you need an inline style, you pass an object to the style attribute:

Try changing the values of backgroundColor and color.

You can really see the JavaScript object inside the curly braces when you write it like this:

The next time you see {{ and }} in JSX, know that it’s nothing more than an object inside the JSX curlies!

Inline style properties are written in camelCase. For example, HTML <ul style="background-color: black"> would be written as <ul style={{ backgroundColor: 'black' }}> in your component.

You can move several expressions into one object, and reference them in your JS

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<ul style={  {    backgroundColor: 'black',    color: 'pink'  }}>
```

Example 2 (javascript):
```javascript
const person = {  name: 'Gregorio Y. Zara',  theme: {    backgroundColor: 'black',    color: 'pink'  }};
```

Example 3 (unknown):
```unknown
<div style={person.theme}>  <h1>{person.name}'s Todos</h1>
```

---

## Adding Interactivity

**URL:** https://react.dev/learn/adding-interactivity#state-as-a-snapshot

**Contents:**
- Adding Interactivity
  - In this chapter
- Responding to events
- Ready to learn this topic?
- State: a component’s memory
- Ready to learn this topic?
- Render and commit
- Ready to learn this topic?
- State as a snapshot
- Ready to learn this topic?

Some things on the screen update in response to user input. For example, clicking an image gallery switches the active image. In React, data that changes over time is called state. You can add state to any component, and update it as needed. In this chapter, you’ll learn how to write components that handle interactions, update their state, and display different output over time.

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to user interactions like clicking, hovering, focusing on form inputs, and so on.

Built-in components like <button> only support built-in browser events like onClick. However, you can also create your own components, and give their event handler props any application-specific names that you like.

Read Responding to Events to learn how to add event handlers.

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” puts a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

You can add state to a component with a useState Hook. Hooks are special functions that let your components use React features (state is one of those features). The useState Hook lets you declare a state variable. It takes the initial state and returns a pair of values: the current state, and a state setter function that lets you update it.

Here is how an image gallery uses and updates state on click:

Read State: A Component’s Memory to learn how to remember a value and update it on interaction.

Before your components are displayed on the screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

Read Render and Commit to learn the lifecycle of a UI update.

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already ha

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

Example 2 (unknown):
```unknown
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

Example 3 (unknown):
```unknown
console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0
```

---

## Adding Interactivity

**URL:** https://react.dev/learn/adding-interactivity#updating-objects-in-state

**Contents:**
- Adding Interactivity
  - In this chapter
- Responding to events
- Ready to learn this topic?
- State: a component’s memory
- Ready to learn this topic?
- Render and commit
- Ready to learn this topic?
- State as a snapshot
- Ready to learn this topic?

Some things on the screen update in response to user input. For example, clicking an image gallery switches the active image. In React, data that changes over time is called state. You can add state to any component, and update it as needed. In this chapter, you’ll learn how to write components that handle interactions, update their state, and display different output over time.

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to user interactions like clicking, hovering, focusing on form inputs, and so on.

Built-in components like <button> only support built-in browser events like onClick. However, you can also create your own components, and give their event handler props any application-specific names that you like.

Read Responding to Events to learn how to add event handlers.

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” puts a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

You can add state to a component with a useState Hook. Hooks are special functions that let your components use React features (state is one of those features). The useState Hook lets you declare a state variable. It takes the initial state and returns a pair of values: the current state, and a state setter function that lets you update it.

Here is how an image gallery uses and updates state on click:

Read State: A Component’s Memory to learn how to remember a value and update it on interaction.

Before your components are displayed on the screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

Read Render and Commit to learn the lifecycle of a UI update.

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already ha

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

Example 2 (unknown):
```unknown
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

Example 3 (unknown):
```unknown
console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0
```

---

## <option>

**URL:** https://react.dev/reference/react-dom/components/option

**Contents:**
- <option>
- Reference
  - <option>
    - Props
    - Caveats
- Usage
  - Displaying a select box with options

The built-in browser <option> component lets you render an option inside a <select> box.

The built-in browser <option> component lets you render an option inside a <select> box.

See more examples below.

<option> supports all common element props.

Additionally, <option> supports these props:

Render a <select> with a list of <option> components inside to display a select box. Give each <option> a value representing the data to be submitted with the form.

Read more about displaying a <select> with a list of <option> components.

**Examples:**

Example 1 (unknown):
```unknown
<select>  <option value="someOption">Some option</option>  <option value="otherOption">Other option</option></select>
```

Example 2 (unknown):
```unknown
<select>  <option value="someOption">Some option</option>  <option value="otherOption">Other option</option></select>
```

---

## Quick Start

**URL:** https://react.dev/learn#components

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

## Removing Effect Dependencies

**URL:** https://react.dev/learn/removing-effect-dependencies#move-dynamic-objects-and-functions-inside-your-effect

**Contents:**
- Removing Effect Dependencies
  - You will learn
- Dependencies should match the code
  - To remove a dependency, prove that it’s not a dependency
  - To change the dependencies, change the code
  - Pitfall
      - Deep Dive
    - Why is suppressing the dependency linter so dangerous?
- Removing unnecessary dependencies
  - Should this code move to an event handler?

When you write an Effect, the linter will verify that you’ve included every reactive value (like props and state) that the Effect reads in the list of your Effect’s dependencies. This ensures that your Effect remains synchronized with the latest props and state of your component. Unnecessary dependencies may cause your Effect to run too often, or even create an infinite loop. Follow this guide to review and remove unnecessary dependencies from your Effects.

When you write an Effect, you first specify how to start and stop whatever you want your Effect to be doing:

Then, if you leave the Effect dependencies empty ([]), the linter will suggest the correct dependencies:

Fill them in according to what the linter says:

Effects “react” to reactive values. Since roomId is a reactive value (it can change due to a re-render), the linter verifies that you’ve specified it as a dependency. If roomId receives a different value, React will re-synchronize your Effect. This ensures that the chat stays connected to the selected room and “reacts” to the dropdown:

Notice that you can’t “choose” the dependencies of your Effect. Every reactive value used by your Effect’s code must be declared in your dependency list. The dependency list is determined by the surrounding code:

Reactive values include props and all variables and functions declared directly inside of your component. Since roomId is a reactive value, you can’t remove it from the dependency list. The linter wouldn’t allow it:

And the linter would be right! Since roomId may change over time, this would introduce a bug in your code.

To remove a dependency, “prove” to the linter that it doesn’t need to be a dependency. For example, you can move roomId out of your component to prove that it’s not reactive and won’t change on re-renders:

Now that roomId is not a reactive value (and can’t change on a re-render), it doesn’t need to be a dependency:

This is why you could now specify an empty ([]) dependency list. Your Effect really doesn’t depend on any reactive value anymore, so it really doesn’t need to re-run when any of the component’s props or state change.

You might have noticed a pattern in your workflow:

The last part is important. If you want to change the dependencies, change the surrounding code first. You can think of the dependency list as a list of all the reactive values used by your Effect’s code. You don’t choose what to put on that list. The list describes your code. To change the dependency li

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const serverUrl = 'https://localhost:1234';function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => connection.disconnect();  	// ...}
```

Example 2 (javascript):
```javascript
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]); // ✅ All dependencies declared  // ...}
```

Example 3 (javascript):
```javascript
const serverUrl = 'https://localhost:1234';function ChatRoom({ roomId }) { // This is a reactive value  useEffect(() => {    const connection = createConnection(serverUrl, roomId); // This Effect reads that reactive value    connection.connect();    return () => connection.disconnect();  }, [roomId]); // ✅ So you must specify that reactive value as a dependency of your Effect  // ...}
```

Example 4 (javascript):
```javascript
const serverUrl = 'https://localhost:1234';function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => connection.disconnect();  }, []); // 🔴 React Hook useEffect has a missing dependency: 'roomId'  // ...}
```

---

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component#step-2-read-props-inside-the-child-component

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## React DOM Components

**URL:** https://react.dev/reference/react-dom/components

**Contents:**
- React DOM Components
- Common components
- Form components
- Resource and Metadata Components
- All HTML components
  - Note
  - Custom HTML elements
    - Setting values on custom elements
    - Listening for events on custom elements
  - Note

React supports all of the browser built-in HTML and SVG components.

All of the built-in browser components support some props and events.

This includes React-specific props like ref and dangerouslySetInnerHTML.

These built-in browser components accept user input:

They are special in React because passing the value prop to them makes them controlled.

These built-in browser components let you load external resources or annotate the document with metadata:

They are special in React because React can render them into the document head, suspend while resources are loading, and enact other behaviors that are described on the reference page for each specific component.

React supports all built-in browser HTML components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing HTML to JSX with an online converter.

If you render a tag with a dash, like <my-element>, React will assume you want to render a custom HTML element.

If you render a built-in browser HTML element with an is attribute, it will also be treated as a custom element.

Custom elements have two methods of passing data into them:

By default, React will pass values bound in JSX as attributes:

Non-string JavaScript values passed to custom elements will be serialized by default:

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

A common pattern when using custom elements is that they may dispatch CustomEvents rather than accept a function to call when an event occur. You can listen for these events using an on prefix when binding to the event via JSX.

Events are case-sensitive and support dashes (-). Preserve the casing of the event and include all dashes when listening for custom element’s events:

React supports all built-in browser SVG components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing SVG to JSX with an online converter.

Namespaced attributes also have to be written without the colon:

**Examples:**

Example 1 (unknown):
```unknown
<my-element value="Hello, world!"></my-element>
```

Example 2 (unknown):
```unknown
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`<my-element value={[1,2,3]}></my-element>
```

Example 3 (unknown):
```unknown
// Listens for `say-hi` events<my-element onsay-hi={console.log}></my-element>// Listens for `sayHi` events<my-element onsayHi={console.log}></my-element>
```

---

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui#passing-props-to-a-component

**Contents:**
- Describing the UI
  - In this chapter
- Your first component
- Ready to learn this topic?
- Importing and exporting components
- Ready to learn this topic?
- Writing markup with JSX
- Ready to learn this topic?
- JavaScript in JSX with curly braces
- Ready to learn this topic?

React is a JavaScript library for rendering user interfaces (UI). UI is built from small units like buttons, text, and images. React lets you combine them into reusable, nestable components. From web sites to phone apps, everything on the screen can be broken down into components. In this chapter, you’ll learn to create, customize, and conditionally display React components.

React applications are built from isolated pieces of UI called components. A React component is a JavaScript function that you can sprinkle with markup. Components can be as small as a button, or as large as an entire page. Here is a Gallery component rendering three Profile components:

Read Your First Component to learn how to declare and use React components.

You can declare many components in one file, but large files can get difficult to navigate. To solve this, you can export a component into its own file, and then import that component from another file:

Read Importing and Exporting Components to learn how to split components into their own files.

Each React component is a JavaScript function that may contain some markup that React renders into the browser. React components use a syntax extension called JSX to represent that markup. JSX looks a lot like HTML, but it is a bit stricter and can display dynamic information.

If we paste existing HTML markup into a React component, it won’t always work:

If you have existing HTML like this, you can fix it using a converter:

Read Writing Markup with JSX to learn how to write valid JSX.

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to “open a window” to JavaScript:

Read JavaScript in JSX with Curly Braces to learn how to access JavaScript data from JSX.

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, functions, and even JSX!

Read Passing Props to a Component to learn how to pass and read props.

Your components will often need to display different things depending on different conditions. In React, you can conditionally render JSX using JavaScript syntax like if statement

*[Content truncated]*

---

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory#how-does-react-know-which-state-to-return

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

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory

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

## Your First Component

**URL:** https://react.dev/learn/your-first-component#nesting-and-organizing-components

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## memo

**URL:** https://react.dev/reference/react/memo

**Contents:**
- memo
  - Note
- Reference
  - memo(Component, arePropsEqual?)
    - Parameters
    - Returns
- Usage
  - Skipping re-rendering when props are unchanged
  - Note
      - Deep Dive

memo lets you skip re-rendering a component when its props are unchanged.

React Compiler automatically applies the equivalent of memo to all components, reducing the need for manual memoization. You can use the compiler to handle component memoization automatically.

Wrap a component in memo to get a memoized version of that component. This memoized version of your component will usually not be re-rendered when its parent component is re-rendered as long as its props have not changed. But React may still re-render it: memoization is a performance optimization, not a guarantee.

See more examples below.

Component: The component that you want to memoize. The memo does not modify this component, but returns a new, memoized component instead. Any valid React component, including functions and forwardRef components, is accepted.

optional arePropsEqual: A function that accepts two arguments: the component’s previous props, and its new props. It should return true if the old and new props are equal: that is, if the component will render the same output and behave in the same way with the new props as with the old. Otherwise it should return false. Usually, you will not specify this function. By default, React will compare each prop with Object.is.

memo returns a new React component. It behaves the same as the component provided to memo except that React will not always re-render it when its parent is being re-rendered unless its props have changed.

React normally re-renders a component whenever its parent re-renders. With memo, you can create a component that React will not re-render when its parent re-renders so long as its new props are the same as the old props. Such a component is said to be memoized.

To memoize a component, wrap it in memo and use the value that it returns in place of your original component:

A React component should always have pure rendering logic. This means that it must return the same output if its props, state, and context haven’t changed. By using memo, you are telling React that your component complies with this requirement, so React doesn’t need to re-render as long as its props haven’t changed. Even with memo, your component will re-render if its own state changes or if a context that it’s using changes.

In this example, notice that the Greeting component re-renders whenever name is changed (because that’s one of its props), but not when address is changed (because it’s not passed to Greeting as a prop):

You should only re

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const MemoizedComponent = memo(SomeComponent, arePropsEqual?)
```

Example 2 (python):
```python
import { memo } from 'react';const SomeComponent = memo(function SomeComponent(props) {  // ...});
```

Example 3 (javascript):
```javascript
const Greeting = memo(function Greeting({ name }) {  return <h1>Hello, {name}!</h1>;});export default Greeting;
```

Example 4 (javascript):
```javascript
function Page() {  const [name, setName] = useState('Taylor');  const [age, setAge] = useState(42);  const person = useMemo(    () => ({ name, age }),    [name, age]  );  return <Profile person={person} />;}const Profile = memo(function Profile({ person }) {  // ...});
```

---

## Your First Component

**URL:** https://react.dev/learn/your-first-component#export-the-component

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## <link>

**URL:** https://react.dev/reference/react-dom/components/link

**Contents:**
- <link>
- Reference
  - <link>
    - Props
    - Special rendering behavior
    - Special behavior for stylesheets
- Usage
  - Linking to related resources
  - Linking to a stylesheet
  - Note

The built-in browser <link> component lets you use external resources such as stylesheets or annotate the document with link metadata.

To link to external resources such as stylesheets, fonts, and icons, or to annotate the document with link metadata, render the built-in browser <link> component. You can render <link> from any component and React will in most cases place the corresponding DOM element in the document head.

See more examples below.

<link> supports all common element props.

These props apply when rel="stylesheet":

These props apply when rel="stylesheet" but disable React’s special treatment of stylesheets:

These props apply when rel="preload" or rel="modulepreload":

These props apply when rel="icon" or rel="apple-touch-icon":

These props apply in all cases:

Props that are not recommended for use with React:

React will always place the DOM element corresponding to the <link> component within the document’s <head>, regardless of where in the React tree it is rendered. The <head> is the only valid place for <link> to exist within the DOM, yet it’s convenient and keeps things composable if a component representing a specific page can render <link> components itself.

There are a few exceptions to this:

In addition, if the <link> is to a stylesheet (namely, it has rel="stylesheet" in its props), React treats it specially in the following ways:

There are two exception to this special behavior:

This special treatment comes with two caveats:

You can annotate the document with links to related resources such as an icon, canonical URL, or pingback. React will place this metadata within the document <head> regardless of where in the React tree it is rendered.

If a component depends on a certain stylesheet in order to be displayed correctly, you can render a link to that stylesheet within the component. Your component will suspend while the stylesheet is loading. You must supply the precedence prop, which tells React where to place this stylesheet relative to others — stylesheets with higher precedence can override those with lower precedence.

When you want to use a stylesheet, it can be beneficial to call the preinit function. Calling this function may allow the browser to start fetching the stylesheet earlier than if you just render a <link> component, for example by sending an HTTP Early Hints response.

Stylesheets can conflict with each other, and when they do, the browser goes with the one that comes later in the document. React let

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<link rel="icon" href="favicon.ico" />
```

Example 2 (unknown):
```unknown
<link rel="icon" href="favicon.ico" />
```

Example 3 (unknown):
```unknown
<section itemScope>  <h3>Annotating specific items</h3>  <link itemProp="author" href="http://example.com/" />  <p>...</p></section>
```

---

## React DOM Components

**URL:** https://react.dev/reference/react-dom/components#custom-element-events

**Contents:**
- React DOM Components
- Common components
- Form components
- Resource and Metadata Components
- All HTML components
  - Note
  - Custom HTML elements
    - Setting values on custom elements
    - Listening for events on custom elements
  - Note

React supports all of the browser built-in HTML and SVG components.

All of the built-in browser components support some props and events.

This includes React-specific props like ref and dangerouslySetInnerHTML.

These built-in browser components accept user input:

They are special in React because passing the value prop to them makes them controlled.

These built-in browser components let you load external resources or annotate the document with metadata:

They are special in React because React can render them into the document head, suspend while resources are loading, and enact other behaviors that are described on the reference page for each specific component.

React supports all built-in browser HTML components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing HTML to JSX with an online converter.

If you render a tag with a dash, like <my-element>, React will assume you want to render a custom HTML element.

If you render a built-in browser HTML element with an is attribute, it will also be treated as a custom element.

Custom elements have two methods of passing data into them:

By default, React will pass values bound in JSX as attributes:

Non-string JavaScript values passed to custom elements will be serialized by default:

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

A common pattern when using custom elements is that they may dispatch CustomEvents rather than accept a function to call when an event occur. You can listen for these events using an on prefix when binding to the event via JSX.

Events are case-sensitive and support dashes (-). Preserve the casing of the event and include all dashes when listening for custom element’s events:

React supports all built-in browser SVG components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing SVG to JSX with an online converter.

Namespaced attributes also have to be written without the colon:

**Examples:**

Example 1 (unknown):
```unknown
<my-element value="Hello, world!"></my-element>
```

Example 2 (unknown):
```unknown
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`<my-element value={[1,2,3]}></my-element>
```

Example 3 (unknown):
```unknown
// Listens for `say-hi` events<my-element onsay-hi={console.log}></my-element>// Listens for `sayHi` events<my-element onsayHi={console.log}></my-element>
```

---

## React DOM Components

**URL:** https://react.dev/reference/react-dom/components#resource-and-metadata-components

**Contents:**
- React DOM Components
- Common components
- Form components
- Resource and Metadata Components
- All HTML components
  - Note
  - Custom HTML elements
    - Setting values on custom elements
    - Listening for events on custom elements
  - Note

React supports all of the browser built-in HTML and SVG components.

All of the built-in browser components support some props and events.

This includes React-specific props like ref and dangerouslySetInnerHTML.

These built-in browser components accept user input:

They are special in React because passing the value prop to them makes them controlled.

These built-in browser components let you load external resources or annotate the document with metadata:

They are special in React because React can render them into the document head, suspend while resources are loading, and enact other behaviors that are described on the reference page for each specific component.

React supports all built-in browser HTML components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing HTML to JSX with an online converter.

If you render a tag with a dash, like <my-element>, React will assume you want to render a custom HTML element.

If you render a built-in browser HTML element with an is attribute, it will also be treated as a custom element.

Custom elements have two methods of passing data into them:

By default, React will pass values bound in JSX as attributes:

Non-string JavaScript values passed to custom elements will be serialized by default:

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

A common pattern when using custom elements is that they may dispatch CustomEvents rather than accept a function to call when an event occur. You can listen for these events using an on prefix when binding to the event via JSX.

Events are case-sensitive and support dashes (-). Preserve the casing of the event and include all dashes when listening for custom element’s events:

React supports all built-in browser SVG components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing SVG to JSX with an online converter.

Namespaced attributes also have to be written without the colon:

**Examples:**

Example 1 (unknown):
```unknown
<my-element value="Hello, world!"></my-element>
```

Example 2 (unknown):
```unknown
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`<my-element value={[1,2,3]}></my-element>
```

Example 3 (unknown):
```unknown
// Listens for `say-hi` events<my-element onsay-hi={console.log}></my-element>// Listens for `sayHi` events<my-element onsayHi={console.log}></my-element>
```

---

## Quick Start

**URL:** https://react.dev/learn#sharing-data-between-components

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

## <StrictMode>

**URL:** https://react.dev/reference/react/StrictMode

**Contents:**
- <StrictMode>
- Reference
  - <StrictMode>
    - Props
    - Caveats
- Usage
  - Enabling Strict Mode for entire app
  - Note
  - Enabling Strict Mode for a part of the app
  - Note

<StrictMode> lets you find common bugs in your components early during development.

Use StrictMode to enable additional development behaviors and warnings for the component tree inside:

See more examples below.

Strict Mode enables the following development-only behaviors:

StrictMode accepts no props.

Strict Mode enables extra development-only checks for the entire component tree inside the <StrictMode> component. These checks help you find common bugs in your components early in the development process.

To enable Strict Mode for your entire app, wrap your root component with <StrictMode> when you render it:

We recommend wrapping your entire app in Strict Mode, especially for newly created apps. If you use a framework that calls createRoot for you, check its documentation for how to enable Strict Mode.

Although the Strict Mode checks only run in development, they help you find bugs that already exist in your code but can be tricky to reliably reproduce in production. Strict Mode lets you fix bugs before your users report them.

Strict Mode enables the following checks in development:

All of these checks are development-only and do not impact the production build.

You can also enable Strict Mode for any part of your application:

In this example, Strict Mode checks will not run against the Header and Footer components. However, they will run on Sidebar and Content, as well as all of the components inside them, no matter how deep.

When StrictMode is enabled for a part of the app, React will only enable behaviors that are possible in production. For example, if <StrictMode> is not enabled at the root of the app, it will not re-run Effects an extra time on initial mount, since this would cause child effects to double fire without the parent effects, which cannot happen in production.

React assumes that every component you write is a pure function. This means that React components you write must always return the same JSX given the same inputs (props, state, and context).

Components breaking this rule behave unpredictably and cause bugs. To help you find accidentally impure code, Strict Mode calls some of your functions (only the ones that should be pure) twice in development. This includes:

If a function is pure, running it twice does not change its behavior because a pure function produces the same result every time. However, if a function is impure (for example, it mutates the data it receives), running it twice tends to be noticeable (that’s wh

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<StrictMode>  <App /></StrictMode>
```

Example 2 (python):
```python
import { StrictMode } from 'react';import { createRoot } from 'react-dom/client';const root = createRoot(document.getElementById('root'));root.render(  <StrictMode>    <App />  </StrictMode>);
```

Example 3 (python):
```python
import { StrictMode } from 'react';import { createRoot } from 'react-dom/client';const root = createRoot(document.getElementById('root'));root.render(  <StrictMode>    <App />  </StrictMode>);
```

Example 4 (python):
```python
import { StrictMode } from 'react';function App() {  return (    <>      <Header />      <StrictMode>        <main>          <Sidebar />          <Content />        </main>      </StrictMode>      <Footer />    </>  );}
```

---

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui#writing-markup-with-jsx

**Contents:**
- Describing the UI
  - In this chapter
- Your first component
- Ready to learn this topic?
- Importing and exporting components
- Ready to learn this topic?
- Writing markup with JSX
- Ready to learn this topic?
- JavaScript in JSX with curly braces
- Ready to learn this topic?

React is a JavaScript library for rendering user interfaces (UI). UI is built from small units like buttons, text, and images. React lets you combine them into reusable, nestable components. From web sites to phone apps, everything on the screen can be broken down into components. In this chapter, you’ll learn to create, customize, and conditionally display React components.

React applications are built from isolated pieces of UI called components. A React component is a JavaScript function that you can sprinkle with markup. Components can be as small as a button, or as large as an entire page. Here is a Gallery component rendering three Profile components:

Read Your First Component to learn how to declare and use React components.

You can declare many components in one file, but large files can get difficult to navigate. To solve this, you can export a component into its own file, and then import that component from another file:

Read Importing and Exporting Components to learn how to split components into their own files.

Each React component is a JavaScript function that may contain some markup that React renders into the browser. React components use a syntax extension called JSX to represent that markup. JSX looks a lot like HTML, but it is a bit stricter and can display dynamic information.

If we paste existing HTML markup into a React component, it won’t always work:

If you have existing HTML like this, you can fix it using a converter:

Read Writing Markup with JSX to learn how to write valid JSX.

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to “open a window” to JavaScript:

Read JavaScript in JSX with Curly Braces to learn how to access JavaScript data from JSX.

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, functions, and even JSX!

Read Passing Props to a Component to learn how to pass and read props.

Your components will often need to display different things depending on different conditions. In React, you can conditionally render JSX using JavaScript syntax like if statement

*[Content truncated]*

---

## <progress>

**URL:** https://react.dev/reference/react-dom/components/progress

**Contents:**
- <progress>
- Reference
  - <progress>
    - Props
- Usage
  - Controlling a progress indicator

The built-in browser <progress> component lets you render a progress indicator.

To display a progress indicator, render the built-in browser <progress> component.

See more examples below.

<progress> supports all common element props.

Additionally, <progress> supports these props:

To display a progress indicator, render a <progress> component. You can pass a number value between 0 and the max value you specify. If you don’t pass a max value, it will assumed to be 1 by default.

If the operation is not ongoing, pass value={null} to put the progress indicator into an indeterminate state.

**Examples:**

Example 1 (unknown):
```unknown
<progress value={0.5} />
```

Example 2 (unknown):
```unknown
<progress value={0.5} />
```

---

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## Built-in React Components

**URL:** https://react.dev/reference/react/components#built-in-components

**Contents:**
- Built-in React Components
- Built-in components
- Your own components

React exposes a few built-in components that you can use in your JSX.

You can also define your own components as JavaScript functions.

---

## React DOM Components

**URL:** https://react.dev/reference/react-dom/components#attributes-vs-properties

**Contents:**
- React DOM Components
- Common components
- Form components
- Resource and Metadata Components
- All HTML components
  - Note
  - Custom HTML elements
    - Setting values on custom elements
    - Listening for events on custom elements
  - Note

React supports all of the browser built-in HTML and SVG components.

All of the built-in browser components support some props and events.

This includes React-specific props like ref and dangerouslySetInnerHTML.

These built-in browser components accept user input:

They are special in React because passing the value prop to them makes them controlled.

These built-in browser components let you load external resources or annotate the document with metadata:

They are special in React because React can render them into the document head, suspend while resources are loading, and enact other behaviors that are described on the reference page for each specific component.

React supports all built-in browser HTML components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing HTML to JSX with an online converter.

If you render a tag with a dash, like <my-element>, React will assume you want to render a custom HTML element.

If you render a built-in browser HTML element with an is attribute, it will also be treated as a custom element.

Custom elements have two methods of passing data into them:

By default, React will pass values bound in JSX as attributes:

Non-string JavaScript values passed to custom elements will be serialized by default:

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

A common pattern when using custom elements is that they may dispatch CustomEvents rather than accept a function to call when an event occur. You can listen for these events using an on prefix when binding to the event via JSX.

Events are case-sensitive and support dashes (-). Preserve the casing of the event and include all dashes when listening for custom element’s events:

React supports all built-in browser SVG components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing SVG to JSX with an online converter.

Namespaced attributes also have to be written without the colon:

**Examples:**

Example 1 (unknown):
```unknown
<my-element value="Hello, world!"></my-element>
```

Example 2 (unknown):
```unknown
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`<my-element value={[1,2,3]}></my-element>
```

Example 3 (unknown):
```unknown
// Listens for `say-hi` events<my-element onsay-hi={console.log}></my-element>// Listens for `sayHi` events<my-element onsayHi={console.log}></my-element>
```

---

## Sharing State Between Components

**URL:** https://react.dev/learn/sharing-state-between-components

**Contents:**
- Sharing State Between Components
  - You will learn
- Lifting state up by example
  - Step 1: Remove state from the child components
  - Step 2: Pass hardcoded data from the common parent
  - Step 3: Add state to the common parent
      - Deep Dive
    - Controlled and uncontrolled components
- A single source of truth for each state
- Recap

Sometimes, you want the state of two components to always change together. To do it, remove state from both of them, move it to their closest common parent, and then pass it down to them via props. This is known as lifting state up, and it’s one of the most common things you will do writing React code.

In this example, a parent Accordion component renders two separate Panels:

Each Panel component has a boolean isActive state that determines whether its content is visible.

Press the Show button for both panels:

Notice how pressing one panel’s button does not affect the other panel—they are independent.

Initially, each Panel’s isActive state is false, so they both appear collapsed

Clicking either Panel’s button will only update that Panel’s isActive state alone

But now let’s say you want to change it so that only one panel is expanded at any given time. With that design, expanding the second panel should collapse the first one. How would you do that?

To coordinate these two panels, you need to “lift their state up” to a parent component in three steps:

This will allow the Accordion component to coordinate both Panels and only expand one at a time.

You will give control of the Panel’s isActive to its parent component. This means that the parent component will pass isActive to Panel as a prop instead. Start by removing this line from the Panel component:

And instead, add isActive to the Panel’s list of props:

Now the Panel’s parent component can control isActive by passing it down as a prop. Conversely, the Panel component now has no control over the value of isActive—it’s now up to the parent component!

To lift state up, you must locate the closest common parent component of both of the child components that you want to coordinate:

In this example, it’s the Accordion component. Since it’s above both panels and can control their props, it will become the “source of truth” for which panel is currently active. Make the Accordion component pass a hardcoded value of isActive (for example, true) to both panels:

Try editing the hardcoded isActive values in the Accordion component and see the result on the screen.

Lifting state up often changes the nature of what you’re storing as state.

In this case, only one panel should be active at a time. This means that the Accordion common parent component needs to keep track of which panel is the active one. Instead of a boolean value, it could use a number as the index of the active Panel for the state varia

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [isActive, setIsActive] = useState(false);
```

Example 2 (unknown):
```unknown
function Panel({ title, children, isActive }) {
```

Example 3 (javascript):
```javascript
const [activeIndex, setActiveIndex] = useState(0);
```

Example 4 (javascript):
```javascript
<>  <Panel    isActive={activeIndex === 0}    onShow={() => setActiveIndex(0)}  >    ...  </Panel>  <Panel    isActive={activeIndex === 1}    onShow={() => setActiveIndex(1)}  >    ...  </Panel></>
```

---

## React DOM Components

**URL:** https://react.dev/reference/react-dom/components#form-components

**Contents:**
- React DOM Components
- Common components
- Form components
- Resource and Metadata Components
- All HTML components
  - Note
  - Custom HTML elements
    - Setting values on custom elements
    - Listening for events on custom elements
  - Note

React supports all of the browser built-in HTML and SVG components.

All of the built-in browser components support some props and events.

This includes React-specific props like ref and dangerouslySetInnerHTML.

These built-in browser components accept user input:

They are special in React because passing the value prop to them makes them controlled.

These built-in browser components let you load external resources or annotate the document with metadata:

They are special in React because React can render them into the document head, suspend while resources are loading, and enact other behaviors that are described on the reference page for each specific component.

React supports all built-in browser HTML components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing HTML to JSX with an online converter.

If you render a tag with a dash, like <my-element>, React will assume you want to render a custom HTML element.

If you render a built-in browser HTML element with an is attribute, it will also be treated as a custom element.

Custom elements have two methods of passing data into them:

By default, React will pass values bound in JSX as attributes:

Non-string JavaScript values passed to custom elements will be serialized by default:

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

A common pattern when using custom elements is that they may dispatch CustomEvents rather than accept a function to call when an event occur. You can listen for these events using an on prefix when binding to the event via JSX.

Events are case-sensitive and support dashes (-). Preserve the casing of the event and include all dashes when listening for custom element’s events:

React supports all built-in browser SVG components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing SVG to JSX with an online converter.

Namespaced attributes also have to be written without the colon:

**Examples:**

Example 1 (unknown):
```unknown
<my-element value="Hello, world!"></my-element>
```

Example 2 (unknown):
```unknown
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`<my-element value={[1,2,3]}></my-element>
```

Example 3 (unknown):
```unknown
// Listens for `say-hi` events<my-element onsay-hi={console.log}></my-element>// Listens for `sayHi` events<my-element onsayHi={console.log}></my-element>
```

---

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory#undefined

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

## Passing Data Deeply with Context

**URL:** https://react.dev/learn/passing-data-deeply-with-context

**Contents:**
- Passing Data Deeply with Context
  - You will learn
- The problem with passing props
- Context: an alternative to passing props
  - Step 1: Create the context
  - Step 2: Use the context
  - Step 3: Provide the context
- Using and providing context from the same component
  - Note
- Context passes through intermediate components

Usually, you will pass information from a parent component to a child component via props. But passing props can become verbose and inconvenient if you have to pass them through many components in the middle, or if many components in your app need the same information. Context lets the parent component make some information available to any component in the tree below it—no matter how deep—without passing it explicitly through props.

Passing props is a great way to explicitly pipe data through your UI tree to the components that use it.

But passing props can become verbose and inconvenient when you need to pass some prop deeply through the tree, or if many components need the same prop. The nearest common ancestor could be far removed from the components that need data, and lifting state up that high can lead to a situation called “prop drilling”.

Wouldn’t it be great if there were a way to “teleport” data to the components in the tree that need it without passing props? With React’s context feature, there is!

Context lets a parent component provide data to the entire tree below it. There are many uses for context. Here is one example. Consider this Heading component that accepts a level for its size:

Let’s say you want multiple headings within the same Section to always have the same size:

Currently, you pass the level prop to each <Heading> separately:

It would be nice if you could pass the level prop to the <Section> component instead and remove it from the <Heading>. This way you could enforce that all headings in the same section have the same size:

But how can the <Heading> component know the level of its closest <Section>? That would require some way for a child to “ask” for data from somewhere above in the tree.

You can’t do it with props alone. This is where context comes into play. You will do it in three steps:

Context lets a parent—even a distant one!—provide some data to the entire tree inside of it.

Using context in close children

Using context in distant children

First, you need to create the context. You’ll need to export it from a file so that your components can use it:

The only argument to createContext is the default value. Here, 1 refers to the biggest heading level, but you could pass any kind of value (even an object). You will see the significance of the default value in the next step.

Import the useContext Hook from React and your context:

Currently, the Heading component reads level from props:

Instead, remove the

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<Section>  <Heading level={3}>About</Heading>  <Heading level={3}>Photos</Heading>  <Heading level={3}>Videos</Heading></Section>
```

Example 2 (unknown):
```unknown
<Section level={3}>  <Heading>About</Heading>  <Heading>Photos</Heading>  <Heading>Videos</Heading></Section>
```

Example 3 (python):
```python
import { useContext } from 'react';import { LevelContext } from './LevelContext.js';
```

Example 4 (unknown):
```unknown
export default function Heading({ level, children }) {  // ...}
```

---

## State: A Component's Memory

**URL:** https://react.dev/learn/state-a-components-memory#giving-a-component-multiple-state-variables

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

## Preserving and Resetting State

**URL:** https://react.dev/learn/preserving-and-resetting-state#different-components-at-the-same-position-reset-state

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

## <Profiler>

**URL:** https://react.dev/reference/react/Profiler

**Contents:**
- <Profiler>
- Reference
  - <Profiler>
    - Props
    - Caveats
  - onRender callback
    - Parameters
- Usage
  - Measuring rendering performance programmatically
  - Pitfall

<Profiler> lets you measure rendering performance of a React tree programmatically.

Wrap a component tree in a <Profiler> to measure its rendering performance.

React will call your onRender callback with information about what was rendered.

Wrap the <Profiler> component around a React tree to measure its rendering performance.

It requires two props: an id (string) and an onRender callback (function) which React calls any time a component within the tree “commits” an update.

Profiling adds some additional overhead, so it is disabled in the production build by default. To opt into production profiling, you need to enable a special production build with profiling enabled.

<Profiler> lets you gather measurements programmatically. If you’re looking for an interactive profiler, try the Profiler tab in React Developer Tools. It exposes similar functionality as a browser extension.

Components wrapped in <Profiler> will also be marked in the Component tracks of React Performance tracks even in profiling builds. In development builds, all components are marked in the Components track regardless of whether they’re wrapped in <Profiler>.

You can use multiple <Profiler> components to measure different parts of your application:

You can also nest <Profiler> components:

Although <Profiler> is a lightweight component, it should be used only when necessary. Each use adds some CPU and memory overhead to an application.

**Examples:**

Example 1 (unknown):
```unknown
<Profiler id="App" onRender={onRender}>  <App /></Profiler>
```

Example 2 (unknown):
```unknown
<Profiler id="App" onRender={onRender}>  <App /></Profiler>
```

Example 3 (unknown):
```unknown
function onRender(id, phase, actualDuration, baseDuration, startTime, commitTime) {  // Aggregate or log render timings...}
```

Example 4 (unknown):
```unknown
<App>  <Profiler id="Sidebar" onRender={onRender}>    <Sidebar />  </Profiler>  <PageContent /></App>
```

---

## Your First Component

**URL:** https://react.dev/learn/your-first-component#challenges

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## Adding Interactivity

**URL:** https://react.dev/learn/adding-interactivity#whats-next

**Contents:**
- Adding Interactivity
  - In this chapter
- Responding to events
- Ready to learn this topic?
- State: a component’s memory
- Ready to learn this topic?
- Render and commit
- Ready to learn this topic?
- State as a snapshot
- Ready to learn this topic?

Some things on the screen update in response to user input. For example, clicking an image gallery switches the active image. In React, data that changes over time is called state. You can add state to any component, and update it as needed. In this chapter, you’ll learn how to write components that handle interactions, update their state, and display different output over time.

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to user interactions like clicking, hovering, focusing on form inputs, and so on.

Built-in components like <button> only support built-in browser events like onClick. However, you can also create your own components, and give their event handler props any application-specific names that you like.

Read Responding to Events to learn how to add event handlers.

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” puts a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

You can add state to a component with a useState Hook. Hooks are special functions that let your components use React features (state is one of those features). The useState Hook lets you declare a state variable. It takes the initial state and returns a pair of values: the current state, and a state setter function that lets you update it.

Here is how an image gallery uses and updates state on click:

Read State: A Component’s Memory to learn how to remember a value and update it on interaction.

Before your components are displayed on the screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

Read Render and Commit to learn the lifecycle of a UI update.

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already ha

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

Example 2 (unknown):
```unknown
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

Example 3 (unknown):
```unknown
console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0
```

---

## Passing Props to a Component

**URL:** https://react.dev/learn/passing-props-to-a-component#extract-a-component

**Contents:**
- Passing Props to a Component
  - You will learn
- Familiar props
- Passing props to a component
  - Step 1: Pass props to the child component
  - Note
  - Step 2: Read props inside the child component
  - Pitfall
- Specifying a default value for a prop
- Forwarding props with the JSX spread syntax

React components use props to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

Props are the information that you pass to a JSX tag. For example, className, src, alt, width, and height are some of the props you can pass to an <img>:

The props you can pass to an <img> tag are predefined (ReactDOM conforms to the HTML standard). But you can pass any props to your own components, such as <Avatar>, to customize them. Here’s how!

In this code, the Profile component isn’t passing any props to its child component, Avatar:

You can give Avatar some props in two steps.

First, pass some props to Avatar. For example, let’s pass two props: person (an object), and size (a number):

If double curly braces after person= confuse you, recall they’re merely an object inside the JSX curlies.

Now you can read these props inside the Avatar component.

You can read these props by listing their names person, size separated by the commas inside ({ and }) directly after function Avatar. This lets you use them inside the Avatar code, like you would with a variable.

Add some logic to Avatar that uses the person and size props for rendering, and you’re done.

Now you can configure Avatar to render in many different ways with different props. Try tweaking the values!

Props let you think about parent and child components independently. For example, you can change the person or the size props inside Profile without having to think about how Avatar uses them. Similarly, you can change how the Avatar uses these props, without looking at the Profile.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props are the only argument to your component! React component functions accept a single argument, a props object:

Usually you don’t need the whole props object itself, so you destructure it into individual props.

Don’t miss the pair of { and } curlies inside of ( and ) when declaring props:

This syntax is called “destructuring” and is equivalent to reading properties from a function parameter:

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting = and the default value right after the parameter:

Now, if <Avatar person={

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
export default function Profile() {  return (    <Avatar />  );}
```

Example 2 (unknown):
```unknown
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

Example 3 (unknown):
```unknown
function Avatar({ person, size }) {  // person and size are available here}
```

Example 4 (javascript):
```javascript
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

---

## Adding Interactivity

**URL:** https://react.dev/learn/adding-interactivity#state-a-components-memory

**Contents:**
- Adding Interactivity
  - In this chapter
- Responding to events
- Ready to learn this topic?
- State: a component’s memory
- Ready to learn this topic?
- Render and commit
- Ready to learn this topic?
- State as a snapshot
- Ready to learn this topic?

Some things on the screen update in response to user input. For example, clicking an image gallery switches the active image. In React, data that changes over time is called state. You can add state to any component, and update it as needed. In this chapter, you’ll learn how to write components that handle interactions, update their state, and display different output over time.

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to user interactions like clicking, hovering, focusing on form inputs, and so on.

Built-in components like <button> only support built-in browser events like onClick. However, you can also create your own components, and give their event handler props any application-specific names that you like.

Read Responding to Events to learn how to add event handlers.

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” puts a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called state.

You can add state to a component with a useState Hook. Hooks are special functions that let your components use React features (state is one of those features). The useState Hook lets you declare a state variable. It takes the initial state and returns a pair of values: the current state, and a state setter function that lets you update it.

Here is how an image gallery uses and updates state on click:

Read State: A Component’s Memory to learn how to remember a value and update it on interaction.

Before your components are displayed on the screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

Read Render and Commit to learn the lifecycle of a UI update.

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already ha

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

Example 2 (unknown):
```unknown
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

Example 3 (unknown):
```unknown
console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0
```

---

## React DOM Components

**URL:** https://react.dev/reference/react-dom/components#common-components

**Contents:**
- React DOM Components
- Common components
- Form components
- Resource and Metadata Components
- All HTML components
  - Note
  - Custom HTML elements
    - Setting values on custom elements
    - Listening for events on custom elements
  - Note

React supports all of the browser built-in HTML and SVG components.

All of the built-in browser components support some props and events.

This includes React-specific props like ref and dangerouslySetInnerHTML.

These built-in browser components accept user input:

They are special in React because passing the value prop to them makes them controlled.

These built-in browser components let you load external resources or annotate the document with metadata:

They are special in React because React can render them into the document head, suspend while resources are loading, and enact other behaviors that are described on the reference page for each specific component.

React supports all built-in browser HTML components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing HTML to JSX with an online converter.

If you render a tag with a dash, like <my-element>, React will assume you want to render a custom HTML element.

If you render a built-in browser HTML element with an is attribute, it will also be treated as a custom element.

Custom elements have two methods of passing data into them:

By default, React will pass values bound in JSX as attributes:

Non-string JavaScript values passed to custom elements will be serialized by default:

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

A common pattern when using custom elements is that they may dispatch CustomEvents rather than accept a function to call when an event occur. You can listen for these events using an on prefix when binding to the event via JSX.

Events are case-sensitive and support dashes (-). Preserve the casing of the event and include all dashes when listening for custom element’s events:

React supports all built-in browser SVG components. This includes:

Similar to the DOM standard, React uses a camelCase convention for prop names. For example, you’ll write tabIndex instead of tabindex. You can convert existing SVG to JSX with an online converter.

Namespaced attributes also have to be written without the colon:

**Examples:**

Example 1 (unknown):
```unknown
<my-element value="Hello, world!"></my-element>
```

Example 2 (unknown):
```unknown
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`<my-element value={[1,2,3]}></my-element>
```

Example 3 (unknown):
```unknown
// Listens for `say-hi` events<my-element onsay-hi={console.log}></my-element>// Listens for `sayHi` events<my-element onsayHi={console.log}></my-element>
```

---

## Your First Component

**URL:** https://react.dev/learn/your-first-component#recap

**Contents:**
- Your First Component
  - You will learn
- Components: UI building blocks
- Defining a component
  - Step 1: Export the component
  - Step 2: Define the function
  - Pitfall
  - Step 3: Add markup
  - Pitfall
- Using a component

Components are one of the core concepts of React. They are the foundation upon which you build user interfaces (UI), which makes them the perfect place to start your React journey!

On the Web, HTML lets us create rich structured documents with its built-in set of tags like <h1> and <li>:

This markup represents this article <article>, its heading <h1>, and an (abbreviated) table of contents as an ordered list <ol>. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, reusable UI elements for your app. The table of contents code you saw above could be turned into a <TableOfContents /> component you could render on every page. Under the hood, it still uses the same HTML tags like <article>, <h1>, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with <TableOfContents />! You can even jumpstart your project with the thousands of components shared by the React open source community like Chakra UI and Material UI.

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: a React component is a JavaScript function that you can sprinkle with markup. Here’s what that looks like (you can edit the example below):

And here’s how to build a component:

The export default prefix is a standard JavaScript syntax (not specific to React). It lets you mark the main function in a file so that you can later import it from other files. (More on importing in Importing and Exporting Components!)

With function Profile() { } you define a JavaScript function with the name Profile.

React components are regular JavaScript functions, but their names must start with a capital letter or they won’t work!

The component returns an <img /> tag with src and alt attributes. <img /> is written li

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<article>  <h1>My First Component</h1>  <ol>    <li>Components: UI Building Blocks</li>    <li>Defining a Component</li>    <li>Using a Component</li>  </ol></article>
```

Example 2 (unknown):
```unknown
<PageLayout>  <NavigationHeader>    <SearchBar />    <Link to="/docs">Docs</Link>  </NavigationHeader>  <Sidebar />  <PageContent>    <TableOfContents />    <DocumentationText />  </PageContent></PageLayout>
```

Example 3 (unknown):
```unknown
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

Example 4 (unknown):
```unknown
return (  <div>    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />  </div>);
```

---

## createPortal

**URL:** https://react.dev/reference/react-dom/createPortal

**Contents:**
- createPortal
- Reference
  - createPortal(children, domNode, key?)
    - Parameters
    - Returns
    - Caveats
- Usage
  - Rendering to a different part of the DOM
  - Rendering a modal dialog with a portal
  - Pitfall

createPortal lets you render some children into a different part of the DOM.

To create a portal, call createPortal, passing some JSX, and the DOM node where it should be rendered:

See more examples below.

A portal only changes the physical placement of the DOM node. In every other way, the JSX you render into a portal acts as a child node of the React component that renders it. For example, the child can access the context provided by the parent tree, and events bubble up from children to parents according to the React tree.

children: Anything that can be rendered with React, such as a piece of JSX (e.g. <div /> or <SomeComponent />), a Fragment (<>...</>), a string or a number, or an array of these.

domNode: Some DOM node, such as those returned by document.getElementById(). The node must already exist. Passing a different DOM node during an update will cause the portal content to be recreated.

optional key: A unique string or number to be used as the portal’s key.

createPortal returns a React node that can be included into JSX or returned from a React component. If React encounters it in the render output, it will place the provided children inside the provided domNode.

Portals let your components render some of their children into a different place in the DOM. This lets a part of your component “escape” from whatever containers it may be in. For example, a component can display a modal dialog or a tooltip that appears above and outside of the rest of the page.

To create a portal, render the result of createPortal with some JSX and the DOM node where it should go:

React will put the DOM nodes for the JSX you passed inside of the DOM node you provided.

Without a portal, the second <p> would be placed inside the parent <div>, but the portal “teleported” it into the document.body:

Notice how the second paragraph visually appears outside the parent <div> with the border. If you inspect the DOM structure with developer tools, you’ll see that the second <p> got placed directly into the <body>:

A portal only changes the physical placement of the DOM node. In every other way, the JSX you render into a portal acts as a child node of the React component that renders it. For example, the child can access the context provided by the parent tree, and events still bubble up from children to parents according to the React tree.

You can use a portal to create a modal dialog that floats above the rest of the page, even if the component that summons the dial

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<div>  <SomeComponent />  {createPortal(children, domNode, key?)}</div>
```

Example 2 (python):
```python
import { createPortal } from 'react-dom';// ...<div>  <p>This child is placed in the parent div.</p>  {createPortal(    <p>This child is placed in the document body.</p>,    document.body  )}</div>
```

Example 3 (python):
```python
import { createPortal } from 'react-dom';function MyComponent() {  return (    <div style={{ border: '2px solid black' }}>      <p>This child is placed in the parent div.</p>      {createPortal(        <p>This child is placed in the document body.</p>,        document.body      )}    </div>  );}
```

Example 4 (unknown):
```unknown
<body>  <div id="root">    ...      <div style="border: 2px solid black">        <p>This child is placed inside the parent div.</p>      </div>    ...  </div>  <p>This child is placed in the document body.</p></body>
```

---
