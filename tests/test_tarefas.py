import pytest

from gestor_tarefas.tarefas import GestorTarefas


def test_adicionar_tarefa():
    gestor = GestorTarefas()
    tarefa = gestor.adicionar("Estudar Gitflow")
    assert tarefa.id == 1
    assert tarefa.titulo == "Estudar Gitflow"
    assert not tarefa.concluida


def test_titulo_vazio_gera_erro():
    gestor = GestorTarefas()
    with pytest.raises(ValueError):
        gestor.adicionar("   ")


def test_concluir_tarefa():
    gestor = GestorTarefas()
    gestor.adicionar("Fazer pipeline")
    assert gestor.concluir(1).concluida


def test_remover_tarefa():
    gestor = GestorTarefas()
    gestor.adicionar("Remover depois")
    gestor.remover(1)
    assert gestor.listar() == []


def test_buscar_inexistente_gera_erro():
    gestor = GestorTarefas()
    with pytest.raises(KeyError):
        gestor.buscar(99)


def test_listar_apenas_pendentes():
    gestor = GestorTarefas()
    gestor.adicionar("A")
    gestor.adicionar("B")
    gestor.concluir(1)
    pendentes = gestor.listar(apenas_pendentes=True)
    assert [t.titulo for t in pendentes] == ["B"]


def test_editar_titulo():
    gestor = GestorTarefas()
    gestor.adicionar("Titulo antigo")
    assert gestor.editar_titulo(1, "Titulo novo").titulo == "Titulo novo"


def test_editar_titulo_vazio_gera_erro():
    gestor = GestorTarefas()
    gestor.adicionar("Tarefa")
    with pytest.raises(ValueError):
        gestor.editar_titulo(1, "")



  

