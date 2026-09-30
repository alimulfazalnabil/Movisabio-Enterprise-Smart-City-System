import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './index.css';

// Locate the root HTML container element
const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Failed to find the root element (#root) in the DOM.');
}

// Mount the MoviSabio Enterprise Command Center using React 18 createRoot API
createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
