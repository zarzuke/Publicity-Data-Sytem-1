const openModal = document.querySelector('.contacto');
const modal = document.querySelector('.modal');
const cerrarbtn = document.querySelector('.btn__cerrar');

openModal.addEventListener('click', (e)=>{
    e.preventDefault();
    modal.classList.add('modal--show');
});

cerrarbtn.addEventListener('click', (e)=>{
    e.preventDefault();
    modal.classList.remove('modal--show');
});