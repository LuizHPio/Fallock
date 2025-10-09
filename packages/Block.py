class Block:
    color: list[int]
    symbol: str

    def __init__(self, symbol:str = 'X'):
        self.symbol = symbol