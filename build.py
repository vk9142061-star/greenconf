import os
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader
#vikash kumar
#2025mme033
# Load configuration
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

# Load data
with open('data.yml', 'r') as f:
    data = yaml.safe_load(f)

# Create build directory if it doesn't exist
BUILD_DIR = 'build'
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)
os.makedirs(BUILD_DIR)

# Copy static files
shutil.copytree('static', os.path.join(BUILD_DIR, 'static'))

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

# Process entries and categories
categories = {}
for entry in data:
    # Add taxonomies dict if not present
    if 'taxonomies' not in entry:
        entry['taxonomies'] = {'tags': [{'name': tag, 'slug': tag.lower().replace(' ', '-')} for tag in entry.get('tags', [])]}
    
    for category in entry['categories']:
        if category not in categories:
            categories[category] = []
        categories[category].append(entry)

# Generate pages
for category_name, entries in categories.items():
    category = {
        'name': category_name,
        'slug': category_name.lower().replace(' ', '-'),
        'count': len(entries)
    }
    
    all_categories = [
        {
            'name': cat,
            'slug': cat.lower().replace(' ', '-'),
            'count': len(cat_entries)
        }
        for cat, cat_entries in categories.items()
    ]

    # Get all unique tags
    all_tags = set()
    for entry in entries:
        if 'tags' in entry:
            all_tags.update(entry['tags'])

    taxonomies = {
        'tags': [{'name': tag, 'slug': tag.lower().replace(' ', '-')} for tag in sorted(all_tags)]
    }

    # Render template
    html = template.render(
        config=config,
        category=category,
        entries=entries,
        all_categories=all_categories,
        taxonomies=taxonomies,
        all_taxonomies=['tags']
    )

    # Write output file
    output_file = os.path.join(BUILD_DIR, f"{category['slug']}.html")
    with open(output_file, 'w') as f:
        f.write(html)

    # Create index.html for the first category
    if category_name == list(categories.keys())[0]:
        with open(os.path.join(BUILD_DIR, 'index.html'), 'w') as f:
            f.write(html)

print("Build completed. Files are in the 'build' directory.")
print("Run 'python -m http.server 8000' in the build directory to test locally.") 