# Imagem base
FROM python:3.10

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Crie o diretório de saída
RUN mkdir -p /app/output

# Copie todo o conteúdo do projeto para o diretório de trabalho
RUN mkdir -p /app/pedidos
COPY /pedidos/. /app/pedidos/
COPY scrapy.cfg /app/

# Defina o comando padrão para rodar o spider
ENTRYPOINT ["scrapy", "crawl"]