const btnMenu = document.querySelector(".hamburger");
const nav = document.querySelector("#menu");
btnMenu.addEventListener("click", () => {
  nav.classList.toggle("showNav");
});
