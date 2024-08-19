# Projeto Questao2 com Docker

Este projeto contém um spider Scrapy chamados Pedidos que faz login em uma API, obtém informações de pedidos, e salva os resultados em um arquivo JSON. O projeto é containerizado usando Docker, permitindo uma execução consistente e reproduzível.

## Pré-requisitos

- **Docker**: Certifique-se de que o Docker esteja instalado na sua máquina.
- **Make (Opcional)**: Para facilitar a execução dos comandos, o `make` pode ser usado. Ele vem pré-instalado em sistemas Linux e macOS, mas pode ser instalado no Windows via [Chocolatey](https://chocolatey.org/install) ou [WSL](https://docs.microsoft.com/pt-br/windows/wsl/install).

## Estrutura do Projeto

```plaintext
questao2/
├── Dockerfile
├── Makefile
├── README.md
├── requirements.txt
├── scrapy.cfg
└── pedidos/
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders/
        ├── __init__.py
        └── pedidos.py

```
## Usando o Makefile
O `Makefile` automatiza a construção, execução e limpeza do ambiente Docker. Siga os passos abaixo para usar os comandos do `make`.

1. Construir a Imagem Docker
Para construir a imagem Docker do projeto, use:

```bash
make build
```

2. Executar o Spider e Copiar o Resultado
Para executar o spider dentro do container Docker e copiar o arquivo JSON gerado para o diretório `output` no host, use o comando abaixo seguido do numero do pedido numeroPedido:

```bash
make run idFiltro=NumeroPedido
```

3. Recompilar e Executar
Se você quiser limpar o ambiente, reconstruir a imagem Docker, executar o spider e copiar o resultado automaticamente, use:

```bash
make rebuild
```

4. Limpar o Ambiente
Para limpar o diretório de saída e remover as imagens Docker criadas:

```bash
make clean
```

## Usando Docker Diretamente
Se preferir, você também pode usar comandos Docker diretamente, sem o Makefile.

1. Construir a Imagem Docker

```bash
docker build -t questao_2 .
```

2. Executar o Container e Copiar o JSON
Execute o container em segundo plano, aguarde a conclusão, e copie o JSON para o diretório output no host (O nome do file `pedido_NumeroPedido_filtrado.json` deverar ter o `NumeroPedido` substituido pelo numero utilizado na pesquisa):

```bash
docker run -d --name questao2_temp questao_2 pedidos -a idFiltro=numeroPedido
docker wait questao2_temp
docker cp questao2_temp:/app/output/pedido_NumeroPedido_filtrado.json ./output/
docker rm questao2_temp
```

3. Limpar o Ambiente
Para limpar o ambiente, remova o container temporário e a imagem Docker:

```bash
docker rmi questao2
docker system prune -f
```

## Notas
Certifique-se de que o diretório `output` no host exista antes de executar os comandos. O `Makefile` cuida disso automaticamente.
Os arquivos JSON gerados pelo spider serão salvos no diretório `output` no host.
Você pode personalizar o nome do arquivo JSON ou o diretório de saída conforme necessário, ajustando o código no `pedidos.spider.pedidos.py` ou no `Makefile`.