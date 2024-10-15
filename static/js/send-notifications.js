document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    let notificationCount = 0;
    const originalTitle = document.title;

    // Recibir y mostrar notificaciones en tiempo real
    socket.on('notification', function(data) {
        const notificationsContainer = document.getElementById('notificationDropdown');
        const notificationElement = document.createElement('div');
        notificationElement.className = 'notification-item';
        notificationElement.textContent = data.message;
        notificationsContainer.appendChild(notificationElement);

        // Incrementar el contador de notificaciones y actualizar el título
        notificationCount++;
        updateTitle();

        // Mostrar el indicador de nueva notificación
        const notificationIndicator = document.getElementById('notificationIndicator');
        notificationIndicator.style.display = 'block';
    });

    // Evento para mostrar/ocultar el menú desplegable
    document.getElementById('notificationButton').addEventListener('click', function() {
        const dropdown = document.getElementById('notificationDropdown');
        dropdown.classList.toggle('show');
        const notificationIndicator = document.getElementById('notificationIndicator');
        notificationIndicator.style.display = 'none'; // Ocultar el indicador al abrir el menú

        // Restablecer el contador de notificaciones y el título al abrir el menú
        notificationCount = 0;
        updateTitle();
    });

    // Función para actualizar el título de la pestaña
    function updateTitle() {
        if (notificationCount > 0) {
            document.title = `(${notificationCount}) ${originalTitle}`;
        } else {
            document.title = originalTitle;
        }
    }
});
