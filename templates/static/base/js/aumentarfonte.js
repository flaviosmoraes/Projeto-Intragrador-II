document.getElementById('btn-increase-font').addEventListener('click', function () {
    changeFontSize(2);
});

document.getElementById('btn-decrease-font').addEventListener('click', function () {
    changeFontSize(-2);
});

function changeFontSize(change) {
    const content = document.querySelector('.content')
    const elements = content.querySelectorAll('*');
    elements.forEach(function (element) {
    const currentSize = window.getComputedStyle(element, null).getPropertyValue('font-size');
    const newSize = (parseFloat(currentSize) + change) + 'px';
    element.style.fontSize = newSize;
    });
}