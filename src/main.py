import os
import shutil

from block_markdown import extract_title, markdown_to_html_node

def copy_source_to_destination(source, destination):
    print(f'Moving files\nSource: {source} -> Destination: {destination}\n')

    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    shutil.copytree(source, destination)

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    # Read source and template files
    source_file = open(from_path, 'r')
    source_content = source_file.read()
    template_file = open(template_path, 'r')
    template_content = template_file.read()

    # Convert markdown to HTML and extract title
    html_content = markdown_to_html_node(source_content).to_html()
    title = extract_title(source_content)

    # Replace template placeholders with content
    finished_template = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
    
    # Write to destination file
    destination_file = open(dest_path, 'w')
    destination_file.write(finished_template)
    
    # Close files
    source_file.close()
    template_file.close()
    destination_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    entries = os.listdir(dir_path_content)

    for entry in entries:
        if os.path.isfile(f'{dir_path_content}/{entry}') and entry.endswith('.md'):
            generate_page(f'{dir_path_content}/{entry}', template_path, f'{dest_dir_path}/{entry.replace(".md", ".html")}')
        elif os.path.isdir(f'{dir_path_content}/{entry}'):
            os.makedirs(f'{dest_dir_path}/{entry}', exist_ok=True)
            generate_pages_recursive(f'{dir_path_content}/{entry}', template_path, f'{dest_dir_path}/{entry}')

def main():
    copy_source_to_destination('static', 'public')
    generate_pages_recursive('content', 'template.html', 'public')

main()