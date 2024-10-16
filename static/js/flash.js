document.addEventListener('DOMContentLoaded', function () {
    const messages = document.querySelectorAll('.flash-message');
    messages.forEach((message) => {
        // Asegúrate de que el mensaje se muestre inicialmente
        message.classList.add('show');

        // Después de 7 segundos, quita la clase 'show' para iniciar la salida
        setTimeout(() => {
            message.classList.add('fade-out');

            // Luego de que finaliza la animación de salida, se elimina el mensaje del DOM
            setTimeout(() => {
                message.remove();
            }, 500); // Asegúrate de que coincide con la duración de la transición de salida
        }, 7000); // Tiempo en milisegundos: 7 segundos
    });
});


