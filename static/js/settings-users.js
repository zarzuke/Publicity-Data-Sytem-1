function deleteUser() {
    var selector = document.getElementById('editUsername');
    var valorSeleccionado = selector.value;
    // Redirección directa a la URL de Flask usando el id guardado
    const url = `/delete_user/${valorSeleccionado}`;
    window.location.href = url;
}