import json

def save_file(outfile, files):
    with open(outfile, 'w') as outfile:
        json.dump(files, outfile, indent=4)

def load_file(infile):
    with open(infile, 'r') as infile:
        return json.load(infile)
