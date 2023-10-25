const forms = document.querySelectorAll('.ajax-form');
const dialog = document.querySelector('dialog');
const dialogBody = document.getElementById('dialog-body');
const dialogTitle = document.getElementById('dialog-title');

forms.forEach(form => {
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.text())
        .then(data => {
            dialogTitle.innerHTML = form.id;
            dialogBody.innerHTML = data;
            dialog.showModal();
        })
        .catch(error => {
            console.error('Erro ao enviar o formulário via Ajax:', error);
        });
    });
});

const dialogBtn = document.getElementById('dialog-btn');
dialogBtn.addEventListener('click', function () {
    dialog.close();
});

