const funcionarioForm = document.getElementById('funcionarioForm');
if (funcionarioForm) {
    funcionarioForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const dados = {
            matricula_funcionario: document.getElementById('matricula').value.toUpperCase(),
            nome_funcionario: document.getElementById('nome').value,
            cpf_funcionario: document.getElementById('cpf').value,
            setor_funcionario: document.getElementById('setor').value,
            funcao_funcionario: document.getElementById('funcao').value,
            data_admissao_funcionario: document.getElementById('data_admissao').value,
            telefone: document.getElementById('telefone').value,
            email: document.getElementById('email').value,
            whatsapp: document.getElementById('whatsapp').value
        };

        const resposta = await fetch('/api/funcionario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();
        alert(resultado.message || 'Erro ao cadastrar funcionário');
        if (resposta.ok) {
            funcionarioForm.reset();
        }
    });
}

function formatarCPF(input) {
    let v = input.value.replace(/\D/g, "");

    v = v.replace(/(\d{3})(\d)/, "$1.$2");
    v = v.replace(/(\d{3})(\d)/, "$1.$2");
    v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

    input.value = v;
}

function formatarTelefone(input) {
  let v = input.value.replace(/\D/g, "");

  v = v.replace(/(\d{2})(\d)/, "($1) $2");
  v = v.replace(/(\d{5})(\d)/, "$1-$2");

  input.value = v;
}

document.addEventListener('DOMContentLoaded', () => {
    buscarFuncionarios();
});
document.addEventListener("change", (e) => {
    if (e.target.name === "registro") {
        document.getElementById("toolbar").classList.add("ativo");
    }
});


async function buscarFuncionarios() {
    const toolbar = document.getElementById("toolbar");

    if (toolbar) {
        toolbar.classList.remove("ativo");
        toolbar.classList.remove("editando");
    }

    const resposta = await fetch('/api/funcionario/');
    const funcionarios = await resposta.json();

    const tbody = document.getElementById('funcBody');
    tbody.innerHTML = "";

    funcionarios.forEach(funcionario => {
        tbody.innerHTML += `
            <tr>
                <td>
                    <input
                        type="radio"
                        name="registro"
                        value="${funcionario.matricula_funcionario}"
                    >
                </td>
                <td>${funcionario.matricula_funcionario}</td>
                <td>${funcionario.nome_funcionario}</td>
                <td>${funcionario.cpf_funcionario}</td>
                <td>${funcionario.setor_funcionario}</td>
                <td>${funcionario.funcao_funcionario}</td>
                <td>${funcionario.data_admissao_funcionario}</td>
                <td>${funcionario.telefone}</td>
                <td>${funcionario.email}</td>
                <td>${funcionario.whatsapp}</td>
            </tr>
        `;
    });
}

function editarFuncionario() {
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
    linha.cells[4].innerHTML = `<input class="edit" value="${linha.cells[4].textContent}">`;
    linha.cells[5].innerHTML = `<input class="edit" value="${linha.cells[5].textContent}">`;
    linha.cells[6].innerHTML = `<input class="edit" type="date" value="${linha.cells[6].textContent}">`;
    linha.cells[7].innerHTML = `<input class="edit" value="${linha.cells[7].textContent}">`;
    linha.cells[8].innerHTML = `<input class="edit" value="${linha.cells[8].textContent}">`;
    linha.cells[9].innerHTML = `<input class="edit" value="${linha.cells[9].textContent}">`;


    document
        .getElementById("toolbar")
        .classList.add("editando");
}

async function salvarFuncionario() {
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
        nome_funcionario: inputs[1].value,
        cpf_funcionario: inputs[2].value,
        setor_funcionario: inputs[3].value,
        funcao_funcionario: inputs[4].value,
        data_admissao_funcionario: inputs[5].value,
        telefone: inputs[6].value,
        email: inputs[7].value,
        whatsapp: inputs[8].value
    };

    const matriculaOriginal = selecionado.value;

    const resposta = await fetch(
        `/api/funcionario/${matriculaOriginal}`,
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
        "Erro ao atualizar funcionário"
    );

    if (resposta.ok) {
        buscarFuncionarios();
    }
}

async function deletarFuncionario() {
    const selecionado = document.querySelector(
        'input[name="registro"]:checked'
    );

    if (!selecionado) {
        alert("Selecione um funcionário");
        return;
    }

    const matricula = selecionado.value;

    if (!confirm(`Excluir funcionário ${matricula}?`)) {
        return;
    }

    const resposta = await fetch(
        `/api/funcionario/${matricula}`,
        {
            method: "DELETE"
        }
    );

    const resultado = await resposta.json();

    alert(
        resultado.message ||
        resultado.erro ||
        "Erro ao excluir funcionário"
    );

    if (resposta.ok) {
        buscarFuncionarios();
    }
}