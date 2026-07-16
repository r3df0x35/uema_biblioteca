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


def test_buscar_por_titulo_parcial_case_insensitive():
    acervo = _acervo_exemplo()
    resultado = acervo.buscar_por_titulo("revolução")
    assert len(resultado) == 1
    assert resultado[0].titulo == "A Revolução dos Bichos"


def test_buscar_por_autor_case_insensitive():
    acervo = _acervo_exemplo()
    resultado_minusculo = acervo.buscar_por_autor("george orwell")
    resultado_maiusculo = acervo.buscar_por_autor("GEORGE ORWELL")
    assert len(resultado_minusculo) == 2, (
        "buscar_por_autor deveria ignorar maiúsculas/minúsculas"
    )
    assert len(resultado_maiusculo) == 2


def test_livros_disponiveis_e_emprestados():
    acervo = _acervo_exemplo()
    acervo.livros[0].emprestar()
    assert len(acervo.livros_emprestados()) == 1
    assert len(acervo.livros_disponiveis()) == 1
