
$(document).ready(function() {
    $('#updateButton').click(function() {
        var client = $('#select-client').val();
        var date = $('#date').val();
        console.log('Cliente:', client); // Depuración
        console.log('Fecha:', date); // Depuración

        $.post('/update_grid', {client: client, date: date})
            .done(function(data) {
                console.log('Datos recibidos:', data); // Depuración
                var gridContainer = $('.grid-container');
                gridContainer.empty();
                data.forEach(function(row) {
                    row.forEach(function(cell) {
                        var div = $('<div>').addClass('grid-item').text(cell);
                        gridContainer.append(div);
                    });
                });
            })
            .fail(function() {
                alert('Error al actualizar la cuadrícula.');
            });
    });
});  

