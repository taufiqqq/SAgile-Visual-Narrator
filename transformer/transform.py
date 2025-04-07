import tempfile
import os

class Transformer:
    def __init__(self, userStories, systemName) -> None:
        self.userStories = userStories
        self.systemName = systemName
        self.actors = None
        self.useCases = None
        self.relationships = None
        self.ucdPath = None
        self.ucdName = None

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

    def create_text_file(self) -> None:
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
        
        ucdName = f"{self.systemName}.txt"

        # Use tempfile to create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Path for the UCD text file in the temporary directory
            pathToUCDText = os.path.join(temp_dir, ucdName)
            
            # Write the PlantUML text to the temporary file
            with open(pathToUCDText, "w") as f:
                f.write(plantuml)
            
            # Store path and filename for later use
            self.ucdPath = temp_dir  # Temporary directory path
            self.ucdName = ucdName    # The file name

    def make_diagram(self) -> None:
        # change path to plantuml directory
        os.chdir(self.ucdPath)
        
        # add java to PATH in venv
        current_path = os.environ.get('PATH', '')
        java_path = 'C:\Program Files (x86)\Common Files\Oracle\Java\javapath'
        new_path = f"{java_path};{current_path}" if current_path else java_path
        os.environ['PATH'] = new_path
        
        # run command to make diagram
        os.system(f"java -jar plantuml.jar {self.ucdName}")
        
    def get_filepath(self) -> str:
        return self.ucdPath
    
    def get_filename(self) -> str:
        return self.ucdName
