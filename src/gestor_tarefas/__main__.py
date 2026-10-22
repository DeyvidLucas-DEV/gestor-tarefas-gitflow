from gestor_tarefas.tarefas import GestorTarefas


def main() -> None:
    gestor = GestorTarefas()
    gestor.adicionar("Criar repositório no GitHub")
    gestor.adicionar("Configurar pipeline")
    gestor.concluir(1)
    for tarefa in gestor.listar():
        status = "[x]" if tarefa.concluida else "[ ]"
        print(f"{status} {tarefa.id} - {tarefa.titulo}")


if __name__ == "__main__":
    main()
