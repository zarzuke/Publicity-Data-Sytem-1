function sendData(id, user) {
    var comments = document.getElementById('comments').value;
    
    var url = `/update?id=${id}&user=${user}&comments=${comments}`;
    
    window.location.href = url;
}

function showModal(itemId) {
    document.getElementById('confirmationModal').classList.remove('hidden');
    document.getElementById('confirmDelete').onclick = function() {
        var status = document.getElementById('status').value;
        var url = `/next/${itemId}/${status}`;
        window.location.href = url;
    };
}

document.getElementById('cancelDelete').addEventListener('click', function() {
    document.getElementById('confirmationModal').classList.add('hidden');
});