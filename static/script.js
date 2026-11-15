const inputData = document.getElementById("data");
const inputHora = document.getElementById("hora");

async function chamarApi(data) {
    const url = "/horarios_livres/" + data;

    try {
        const resp = await fetch(url);
        const resultado = await resp.json();
        console.log("Dados recebidos:", resultado);
    } catch (error) {
        console.error("Erro ao chamar a API:", error);
    }
}

inputData.addEventListener("change", () => {
    const dataSelecionada = inputData.value;
    chamarApi(dataSelecionada);
    console.log("Data selecionada:", dataSelecionada);
});

inputHora.addEventListener("change", () => {
    const horaSelecionada = inputHora.value;
    
    console.log("Hora selecionada:", horaSelecionada);
});
    

