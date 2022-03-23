INTEGER, PLUS, MINUS, MUTIPLY, DIVISION, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUTIPLY', 'DIVISION', 'EOF'

class Token(object):

    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return 'Token ({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self) -> str:
        return self.__str__()


class Interpreter(object):

    def __init__(self, text) -> None:
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid syntax')

    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        whole_number = ''

        while self.current_char is not None and self.current_char.isdigit():
            whole_number += self.current_char
            self.advance()

        return int(whole_number)

    def get_next_token(self):

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIVISION, '/')

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        if (self.current_token.type == token_type):
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):

        self.current_token = self.get_next_token()

        result = self.term()

        while self.current_token.type in (PLUS, MINUS, MUTIPLY, DIVISION):

            token = self.current_token

            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()
            elif token.type == MUTIPLY:
                self.eat(MUTIPLY)
                result = result * self.term()
            else:
                self.eat(DIVISION)
                result = result / self.term()

        return result


def main():
    while True:
        try:
            text = input('> ')
        except EOFError:
            break

        if not text:
            continue

        interpreter = Interpreter(text)

        result = interpreter.expr()

        print(result)


if __name__ == '__main__':
    main()
