var total = document.getElementById("total");
var produto1 = document.getElementsByClassName("produto1");
console.log(produto1);

var preco1 = 29.99;
var quantidade1 = document.getElementsByClassName("quantidade1");
document.write(typeof(quantidade1));
var preco2 = 18.50;
var quantidade2 = document.getElementsByClassName("quantidade2");
document.write(typeof(quantidade2));

var resultado = (preco1*quantidade1)+(preco2*quantidade2);
total.innerHTML = "Resultado = ";
document.write(preco1*2," ");
document.write(preco2*3," ");
document.write(preco1*2+preco2*3);
window.alert(preco1*2+preco2*3);
window.print("Ola");

document.getElementById("paragrafo").innerHTML = "Parágrafo 1";