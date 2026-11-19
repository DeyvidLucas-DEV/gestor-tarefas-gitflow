"""API HTTP mínima do gestor de tarefas, usada como alvo do DAST (OWASP ZAP) na pipeline."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from gestor_tarefas import __version__
from gestor_tarefas.tarefas import GestorTarefas

TAMANHO_MAXIMO_CORPO = 10_000

CABECALHOS_SEGURANCA = {
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "geolocation=(), camera=(), microphone=()",
    "Cross-Origin-Resource-Policy": "same-origin",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Embedder-Policy": "require-corp",
    "Cache-Control": "no-store",
}


def criar_handler(gestor: GestorTarefas) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        # Não expõe a versão do Python no cabeçalho Server.
        server_version = "gestor-tarefas"
        sys_version = ""

        def _responder(self, status: int, corpo: object) -> None:
            dados = json.dumps(corpo, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(dados)))
            for nome, valor in CABECALHOS_SEGURANCA.items():
                self.send_header(nome, valor)
            self.end_headers()
            self.wfile.write(dados)

        def _tarefa_id(self) -> int | None:
            partes = self.path.strip("/").split("/")
            if len(partes) == 2 and partes[0] == "tarefas" and partes[1].isdigit():
                return int(partes[1])
            return None

        def do_GET(self) -> None:
            if self.path == "/":
                self._responder(200, {"app": "gestor-tarefas", "versao": __version__})
            elif self.path == "/tarefas":
                self._responder(200, [vars(t) for t in gestor.listar()])
            elif (tarefa_id := self._tarefa_id()) is not None:
                try:
                    self._responder(200, vars(gestor.buscar(tarefa_id)))
                except KeyError:
                    self._responder(404, {"erro": "Tarefa não encontrada."})
            else:
                self._responder(404, {"erro": "Rota não encontrada."})

        def do_POST(self) -> None:
            if self.path != "/tarefas":
                self._responder(404, {"erro": "Rota não encontrada."})
                return
            try:
                tamanho = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                tamanho = -1
            if tamanho < 0:
                self._responder(400, {"erro": "Content-Length inválido."})
                return
            if tamanho > TAMANHO_MAXIMO_CORPO:
                self._responder(413, {"erro": "Corpo da requisição muito grande."})
                return
            try:
                dados = json.loads(self.rfile.read(tamanho) or b"{}")
                titulo = dados["titulo"]
                if not isinstance(titulo, str):
                    raise TypeError
                tarefa = gestor.adicionar(titulo)
            except (ValueError, KeyError, TypeError):
                self._responder(400, {"erro": "Envie um JSON com um 'titulo' não vazio."})
                return
            self._responder(201, vars(tarefa))

        def log_message(self, formato: str, *args: object) -> None:
            pass

    return Handler


def criar_servidor(host: str = "127.0.0.1", porta: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, porta), criar_handler(GestorTarefas()))


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    porta = int(os.environ.get("PORT", "8000"))
    print(f"API do gestor de tarefas em http://{host}:{porta}")
    criar_servidor(host, porta).serve_forever()
