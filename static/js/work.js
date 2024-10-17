function updateCurrency() {
    var id = document.getElementById('id').value;
    var charge = document.getElementById('newTotalInput').value;
    var comments = document.getElementById('TotalReason').value;
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
    if (event.key === 'Enter') {
        event.preventDefault();
        sendData();
    }
});

// Obtener los elementos necesarios
const editTotalButton = document.querySelector('.edit-total');
const totalEditModal = document.getElementById('totalEditModal');
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

// Agregar los event listeners
if (editTotalButton) {
    editTotalButton.addEventListener('click', showTotalEditModal);
}
if (confirmTotalEditButton) {
    confirmTotalEditButton.addEventListener('click', updateCurrency);
}
if (cancelTotalEditButton) {
    cancelTotalEditButton.addEventListener('click', closeTotalEditModal);
}

// Manejar completado
function handleComplete(id) {
    const approvedButton = document.getElementById('approved');
    const rejectedButton = document.getElementById('rejected');

    if (approvedButton.classList.contains('active')) {
        showModal('approved', id);
    } else if (rejectedButton.classList.contains('active')) {
        showModal1('canceled', id);
    } else {
        alert('Por favor, selecciona una decisión antes de completar.');
    }
}

function setStatus(status, element) {
    document.querySelectorAll('.status-button').forEach(button => {
        button.classList.remove('active');
    });
    element.classList.add('active');
    document.getElementById('status').value = status;
}

function showModal(status, itemId) {
    document.getElementById('confirmationModal').classList.remove('hidden');
    
    var phase = document.getElementById('phase').value;
    
    if (phase == 1) {
        document.getElementById('confirmDelete').onclick = function() {
            var designFile = document.getElementById('designFile').value;
            if (!designFile.trim()) {
                alert("Por favor, ingrese el .CDR del diseño del trabajo");
                return;
            }
            const fileName = designFile.split('\\').pop().split('/').pop();
            var url = `/next/${itemId}/${status}?cdr=${encodeURIComponent(fileName)}`;
            window.location.href = url;
        };
    } else {
        document.getElementById('confirmDelete').onclick = function() {
            var url = `/next/${itemId}/${status}`;
            window.location.href = url;
        };
    }
}

function showModal1(status, itemId) {
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

// Cerrar el modal de editar total con Esc
function handleKeyClose(event) {
    if (event.key === 'Escape') {
        closeTotalEditModal();
    }
}

document.addEventListener('keydown', handleKeyClose);

// Cerrar el modal de añadir abono con Esc
function handleKeyCloseAbonado(event) {
    if (event.key === 'Escape') {
        document.getElementById('abonadoEditModal').classList.add('hidden');
    }
}

document.addEventListener('keydown', handleKeyCloseAbonado);

