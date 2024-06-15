# Use uma imagem base do Python
FROM python:3.10.12

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos e instale as dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copie o código da aplicação
COPY app.py app.py

# Defina o comando padrão a ser executado quando o container iniciar
CMD ["python", "app.py"]