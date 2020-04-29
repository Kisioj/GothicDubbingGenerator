import antlr4


class SyntaxErrorListener(antlr4.DiagnosticErrorListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors_count = 0

    def syntaxError(self, *args, **kwargs):
        self.errors_count += 1
