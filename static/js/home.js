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

    previewTitle.textContent = titleInput.value;
    previewName.textContent = nameInput.value;
    previewLastname.textContent = surnameInput.value;

// Obtener todos los checkboxes que están seleccionados (checked)
    const selectedJobTypes = Array.from(document.querySelectorAll('input[name="job-type"]:checked')).map(checkbox => checkbox.value);
    previewJobTitle.textContent = selectedJobTypes.length > 0 ? selectedJobTypes.join(', ') : 'Selecciona un tipo de trabajo';

    previewDate.textContent = dateInput.value;
    previewPhone.textContent = `(${phoneInput.value.slice(0, 3)}) ${phoneInput.value.slice(3)}`;
    previewDescription.textContent = descriptionInput.value;

// Previsualizar la imagen cargada
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImage.src = e.target.result;
        };
        reader.readAsDataURL(fileInput.files[0]);
    } else {
        previewImage.src = 'images/editor.jpg'; // Imagen predeterminada
    }
}

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
addForm.addEventListener('submit', (event) => {
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
});

closeButton.addEventListener('click', () => {
    addModal.classList.add('hidden');
    addModal.classList.remove('visible');
    modalBackdrop.classList.add('hidden');
    modalBackdrop.classList.remove('visible');
    document.body.style.overflow = 'auto'; // Restaura el scroll
});

// CALCULAR RESTANTE

document.addEventListener("DOMContentLoaded", function() {
    const totalCostInput = document.getElementById('total-cost');
    const downPaymentInput = document.getElementById('down-payment');
    const remainingInput = document.getElementById('remaining');
  
    function calculateRemaining() {
      const totalCost = parseFloat(totalCostInput.value) || 0;
      const downPayment = parseFloat(downPaymentInput.value) || 0;
      const remaining = totalCost - downPayment;
  
      // Format the remaining amount with dots as thousands separators
      const formattedRemaining = remaining.toLocaleString('es-ES'); // Adjust the locale if needed
  
      remainingInput.value = remaining < 0 ? '0' : formattedRemaining;
    }
  
    totalCostInput.oninput = calculateRemaining;
    downPaymentInput.oninput = calculateRemaining;
  });
  

