class Actor:
    def __init__(self, name) -> None:
        self.name = name
        
    def __repr__(self) -> str:
        return self.name