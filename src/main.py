import os
import shutil

def copy_source_to_destination(source, destination):
    print(f'Source: {source} -> Destination: {destination}')

    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    shutil.copytree(source, destination)

def main():
    copy_source_to_destination('static', 'public')

main()