function deleteUser() {
    var selector = document.getElementById('editUsername');
    var valorSeleccionado = selector.value;
    // Redirección directa a la URL de Flask usando el id guardado
    const url = `/delete_user/${valorSeleccionado}`;
    window.location.href = url;
}
document.addEventListener('DOMContentLoaded', function() {
    // Selecciona todos los inputs por la clase
    const inputFields = document.querySelectorAll('.no-space');

    // Añade un evento 'keydown' a cada input
    inputFields.forEach(inputField => {
        inputField.addEventListener('keydown', function(event) {
            if (event.key === ' ') {
                alert("No se pueden usar espacios en este campo, solo 1 nombre y 1 apellido");
                event.preventDefault(); // Evita la acción predeterminada de la barra espaciadora
            }
        });
    });
});
