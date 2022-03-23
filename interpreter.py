INTEGER, PLUS, MINUS, MUTIPLY, DIVISION, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUTIPLY', 'DIVISION', 'EOF'

# Modify the code to intepret expressions with both addition and subtraction

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
        raise Exception('Error parsing input')

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

    def expr(self):

        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token

        if op.type == PLUS:
            self.eat(PLUS)
        elif op.type == MINUS:
            self.eat(MINUS)
        elif op.type == MUTIPLY:
            self.eat(MUTIPLY)
        else:
            self.eat(DIVISION)

        right = self.current_token
        self.eat(INTEGER)

        if op.type == PLUS:
            return left.value + right.value
        elif op.type == MINUS:
            return left.value - right.value
        elif op.type == MUTIPLY:
            return left.value * right.value

        return left.value / right.value


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
