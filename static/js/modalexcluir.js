const excluirBtns = document.querySelectorAll(".excluir-btn");
const modal = document.getElementById("modal-confirmacao");
const confirmarBtn = document.getElementById("confirmar-exclusao");
const cancelarBtn = document.getElementById("cancelar-exclusao");

excluirBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const itemId = btn.getAttribute("data-item-id");
    modal.style.display = "block";

    confirmarBtn.onclick = () => {
      window.location.href = `/pessoas/${itemId}`;
    };

    cancelarBtn.onclick = () => {
      modal.style.display = "none";
    };
  });
});

window.onclick("click",(event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});
