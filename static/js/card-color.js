window.onload = function() {
    const cardItems = document.querySelectorAll('.card-item');
    
    // Conjunto de imágenes fijas
    const fixedImages = [
        '../static/img/background-1.png',  // Imagen para el card 1
        '../static/img/background-2.png',  // Imagen para el card 2
        '../static/img/background-3.png',  // Imagen para el card 3
        '../static/img/background-4.png',  // Imagen para el card 4
        '../static/img/background-5.png',  // Imagen para el card 5
    ];

    cardItems.forEach((card, index) => {
        // Asigna la imagen fija según el índice del card
        const imgElement = card.querySelector('.card-image');
        if (index < fixedImages.length) {
            imgElement.src = fixedImages[index];
        }
    });

    // Asignar la primera imagen para la previsualización
    const previewImage = document.getElementById('preview-image');
    previewImage.src = fixedImages[0]; // Asignar imagen deseada para la previsualización
}
