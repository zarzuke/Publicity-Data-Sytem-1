function formatPhoneNumber(phoneNumber) {
    // Asegúrate de que el número sea solo dígitos
    const cleaned = ('' + phoneNumber).replace(/\D/g, '');
  
    // Expresión regular más flexible
    const match = cleaned.match(/^(\d{4})(\d{3})(\d{4})$/);
  
    if (match) {
      return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phoneNumber; // Devuelve el teléfono sin cambios si no coincide con el formato
  }


// Función para actualizar la previsualización
function updatePreview() {
    const titleInput = document.getElementById('title');
    const nameInput = document.getElementById('name');
    const surnameInput = document.getElementById('surname');
    const phoneInput = document.getElementById('phone');
    const dateInput = document.getElementById('date');
    const totalCostInput = document.getElementById('total-cost');
    const descriptionInput = document.getElementById('description');
    const fileInput = document.getElementById('file');

    const previewImage = document.getElementById('preview-image');
    const previewTitle = document.querySelector('.preview-card-title');
    const previewName = document.querySelector('.preview-card-name');
    const previewLastname = document.querySelector('.preview-card-lastname');
    const previewJobTitle = document.querySelector('.preview-job-title');
    const previewDate = document.querySelector('.preview-date');
    const previewPhone = document.querySelector('.preview-phone');
    const previewDescription = document.querySelector('.preview-card-description');

// Establecer los valores de la previsualización
    previewTitle.textContent = titleInput.value;
    previewName.textContent = nameInput.value;
    previewLastname.textContent = surnameInput.value;


// Obtener todos los checkboxes que están seleccionados (checked)
    const selectedJobTypes = Array.from(document.querySelectorAll('input[name="job-type"]:checked')).map(checkbox => checkbox.id);
    previewJobTitle.textContent = selectedJobTypes.length > 0 ? selectedJobTypes.join(', ') : '';

    let jobTitleText = selectedJobTypes.join(', ');
    previewJobTitle.textContent = jobTitleText;


    previewDate.textContent = dateInput.value;
    previewPhone.textContent = `(${phoneInput.value.slice(0, 3)}) ${phoneInput.value.slice(3)}`;
    previewDescription.textContent = descriptionInput.value;

    // Formatear el número de teléfono
    const formattedPhone = formatPhoneNumber(phoneInput.value);
    previewPhone.textContent = formattedPhone;
    
    previewDescription.textContent = descriptionInput.value;

// Previsualizar la imagen cargada
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImage.src = e.target.result; // Imagen cargada seleccionada
        };
        reader.readAsDataURL(fileInput.files[0]);
    } else {
        previewImage.src = '../static/img/default-image.jpg'; // Imagen predeterminada. Asegúrate de que la ruta sea correcta
    }
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && addModal.classList.contains('visible')) {
      closeButton.click(); // Simulate click on close button
    }
  });

// Agregar evento de entrada para actualizar la previsualización
const formInputs = document.querySelectorAll('.add-form input, .add-form textarea, #file');
formInputs.forEach((input) => {
    input.addEventListener('input', updatePreview);
});

searchInput = document.getElementById("searchInput"),
    cardList = document.getElementById("cardList"),
    cardItems = cardList.getElementsByClassName("card-item"),
    addBtn = document.querySelector('.add-btn'),
    addModal = document.querySelector('.add-modal'),
    modalBackdrop = document.querySelector('.modal-backdrop'),
    closeButton = addModal.querySelector('.close-button'),
    jobTypeButtons = addModal.querySelectorAll('.job-type-btn'),
    addForm = addModal.querySelector('.add-form');

let previouslySelectedJobTypeBtn = null; // Store previously selected button

jobTypeButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
        if (previouslySelectedJobTypeBtn !== btn) { // Check if selection changed
            previouslySelectedJobTypeBtn.classList.remove('active'); // Remove active class from previous
            btn.classList.add('active'); // Add active class to current
            updatePreview(); // Update preview
            previouslySelectedJobTypeBtn = btn; // Update previously selected button
        }
    });
});

// Agregar evento para el envío del formulario
addForm.addEventListener('submit-btn', (event) => {
    event.preventDefault();

    const name = addForm.elements.name.value;
    const surname = addForm.elements.surname.value;
    const phone = addForm.elements.phone.value;

    // Obtener todos los tipos de trabajo seleccionados
    const jobTypes = Array.from(document.querySelectorAll('input[name="job-type"]:checked')).map(checkbox => checkbox.value);
    
    const totalCost = addForm.elements['total-cost'].value;
    const downPayment = addForm.elements['down-payment'].value;
    const remaining = addForm.elements.remaining.value;
    const description = addForm.elements.description.value;

    console.log('Name:', name);
    console.log('Surname:', surname);
    console.log('Phone:', phone);
    console.log('Job Types:', jobTypes.join(', ')); // Mostrar todos los tipos de trabajo seleccionados
    console.log('Total Cost:', totalCost);
    console.log('Down Payment:', downPayment);
    console.log('Remaining:', remaining);
    console.log('Description:', description);
});


// Funcion de buscar en el input
searchInput.addEventListener("input", () => {
    const searchTerm = searchInput.value.toLowerCase();
    for (let i = 0; i < cardItems.length; i++) {
        const cardItem = cardItems[i];
        const cardContent = cardItem.textContent.toLowerCase();
        if (cardContent.includes(searchTerm)) {
            cardItem.style.display = "block";
        } else {
            cardItem.style.display = "none";
        }
    }
});

addBtn.addEventListener('click', () => {
    addModal.classList.remove('hidden');
    addModal.classList.add('visible');
    modalBackdrop.classList.remove('hidden');
    modalBackdrop.classList.add('visible');
    document.body.style.overflow = 'hidden'; // Bloquea el scroll
    addModal.focus(); // Enfoca la ventana modal

    updatePreview();
});

closeButton.addEventListener('click', () => {
    addModal.classList.add('hidden');
    addModal.classList.remove('visible');
    modalBackdrop.classList.add('hidden');
    modalBackdrop.classList.remove('visible');
    document.body.style.overflow = 'auto'; // Restaura el scroll
});

let currentDeleteItem = null;
let currentDeleteId = null;

function handleDelete(event, itemId) {
    event.stopPropagation();
    event.preventDefault();
    
    currentDeleteItem = this.closest('.card-item'); // Guardar el elemento a eliminar
    currentDeleteId = itemId; // Guardar el id del elemento a eliminar

    document.body.style.overflow = 'hidden'; // Bloquea el scroll
    document.getElementById('confirmationModal').classList.remove('hidden'); // Mostrar el modal
    modalBackdrop.classList.remove('hidden');
    modalBackdrop.classList.add('visible');
}

// Agregar evento de confirmación para eliminar
document.getElementById('confirmDelete').addEventListener('click', function() {
    if (currentDeleteItem) {
        currentDeleteItem.remove(); // Eliminar el elemento del DOM
    }
    document.getElementById('confirmationModal').classList.add('hidden'); // Ocultar el modal

    currentDeleteItem = null; // Restablecer la variable
    document.body.style.overflow = 'auto'; // Restaura el scroll
    modalBackdrop.classList.add('hidden');
    modalBackdrop.classList.remove('visible');

    // Redirección directa a la URL de Flask usando el id guardado
    const url = `/delete/${currentDeleteId}`;
    window.location.href = url;
});



// Agregar evento de cancelación para eliminar
document.getElementById('cancelDelete').addEventListener('click', function() {
    document.getElementById('confirmationModal').classList.add('hidden'); // Ocultar el modal
    currentDeleteItem = null; // Restablecer la variable
    currentDeleteId = null; // Restablecer el id
    document.body.style.overflow = 'auto'; // Restaura el scroll
    modalBackdrop.classList.add('hidden');
    modalBackdrop.classList.remove('visible');
});


// Mostrar modal de confirmación al hacer clic en el botón de eliminar
document.querySelectorAll('.delete').forEach(button => {
    button.addEventListener('click', function() {
        document.body.style.overflow = 'hidden'; // Bloquea el scroll
        document.getElementById('confirmationModal').classList.remove('hidden'); // Mostrar el modal
        currentDeleteItem = this.closest('.card-item'); // Guardar el elemento a eliminar
        currentDeleteId = this.querySelector('#nfo').getAttribute('value'); // Guardar el id del elemento a eliminar
        modalBackdrop.classList.remove('hidden');
        modalBackdrop.classList.add('visible');
    });
});


// Función para formatear números con separadores de miles
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

// CALCULAR RESTANTE
document.addEventListener("DOMContentLoaded", function() {
    const totalCostInput = document.getElementById('total-cost');
    const downPaymentInput = document.getElementById('down-payment');
    const remainingInput = document.getElementById('remaining');
    const currencySelect = document.getElementById('currency');

    function calculateRemaining() {
        const totalCost = parseFloat(totalCostInput.value) || 0;
        const downPayment = parseFloat(downPaymentInput.value) || 0;
        const remaining = totalCost - downPayment;

        // Asegúrate de no mostrar un valor negativo
        remainingInput.value = remaining < 0 ? '0' : formatNumber(remaining);
    }

    totalCostInput.oninput = calculateRemaining; // Calcula al cambiar el costo total
    downPaymentInput.oninput = calculateRemaining; // Calcula al cambiar el abono

    // Agregar un evento de cambio para el selector de moneda
    currencySelect.addEventListener('change', calculateRemaining);
});

document.addEventListener('click', function (event) {
    const sidebar = document.querySelector('.sidebar');
    const toggle = document.querySelector('.toggle');
    const searchInput = document.getElementById("searchInput");
    const cardList = document.getElementById("cardList");

    const clickedElement = event.target;
    const isClickOutside = !sidebar.contains(clickedElement) &&
                            !toggle.contains(clickedElement) &&
                            !clickedElement.closest('.card-item') &&
                            !searchInput.contains(clickedElement); // Evitar cerrarlo al hacer clic dentro del input de búsqueda

    if (isClickOutside) {
      sidebar.classList.add('close');
    }
});

function resetPreview() {
    // Restablecer los valores de la previsualización a los valores iniciales
    const initialTitle = "";
    const initialName = "";
    const initialLastname = "";
    const initialJobTitle = "";
    const initialDate = "";
    const initialPhone = "";
    const initialDescription = "";

    // Actualizar los elementos de la previsualización con los valores iniciales
    const previewTitle = document.querySelector('.preview-card-title');
    const previewName = document.querySelector('.preview-card-name');
    const previewLastname = document.querySelector('.preview-card-lastname');
    const previewJobTitle = document.querySelector('.preview-job-title');
    const previewDate = document.querySelector('.preview-date');
    const previewPhone = document.querySelector('.preview-phone');
    const previewDescription = document.querySelector('.preview-card-description');

    previewTitle.textContent = initialTitle;
    previewName.textContent = initialName;
    previewLastname.textContent = initialLastname;
    previewJobTitle.textContent = initialJobTitle;
    previewDate.textContent = initialDate;
    previewPhone.textContent = initialPhone;
    previewDescription.textContent = initialDescription;
}

// Asignar la función al botón de restablecimiento
const resetButton = document.querySelector('.reset-btn');
resetButton.addEventListener('click', resetPreview);

function openDetails(title, date, name, phone, description) {
    const url = `details.html?title=${encodeURIComponent(title)}&date=${encodeURIComponent(date)}&name=${encodeURIComponent(name)}&phone=${encodeURIComponent(phone)}&description=${encodeURIComponent(description)}`;
    window.open(url, '_blank'); // Abre en una nueva pestaña
}

// JOB ANIMACION Y ARREGLO

document.addEventListener('DOMContentLoaded', () => {
    const cardItems = document.querySelectorAll('.card-item');

    cardItems.forEach(item => {
        const jobTypesContainer = item.querySelector('.job-types-container');
        const jobTypesWrapper = item.querySelector('.job-types-wrapper');

        // Función para verificar si el contenido desborda
        const isOverflowing = () => {
            return jobTypesContainer.scrollWidth > jobTypesWrapper.clientWidth;
        };

        // Ajusta el ancho del contenedor basado en su contenido
        jobTypesContainer.style.width = `${jobTypesContainer.scrollWidth}px`;

        let scrollAmount = 0;
        const scrollStep = 1; // Cambia la velocidad de desplazamiento aquí
        let scrolling; // Variable para mantener el ciclo de desplazamiento
        let direction = 1; // Direccion del desplazamiento: 1 para izquierda, -1 para derecha

        const scroll = () => {
            if (direction === 1) { // Desplazamiento hacia la izquierda
                if (scrollAmount < jobTypesContainer.scrollWidth - jobTypesWrapper.clientWidth) {
                    scrollAmount += scrollStep;
                } else {
                    // Cambia la dirección al llegar al final
                    direction = -1; // Cambia a desplazamiento a la derecha
                }
            } else { // Desplazamiento hacia la derecha
                if (scrollAmount > 0) {
                    scrollAmount -= scrollStep;
                } else {
                    // Cambia la dirección al llegar al inicio
                    direction = 1; // Cambia a desplazamiento a la izquierda
                }
            }
            jobTypesContainer.style.transform = `translateX(-${scrollAmount}px)`;
            scrolling = requestAnimationFrame(scroll);
        };

        // Al pasar el mouse
        item.addEventListener('mouseenter', () => {
            if (isOverflowing()) {
                scrolling = requestAnimationFrame(scroll);
            }
        });

        // Al salir del mouse
        item.addEventListener('mouseleave', () => {
            jobTypesContainer.style.transform = 'translateX(0)'; // Resetea la posición
            cancelAnimationFrame(scrolling); // Detiene el desplazamiento
            scrollAmount = 0; // Resetea el desplazamiento
            direction = 1; // Resetea la dirección
        });
    });
});