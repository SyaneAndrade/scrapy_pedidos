import scrapy
from scrapy.http import FormRequest
import json
import jwt
import os

class PedidoSpider(scrapy.Spider):
    name = "pedidos"
    filtro = ""
    output_dir = '/app/output'

    def start_requests(self, idFiltro = ""):
        # URL da rota de login
        self.filtro = self.__getattribute__('idFiltro') or idFiltro
        login_url = "https://peapi.servimed.com.br/api/usuario/login"
        login_payload = {
            "usuario": "juliano@farmaprevonline.com.br",
            "senha": "a007299A"
        }

        # Faz a requisição de login
        yield FormRequest(
            url=login_url,
            method="POST",
            formdata=login_payload,
            callback=self.after_login
        )

    def after_login(self, response):
        # Verifica se o login foi bem-sucedido
        if response.status == 200:
            # Parse do JSON na resposta de login
            login_data = response.json()
            self.logger.info("Login feito com sucesso!")

            # Extrai os cookies da resposta
            cookies = response.headers.getlist('Set-Cookie')

            # Função para extrair valores de tokens específicos dos cookies
            def get_cookie_value(cookie_name, cookies):
                for cookie in cookies:
                    if cookie_name in cookie.decode('utf-8'):
                        return cookie.decode('utf-8').split(f"{cookie_name}=")[1].split(";")[0]
                return None

            # Extração dos tokens específicos
            access_token = get_cookie_value('accesstoken', cookies)
            session_token = get_cookie_value('sessiontoken', cookies)

            # Extrai os dados necessários da resposta
            usuario_info = login_data.get("usuario", {})
            codigo_externo = usuario_info.get("codigoExterno")
            codigo_usuario = usuario_info.get("codigoUsuario")
            users = usuario_info.get("users", [])

            # URL da rota de pedidos
            pedido_url = f"https://peapi.servimed.com.br/api/Pedido/ObterTodasInformacoesPedidoPendentePorId/{self.filtro}"
            pedido_payload = {
                "dataInicio": "",
                "dataFim": "",
                "filtro": self.filtro,
                "pagina": 1,
                "registrosPorPagina": 10,
                "codigoExterno": codigo_externo,
                "codigoUsuario": codigo_usuario,
                "kindSeller": 0,
                "users": users
            }
            
            # 
            jwt_token = jwt.decode(session_token, options={"verify_signature": False})
            headers = {
                "cookie": f"session_token={session_token};access_token={access_token}",
                "accesstoken": jwt_token.get('token'),
                "content-type": "application/json",
                "contenttype": "application/json",
                "loggeduser": str(codigo_usuario),
            }

            # Faz a requisição para obter os dados do pedido
            yield scrapy.Request(
                url=pedido_url,
                method="GET",
                headers=headers,
                cookies={
                    "sessiontoken": session_token,
                    "accesstoken": access_token,
                },
                callback=self.parse_pedido
            )
        else:
            self.logger.error(f"Falha no login: {response.status}")

    def parse_pedido(self, response):
        # Verifica se a requisição de pedido foi bem-sucedida
        if response.status == 200:
            # Processar os dados do pedido
            pedido_data = json.loads(response.text)

            # Filtrar as informações desejadas
            itens_filtrados = []
            for item in pedido_data.get('itens', []):
                item_info = {
                    'rejeicao': pedido_data.get('rejeicao'),
                    'produto_id': item['produto'].get('id'),
                    'produto_descricao': item['produto'].get('descricao'),
                    'quantidade_faturada': item.get('quantidadeFaturada')
                }
                itens_filtrados.append(item_info)
            

            output_dir = '/app/output'
            path = f'pedido_{self.filtro}_filtrado.json'
            if os.path.exists(output_dir):
                path = os.path.join(output_dir, path)

            # Salvar as informações filtradas em um arquivo JSON
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(itens_filtrados, f, ensure_ascii=False, indent=4)

            # Aqui você pode salvar ou processar os dados conforme necessário
        else:
            self.logger.error(f"Falha ao buscar os dados do pedido: {response.status}")