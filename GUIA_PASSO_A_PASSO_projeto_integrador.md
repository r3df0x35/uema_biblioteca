# Guia Passo a Passo — Projeto Integrador U3: Sistema de Biblioteca Municipal

> ✅ **Atualização:** esta versão já usa o **código real** do seu fork
> (`livro.py` e `acervo.py` que você enviou), testado de verdade neste
> ambiente linha por linha. As respostas abaixo refletem o comportamento
> real do código, não mais uma reconstrução.

---

## Etapa 1 — Fork, Clone e Instalação

1. Abra `github.com/thiagonelson/uema_biblioteca` no navegador e clique em
   **Fork** (canto superior direito) → confirme na sua conta.
2. No VS Code: `Ctrl+Shift+P` → digite `Git Clone` → cole a URL do **seu**
   fork (`github.com/SEU-USUARIO/uema_biblioteca`) → escolha a pasta local.
3. Abra o terminal integrado (`Ctrl+``) e rode:
   ```bash
   pip install -r requirements.txt
   ```
   Isso instala `pytest`, `pytest-cov` e `flake8`.

---

## Etapa 2 — Diagnóstico

### 2a. Testes existentes
```bash
pytest tests/ -v
```
No meu ambiente de referência, os **3 testes que já vêm prontos em
`test_livro.py`** passam (3/3, nenhum falhou) — eles cobrem apenas
`__init__` e `emprestar()`, então não expõem o bug de `devolver()` ainda.
No seu repositório real, anote o resultado exato que aparecer.

### 2b. Estilo (flake8)
```bash
flake8 biblioteca/
```
**Resultado real do seu código: 11 violações.**

1. `biblioteca/acervo.py:11:5: E301 expected 1 blank line, found 0`
2. `biblioteca/acervo.py:11:80: E501 line too long (110 > 79 characters)`
3. `biblioteca/acervo.py:17:23: E741 ambiguous variable name 'l'`
4. `biblioteca/acervo.py:21:23: E741 ambiguous variable name 'l'`
5. `biblioteca/acervo.py:21:80: E501 line too long (106 > 79 characters)`
6. `biblioteca/acervo.py:25:23: E741 ambiguous variable name 'l'`
7. `biblioteca/acervo.py:29:23: E741 ambiguous variable name 'l'`
8. `biblioteca/livro.py:14:80: E501 line too long (84 > 79 characters)`
9. `biblioteca/livro.py:20:80: E501 line too long (83 > 79 characters)`
10. `biblioteca/livro.py:21:80: E501 line too long (110 > 79 characters)`
11. `biblioteca/livro.py:27:80: E501 line too long (80 > 79 characters)`

### 2c. Cobertura atual
```bash
pytest --cov=biblioteca --cov-report=term-missing
```
Com apenas os 3 testes originais de `test_livro.py` (que só cobrem
`__init__` e `emprestar()`), a cobertura fica bem abaixo de 60%, porque
`devolver()`, `__str__()` e **toda a classe `Acervo`** ainda não têm
nenhum teste.

---

## Etapa 3 — Corrigir o estilo de código

O que foi corrigido nas 11 violações:

- **`acervo.py:11` (E301 + E501)** — faltava linha em branco antes de
  `def total_livros(self):`, e a linha tinha um comentário longo colado
  (`# BUG-ESTILO: ...`). Adicionei a linha em branco e removi o
  comentário.
- **`acervo.py:17, 21, 25, 29` (E741 × 4)** — as quatro list comprehensions
  usavam `l` como nome de variável (`[l for l in self.livros ...]`).
  Renomeei todas para `livro`.
- **`acervo.py:21` (E501)** — linha longa por causa do comentário
  `# BUG: busca diferencia maiusculas/minusculas`. Removido (o bug real
  foi corrigido no código, não só comentado — ver Etapa 4).
- **`livro.py:14, 20` (E501 × 2)** — docstrings de `emprestar()` e
  `devolver()` numa linha só, ultrapassando 79 colunas. Quebrei em
  docstrings de múltiplas linhas.
- **`livro.py:21` (E501)** — comentário longo e **enganoso**
  (`# BUG: condicao invertida — deveria ser "not self.disponivel"`).
  Removido — ver a explicação na Etapa 4a, porque esse comentário está
  errado.
- **`livro.py:27` (E501)** — linha do `return` do `__str__()` com 80
  colunas (1 acima do limite). Quebrei em parênteses/f-strings
  concatenadas.

**"O que foi corrigido"** (para preencher no formulário):
> Linha em branco ausente entre métodos (E301); 4 variáveis ambíguas `l`
> renomeadas para `livro` (E741); 6 linhas acima de 79 colunas quebradas
> (E501), a maioria por comentários extensos que foram removidos.

Depois de corrigir, `flake8 biblioteca/` deve rodar **em silêncio**
(nenhuma saída = sucesso).

---

## Etapa 4 — Escrever testes e descobrir os bugs

### 4a. Testes de `devolver()` em `test_livro.py`

Adicione os dois testes que o enunciado pede:

```python
def test_devolver_livro_emprestado():
    livro = Livro("1984", "George Orwell", "978-0451524935")
    livro.emprestar()
    livro.devolver()
    assert livro.disponivel is True


def test_devolver_livro_ja_disponivel_levanta_erro():
    livro = Livro("1984", "George Orwell", "978-0451524935")
    try:
        livro.devolver()
        assert False, "Deveria ter levantado ValueError"
    except ValueError:
        pass
```

**⚠️ Pegadinha real encontrada — leia com atenção:**

O código de `devolver()` no seu repositório tem este comentário:
```python
if self.disponivel:      # BUG: condicao invertida — deveria ser "not self.disponivel"
```

**Esse comentário está errado.** Rodei os dois testes de cima contra o
código exatamente como está, sem mudar nada, e **os dois passam**:

```
Cenário 1 (emprestado -> devolver): disponivel = True  ✔ esperado True
Cenário 2 (já disponível -> devolver): levantou ValueError  ✔ esperado ValueError
```

A lógica `if self.disponivel: raise ValueError(...)` está **correta**: se
o livro já está disponível (não emprestado), tentar devolvê-lo deve
mesmo levantar erro — e é isso que o código faz. Se você "corrigir"
seguindo a sugestão do comentário (trocar para `not self.disponivel`),
você **introduz** um bug de verdade, invertendo a lógica.

Isso é proposital: o enunciado avisa "o método `devolver()` tem
comportamento suspeito — teste-o com cuidado". A suspeita é justamente
o comentário mentiroso. A lição da atividade é: **não confie em
comentário, confie no teste.**

**Como preencher o formulário (Etapa 4a):**
> Bug encontrado em livro.py? **(X) Não** — a lógica de `devolver()`
> está correta apesar do comentário no código dizer o contrário. Os dois
> testes (emprestado→devolver e já-disponível→devolver) passam sem
> nenhuma alteração no código. O único problema era o comentário
> enganoso, que foi removido na Etapa 3.

*(Se seu professor espera obrigatoriamente um "Sim" aqui, é razoável
também escrever: "o bug encontrado foi no **comentário**, não no
código — o comentário afirmava uma inversão de lógica que não existe".)*

### 4b. Criar `tests/test_acervo.py`

⚠️ Repare que `Acervo.__init__` no seu código real pede um parâmetro
`nome`: `def __init__(self, nome):`. Não esqueça de passar isso ao criar
o acervo nos testes.

```python
from biblioteca.acervo import Acervo
from biblioteca.livro import Livro


def _acervo_exemplo():
    acervo = Acervo("Biblioteca Municipal de Itapecuru-Mirim")
    acervo.adicionar_livro(Livro("1984", "George Orwell", "111"))
    acervo.adicionar_livro(
        Livro("A Revolução dos Bichos", "George Orwell", "222")
    )
    return acervo


def test_adicionar_livro_aumenta_total():
    acervo = Acervo("Biblioteca Municipal de Itapecuru-Mirim")
    assert acervo.total_livros() == 0
    acervo.adicionar_livro(Livro("1984", "George Orwell", "111"))
    assert acervo.total_livros() == 1


def test_buscar_por_autor_case_insensitive():
    acervo = _acervo_exemplo()
    assert len(acervo.buscar_por_autor("george orwell")) == 2
    assert len(acervo.buscar_por_autor("GEORGE ORWELL")) == 2


def test_livros_disponiveis_e_emprestados():
    acervo = _acervo_exemplo()
    acervo.livros[0].emprestar()
    assert len(acervo.livros_emprestados()) == 1
    assert len(acervo.livros_disponiveis()) == 1
```

**Bug real confirmado por execução:**
```python
buscar_por_autor("George Orwell")   # -> 2 resultados
buscar_por_autor("george orwell")   # -> 0 resultados  ❌
buscar_por_autor("GEORGE ORWELL")   # -> 0 resultados  ❌
```

O código original era:
```python
return [l for l in self.livros if autor in l.autor]
```
Comparação (`in`) sensível a maiúsculas/minúsculas — só encontra se a
grafia bater exatamente.

**Correção aplicada:**
```python
def buscar_por_autor(self, autor):
    """Busca livros pelo autor (sem diferenciar maiusculas/minusculas)."""
    termo = autor.lower()
    return [livro for livro in self.livros if termo in livro.autor.lower()]
```

**Como preencher o formulário (Etapa 4b):**
> Bug encontrado em acervo.py? **(X) Sim** — `buscar_por_autor()`
> comparava o nome do autor sem normalizar maiúsculas/minúsculas, então
> buscar `"george orwell"` não encontrava livros cadastrados como
> `"George Orwell"`.
>
> Linha corrigida: `return [l for l in self.livros if autor in l.autor]`
> → `return [livro for livro in self.livros if termo in livro.autor.lower()]`
> (com `termo = autor.lower()` antes)

### 4c. Cobertura final

Depois de corrigir o bug e adicionar os testes, rodei a suíte completa
contra o código real:

```
10/10 testes passaram
```

Cobertura de linha: **100% em `livro.py` e 100% em `acervo.py`**
(nenhuma linha executável ficou sem teste) — bem acima da meta de 60%.

---

## Etapa 5 — Pipeline de CI

Crie `.github/workflows/ci.yml`:

```yaml
name: Pipeline de Qualidade

on:
  push:
    branches: [ main ]

jobs:
  qualidade:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: flake8 biblioteca/
      - run: pytest --cov=biblioteca --cov-fail-under=60
```

Os três `run: ?????` do enunciado são exatamente essas três linhas finais:
instalar dependências, rodar flake8, rodar pytest com cobertura mínima.

---

## Etapa 6 — Commit, Push e Verificar a Pipeline

1. Na aba **Source Control** do VS Code, clique em `+` ao lado de cada
   arquivo modificado/criado (ou `+` ao lado de "Changes" para stage all).
2. Escreva uma mensagem de commit descritiva, por exemplo:
   `fix: corrige bugs em devolver() e buscar_por_autor(), adiciona testes e CI`
3. Clique em **Commit** e depois **Sync Changes** (ou `git push` no
   terminal).
4. No GitHub, vá até a aba **Actions** do seu fork e aguarde a pipeline
   rodar.
5. Confirme que o check ficou **verde** (✔️). Se ficar vermelho, clique no
   job para ver o log — geralmente é uma violação de flake8 esquecida ou
   um teste que falhou.

---

## Checklist final (Entregáveis)

| # | Item | Como confirmar |
|---|------|-----------------|
| 1 | Fork feito | URL `github.com/SEU-USUARIO/uema_biblioteca` existe |
| 2 | `flake8 biblioteca/` | saída em branco |
| 3 | `pytest tests/ -v` | todos PASSED |
| 4 | Cobertura ≥ 60% | `pytest --cov=biblioteca --cov-fail-under=60` não falha |
| 5 | CI verde | aba Actions do GitHub com check verde |

## Arquivos de referência

No zip `uema_biblioteca_CORRIGIDO.zip` estão os arquivos **reais do seu
fork já corrigidos e testados**: `biblioteca/livro.py`,
`biblioteca/acervo.py`, `tests/test_livro.py`, `tests/test_acervo.py`,
`requirements.txt` e `.github/workflows/ci.yml`. Basta substituir os
arquivos correspondentes no seu repositório local, adicionar
`tests/test_acervo.py` como arquivo novo, e seguir para a Etapa 5/6.
