var perguntas = [
    { pergunta: 'Qual é a capital do Brasil?', resposta: 'Brasília' },
    { pergunta: 'Qual é a maior cidade do mundo?', resposta: 'Tóquio' },
    // Adicione mais perguntas conforme necessário
];

var perguntaAtual = Math.floor(Math.random() * perguntas.length);
document.getElementById('pergunta').textContent = perguntas[perguntaAtual].pergunta;

document.getElementById('verificar').addEventListener('click', function() {
    var resposta = document.getElementById('resposta').value;
    if (resposta.toLowerCase() == perguntas[perguntaAtual].resposta.toLowerCase()) {
        document.getElementById('resultado').textContent = 'Parabéns! Você acertou!';
    } else {
        document.getElementById('resultado').textContent = 'Desculpe, você errou. A resposta correta era ' + perguntas[perguntaAtual].resposta;
    }
});
