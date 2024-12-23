const body = document.querySelector('body');
const sidebar = body.querySelector('nav');
const toggle = body.querySelector('.toggle');
const modeSwitch = body.querySelector('.toggle-switch');
const modeText = body.querySelector('.mode-text');

// Verificamos si search-box y el input existen antes de intentar usarlos
const searchBtn = body.querySelector('.search-box');
const searchInput = body.querySelector('#searchInput'); 

// Function to toggle sidebar visibility
function toggleSidebar() {
  sidebar.classList.toggle("close");
}

// Function to toggle search and focus on input
function toggleSearch() {
  if (searchInput) { // Solo ejecuta si searchInput existe
    sidebar.classList.remove("close");
    setTimeout(() => {
      searchInput.focus();
    }, 300);
  }
}

// Function to toggle dark mode
function toggleTheme() {
  body.classList.toggle("dark");
  body.classList.toggle('dark-mode');
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
    body.classList.toggle('dark-mode');
    document.documentElement.style.setProperty("--scrollbar-track-color", "#333");
    document.documentElement.style.setProperty("--scrollbar-thumb-color", "#555");
    document.documentElement.style.setProperty("--scrollbar-thumb-hover-color", "#777");
  } else {
    body.classList.remove("dark");
    document.documentElement.style.setProperty("--scrollbar-track-color", "#f1f1f1");
    document.documentElement.style.setProperty("--scrollbar-thumb-color", "#888");
    document.documentElement.style.setProperty("--scrollbar-thumb-hover-color", "#555");
  }
  modeText.innerText = body.classList.contains("dark") ? "Modo claro" : "Modo oscuro";
}

// Event listeners for sidebar interactions
toggle.addEventListener("click", toggleSidebar);
modeSwitch.addEventListener("click", toggleTheme);

// Solo agrega el evento de búsqueda si el botón existe
if (searchBtn) {
  searchBtn.addEventListener("click", toggleSearch);
}

// Load theme preference on initial page load
loadThemePreference();

// Código para abrir/cerrar el modal
/*
addBtn = document.querySelector('.add-btn');

addBtn.addEventListener('click', () => {
  addModal.classList.remove('hidden');
  addModal.classList.add('visible');
  modalBackdrop.classList.remove('hidden');
  modalBackdrop.classList.add('visible');
  document.body.style.overflow = 'hidden'; // Bloquea el scroll
  addModal.focus(); // Enfoca la ventana modal
});

addModal = document.querySelector('.add-modal');
closeButton = addModal.querySelector('.close-button');

closeButton.addEventListener('click', () => {
  addModal.classList.add('hidden');
  addModal.classList.remove('visible');
  modalBackdrop.classList.add('hidden');
  modalBackdrop.classList.remove('visible');
  document.body.style.overflow = 'auto'; // Restaura el scroll
});
*/

document.querySelectorAll('.grid-item').forEach(item => {
  item.addEventListener('click', () => {
      item.classList.toggle('active');
  });
});
