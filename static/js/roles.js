document.addEventListener('DOMContentLoaded', function() {
    var role = document.getElementById('role').textContent.trim();
    const client = document.getElementById('client');
    const diseño = document.getElementById('diseño');
    const aprobacion = document.getElementById('aprobacion');
    const elaboracion = document.getElementById('elaboracion');
    const entrega = document.getElementById('entrega');
    const home = document.getElementById('home');
    const setting = document.getElementById('setting');
    const edit = document.getElementById('editbutton');
  
    if (role === 'Designer') {
        client.style.display = 'none';
        diseño.style.display = 'block';
        aprobacion.style.display = 'none';
        elaboracion.style.display = 'none';
        entrega.style.display = 'none';
        home.style.display = 'none';
        setting.style.display = 'none';
    } 
    else if (role === 'Administrator') {
        diseño.style.display = 'block';
        aprobacion.style.display = 'block';
        elaboracion.style.display = 'block';
        entrega.style.display = 'block';
    }
    else if (role === 'Crafter') {
        client.style.display = 'none';
        diseño.style.display = 'none';
        aprobacion.style.display = 'none';
        elaboracion.style.display = 'block';
        entrega.style.display = 'none';
        home.style.display = 'none';
        setting.style.display = 'none';
    }
    else if (role === 'Installer') {
        client.style.display = 'none';
        diseño.style.display = 'none';
        aprobacion.style.display = 'none';
        elaboracion.style.display = 'none';
        entrega.style.display = 'block';
        home.style.display = 'none';
        setting.style.display = 'none';
        edit.style.display = "none";
    }
});
