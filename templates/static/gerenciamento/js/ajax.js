const forms = document.querySelectorAll('.ajax-form');
const dialog = document.querySelector('dialog');
const dialogBody = document.getElementById('dialog-body');
const dialogTitle = document.getElementById('dialog-title');
const table = document.getElementById('postos-tabela');
var tableRow = document.querySelectorAll('.t-row');

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
            table.innerHTML='<div style="width: 100%;height: fit-content;display: flex;justify-content: center;align-items: center;padding: 20px;"><span class="loader" style="display: block;"></span><p style="font-weight: bold;padding-left:10px;">Atualizando tabela...</p></div>'

            // Realize a segunda requisição após o sucesso do formulário
            fetch('/gerenciamento/atualizar', {
                method: 'POST', // Ou outro método HTTP, se necessário
                body: formData,
            })
            .then(response => response.text())
            .then(data => {
                // Insira a resposta da segunda requisição na tabela
                table.innerHTML = data;
                tableRow = document.querySelectorAll('.t-row');
                tableRow.forEach(row =>{
                    row.addEventListener('click', () =>{
                        row.classList.toggle('selecionado');
                });
                });
            })
            .catch(error => {
                console.error('Erro ao realizar a segunda requisição:', error);
            });
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

tableRow.forEach(row =>{
    row.addEventListener('click', () =>{
        row.classList.toggle('selecionado');
});
});
