// Obtén los botones
const addButton = document.getElementById('addButton');
const sortButton = document.getElementById('sortButton');
const floatingButtons = document.querySelector('.floating-buttons');

// Variable para rastrear la posición anterior del scroll
let lastScrollY = window.scrollY;

// Escucha el evento de scroll
window.addEventListener('scroll', () => {
    // Si estamos hacia abajo
    if (window.scrollY > 1) { 
        if (window.scrollY > lastScrollY) { // Si estamos bajando
            // Mostrar los botones
            floatingButtons.classList.add('show');
            floatingButtons.classList.remove('hide');
        } else { // Si estamos subiendo
            // Ocultar los botones
            floatingButtons.classList.add('hide');
            floatingButtons.classList.remove('show');
        }
    } else {
        // Si no estamos hacia abajo, ocultar los botones
        floatingButtons.classList.remove('show');
        floatingButtons.classList.remove('hide');
    }
    lastScrollY = window.scrollY; // Actualiza la posición del scroll
});

// Funciones para manejar los clics en los botones
addButton.addEventListener('click', () => {
    // Aquí debes llamar a la función que abre el modal de añadir
    const addModal = document.querySelector('.add-modal');
    addModal.classList.add('visible'); // Mostrar el modal
});






