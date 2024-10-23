document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    let notificationCount = 0;
    const originalTitle = document.title;

    // Ocultar el indicador de notificaciones al cargar la página
    const notificationIndicator = document.getElementById('notificationIndicator');
    notificationIndicator.style.display = 'none';

    // Recibir y mostrar notificaciones en tiempo real
    socket.on('notification', function(data) {
        const notificationsContainer = document.getElementById('notificationDropdown');
        
        // Crear y agregar el nuevo elemento de notificación
        const notificationElement = document.createElement('div');
        notificationElement.className = 'notification-item';
        notificationElement.textContent = data.message;
        notificationsContainer.appendChild(notificationElement);
    
        // Incrementar el contador de notificaciones
        notificationCount++;
        updateTitle();
    
        // Mostrar el indicador de nueva notificación
        notificationIndicator.style.display = 'block';
    
        // Limitar la visualización a 4 notificaciones
        if (notificationsContainer.children.length > 4) {
            notificationsContainer.scrollTop = notificationsContainer.scrollHeight; // Desplazar hacia abajo si hay más de 4
        }
    });

    // Evento para mostrar/ocultar el menú desplegable
    document.getElementById('notificationButton').addEventListener('click', function(event) {
        const dropdown = document.getElementById('notificationDropdown');
        dropdown.classList.toggle('show');
        
        // Ocultar el indicador al abrir el menú
        notificationIndicator.style.display = 'none'; 

        // Restablecer el contador de notificaciones y el título al abrir el menú
        notificationCount = 0;
        updateTitle();
        
        // Evitar que el clic en el botón cierre el menú inmediatamente
        event.stopPropagation();
    });

    // Cerrar el menú si se hace clic fuera de él
    document.addEventListener('click', function(event) {
        const dropdown = document.getElementById('notificationDropdown');
        if (!dropdown.contains(event.target) && !event.target.matches('#notificationButton')) {
            dropdown.classList.remove('show');
        }
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

