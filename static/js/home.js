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

function updatePreview() {
    const titleInput = document.getElementById('title');
    const nameInput = document.getElementById('name');
    const surnameInput = document.getElementById('surname');
    const phoneInput = document.getElementById('phone');
    const dateInput = document.getElementById('date');
    const descriptionInput = document.getElementById('description');
    const fileInput = document.getElementById('file');

    const previewImage = document.getElementById('preview-image');
    const previewTitle = document.querySelector('.preview-card-title');
    const previewName = document.querySelector('.card-name');
    const previewSurname = document.querySelector('.card-surname');
    const previewDate = document.querySelector('.preview-date'); // Añadir esta línea
    const previewPhone = document.querySelector('.preview-phone');
    const previewDescription = document.querySelector('.preview-card-description');

    // Establecer los valores de la previsualización
    previewTitle.textContent = titleInput.value;
    previewName.textContent = nameInput.value;
    previewSurname.textContent = surnameInput.value;

    // Formatear y establecer la fecha
    if (dateInput.value) {
        previewDate.textContent = `${dateInput.value}`; // Establecer la fecha en la previsualización
    } else {
        previewDate.textContent = ""; // Limpiar si no hay fecha
    }

    const selectedJobTypes = Array.from(document.querySelectorAll('input[name="job-type"]:checked')).map(checkbox => {
        return checkbox.closest('.job-type-btn').textContent.trim();
    });

    const previewJobTypesContainer = document.querySelector('.preview-job-types-container');
    previewJobTypesContainer.innerHTML = ''; // Limpiar los tipos de trabajo existentes

    selectedJobTypes.forEach(jobType => {
        const jobTypeElement = document.createElement('span');
        jobTypeElement.textContent = jobType;
        jobTypeElement.classList.add('types', `job-type-${jobType.toLowerCase().replace(' ', '-')}`);
        previewJobTypesContainer.appendChild(jobTypeElement);
    });

    // Iniciar desplazamiento si hay más de un tipo de trabajo
    if (selectedJobTypes.length > 1) {
        startPreviewScrolling(previewJobTypesContainer);
    } else {
        cancelAnimationFrame(scrollingPreview); // Detener desplazamiento si no hay suficientes elementos
        previewJobTypesContainer.style.transform = 'translateX(0px)'; // Resetea la posición
    }

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
        previewImage.src = '../static/img/default-image.jpg'; // Imagen predeterminada
    }
}


document.addEventListener('keydown', function (event) {
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
document.getElementById('confirmDelete').addEventListener('click', function () {
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
document.getElementById('cancelDelete').addEventListener('click', function () {
    document.getElementById('confirmationModal').classList.add('hidden'); // Ocultar el modal
    currentDeleteItem = null; // Restablecer la variable
    currentDeleteId = null; // Restablecer el id
    document.body.style.overflow = 'auto'; // Restaura el scroll
    modalBackdrop.classList.add('hidden');
    modalBackdrop.classList.remove('visible');
});


// Mostrar modal de confirmación al hacer clic en el botón de eliminar
document.querySelectorAll('.delete').forEach(button => {
    button.addEventListener('click', function () {
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
    return Math.round(num).toString();
}

// CALCULAR RESTANTE
document.addEventListener("DOMContentLoaded", function () {
    const totalCostInput = document.getElementById('total-cost');
    const downPaymentInput = document.getElementById('down-payment');
    const remainingInput = document.getElementById('remaining');
    const currencySelect = document.getElementById('currency');

    function calculateRemaining() {
        const totalCost = parseInt(totalCostInput.value) || 0;
        const downPayment = parseInt(downPaymentInput.value) || 0;
        const remaining = parseInt(totalCost) - parseInt(downPayment);

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
    // Valores iniciales para la previsualización
    const initialTitle = "";
    const initialName = "";
    const initialLastname = "";
    const initialJobTitle = ""; // Si no se está usando, se puede eliminar
    const initialDate = "";
    const initialPhone = "";
    const initialDescription = "";

    // Actualizar los campos del formulario con los valores iniciales
    document.getElementById('title').value = initialTitle;
    document.getElementById('name').value = initialName;
    document.getElementById('surname').value = initialLastname;
    document.getElementById('phone').value = initialPhone;
    document.getElementById('date').value = initialDate;
    document.getElementById('description').value = initialDescription;

    // Reiniciar el estado de los checkboxes
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach((checkbox) => {
        checkbox.checked = false;
    });

    // Reiniciar el estado de los radio buttons
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    radioButtons.forEach((radio) => {
        radio.checked = false;
    });

    // Reiniciar selecciones de listas desplegables
    const dropdowns = document.querySelectorAll('select');
    dropdowns.forEach((dropdown) => {
        dropdown.selectedIndex = 0; // Restablece a la primera opción
    });

    // Reiniciar los tipos de trabajo
    jobTypeButtons.forEach((btn) => {
        btn.classList.remove('active'); // Eliminar la clase de botón activo
    });

    // Actualizar la previsualización para reflejar el estado limpio
    updatePreview();
}

// Agregar evento para el botón de restablecer
document.querySelector('.reset-btn').addEventListener('click', function (event) {
    resetPreview();  // Llama a la función para restablecer y actualizar la previsualización

    // Prevenir comportamiento predeterminado si es necesario
    event.preventDefault(); // Esto no es estrictamente necesario ya que el botón es de tipo "reset"
});



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

function handleUserOptionChange() {
    const userOption = document.getElementById('user-option').value;
    const existingUserSelect = document.getElementById('existing-user-select');

    // Reiniciar valores al seleccionar "Nuevo cliente"
    if (userOption === 'new') {
        document.getElementById('name').value = "";
        document.getElementById('surname').value = "";
        document.getElementById('phone').value = "";
        existingUserSelect.style.display = 'none'; // Ocultar el selector de 'Cliente existente'
    } else if (userOption === 'existing') {
        // Limpiar los campos de Nuevo cliente si se está seleccionando Cliente existente
        document.getElementById('name').value = "";
        document.getElementById('surname').value = "";
        document.getElementById('phone').value = "";

        existingUserSelect.style.display = 'block'; // Mostrar el selector de 'Cliente existente'
        document.getElementById('name').disabled = false;
        document.getElementById('surname').disabled = false;
        document.getElementById('phone').disabled = false;
    } else {
        existingUserSelect.style.display = 'none'; // Mantener oculto si no se selecciona ninguna opción
        document.getElementById('name').disabled = true;
        document.getElementById('surname').disabled = true;
        document.getElementById('phone').disabled = true;
    }

    // Habilitar o deshabilitar los campos según la opción seleccionada
    if (userOption === 'new') {
        document.getElementById('name').disabled = false;
        document.getElementById('surname').disabled = false;
        document.getElementById('phone').disabled = false;
    }
}

function autocompleteUser() {
    const existingUsers = document.getElementById('existing-users');
    const selectedOption = existingUsers.options[existingUsers.selectedIndex];
    const name = selectedOption.getAttribute('data-name');
    const surname = selectedOption.getAttribute('data-surname');
    const phone = selectedOption.getAttribute('data-phone');

    if (name) {
        document.getElementById('name').value = name;
        document.getElementById('surname').value = surname;
        document.getElementById('phone').value = phone;

        // No habilitar los campos, mantenerlos deshabilitados
        // document.getElementById('name').disabled = false; // Elimina esta línea
        // document.getElementById('surname').disabled = false; // Elimina esta línea
        // document.getElementById('phone').disabled = false; // Elimina esta línea
    }
}

function clearUserFields() {
    document.getElementById('name').value = "";
    document.getElementById('surname').value = "";
    document.getElementById('phone').value = "";

}

let scrollingPreview;

function startPreviewScrolling(container) {
    let scrollAmount = 0;
    const scrollStep = 1;
    let direction = 1;

    const scroll = () => {
        if (direction === 1) { // Desplazamiento hacia la izquierda
            if (scrollAmount < container.scrollWidth - container.clientWidth) {
                scrollAmount += scrollStep;
            } else {
                direction = -1; // Cambia a desplazamiento a la derecha
            }
        } else { // Desplazamiento hacia la derecha
            if (scrollAmount > 0) {
                scrollAmount -= scrollStep;
            } else {
                direction = 1; // Cambia a desplazamiento a la izquierda
            }
        }
        container.style.transform = `translateX(-${scrollAmount}px)`;
        scrollingPreview = requestAnimationFrame(scroll);
    };

    scrollingPreview = requestAnimationFrame(scroll);
}

