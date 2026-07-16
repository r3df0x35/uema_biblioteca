class Livro:
    """Representa um livro do acervo."""

    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponivel = True

    def emprestar(self):
        """Registra o emprestimo do livro.

        Levanta erro se ja estiver emprestado.
        """
        if not self.disponivel:
            raise ValueError(f"O livro '{self.titulo}' ja esta emprestado.")
        self.disponivel = False

    def devolver(self):
        """Registra a devolucao do livro.

        Levanta erro se ja estiver disponivel.
        """
        if self.disponivel:
            raise ValueError(f"O livro '{self.titulo}' nao esta emprestado.")
        self.disponivel = True

    def __str__(self):
        status = "Disponivel" if self.disponivel else "Emprestado"
        return (
            f"'{self.titulo}' de {self.autor} "
            f"(ISBN: {self.isbn}) [{status}]"
        )
