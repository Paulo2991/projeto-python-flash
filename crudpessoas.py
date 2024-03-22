pessoas = {
   1: {
       "nome":"Paulo",
       "cpf":"15863652667",
        "sexo":"masculino",
        "datadenascimento":"04/01/2000",
       "tipopessoa":"Pessoa Física"
   },
   2: {
       "nome":"João",
       "cpf":"123456789",
       "sexo":"masculino",
       "datadenascimento":"12/05/1789",
       "tipopessoa":"Pessoa Física"
   }
  
}
def gerarId():
   id = len(pessoas) + 1
   return id

def cadastrarPessoa(nome,cpf,datadenascimento,tipopessoa):
   pessoas[gerarId()] = {"nome":nome,"cpf":cpf,"datadenascimento":datadenascimento,"tipopessoa":tipopessoa}

def retornarPessoas():
   return pessoas

def retornarPessoa(id:int):
   if id in pessoas.keys():
      return pessoas[id]
   else:
      return {}

def atualizarPessoas(id:int,dadosPessoas:dict):
   pessoas[id] = dadosPessoas

def removerPersonagem(id:int):
   del pessoas[id]

print(retornarPessoas())
cadastrarPessoa("Helida","124123","12/05-1969","Física")
print(retornarPessoa(2))  
atualizarPessoas(2,{ "nome":"José",
       "cpf":"437346767",
       "sexo":"masculino",
       "datadenascimento":"12/05/1789",
       "tipopessoa":"Pessoa Física"})
print(retornarPessoa(2))
removerPersonagem(2)
print(retornarPessoa(2))