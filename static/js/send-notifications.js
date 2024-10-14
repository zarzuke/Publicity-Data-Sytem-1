document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const originalTitle = document.title;

    // Recibir y mostrar notificaciones en tiempo real
    socket.on('notification', function(data) {
        const notificationsContainer = document.getElementById('notificationDropdown');
        const notificationElement = document.createElement('div');
        notificationElement.className = 'notification-item';
        notificationElement.textContent = data.message;
        notificationsContainer.appendChild(notificationElement);

        // Mostrar el indicador de nueva notificación
        const notificationIndicator = document.getElementById('notificationIndicator');
        notificationIndicator.style.display = 'block';

        // Actualizar el título de la pestaña con el icono de notificación
        document.title = '🔔 ' + originalTitle;
    });

    // Variable para la función que carga notificaciones existentes
    const loadNotifications = function() {
        fetch('/notifications')
            .then(response => response.json())
            .then(data => {
                const notificationsContainer = document.getElementById('notificationDropdown');
                data.forEach(notification => {
                    const notificationElement = document.createElement('div');
                    notificationElement.className = 'notification-item';
                    notificationElement.textContent = notification.message;
                    notificationsContainer.appendChild(notificationElement);
                });

                // Mostrar el indicador si hay notificaciones
                if (data.length > 0) {
                    const notificationIndicator = document.getElementById('notificationIndicator');
                    notificationIndicator.style.display = 'block';

                    // Actualizar el título de la pestaña con el icono de notificación
                    document.title = '🔔 ' + originalTitle;
                }
            });
    };

    // Llamar a la función al cargar la página
    loadNotifications();
});

document.getElementById('notificationButton').addEventListener('click', function() {
    this.classList.toggle('active');
    document.getElementById('notificationIndicator').style.display = 'none'; // Ocultar el indicador al abrir el menú
    document.title = originalTitle; // Restaurar el título original de la pestaña
});
