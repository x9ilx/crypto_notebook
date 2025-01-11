function modalHandler(val, html) {
    let modal = document.getElementById("modal");
    let modal_content = document.getElementById("modal_content");
    if (val) {
        fadeIn(modal);
        modal_content.innerHTML = html;
    } else {
        fadeOut(modal);
        modal_content.innerHTML = null;
    }
}
function fadeOut(el) {
    el.style.opacity = 1;
    (function fade() {
        if ((el.style.opacity -= 0.1) < 0) {
            el.style.display = "none";
        } else {
            requestAnimationFrame(fade);
        }
    })();
}
function fadeIn(el, display) {
    el.style.opacity = 0;
    el.style.display = display || "flex";
    (function fade() {
        let val = parseFloat(el.style.opacity);
        if (!((val += 0.2) > 1)) {
            el.style.opacity = val;
            requestAnimationFrame(fade);
        }
    })();
}