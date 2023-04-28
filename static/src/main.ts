// the main js file for the application
// this file should contain any code that is needed on every page of the site

// import the polyfill for modulepreload
import "vite/modulepreload-polyfill";

// import the tailwind css file so that vite can bundle it
// including it here and making sure the tailwind config contains
// the Django templates means one build step instead of two (one for js,
// one for Django)
import "./main.css";
