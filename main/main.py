import argparse
from parser.parser import parse_main
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
            
    main(userStories, systemName)

def main(userStories, systemName):
    user_stories = parse_main(userStories)
    actors, uc, relationships = transform.create_relationships(user_stories)
    path, filename = transform.create_text_file(actors, uc, relationships, systemName)
    transform.make_diagram(path, filename)
    
    print("Done")
    return path, filename