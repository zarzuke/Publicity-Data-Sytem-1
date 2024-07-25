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

  // Aplicar estilos del modo claro y oscuro al scroll
  if (isDark) {
    document.documentElement.style.setProperty("--scrollbar-track-color", "#333");
    document.documentElement.style.setProperty("--scrollbar-thumb-color", "#555");
    document.documentElement.style.setProperty("--scrollbar-thumb-hover-color", "#777");
  } else {
    document.documentElement.style.setProperty("--scrollbar-track-color", "#f1f1f1");
    document.documentElement.style.setProperty("--scrollbar-thumb-color", "#888");
    document.documentElement.style.setProperty("--scrollbar-thumb-hover-color", "#555");
  }
}

function loadThemePreference() {
  const storedTheme = localStorage.getItem("theme");
  if (storedTheme === "dark") {
    body.classList.add("dark");
    document.documentElement.style.setProperty("--scrollbar-track-color", "#333");
    document.documentElement.style.setProperty("--scrollbar-thumb-color", "#555");
    document.documentElement.style.setProperty("--scrollbar-thumb-hover-color", "#777");
  } else if (storedTheme === "light") {
    body.classList.remove("dark");
    document.documentElement.style.setProperty("--scrollbar-track-color", "#f1f1f1");
    document.documentElement.style.setProperty("--scrollbar-thumb-color", "#888");
    document.documentElement.style.setProperty("--scrollbar-thumb-hover-color", "#555");
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

addBtn.addEventListener('click', () => {
  addModal.classList.remove('hidden');
  addModal.classList.add('visible');
  modalBackdrop.classList.remove('hidden');
  modalBackdrop.classList.add('visible');
  document.body.style.overflow = 'hidden'; // Bloquea el scroll
  addModal.focus(); // Enfoca la ventana modal
});

closeButton.addEventListener('click', () => {
  addModal.classList.add('hidden');
  addModal.classList.remove('visible');
  modalBackdrop.classList.add('hidden');
  modalBackdrop.classList.remove('visible');
  document.body.style.overflow = 'auto'; // Restaura el scroll
});