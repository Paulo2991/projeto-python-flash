const excluirBtns = document.querySelectorAll(".excluir-btn");
const modal = document.getElementById("myModal");
const resultModal = document.getElementById("resultModal");
const closeButtons = document.querySelectorAll('.close');
const confirmarBtn = document.getElementById("confirmar-exclusao");
const cancelarBtn = document.getElementById("cancelar-exclusao");

excluirBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const itemId = btn.getAttribute("data-item-id");
    modal.style.display = "block";

    confirmarBtn.onclick = () => {
      window.location.href = `/pessoas/${itemId}`;
      resultModal.style.display = "block";
    };

    cancelarBtn.onclick = () => {
      modal.style.display = "none";
    };
  });
});

closeButtons.forEach(function (button) {
  button.addEventListener("click", function () {
    myModal.style.display = "none";
    resultModal.style.display = "none";
  });
});

window.addEventListener("click", (event) => {
  if (event.target === modal || event.target === resultModal) {
    modal.style.display = "none";
    resultModal.style.display = "none";
  }
});
