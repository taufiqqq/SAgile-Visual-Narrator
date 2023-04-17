import argparse
from parser.parser import parse_main
from transformer import transform
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='the name of the file')
    parser.add_argument('systemname', help='the name of the system')
    args = parser.parse_args()

    userStories = None
    with open(args.filename) as f:
        userStories = parse_main(f)
        # for usrSt in userStories:        
        #     print(usrSt)
            
    actors, uc, relationships = transform.create_relationships(userStories)
    # print(actors, uc, relationships)
    
    path, filename = transform.create_text_file(actors, uc, relationships, args.systemname)
    
    transform.make_diagram(path,filename)

    # TODO apply heuristics