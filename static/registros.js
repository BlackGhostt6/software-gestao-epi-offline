const toolbar = document.getElementById("toolbar");
const saveBtn = document.querySelector(".save-btn");

const registrosForm = document.getElementById('registrosForm');
if (registrosForm) {
    registrosForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const dados = {
            matricula_funcionario: document.getElementById('matricula').value,
            ca_EPI: document.getElementById('ca').value,
            data_devolucao: document.getElementById('data-devolucao').value,
            data_troca: null,
            motivo_devolucao: null
        };

        console.log("DATA DEVOLUCAO:", document.getElementById('data-devolucao').value)

        const resposta = await fetch('/api/registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();
        alert(resultado.message || 'Erro ao criar Registro');
        if (resposta.ok) {
            registrosForm.reset()
        }
    });
}

async function buscarRegistros() {
    document
        .getElementById("toolbar")
        .classList.remove("ativo");

    document.getElementById("toolbar").classList.remove("editando");
    
    const resposta = await fetch('/api/registro/');
    const usuarios = await resposta.json();
    const tbody = document.getElementById('registrosBody');
    tbody.innerHTML = "";
    
    usuarios.forEach(usuario => {
        tbody.innerHTML += `<tr>
            <td><input  type="radio" name="registro" value="${usuario.matricula_funcionario}/${usuario.ca_EPI}"></td>
            <td>${usuario.matricula_funcionario}</td>
            <td>${usuario.ca_EPI}</td>
            <td>${usuario.data_devolucao}</td>
            <td>${usuario.data_entrega}</td>
            <td>${usuario.data_troca ?? "Não trocado"}</td>
            <td>${usuario.motivo_devolucao ?? "Em uso"}</td>
        </tr>`;
    });
}

async function deletarRegistro() {
    const selecionado = document.querySelector('input[name="registro"]:checked')

    if (!selecionado){
        alert("Selecione um registro");
        return;
    }

    const matricula = selecionado.value;

    const resposta = await fetch(`/api/registro/${matricula}`, {
        method: 'DELETE'
    }
    )

    const resultado = await resposta.json();
        alert(resultado.message || 'Erro ao deletar Registro');
    if(resposta.ok){
        buscarRegistros()
    }
}

async function editarRegistro() {
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    if (!selecionado) {
        alert("Selecione um registro");
        return;
    }

    const linha = selecionado.closest("tr");

    linha.cells[1].innerHTML = `<input value="${linha.cells[1].textContent}">`;
    linha.cells[2].innerHTML = `<input value="${linha.cells[2].textContent}">`;
    linha.cells[3].innerHTML = `<input type="date" value="${linha.cells[3].textContent}">`;
    linha.cells[5].innerHTML = `<input type="date" value="${linha.cells[5].textContent}">`;
    linha.cells[6].innerHTML = `<input value="${linha.cells[6].textContent}">`;

    toolbar.classList.add("editando");
}

async function salvarRegistro() {
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    if (!selecionado) {
        alert("Selecione um registro");
        return;
    }

    const linha = selecionado.closest("tr");

    const inputs = linha.querySelectorAll("input");

    const dados = {
        matricula_funcionario: inputs[1].value,
        ca_EPI: inputs[2].value,
        data_devolucao: inputs[3].value || null,
        data_troca: inputs[4].value || null,
        motivo_devolucao: inputs[5].value || null
    };

    const [matriculaOriginal, caOriginal] =
        selecionado.value.split("/");

    console.log(dados);

    const resposta = await fetch(
        `/api/registro/${matriculaOriginal}/${caOriginal}`,
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
        "Erro ao atualizar registro"
    );

    if (resposta.ok) {
        buscarRegistros();
    }
}
