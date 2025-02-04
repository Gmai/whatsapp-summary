# Use uma imagem base do Python
FROM python:3.13.1-slim-bullseye

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho no contêiner
WORKDIR /usr/src/app

# Copie os arquivos do projeto para o contêiner
COPY /src .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta (se necessário para APIs locais)
EXPOSE 8000

# Comando para rodar o script principal
# CMD ["python","main.py"]
CMD ["/bin/bash"]
