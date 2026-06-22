const button = document.getElementById("theme-btn");
const icon = document.getElementById("theme-icon");
let lastScroll =0;
const header = document.querySelector("header");

window.addEventListener("scroll", () => {
    const currentScroll = window.scrollY;

    if (currentScroll > lastScroll && currentScroll > 60) {
        header.classList.add("hide");
    } else {
        header.classList.remove("hide");
    }

    lastScroll = currentScroll
});

const setTheme = (dark) => {
    document.body.classList.toggle("dark-theme", dark);
    icon.classList.toggle("fa-sun", dark);
    icon.classList.toggle("fa-moon", !dark);
    localStorage.setItem("theme", dark ? "dark" : "light");
};

setTheme(localStorage.getItem("theme") === "dark");

button.addEventListener("click", () => {
    setTheme(!document.body.classList.contains("dark-theme"));
});

function formatarData(input) {
    let valor = input.value.replace(/\D/g, '');

    if (valor.length > 2) valor = valor.slice(0, 2) + '/' + valor.slice(2);
    if (valor.length > 5) valor = valor.slice(0, 5) + '/' + valor.slice(5);

    input.value = valor.slice(0, 10);
}

function manterPrefixo(input, prefixo) {
    if (!input.value.startsWith(prefixo)) {
        input.value = prefixo;
    }
}