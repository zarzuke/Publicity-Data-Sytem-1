function previewImage(input) {
    const previewImg = document.getElementById('preview-image');
    const previewName = document.getElementById('previewName');

    if (input.files && input.files[0]) {
        const reader = new FileReader();


        reader.onload = function (e) {
            previewImg.src = e.target.result;  // Usa el archivo cargado para la imagen

            // Mantenemos el nombre y apellido en la vista previa
            const name = document.getElementById('name').value || 'Nombre';
            const surname = document.getElementById('surname').value || 'Apellido';
            previewName.textContent = `${name} ${surname}`;
            document.getElementById('previewCompany').textContent = ''; // Si tenías esto, puedes dejarlo o quitarlo
        };


        reader.readAsDataURL(input.files[0]);
    } else {
        previewImg.src = '../static/img/user-default.png'; // Restablece a imagen predeterminada
        previewName.textContent = ''; // Puede dejarse vacío o con texto predeterminado
        document.getElementById('previewCompany').textContent = ''; // Limpia el texto de compañía
    }
}




function editModal(clientId) {
    document.getElementById('editUserModal').classList.remove('hidden');
    document.getElementById('editUserModal').classList.add('visible');
    document.getElementById('modalBackdrop').classList.remove('hidden');
    document.getElementById('modalBackdrop').classList.add('visible');


    // Actualiza el action del formulario
    var form = document.getElementById('editForm');
    form.action = "/change-client/" + clientId; // Cambia '/edit_client/' a la URL correcta si es necesario
}


function showConfirmationModal(itemId) {
    document.getElementById('confirmationModal').classList.remove('hidden');
    document.getElementById('confirmationModal').classList.add('visible');
    document.getElementById('modalBackdrop').classList.remove('hidden');
    document.getElementById('modalBackdrop').classList.add('visible');


    document.getElementById('confirmDelete').onclick = function () {
        var url = `/delete-client/${itemId}`;
        window.location.href = url;
    };
}




function updatePreview() {
    const name = document.getElementById('name').value || '';
    const surname = document.getElementById('surname').value || '';
    const phone = document.getElementById('phone').value || '';

    const previewName = document.getElementById('previewName');
    const previewPhone = document.getElementById('previewPhone');
    const previewImage = document.getElementById('preview-image');


    // Actualiza el texto de la vista previa
    previewName.textContent = `${name} ${surname}`;
    previewPhone.textContent = phone;


    // Actualiza la imagen previa (se puede agregar lógica para previsualizar la imagen también si se desea)
    const fileInput = document.getElementById('file');
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImage.src = e.target.result;  // Establece la fuente de la vista previa como el archivo cargado
        }
        reader.readAsDataURL(fileInput.files[0]);
    }
}








function showModal(itemId) {
    document.getElementById('confirmationModal').classList.remove('hidden');
    document.getElementById('confirmDelete').onclick = function () {
        var url = `/delete-client/${itemId}`;
        window.location.href = url;
    };
}


document.getElementById('cancelDelete').addEventListener('click', function () {
    document.getElementById('confirmationModal').classList.add('hidden');
});


// Editar cliente
document.querySelectorAll('.edit').forEach(function (editButton) {
    editButton.addEventListener('click', function () {
        const clientId = this.getAttribute('data-client-id');
        editModal(clientId);
    });
});


// Eliminar cliente
document.querySelectorAll('.delete').forEach(function (deleteButton) {
    deleteButton.addEventListener('click', function () {
        const clientId = this.getAttribute('data-client-id');
        showConfirmationModal(clientId);
    });
});


// Cerrar el modal de confirmación
document.getElementById('cancelDelete').addEventListener('click', function () {
    document.getElementById('confirmationModal').classList.remove('visible');
    document.getElementById('confirmationModal').classList.add('hidden');
    document.getElementById('modalBackdrop').classList.remove('visible');
    document.getElementById('modalBackdrop').classList.add('hidden');
});


document.getElementById('addForm').addEventListener('reset', function (event) {
    // Llama a la función que restablece la vista previa
    resetPreview();
});


function resetPreview() {
    const previewImg = document.getElementById('preview-image');
    const previewName = document.getElementById('previewName');
    const previewPhone = document.getElementById('previewPhone');

    // Limpiar los campos de vista previa
    previewImg.src = '../static/img/user-default.png'; // Restablece la imagen a la imagen predeterminada
    previewName.textContent = ''; // Restablece el nombre a vacío
    previewPhone.textContent = ''; // Restablece el teléfono a vacío


    // Limpiar el input de archivo
    document.getElementById('file').value = ''; // Limpia el input de archivo
}

// Close the edit modal when the cancel button is clicked
document.querySelector('.cancel-btn').addEventListener('click', function () {
    closeModal();
});

// Function to close modals
function closeModal() {
    document.getElementById('editUserModal').classList.add('hidden');
    document.getElementById('modalBackdrop').classList.remove('visible');
    document.getElementById('modalBackdrop').classList.add('hidden');
}

// Close both modals when pressing the Escape key
document.addEventListener('keydown', function (event) {
    if (event.key === "Escape") {
        // Check if Add modal is visible
        if (!document.getElementById('addModal').classList.contains('hidden')) {
            closeAddModal(); // Close the add modal
        }
        
        // Check if edit modal is visible
        if (!document.getElementById('editUserModal').classList.contains('hidden')) {
            closeModal(); // Close edit modal
        }
        
        // Check if confirmation modal is visible
        if (!document.getElementById('confirmationModal').classList.contains('hidden')) {
            // Close confirmation modal
            document.getElementById('confirmationModal').classList.remove('visible');
            document.getElementById('confirmationModal').classList.add('hidden');
            document.getElementById('modalBackdrop').classList.remove('visible');
            document.getElementById('modalBackdrop').classList.add('hidden');
        }
    }
});

// Close the Add modal when the close button is clicked
document.getElementById('closeModal').addEventListener('click', function () {
    closeAddModal();
});

// Function to close the "Add Client" modal
function closeAddModal() {
    document.getElementById('addModal').classList.add('hidden');
    document.getElementById('modalBackdrop').classList.remove('visible');
    document.getElementById('modalBackdrop').classList.add('hidden');
}

// Close the edit modal when the cancel button is clicked
document.querySelector('.cancel-btn').addEventListener('click', function () {
    closeModal(); // Close the edit modal
});
