from dataclasses import dataclass, field


@dataclass
class Tarefa:
    id: int
    titulo: str
    concluida: bool = False


@dataclass
class GestorTarefas:
    _tarefas: dict[int, Tarefa] = field(default_factory=dict)
    _proximo_id: int = 1

    def adicionar(self, titulo: str) -> Tarefa:
        titulo = titulo.strip()
        if not titulo:
            raise ValueError("O título da tarefa não pode ser vazio.")
        tarefa = Tarefa(id=self._proximo_id, titulo=titulo)
        self._tarefas[tarefa.id] = tarefa
        self._proximo_id += 1
        return tarefa

    def buscar(self, tarefa_id: int) -> Tarefa:
        if tarefa_id not in self._tarefas:
            raise KeyError(f"Tarefa {tarefa_id} não encontrada.")
        return self._tarefas[tarefa_id]

    def concluir(self, tarefa_id: int) -> Tarefa:
        tarefa = self.buscar(tarefa_id)
        tarefa.concluida = True
        return tarefa

    def editar_titulo(self, tarefa_id: int, novo_titulo: str) -> Tarefa:
        novo_titulo = novo_titulo.strip()
        if not novo_titulo:
            raise ValueError("O título da tarefa não pode ser vazio.")
        tarefa = self.buscar(tarefa_id)
        tarefa.titulo = novo_titulo
        return tarefa

    def remover(self, tarefa_id: int) -> None:
        self.buscar(tarefa_id)
        del self._tarefas[tarefa_id]

    def listar(self, apenas_pendentes: bool = False) -> list[Tarefa]:
        tarefas = list(self._tarefas.values())
        if apenas_pendentes:
            return [t for t in tarefas if not t.concluida]
        return tarefas

def reabrir(self, tarefa_id: int) -> Tarefa:
        tarefa = self.buscar(tarefa_id)
        tarefa.concluida = False
        return tarefa
