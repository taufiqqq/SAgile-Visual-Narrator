from . import Actor
from . import UseCase
import os

def create_relationships(userStories):
    actors = {}
    useCases = {}
    relationships = []
    
    for userStory in userStories:
        # extracting role into an Actor instance
        role = userStory['role']
        if role in actors:
            actor = actors[role]
        else:
            actor = Actor.Actor(role)
            actors[role] = actor
            
        # extracting means into a UseCase instance
        means = userStory['means']
        if means in useCases:
            useCase = useCases[means]
        else:
            useCase = UseCase.UseCase(means)
            useCases[means] = useCase
            
        # making a relationship between actor and use case
        # check if relationship already exists
        relationship = (actor, useCase)
        if relationship not in relationships:
            relationships.append(relationship)
            
    return actors, useCases, relationships

def create_text_file(actors, use_cases, relationships, system):
    plantuml = '\n@startuml\nleft to right direction\n'
    
    # declare actors
    for key, item in actors.items():
        plantuml += f'\nactor "{item}"'
    
    # declare uc
    plantuml += f'\n\nrectangle {system} {{'
    for key, item in use_cases.items():
        plantuml += f'\n\tusecase "{item}"'
    plantuml += '\n}\n'
    
    # do connection
    actorIndex = -1
    prevActor = None
    for actor,uc in relationships:
        if actor != prevActor:
            prevActor = actor
            actorIndex += 1
        
        if actorIndex % 2 == 0:
            plantuml += f'\n"{actor}" --> "{uc}"'
        else:
            plantuml += f'\n"{uc}" <-- "{actor}"'
            
    plantuml += '\n\n@enduml'
    
    ucdName = f"{system}.txt"
    # cwd = os.getcwd()
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pathToUCDText = os.path.join(app_dir, 'transformer', 'plantuml', ucdName)
    with open(pathToUCDText, "w") as f:
        f.write(plantuml)
        
    return os.path.dirname(pathToUCDText), ucdName

def make_diagram(path, filename):
    # change path to plantuml directory
    os.chdir(path)
    
    # add java to PATH in venv
    # # ! java_path needs to be manually configured with the path to java.exe, check PATH in system environment variables
    current_path = os.environ.get('PATH', '')
    java_path = 'C:\Program Files (x86)\Common Files\Oracle\Java\javapath'
    new_path = f"{java_path};{current_path}" if current_path else java_path
    os.environ['PATH'] = new_path
    
    # run command to make diagram
    os.system(f"java -jar plantuml.jar {filename}")
    