# Gestor de Tarefas: Gitflow + GitHub Actions

Projeto simples em Python usado para demonstrar o fluxo **Gitflow** e uma **pipeline de CI/CD** no GitHub Actions.

## Como rodar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest                         # roda os testes
ruff check .                   # verifica o estilo do código
PYTHONPATH=src python -m gestor_tarefas
```

## Pipeline (`.github/workflows/ci.yml`)

Roda a cada push em `main`, `develop`, `feature/*`, `release/*`, `hotfix/*` e em todo Pull Request para `main` ou `develop`.

| Etapa | O que faz |
|---|---|
| **Lint** | `ruff check` procura erros e problemas de estilo |
| **Testes** | `pytest` com cobertura, em Python 3.10 e 3.12 (matriz) |
| **Release** | quando uma tag `v*` é enviada, cria a Release no GitHub automaticamente |

Cada etapa só roda se a anterior passar.

## Branches do Gitflow

| Branch | Para que serve |
|---|---|
| `main` | código em produção; só recebe merge de `release/*` e `hotfix/*` |
| `develop` | integração das funcionalidades prontas |
| `feature/*` | uma funcionalidade nova, criada a partir de `develop` |
| `release/*` | preparação de uma versão, criada a partir de `develop` |
| `hotfix/*` | correção urgente, criada a partir de `main` |

## Roteiro para a apresentação

### 1. Feature
```bash
git checkout develop && git pull
git checkout -b feature/minha-funcionalidade
# editar o código e os testes
git add . && git commit -m "feat: minha funcionalidade"
git push -u origin feature/minha-funcionalidade
gh pr create --base develop --title "feat: minha funcionalidade" --body "Nova funcionalidade"
# mostrar a pipeline rodando na aba Actions e no PR
gh pr merge --merge --delete-branch
```

### 2. Release
```bash
git checkout develop && git pull
git checkout -b release/1.1.0
# atualizar a versão em pyproject.toml e src/gestor_tarefas/__init__.py
git commit -am "chore: versão 1.1.0"
git push -u origin release/1.1.0
gh pr create --base main --title "Release 1.1.0" --body "Versão 1.1.0"
gh pr merge --merge
git checkout main && git pull
git tag -a v1.1.0 -m "Versão 1.1.0" && git push origin v1.1.0   # dispara o job de Release
git checkout develop && git merge main && git push              # leva a release de volta para develop
git push origin --delete release/1.1.0
```

### 3. Hotfix
```bash
git checkout main && git pull
git checkout -b hotfix/1.1.1
# corrigir o problema
git commit -am "fix: correção urgente"
git push -u origin hotfix/1.1.1
gh pr create --base main --title "Hotfix 1.1.1" --body "Correção urgente"
gh pr merge --merge
git checkout main && git pull
git tag -a v1.1.1 -m "Versão 1.1.1" && git push origin v1.1.1
git checkout develop && git merge main && git push
git push origin --delete hotfix/1.1.1
```
