// Código para App de Monitoramento Ambiental
const apiUrl = "https://api.sensores.com/ar";
async function obterDadosAr() {
    try {
        const response = await fetch(apiUrl);
        const dados = await response.json();
        console.log("Qualidade do ar:", dados.nivel);
    } catch (error) {
        console.error("Erro:", error);
    }
}
obterDadosAr();