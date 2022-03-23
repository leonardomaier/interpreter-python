INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'


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

    def error(self):
        raise Exception('Error parsing input')
    
    def get_next_token(self):
        
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token
        
        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        
        self.error()

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
        self.eat(PLUS)

        right = self.current_token
        self.eat(INTEGER)

        return left.value + right.value


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
