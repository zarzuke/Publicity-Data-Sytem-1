function sendData(id, user) {
    var comments = document.getElementById('comments').value;
    
    var url = `/update?id=${id}&user=${user}&comments=${comments}`;
    
    window.location.href = url;
}

function showModal(itemId) {
    document.getElementById('confirmationModal').classList.remove('hidden');
    document.getElementById('confirmDelete').onclick = function() {
        var status = document.getElementById('status').value;
        var url = `/next/${itemId}/${status}`;
        window.location.href = url;
    };
}

document.getElementById('cancelDelete').addEventListener('click', function() {
    document.getElementById('confirmationModal').classList.add('hidden');
});



function setStatus(status, button) {
    // Seleccionar todos los botones de estado
    const buttons = document.querySelectorAll('.status-button');
    
    // Quitar la clase activa de todos los botones, excepto el que fue clickeado
    buttons.forEach(btn => {
        if (btn !== button) {
            btn.classList.remove('active');
        }
    });

    // Alternar la clase activa en el botón que fue clickeado
    button.classList.toggle('active');
    
    // Puedes usar el valor del estado si es necesario
    console.log(`Estado seleccionado: ${status}`);
}




    // Seleccionamos el área de comentarios
    const commentInput = document.getElementById('comments');

    // Agregar un evento keypress al textarea
    commentInput.addEventListener('keypress', function(event) {
        // Verificamos si la tecla presionada es la tecla Enter (código 13)
        if (event.key === 'Enter') {
            // Evitar el comportamiento por defecto de crear nueva línea
            event.preventDefault();
            // Llamar a la función sendData al presionar Enter
            sendData('{{ nor }}', '{{ user[0] }}');
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

