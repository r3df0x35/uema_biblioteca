from biblioteca.livro import Livro


def test_criar_livro():
    livro = Livro("1984", "George Orwell", "978-0451524935")
    assert livro.titulo == "1984"
    assert livro.autor == "George Orwell"
    assert livro.disponivel is True


def test_emprestar_livro_disponivel():
    livro = Livro("1984", "George Orwell", "978-0451524935")
    livro.emprestar()
    assert livro.disponivel is False


def test_emprestar_livro_ja_emprestado_levanta_erro():
    livro = Livro("1984", "George Orwell", "978-0451524935")
    livro.emprestar()
    try:
        livro.emprestar()
        assert False, "Deveria ter levantado ValueError"
    except ValueError:
        pass


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


def test_str_livro():
    livro = Livro("1984", "George Orwell", "978-0451524935")
    assert "1984" in str(livro)
    assert "Disponivel" in str(livro)
    livro.emprestar()
    assert "Emprestado" in str(livro)
