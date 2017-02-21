// Register callbacks

function shadeTitle (e) {
    document.querySelector(".title-nav").classList.toggle("shown");
}

function loader (e) {
    document.querySelector("header.site .show-nav")
        .addEventListener("click", shadeTitle);
}

window.addEventListener("load", loader);
