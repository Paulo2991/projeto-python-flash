$(document).ready(function () {
  validate();
  $("#nome,#cpf").change(validate);
});

function validate() {
  if ($("#nome").val().length > 0 && $("#cpf").val().length > 0) {
    $("button[type=submit]").prop("disabled", false);
  } else {
    $("button[type=submit]").prop("disabled", true);
  }
}
