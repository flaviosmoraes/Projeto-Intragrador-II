var menuItem = document.querySelectorAll('.item-menu')

function selectLink(){
    menuItem.forEach((item)=>
        item.classList.remove('ativo')
    )
    this.classList.add('ativo')
}

menuItem.forEach((item)=>
    item.addEventListener('click', selectLink)
)

var btnExp = document.querySelector('.btn-expand')
var sideMenu = document.querySelector('.menu-lateral')
var content = document.querySelector('.content')
btnExp.addEventListener('click', function(){
    sideMenu.classList.toggle('esconder')
    content.classList.toggle('expandido')
})