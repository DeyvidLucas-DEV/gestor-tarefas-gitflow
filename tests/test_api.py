import json
import threading
import urllib.error
import urllib.request

import pytest

from gestor_tarefas.api import criar_servidor


@pytest.fixture
def url():
    servidor = criar_servidor(porta=0)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{servidor.server_address[1]}"
    servidor.shutdown()
    servidor.server_close()


def requisitar(url, metodo="GET", corpo=None):
    dados = json.dumps(corpo).encode() if corpo is not None else None
    req = urllib.request.Request(url, data=dados, method=metodo)
    try:
        with urllib.request.urlopen(req) as resposta:
            return resposta.status, resposta.headers, json.loads(resposta.read())
    except urllib.error.HTTPError as erro:
        return erro.code, erro.headers, json.loads(erro.read())


def test_raiz_retorna_versao(url):
    status, _, corpo = requisitar(url + "/")
    assert status == 200
    assert corpo["app"] == "gestor-tarefas"


def test_criar_e_buscar_tarefa(url):
    status, _, criada = requisitar(url + "/tarefas", "POST", {"titulo": "Rodar o ZAP"})
    assert status == 201
    status, _, buscada = requisitar(f"{url}/tarefas/{criada['id']}")
    assert status == 200
    assert buscada["titulo"] == "Rodar o ZAP"


def test_titulo_invalido_retorna_400(url):
    status, _, _ = requisitar(url + "/tarefas", "POST", {"titulo": "  "})
    assert status == 400


def test_rota_inexistente_retorna_404(url):
    status, _, _ = requisitar(url + "/admin")
    assert status == 404


def test_cabecalhos_de_seguranca(url):
    _, cabecalhos, _ = requisitar(url + "/")
    assert cabecalhos["X-Content-Type-Options"] == "nosniff"
    assert "Content-Security-Policy" in cabecalhos
    assert "Python" not in cabecalhos["Server"]
