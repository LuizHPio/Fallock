class Block:
    is_empty: bool
    color: list[int]

    def __init__(self, is_empty:bool = False):
        self.is_empty = is_empty
