class UseCase:
    def __init__(self, name) -> None:
        self.name = name
        self.includes = []
        self.extends = []
        
    def __repr__(self) -> str:
        return self.name
    
    def __eq__(self, __value: str) -> bool:
        return self.name == __value
    
    def add_include(self, use_case) -> None:
        self.includes.append(use_case)
        
    def add_extend(self, use_case) -> None:
        self.extends.append(use_case)
        
    def get_includes(self) -> list:
        return self.includes