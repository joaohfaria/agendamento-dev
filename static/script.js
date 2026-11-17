const inputData = document.getElementById("data");
const inputHora = document.getElementById("hora");

function atualizarHorarios(lista) {
  const selectHora = document.getElementById("hora");
  selectHora.innerHTML = "";

  if (lista.length === 0) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = "Nenhum horário disponível nesta data";
    selectHora.appendChild(option);

    return;
  }

  const option = document.createElement("option");
  option.value = "";
  option.textContent = "Selecione um horário";
  selectHora.appendChild(option);

  lista.forEach((hora) => {
    const option = document.createElement("option");
    option.value = hora;
    option.textContent = hora;
    selectHora.appendChild(option);
  });
}

async function chamarApi(data) {
  const url = "/horarios_livres/" + data;

  try {
    const resp = await fetch(url);
    const resultado = await resp.json();
    console.log("Dados recebidos:", resultado);
    atualizarHorarios(resultado.horarios_livres);
  } catch (error) {
    console.error("Erro ao chamar a API:", error);
  }
}
if (inputData) {
  inputData.addEventListener("change", () => {
    const dataSelecionada = inputData.value;
    chamarApi(dataSelecionada);
    console.log("Data selecionada:", dataSelecionada);
  });
}

if (inputHora) {
  inputHora.addEventListener("change", () => {
    const horaSelecionada = inputHora.value;

    console.log("Hora selecionada:", horaSelecionada);
  });
}
