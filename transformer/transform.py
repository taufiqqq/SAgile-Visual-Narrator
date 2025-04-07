import plantuml
import requests
from .Actor import Actor
from .UseCase import UseCase

class Transformer:
    def __init__(self, userStories, systemName) -> None:
        self.userStories = userStories
        self.systemName = systemName
        self.actors = None
        self.useCases = None
        self.relationships = None
        self.plantuml_text = None
        self.plantuml_url = None
        self.image_data = None

    def create_relationships(self) -> None:
        actors = {}
        useCases = {}
        relationships = []
        
        for userStory in self.userStories:
            # extracting role into an Actor instance
            role = userStory['role']
            if role in actors:
                actor = actors[role]
            else:
                actor = Actor(role)
                actors[role] = actor
                
            # extracting means into a UseCase instance
            means = userStory['means']
            if means in useCases:
                useCase = useCases[means]
            else:
                useCase = UseCase(means)
                useCases[means] = useCase
                
            # making a relationship between actor and use case
            # check if relationship already exists
            relationship = (actor, useCase)
            if relationship not in relationships:
                relationships.append(relationship)
                
        # another loop, go through all ends
        # for each ends, find a relationship that has usecase with same name
        for userStory in self.userStories:
            if userStory['ends'] != '':
                ends = userStory['ends']
                means = userStory['means']
                found = False
                for actor, uc in relationships:
                    if uc == ends:
                        # create new usecases with ends as main, uc as includes
                        # put in useCases and relationships
                        useCase_main = UseCase(ends)
                        useCase_include = UseCase(means)
                        useCase_main.add_include(useCase_include)
                        
                        useCases[ends] = useCase_main
                        relationship = (useCase_main, 'include')
                        if relationship not in relationships:
                            relationships.append(relationship)
                            
                        found = True
                        break
                    
                # remove actor, uc
                if found:
                    for actor, uc in relationships:
                        if uc == userStory['means']:
                            relationships.remove((actor, uc))
                            break
                
        self.actors = actors
        self.useCases = useCases
        self.relationships = relationships

    def create_plantuml_text(self) -> None:
        plantuml = '\n@startuml\nleft to right direction\n'
        
        # declare actors
        for key, item in self.actors.items():
            plantuml += f'\nactor "{item}"'
        
        # declare uc
        plantuml += f'\n\nrectangle {self.systemName} {{'
        for key, item in self.useCases.items():
            plantuml += f'\n\tusecase "{item}"'
        plantuml += '\n}\n'
        
        # do connection
        actorIndex = -1
        prevActor = None
        for r1, r2 in self.relationships:
            # relationship between actor and uc
            if isinstance(r1, Actor) and isinstance(r2, UseCase):
                if r1 != prevActor:
                    prevActor = r1
                    actorIndex += 1
                
                if actorIndex % 2 == 0:
                    plantuml += f'\n"{r1}" --> "{r2}"'
                else:
                    plantuml += f'\n"{r2}" <-- "{r1}"'
            # relationship between uc and uc
            else:
                if isinstance(r1, UseCase):
                    if r2 == 'include':
                        for incl in r1.get_includes():
                            plantuml += f'\n"{r1}" .> "{incl}" : {r2}'
                
        plantuml += '\n\n@enduml'
        self.plantuml_text = plantuml
        print("\n=== PlantUML Text ===")
        print(self.plantuml_text)
        print("===================\n")

    def make_diagram(self) -> None:
        # Create PlantUML server instance with PNG format
        plantuml_server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/png/')
        
        # Generate the PlantUML URL
        self.plantuml_url = plantuml_server.get_url(self.plantuml_text)
        print("\n=== PlantUML URL ===")
        print(self.plantuml_url)
        print("==================\n")
        
        # Fetch the actual image data
        response = requests.get(self.plantuml_url)
        if response.status_code == 200:
            self.image_data = response.content
        else:
            self.image_data = None
        
    def get_plantuml_text(self) -> str:
        return self.plantuml_text
    
    def get_plantuml_url(self) -> str:
        return self.plantuml_url
        
    def get_image_data(self) -> bytes:
        return self.image_data
