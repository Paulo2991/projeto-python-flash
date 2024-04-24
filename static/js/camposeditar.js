let nome = '';
let cpf = '';

$(window).on('load', function() {
  nome = $('#nome').val();
  cpf = $('#cpf').val();
  validate();
})


function validate(){
 if (($('#nome').val().length > 0 && $('#nome').val() != nome) || 
 ($('#cpf').val().length > 0 && $('#cpf').val() != cpf)){
   $("button[type=submit]").prop("disabled", false);
  }else {
   $("button[type=submit]").prop("disabled", true);

  }
}