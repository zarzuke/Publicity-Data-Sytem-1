function showModal(itemId) {
    document.getElementById('confirmationModal').classList.remove('hidden');
    document.getElementById('confirmDelete').onclick = function() {
        var url = `/delete-client/${itemId}`;
        window.location.href = url;
    };
}

document.getElementById('cancelDelete').addEventListener('click', function() {
    document.getElementById('confirmationModal').classList.add('hidden');
});

