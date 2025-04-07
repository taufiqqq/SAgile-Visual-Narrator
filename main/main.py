import argparse
from parser.parser import Parser
from transformer.transform import Transformer
from transformer import transform

def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='the name of the file')
    parser.add_argument('systemname', help='the name of the system')
    args = parser.parse_args()

    userStories = []
    with open(args.filename) as f:
        for line in f:
            userStories.append(line)
    systemName = args.systemname
            
    main = Main(userStories, systemName)
    main.init_parsing()
    main.init_transform()
    print(f"PlantUML URL: {main.get_plantuml_url()}")

class Main:
    def __init__(self, userStories, systemName) -> None:
        self.userStories = userStories
        self.systemName = systemName
        self.parser = Parser(userStories)
        self.transformer = None
    
    def init_parsing(self) -> None:
        self.parser.start_parse()
        
    def init_transform(self) -> None:
        self.transformer = Transformer(self.parser.get_parsed(), self.systemName)
        self.transformer.create_relationships()
        self.transformer.create_plantuml_text()
        self.transformer.make_diagram()
        
    def get_plantuml_url(self) -> str:
        return self.transformer.get_plantuml_url()
        
    def get_image_data(self) -> bytes:
        return self.transformer.get_image_data()