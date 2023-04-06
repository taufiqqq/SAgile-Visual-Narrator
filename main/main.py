import argparse
from parser.parser import parse_main
import spacy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='the name of the file')
    args = parser.parse_args()

    with open(args.filename) as f:
        userStories = parse_main(f)
        for usrSt in userStories:        
            print(usrSt)

    # TODO apply heuristics