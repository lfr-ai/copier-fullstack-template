/**
 * Main application entry point.
 */
import './styles/main.css';

const appElement = document.getElementById('app');

if (appElement) {
  appElement.innerHTML = `
    <main>
      <h1>Welcome</h1>
      <p>Application is running.</p>
    </main>
  `;
}
