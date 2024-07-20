const body = document.querySelector('body');
const sidebar = body.querySelector('nav');
const toggle = body.querySelector(".toggle");
const searchBtn = body.querySelector(".search-box");
const modeSwitch = body.querySelector(".toggle-switch");
const modeText = body.querySelector(".mode-text");

// Function to toggle sidebar visibility
function toggleSidebar() {
  sidebar.classList.toggle("close");
}
 
// Function to toggle dark mode
function toggleTheme() {
    body.classList.toggle("dark");
    const isDark = body.classList.contains("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");
    modeText.innerText = isDark ? "Modo claro" : "Modo oscuro";
  }

  function loadThemePreference() {
    const storedTheme = localStorage.getItem("theme");
    if (storedTheme === "dark") {
      body.classList.add("dark");
    } else if (storedTheme === "light") {
      body.classList.remove("dark");
    }
    if (body.classList.contains("dark")) {
      modeText.innerText = "Modo claro";
    } else {
      modeText.innerText = "Modo oscuro";
    }
  }

// Event listeners for sidebar interactions
toggle.addEventListener("click", toggleSidebar);
modeSwitch.addEventListener("click", toggleTheme);

// Event listener for theme switch, applying preference
modeSwitch.addEventListener("click", toggleTheme);

// Load theme preference on initial page load
loadThemePreference();