# React - Other

**Pages:** 33

---

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui#undefined

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

## Thinking in React

**URL:** https://react.dev/learn/thinking-in-react#step-5-add-inverse-data-flow

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

## Quick Start

**URL:** https://react.dev/learn#updating-the-screen

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

## Creating a React App

**URL:** https://react.dev/learn/creating-a-react-app

**Contents:**
- Creating a React App
- Full-stack frameworks
  - Note
    - Full-stack frameworks do not require a server.
  - Next.js (App Router)
  - React Router (v7)
  - Expo (for native apps)
- Other frameworks
      - Deep Dive
    - Which features make up the React team’s full-stack architecture vision?

If you want to build a new app or website with React, we recommend starting with a framework.

If your app has constraints not well-served by existing frameworks, you prefer to build your own framework, or you just want to learn the basics of a React app, you can build a React app from scratch.

These recommended frameworks support all the features you need to deploy and scale your app in production. They have integrated the latest React features and take advantage of React’s architecture.

All the frameworks on this page support client-side rendering (CSR), single-page apps (SPA), and static-site generation (SSG). These apps can be deployed to a CDN or static hosting service without a server. Additionally, these frameworks allow you to add server-side rendering on a per-route basis, when it makes sense for your use case.

This allows you to start with a client-only app, and if your needs change later, you can opt-in to using server features on individual routes without rewriting your app. See your framework’s documentation for configuring the rendering strategy.

Next.js’s App Router is a React framework that takes full advantage of React’s architecture to enable full-stack React apps.

Next.js is maintained by Vercel. You can deploy a Next.js app to any hosting provider that supports Node.js or Docker containers, or to your own server. Next.js also supports static export which doesn’t require a server.

React Router is the most popular routing library for React and can be paired with Vite to create a full-stack React framework. It emphasizes standard Web APIs and has several ready to deploy templates for various JavaScript runtimes and platforms.

To create a new React Router framework project, run:

React Router is maintained by Shopify.

Expo is a React framework that lets you create universal Android, iOS, and web apps with truly native UIs. It provides an SDK for React Native that makes the native parts easier to use. To create a new Expo project, run:

If you’re new to Expo, check out the Expo tutorial.

Expo is maintained by Expo (the company). Building apps with Expo is free, and you can submit them to the Google and Apple app stores without restrictions. Expo additionally provides opt-in paid cloud services.

There are other up-and-coming frameworks that are working towards our full stack React vision:

Next.js’s App Router bundler fully implements the official React Server Components specification. This lets you mix build-time, server-only, and 

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
// This component runs *only* on the server (or during the build).async function Talks({ confId }) {  // 1. You're on the server, so you can talk to your data layer. API endpoint not required.  const talks = await db.Talks.findAll({ confId });  // 2. Add any amount of rendering logic. It won't make your JavaScript bundle larger.  const videos = talks.map(talk => talk.video);  // 3. Pass the data down to the components that will run in the browser.  return <SearchableVideoList videos={videos} />;}
```

Example 2 (unknown):
```unknown
<Suspense fallback={<TalksLoading />}>  <Talks confId={conf.id} /></Suspense>
```

---

## Render and Commit

**URL:** https://react.dev/learn/render-and-commit#step-1-trigger-a-render

**Contents:**
- Render and Commit
  - You will learn
- Step 1: Trigger a render
  - Initial render
  - Re-renders when state updates
- Step 2: React renders your components
  - Pitfall
      - Deep Dive
    - Optimizing performance
- Step 3: React commits changes to the DOM

Before your components are displayed on screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

There are two reasons for a component to render:

When your app starts, you need to trigger the initial render. Frameworks and sandboxes sometimes hide this code, but it’s done by calling createRoot with the target DOM node, and then calling its render method with your component:

Try commenting out the root.render() call and see the component disappear!

Once the component has been initially rendered, you can trigger further renders by updating its state with the set function. Updating your component’s state automatically queues a render. (You can imagine these as a restaurant guest ordering tea, dessert, and all sorts of things after putting in their first order, depending on the state of their thirst or hunger.)

Illustrated by Rachel Lee Nabors

After you trigger a render, React calls your components to figure out what to display on screen. “Rendering” is React calling your components.

This process is recursive: if the updated component returns some other component, React will render that component next, and if that component also returns something, it will render that component next, and so on. The process will continue until there are no more nested components and React knows exactly what should be displayed on screen.

In the following example, React will call Gallery() and Image() several times:

Rendering must always be a pure calculation:

Otherwise, you can encounter confusing bugs and unpredictable behavior as your codebase grows in complexity. When developing in “Strict Mode”, React calls each component’s function twice, which can help surface mistakes caused by impure functions.

The default behavior of rendering all components nested within the updated component is not optimal for performance if the updated component is very high in the tree. If you run into a performance issue, there are several opt-in ways to solve it described in the Performance section. Don’t optimize prematurely!

After rendering (calling) your components, React will modify the DOM.

Rea

*[Content truncated]*

---

## Creating a React App

**URL:** https://react.dev/learn/start-a-new-react-project

**Contents:**
- Creating a React App
- Full-stack frameworks
  - Note
    - Full-stack frameworks do not require a server.
  - Next.js (App Router)
  - React Router (v7)
  - Expo (for native apps)
- Other frameworks
      - Deep Dive
    - Which features make up the React team’s full-stack architecture vision?

If you want to build a new app or website with React, we recommend starting with a framework.

If your app has constraints not well-served by existing frameworks, you prefer to build your own framework, or you just want to learn the basics of a React app, you can build a React app from scratch.

These recommended frameworks support all the features you need to deploy and scale your app in production. They have integrated the latest React features and take advantage of React’s architecture.

All the frameworks on this page support client-side rendering (CSR), single-page apps (SPA), and static-site generation (SSG). These apps can be deployed to a CDN or static hosting service without a server. Additionally, these frameworks allow you to add server-side rendering on a per-route basis, when it makes sense for your use case.

This allows you to start with a client-only app, and if your needs change later, you can opt-in to using server features on individual routes without rewriting your app. See your framework’s documentation for configuring the rendering strategy.

Next.js’s App Router is a React framework that takes full advantage of React’s architecture to enable full-stack React apps.

Next.js is maintained by Vercel. You can deploy a Next.js app to any hosting provider that supports Node.js or Docker containers, or to your own server. Next.js also supports static export which doesn’t require a server.

React Router is the most popular routing library for React and can be paired with Vite to create a full-stack React framework. It emphasizes standard Web APIs and has several ready to deploy templates for various JavaScript runtimes and platforms.

To create a new React Router framework project, run:

React Router is maintained by Shopify.

Expo is a React framework that lets you create universal Android, iOS, and web apps with truly native UIs. It provides an SDK for React Native that makes the native parts easier to use. To create a new Expo project, run:

If you’re new to Expo, check out the Expo tutorial.

Expo is maintained by Expo (the company). Building apps with Expo is free, and you can submit them to the Google and Apple app stores without restrictions. Expo additionally provides opt-in paid cloud services.

There are other up-and-coming frameworks that are working towards our full stack React vision:

Next.js’s App Router bundler fully implements the official React Server Components specification. This lets you mix build-time, server-only, and 

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
// This component runs *only* on the server (or during the build).async function Talks({ confId }) {  // 1. You're on the server, so you can talk to your data layer. API endpoint not required.  const talks = await db.Talks.findAll({ confId });  // 2. Add any amount of rendering logic. It won't make your JavaScript bundle larger.  const videos = talks.map(talk => talk.video);  // 3. Pass the data down to the components that will run in the browser.  return <SearchableVideoList videos={videos} />;}
```

Example 2 (unknown):
```unknown
<Suspense fallback={<TalksLoading />}>  <Talks confId={conf.id} /></Suspense>
```

---

## Quick Start

**URL:** https://react.dev/learn#undefined

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

## Quick Start

**URL:** https://react.dev/learn#responding-to-events

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

## Quick Start

**URL:** https://react.dev/learn#next-steps

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

## Thinking in React

**URL:** https://react.dev/learn/thinking-in-react#start-with-the-mockup

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

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui#conditional-rendering

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

## Thinking in React

**URL:** https://react.dev/learn/thinking-in-react#step-2-build-a-static-version-in-react

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

## Quick Start

**URL:** https://react.dev/learn#conditional-rendering

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

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui

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

## Understanding Your UI as a Tree

**URL:** https://react.dev/learn/understanding-your-ui-as-a-tree

**Contents:**
- Understanding Your UI as a Tree
  - You will learn
- Your UI as a tree
- The Render Tree
      - Deep Dive
    - Where are the HTML tags in the render tree?
- The Module Dependency Tree
- Recap

Your React app is taking shape with many components being nested within each other. How does React keep track of your app’s component structure?

React, and many other UI libraries, model UI as a tree. Thinking of your app as a tree is useful for understanding the relationship between components. This understanding will help you debug future concepts like performance and state management.

Trees are a relationship model between items. The UI is often represented using tree structures. For example, browsers use tree structures to model HTML (DOM) and CSS (CSSOM). Mobile platforms also use trees to represent their view hierarchy.

React creates a UI tree from your components. In this example, the UI tree is then used to render to the DOM.

Like browsers and mobile platforms, React also uses tree structures to manage and model the relationship between components in a React app. These trees are useful tools to understand how data flows through a React app and how to optimize rendering and app size.

A major feature of components is the ability to compose components of other components. As we nest components, we have the concept of parent and child components, where each parent component may itself be a child of another component.

When we render a React app, we can model this relationship in a tree, known as the render tree.

Here is a React app that renders inspirational quotes.

React creates a render tree, a UI tree, composed of the rendered components.

From the example app, we can construct the above render tree.

The tree is composed of nodes, each of which represents a component. App, FancyText, Copyright, to name a few, are all nodes in our tree.

The root node in a React render tree is the root component of the app. In this case, the root component is App and it is the first component React renders. Each arrow in the tree points from a parent component to a child component.

You’ll notice in the above render tree, there is no mention of the HTML tags that each component renders. This is because the render tree is only composed of React components.

React, as a UI framework, is platform agnostic. On react.dev, we showcase examples that render to the web, which uses HTML markup as its UI primitives. But a React app could just as likely render to a mobile or desktop platform, which may use different UI primitives like UIView or FrameworkElement.

These platform UI primitives are not a part of React. React render trees can provide insight to our React app

*[Content truncated]*

---

## Quick Start

**URL:** https://react.dev/learn#rendering-lists

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

## Add React to an Existing Project

**URL:** https://react.dev/learn/add-react-to-an-existing-project

**Contents:**
- Add React to an Existing Project
  - Note
- Using React for an entire subroute of your existing website
- Using React for a part of your existing page
  - Step 1: Set up a modular JavaScript environment
  - Note
  - Step 2: Render React components anywhere on the page
- Using React Native in an existing native mobile app

If you want to add some interactivity to your existing project, you don’t have to rewrite it in React. Add React to your existing stack, and render interactive React components anywhere.

You need to install Node.js for local development. Although you can try React online or with a simple HTML page, realistically most JavaScript tooling you’ll want to use for development requires Node.js.

Let’s say you have an existing web app at example.com built with another server technology (like Rails), and you want to implement all routes starting with example.com/some-app/ fully with React.

Here’s how we recommend to set it up:

This ensures the React part of your app can benefit from the best practices baked into those frameworks.

Many React-based frameworks are full-stack and let your React app take advantage of the server. However, you can use the same approach even if you can’t or don’t want to run JavaScript on the server. In that case, serve the HTML/CSS/JS export (next export output for Next.js, default for Gatsby) at /some-app/ instead.

Let’s say you have an existing page built with another technology (either a server one like Rails, or a client one like Backbone), and you want to render interactive React components somewhere on that page. That’s a common way to integrate React—in fact, it’s how most React usage looked at Meta for many years!

You can do this in two steps:

The exact approach depends on your existing page setup, so let’s walk through some details.

A modular JavaScript environment lets you write your React components in individual files, as opposed to writing all of your code in a single file. It also lets you use all the wonderful packages published by other developers on the npm registry—including React itself! How you do this depends on your existing setup:

If your app is already split into files that use import statements, try to use the setup you already have. Check whether writing <div /> in your JS code causes a syntax error. If it causes a syntax error, you might need to transform your JavaScript code with Babel, and enable the Babel React preset to use JSX.

If your app doesn’t have an existing setup for compiling JavaScript modules, set it up with Vite. The Vite community maintains many integrations with backend frameworks, including Rails, Django, and Laravel. If your backend framework is not listed, follow this guide to manually integrate Vite builds with your backend.

To check whether your setup works, run this command in 

*[Content truncated]*

**Examples:**

Example 1 (python):
```python
import { createRoot } from 'react-dom/client';// Clear the existing HTML contentdocument.body.innerHTML = '<div id="app"></div>';// Render your React component insteadconst root = createRoot(document.getElementById('app'));root.render(<h1>Hello, world</h1>);
```

Example 2 (unknown):
```unknown
<!-- ... somewhere in your html ... --><nav id="navigation"></nav><!-- ... more html ... -->
```

---

## Add React to an Existing Project

**URL:** https://react.dev/learn/add-react-to-an-existing-project#using-react-for-a-part-of-your-existing-page

**Contents:**
- Add React to an Existing Project
  - Note
- Using React for an entire subroute of your existing website
- Using React for a part of your existing page
  - Step 1: Set up a modular JavaScript environment
  - Note
  - Step 2: Render React components anywhere on the page
- Using React Native in an existing native mobile app

If you want to add some interactivity to your existing project, you don’t have to rewrite it in React. Add React to your existing stack, and render interactive React components anywhere.

You need to install Node.js for local development. Although you can try React online or with a simple HTML page, realistically most JavaScript tooling you’ll want to use for development requires Node.js.

Let’s say you have an existing web app at example.com built with another server technology (like Rails), and you want to implement all routes starting with example.com/some-app/ fully with React.

Here’s how we recommend to set it up:

This ensures the React part of your app can benefit from the best practices baked into those frameworks.

Many React-based frameworks are full-stack and let your React app take advantage of the server. However, you can use the same approach even if you can’t or don’t want to run JavaScript on the server. In that case, serve the HTML/CSS/JS export (next export output for Next.js, default for Gatsby) at /some-app/ instead.

Let’s say you have an existing page built with another technology (either a server one like Rails, or a client one like Backbone), and you want to render interactive React components somewhere on that page. That’s a common way to integrate React—in fact, it’s how most React usage looked at Meta for many years!

You can do this in two steps:

The exact approach depends on your existing page setup, so let’s walk through some details.

A modular JavaScript environment lets you write your React components in individual files, as opposed to writing all of your code in a single file. It also lets you use all the wonderful packages published by other developers on the npm registry—including React itself! How you do this depends on your existing setup:

If your app is already split into files that use import statements, try to use the setup you already have. Check whether writing <div /> in your JS code causes a syntax error. If it causes a syntax error, you might need to transform your JavaScript code with Babel, and enable the Babel React preset to use JSX.

If your app doesn’t have an existing setup for compiling JavaScript modules, set it up with Vite. The Vite community maintains many integrations with backend frameworks, including Rails, Django, and Laravel. If your backend framework is not listed, follow this guide to manually integrate Vite builds with your backend.

To check whether your setup works, run this command in 

*[Content truncated]*

**Examples:**

Example 1 (python):
```python
import { createRoot } from 'react-dom/client';// Clear the existing HTML contentdocument.body.innerHTML = '<div id="app"></div>';// Render your React component insteadconst root = createRoot(document.getElementById('app'));root.render(<h1>Hello, world</h1>);
```

Example 2 (unknown):
```unknown
<!-- ... somewhere in your html ... --><nav id="navigation"></nav><!-- ... more html ... -->
```

---

## Thinking in React

**URL:** https://react.dev/learn/thinking-in-react#undefined

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

## Quick Start

**URL:** https://react.dev/learn

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

## Build a React app from Scratch

**URL:** https://react.dev/learn/build-a-react-app-from-scratch

**Contents:**
- Build a React app from Scratch
      - Deep Dive
    - Consider using a framework
- Step 1: Install a build tool
  - Vite
  - Parcel
  - Rsbuild
  - Note
    - Metro for React Native
- Step 2: Build Common Application Patterns

If your app has constraints not well-served by existing frameworks, you prefer to build your own framework, or you just want to learn the basics of a React app, you can build a React app from scratch.

Starting from scratch is an easy way to get started using React, but a major tradeoff to be aware of is that going this route is often the same as building your own adhoc framework. As your requirements evolve, you may need to solve more framework-like problems that our recommended frameworks already have well developed and supported solutions for.

For example, if in the future your app needs support for server-side rendering (SSR), static site generation (SSG), and/or React Server Components (RSC), you will have to implement those on your own. Similarly, future React features that require integrating at the framework level will have to be implemented on your own if you want to use them.

Our recommended frameworks also help you build better performing apps. For example, reducing or eliminating waterfalls from network requests makes for a better user experience. This might not be a high priority when you are building a toy project, but if your app gains users you may want to improve its performance.

Going this route also makes it more difficult to get support, since the way you develop routing, data-fetching, and other features will be unique to your situation. You should only choose this option if you are comfortable tackling these problems on your own, or if you’re confident that you will never need these features.

For a list of recommended frameworks, check out Creating a React App.

The first step is to install a build tool like vite, parcel, or rsbuild. These build tools provide features to package and run source code, provide a development server for local development and a build command to deploy your app to a production server.

Vite is a build tool that aims to provide a faster and leaner development experience for modern web projects.

Vite is opinionated and comes with sensible defaults out of the box. Vite has a rich ecosystem of plugins to support fast refresh, JSX, Babel/SWC, and other common features. See Vite’s React plugin or React SWC plugin and React SSR example project to get started.

Vite is already being used as a build tool in one of our recommended frameworks: React Router.

Parcel combines a great out-of-the-box development experience with a scalable architecture that can take your project from just getting started to massive pro

*[Content truncated]*

---

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui#rendering-lists

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

## Creating a React App

**URL:** https://react.dev/learn/start-a-new-react-project#full-stack-frameworks

**Contents:**
- Creating a React App
- Full-stack frameworks
  - Note
    - Full-stack frameworks do not require a server.
  - Next.js (App Router)
  - React Router (v7)
  - Expo (for native apps)
- Other frameworks
      - Deep Dive
    - Which features make up the React team’s full-stack architecture vision?

If you want to build a new app or website with React, we recommend starting with a framework.

If your app has constraints not well-served by existing frameworks, you prefer to build your own framework, or you just want to learn the basics of a React app, you can build a React app from scratch.

These recommended frameworks support all the features you need to deploy and scale your app in production. They have integrated the latest React features and take advantage of React’s architecture.

All the frameworks on this page support client-side rendering (CSR), single-page apps (SPA), and static-site generation (SSG). These apps can be deployed to a CDN or static hosting service without a server. Additionally, these frameworks allow you to add server-side rendering on a per-route basis, when it makes sense for your use case.

This allows you to start with a client-only app, and if your needs change later, you can opt-in to using server features on individual routes without rewriting your app. See your framework’s documentation for configuring the rendering strategy.

Next.js’s App Router is a React framework that takes full advantage of React’s architecture to enable full-stack React apps.

Next.js is maintained by Vercel. You can deploy a Next.js app to any hosting provider that supports Node.js or Docker containers, or to your own server. Next.js also supports static export which doesn’t require a server.

React Router is the most popular routing library for React and can be paired with Vite to create a full-stack React framework. It emphasizes standard Web APIs and has several ready to deploy templates for various JavaScript runtimes and platforms.

To create a new React Router framework project, run:

React Router is maintained by Shopify.

Expo is a React framework that lets you create universal Android, iOS, and web apps with truly native UIs. It provides an SDK for React Native that makes the native parts easier to use. To create a new Expo project, run:

If you’re new to Expo, check out the Expo tutorial.

Expo is maintained by Expo (the company). Building apps with Expo is free, and you can submit them to the Google and Apple app stores without restrictions. Expo additionally provides opt-in paid cloud services.

There are other up-and-coming frameworks that are working towards our full stack React vision:

Next.js’s App Router bundler fully implements the official React Server Components specification. This lets you mix build-time, server-only, and 

*[Content truncated]*

**Examples:**

Example 1 (javascript):
```javascript
// This component runs *only* on the server (or during the build).async function Talks({ confId }) {  // 1. You're on the server, so you can talk to your data layer. API endpoint not required.  const talks = await db.Talks.findAll({ confId });  // 2. Add any amount of rendering logic. It won't make your JavaScript bundle larger.  const videos = talks.map(talk => talk.video);  // 3. Pass the data down to the components that will run in the browser.  return <SearchableVideoList videos={videos} />;}
```

Example 2 (unknown):
```unknown
<Suspense fallback={<TalksLoading />}>  <Talks confId={conf.id} /></Suspense>
```

---

## Thinking in React

**URL:** https://react.dev/learn/thinking-in-react#where-to-go-from-here

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

## Rendering Lists

**URL:** https://react.dev/learn/rendering-lists

**Contents:**
- Rendering Lists
  - You will learn
- Rendering data from arrays
- Filtering arrays of items
  - Pitfall
- Keeping list items in order with key
  - Note
      - Deep Dive
    - Displaying several DOM nodes for each list item
  - Where to get your key

You will often want to display multiple similar components from a collection of data. You can use the JavaScript array methods to manipulate an array of data. On this page, you’ll use filter() and map() with React to filter and transform your array of data into an array of components.

Say that you have a list of content.

The only difference among those list items is their contents, their data. You will often need to show several instances of the same component using different data when building interfaces: from lists of comments to galleries of profile images. In these situations, you can store that data in JavaScript objects and arrays and use methods like map() and filter() to render lists of components from them.

Here’s a short example of how to generate a list of items from an array:

Notice the sandbox above displays a console error:

You’ll learn how to fix this error later on this page. Before we get to that, let’s add some structure to your data.

This data can be structured even more.

Let’s say you want a way to only show people whose profession is 'chemist'. You can use JavaScript’s filter() method to return just those people. This method takes an array of items, passes them through a “test” (a function that returns true or false), and returns a new array of only those items that passed the test (returned true).

You only want the items where profession is 'chemist'. The “test” function for this looks like (person) => person.profession === 'chemist'. Here’s how to put it together:

Arrow functions implicitly return the expression right after =>, so you didn’t need a return statement:

However, you must write return explicitly if your => is followed by a { curly brace!

Arrow functions containing => { are said to have a “block body”. They let you write more than a single line of code, but you have to write a return statement yourself. If you forget it, nothing gets returned!

Notice that all the sandboxes above show an error in the console:

You need to give each array item a key — a string or a number that uniquely identifies it among other items in that array:

JSX elements directly inside a map() call always need keys!

Keys tell React which array item each component corresponds to, so that it can match them up later. This becomes important if your array items can move (e.g. due to sorting), get inserted, or get deleted. A well-chosen key helps React infer what exactly has happened, and make the correct updates to the DOM tree.

Rather than

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<ul>  <li>Creola Katherine Johnson: mathematician</li>  <li>Mario José Molina-Pasquel Henríquez: chemist</li>  <li>Mohammad Abdus Salam: physicist</li>  <li>Percy Lavon Julian: chemist</li>  <li>Subrahmanyan Chandrasekhar: astrophysicist</li></ul>
```

Example 2 (javascript):
```javascript
const people = [  'Creola Katherine Johnson: mathematician',  'Mario José Molina-Pasquel Henríquez: chemist',  'Mohammad Abdus Salam: physicist',  'Percy Lavon Julian: chemist',  'Subrahmanyan Chandrasekhar: astrophysicist'];
```

Example 3 (javascript):
```javascript
const listItems = people.map(person => <li>{person}</li>);
```

Example 4 (unknown):
```unknown
return <ul>{listItems}</ul>;
```

---

## Render and Commit

**URL:** https://react.dev/learn/render-and-commit

**Contents:**
- Render and Commit
  - You will learn
- Step 1: Trigger a render
  - Initial render
  - Re-renders when state updates
- Step 2: React renders your components
  - Pitfall
      - Deep Dive
    - Optimizing performance
- Step 3: React commits changes to the DOM

Before your components are displayed on screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

Illustrated by Rachel Lee Nabors

There are two reasons for a component to render:

When your app starts, you need to trigger the initial render. Frameworks and sandboxes sometimes hide this code, but it’s done by calling createRoot with the target DOM node, and then calling its render method with your component:

Try commenting out the root.render() call and see the component disappear!

Once the component has been initially rendered, you can trigger further renders by updating its state with the set function. Updating your component’s state automatically queues a render. (You can imagine these as a restaurant guest ordering tea, dessert, and all sorts of things after putting in their first order, depending on the state of their thirst or hunger.)

Illustrated by Rachel Lee Nabors

After you trigger a render, React calls your components to figure out what to display on screen. “Rendering” is React calling your components.

This process is recursive: if the updated component returns some other component, React will render that component next, and if that component also returns something, it will render that component next, and so on. The process will continue until there are no more nested components and React knows exactly what should be displayed on screen.

In the following example, React will call Gallery() and Image() several times:

Rendering must always be a pure calculation:

Otherwise, you can encounter confusing bugs and unpredictable behavior as your codebase grows in complexity. When developing in “Strict Mode”, React calls each component’s function twice, which can help surface mistakes caused by impure functions.

The default behavior of rendering all components nested within the updated component is not optimal for performance if the updated component is very high in the tree. If you run into a performance issue, there are several opt-in ways to solve it described in the Performance section. Don’t optimize prematurely!

After rendering (calling) your components, React will modify the DOM.

Rea

*[Content truncated]*

---

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui#your-ui-as-a-tree

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

## Responding to Events

**URL:** https://react.dev/learn/responding-to-events

**Contents:**
- Responding to Events
  - You will learn
- Adding event handlers
  - Pitfall
  - Reading props in event handlers
  - Passing event handlers as props
  - Naming event handler props
  - Note
- Event propagation
  - Pitfall

React lets you add event handlers to your JSX. Event handlers are your own functions that will be triggered in response to interactions like clicking, hovering, focusing form inputs, and so on.

To add an event handler, you will first define a function and then pass it as a prop to the appropriate JSX tag. For example, here is a button that doesn’t do anything yet:

You can make it show a message when a user clicks by following these three steps:

You defined the handleClick function and then passed it as a prop to <button>. handleClick is an event handler. Event handler functions:

By convention, it is common to name event handlers as handle followed by the event name. You’ll often see onClick={handleClick}, onMouseEnter={handleMouseEnter}, and so on.

Alternatively, you can define an event handler inline in the JSX:

Or, more concisely, using an arrow function:

All of these styles are equivalent. Inline event handlers are convenient for short functions.

Functions passed to event handlers must be passed, not called. For example:

The difference is subtle. In the first example, the handleClick function is passed as an onClick event handler. This tells React to remember it and only call your function when the user clicks the button.

In the second example, the () at the end of handleClick() fires the function immediately during rendering, without any clicks. This is because JavaScript inside the JSX { and } executes right away.

When you write code inline, the same pitfall presents itself in a different way:

Passing inline code like this won’t fire on click—it fires every time the component renders:

If you want to define your event handler inline, wrap it in an anonymous function like so:

Rather than executing the code inside with every render, this creates a function to be called later.

In both cases, what you want to pass is a function:

Read more about arrow functions.

Because event handlers are declared inside of a component, they have access to the component’s props. Here is a button that, when clicked, shows an alert with its message prop:

This lets these two buttons show different messages. Try changing the messages passed to them.

Often you’ll want the parent component to specify a child’s event handler. Consider buttons: depending on where you’re using a Button component, you might want to execute a different function—perhaps one plays a movie and another uploads an image.

To do this, pass a prop the component receives from its parent as 

*[Content truncated]*

**Examples:**

Example 1 (unknown):
```unknown
<button onClick={function handleClick() {  alert('You clicked me!');}}>
```

Example 2 (javascript):
```javascript
<button onClick={() => {  alert('You clicked me!');}}>
```

Example 3 (unknown):
```unknown
// This alert fires when the component renders, not when clicked!<button onClick={alert('You clicked me!')}>
```

Example 4 (javascript):
```javascript
<button onClick={() => alert('You clicked me!')}>
```

---

## Synchronizing with Effects

**URL:** https://react.dev/learn/synchronizing-with-effects

**Contents:**
- Synchronizing with Effects
  - You will learn
- What are Effects and how are they different from events?
  - Note
- You might not need an Effect
- How to write an Effect
  - Step 1: Declare an Effect
  - Pitfall
  - Step 2: Specify the Effect dependencies
  - Pitfall

Some components need to synchronize with external systems. For example, you might want to control a non-React component based on the React state, set up a server connection, or send an analytics log when a component appears on the screen. Effects let you run some code after rendering so that you can synchronize your component with some system outside of React.

Before getting to Effects, you need to be familiar with two types of logic inside React components:

Rendering code (introduced in Describing the UI) lives at the top level of your component. This is where you take the props and state, transform them, and return the JSX you want to see on the screen. Rendering code must be pure. Like a math formula, it should only calculate the result, but not do anything else.

Event handlers (introduced in Adding Interactivity) are nested functions inside your components that do things rather than just calculate them. An event handler might update an input field, submit an HTTP POST request to buy a product, or navigate the user to another screen. Event handlers contain “side effects” (they change the program’s state) caused by a specific user action (for example, a button click or typing).

Sometimes this isn’t enough. Consider a ChatRoom component that must connect to the chat server whenever it’s visible on the screen. Connecting to a server is not a pure calculation (it’s a side effect) so it can’t happen during rendering. However, there is no single particular event like a click that causes ChatRoom to be displayed.

Effects let you specify side effects that are caused by rendering itself, rather than by a particular event. Sending a message in the chat is an event because it is directly caused by the user clicking a specific button. However, setting up a server connection is an Effect because it should happen no matter which interaction caused the component to appear. Effects run at the end of a commit after the screen updates. This is a good time to synchronize the React components with some external system (like network or a third-party library).

Here and later in this text, capitalized “Effect” refers to the React-specific definition above, i.e. a side effect caused by rendering. To refer to the broader programming concept, we’ll say “side effect”.

Don’t rush to add Effects to your components. Keep in mind that Effects are typically used to “step out” of your React code and synchronize with some external system. This includes browser APIs, third-party w

*[Content truncated]*

**Examples:**

Example 1 (python):
```python
import { useEffect } from 'react';
```

Example 2 (javascript):
```javascript
function MyComponent() {  useEffect(() => {    // Code here will run after *every* render  });  return <div />;}
```

Example 3 (unknown):
```unknown
<VideoPlayer isPlaying={isPlaying} />;
```

Example 4 (unknown):
```unknown
function VideoPlayer({ src, isPlaying }) {  // TODO: do something with isPlaying  return <video src={src} />;}
```

---

## Describing the UI

**URL:** https://react.dev/learn/describing-the-ui#whats-next

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

## Quick Start

**URL:** https://react.dev/learn#adding-styles

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

## Quick Start

**URL:** https://react.dev/learn#displaying-data

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

## Thinking in React

**URL:** https://react.dev/learn/thinking-in-react

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
