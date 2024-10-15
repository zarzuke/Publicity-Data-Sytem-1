function updateCurrency(){
    var id = document.getElementById('id').value;
    var charge = document.getElementById('newTotalInput').value;
    var comments= document.getElementById('TotalReason').value;
    var url = `/work/balance?id=${id}&charge=${charge}&args=${comments}`;
    window.location.href = url;
}



function sendData() {
    var comments = document.getElementById('comments').value;
    var id = document.getElementById('id').value;
    var user = document.getElementById('user').value;

    if (comments.trim() === "") {
        alert("Ingrese comentarios");
    } else {
        var url = `/update?id=${id}&user=${user}&comments=${comments}`;
        window.location.href = url;
    }
}

    // Seleccionamos el área de comentarios
    const commentInput = document.getElementById('comments');

    // Agregar un evento keypress al textarea
    commentInput.addEventListener('keypress', function(event) {
        // Verificamos si la tecla presionada es la tecla Enter (código 13)
        if (event.key === 'Enter') {
            // Evitar el comportamiento por defecto de crear nueva línea
            event.preventDefault();
            // Llamar a la función sendData al presionar Enter{
            
            sendData();
        }
    });


    // Obtener los elementos necesarios
const editTotalButton = document.querySelector('.edit-total');
const totalEditModal = document.getElementById('totalEditModal');
const newTotalInput = document.getElementById('newTotalInput');
const changeTotalReasonInput = document.getElementById('changeTotalReason');
const confirmTotalEditButton = document.getElementById('confirmTotalEdit');
const cancelTotalEditButton = document.getElementById('cancelTotalEdit');

// Función para mostrar la ventana flotante
function showTotalEditModal() {
    totalEditModal.classList.remove('hidden');
}

// Función para cerrar la ventana flotante
function closeTotalEditModal() {
    totalEditModal.classList.add('hidden');
}

// Función para actualizar el total
function updateTotal() {
    const newTotal = newTotalInput.value;
    const changeTotalReason = changeTotalReasonInput.value;

    // Aquí puedes agregar la lógica para enviar la nueva información al servidor y actualizar la página

    closeTotalEditModal();
}

// Agregar los event listeners
editTotalButton.addEventListener('click', showTotalEditModal);
confirmTotalEditButton.addEventListener('click', updateTotal);
cancelTotalEditButton.addEventListener('click', closeTotalEditModal);



function handleComplete(id) {
    const approvedButton = document.getElementById('approved');
    const rejectedButton = document.getElementById('rejected');

    if (approvedButton.classList.contains('active')) {
        // Acción si el estado es "Aprobado"
        showModal('approved',id);
    } else if (rejectedButton.classList.contains('active')) {
        // Acción si el estado es "Rechazado"
        showModal('canceled',id);
    } else {
        // Acción si no se ha seleccionado ningún estado
        alert('Por favor, selecciona un estado antes de completar.');
    }
}


function setStatus(status, element) {
    // Reset all buttons
    document.querySelectorAll('.status-button').forEach(button => {
        button.classList.remove('active');
    });
    // Set the clicked button as active
    element.classList.add('active');
    // Store the status in a hidden input or a variable
    document.getElementById('status').value = status;
}


function showModal(status,itemId) {
    document.getElementById('confirmationModal').classList.remove('hidden');
    document.getElementById('confirmDelete').onclick = function() {
        var url = `/next/${itemId}/${status}`;
        window.location.href = url;
    };
}

document.getElementById('cancelDelete').addEventListener('click', function() {
    document.getElementById('confirmationModal').classList.add('hidden');
});


document.getElementById('editAbonadoButton').onclick = function() {
    document.getElementById('abonadoEditModal').classList.remove('hidden');
};

document.getElementById('cancelAbonadoEdit').onclick = function() {
    document.getElementById('abonadoEditModal').classList.add('hidden');
};

function updateAbonado() {
    var abono = document.getElementById('newAbonadoInput').value;
    var id = document.getElementById('id').value;
    var url = `/work/down?id=${id}&down=${abono}`;
    window.location.href = url;
}

    // Función para cerrar el modal
    function closeModal() {
        const modal = document.getElementById('totalEditModal');
        modal.classList.add('hidden'); // Asegúrate de que la clase 'hidden' oculta el modal
    }

    // Agregar evento de teclado para cerrar el modal con la tecla Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModal(); // Cierra el modal
            // Puedes hacer una simulación de click en el botón de cancelar si es necesario
            const cancelButton = document.getElementById('cancelTotalEdit');
            if (cancelButton) {
                cancelButton.click(); // Simula el clic en el botón de cancelar
            }
        }
    });

        // Función para cerrar el modal
        function closeModal() {
            const modal = document.getElementById('abonadoEditModal');
            modal.classList.add('hidden'); // Asegúrate de que la clase 'hidden' oculta el modal
        }
    
        // Agregar evento de teclado para cerrar el modal con la tecla Escape
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeModal(); // Cierra el modal
                // Puedes hacer una simulación de click en el botón de cancelar si es necesario
                const cancelButton = document.getElementById('cancelAbonadoEdit');
                if (cancelButton) {
                    cancelButton.click(); // Simula el clic en el botón de cancelar
                }
            }
        });