document.querySelectorAll('button').forEach(function(button) {
    button.addEventListener('click', function() {
        alert('Produto adicionado ao carrinho!');
    });
});
function decreaseImagesSize() {
    let images = document.getElementsByTagName('img');

    for(let i = 0; i < images.length; i++) {
        images[i].style.width = '50%'; // Altere o valor de acordo com a largura desejada
        images[i].style.height = 'auto'; // Isso manterá a proporção original da imagem
    }
}

decreaseImagesSize();