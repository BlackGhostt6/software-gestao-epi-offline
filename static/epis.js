document.addEventListener('DOMContentLoaded', () => {
    buscarEpi();
});
document.addEventListener("change", (e) => {
    if (e.target.name === "registro") {
        document.getElementById("toolbar").classList.add("ativo");
    }
});

const epiForm = document.getElementById('epiForm');
if (epiForm) {
    epiForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const dados = {
            nome_epi: document.getElementById('nome').value,
            tipo_epi: document.getElementById('tipo').value,
            certificado_aprovacao_epi: document.getElementById('ca').value.toUpperCase(),
            validade_certificado_aprovacao: document.getElementById('validade_ca').value
        };

        const resposta = await fetch('/api/epi', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();
        alert(resultado.message || 'Erro ao cadastrar EPI');
        if (resposta.ok) {
            epiForm.reset();
        }
    });
}


async function buscarEpi() {
    const toolbar = document.getElementById("toolbar");

    if (toolbar) {
        toolbar.classList.remove("ativo");
        toolbar.classList.remove("editando");
    }

    const resposta = await fetch('/api/epi/');
    const funcionarios = await resposta.json();

    const tbody = document.getElementById('epiBody');
    tbody.innerHTML = "";

    funcionarios.forEach(epi => {
        tbody.innerHTML += `
            <tr>
                <td>
                    <input
                        type="radio"
                        name="registro"
                        value="${epi.certificado_aprovacao_epi}"
                    >
                </td>
                <td>${epi.certificado_aprovacao_epi}</td>
                <td>${epi.nome_epi}</td>
                <td>${epi.tipo_epi}</td>
                <td>${epi.validade_certificado_aprovacao}</td>
            </tr>
        `;
    });
}

function editarEpi() {
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    if (!selecionado) {
        alert("Selecione um funcionário");
        return;
    }

    const linha = selecionado.closest("tr");

    linha.cells[2].innerHTML = `<input class="edit" value="${linha.cells[2].textContent}">`;
    linha.cells[3].innerHTML = `<input class="edit" value="${linha.cells[3].textContent}">`;
    linha.cells[4].innerHTML = `<input class="edit" type="date" value="${linha.cells[4].textContent}">`;


    document
        .getElementById("toolbar")
        .classList.add("editando");
}

async function salvarEpi() {
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    if (!selecionado) {
        alert("Selecione um funcionário");
        return;
    }

    const linha = selecionado.closest("tr");
    const inputs = linha.querySelectorAll("input");

    const dados = {
        nome_epi: inputs[1].value,
        tipo_epi: inputs[2].value,
        validade_certificado_aprovacao: inputs[3].value,
    };

    const ca = selecionado.value;

    const resposta = await fetch(
        `/api/epi/${ca}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        }
    );

    const resultado = await resposta.json();

    alert(
        resultado.message ||
        resultado.erro ||
        "Erro ao atualizar epi"
    );

    if (resposta.ok) {
        buscarEpi();
    }
}

async function deletarEpi() {
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    if (!selecionado) {
        alert("Selecione um Epi");
        return;
    }

    const ca = selecionado.value;

    if (!confirm(`Excluir funcionário ${ca}?`)) {
        return;
    }

    const resposta = await fetch(
        `/api/epi/${ca}`,
        {
            method: "DELETE"
        }
    );

    const resultado = await resposta.json();

    alert(
        resultado.message ||
        resultado.erro ||
        "Erro ao excluir epi"
    );

    if (resposta.ok) {
        buscarEpi();
    }
}

