# Nome da imagem Docker
IMAGE_NAME = questao2

# Diretório de saída para os arquivos gerados
OUTPUT_DIR = ./output
OUTPUT_FILE = pedido_$(idFiltro)_filtrado.json

# Comando para construir a imagem Docker
build:
	docker build -t $(IMAGE_NAME) .

# Comando para executar o container Docker
run:
	docker run -d --name $(IMAGE_NAME)_temp $(IMAGE_NAME) pedidos -a idFiltro=$(idFiltro)
	docker wait $(IMAGE_NAME)_temp
	docker cp $(IMAGE_NAME)_temp:/app/output/$(OUTPUT_FILE) $(OUTPUT_DIR)/
	docker rm $(IMAGE_NAME)_temp

# Comando para limpar os arquivos de saída e remover imagens Docker não usadas
clean:
	docker rmi $(IMAGE_NAME)
	docker system prune -f

# Comando para reconstruir e executar
rebuild: clean build