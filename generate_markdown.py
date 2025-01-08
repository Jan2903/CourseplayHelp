import os
import json
import shutil

# Constants for directories
BASE_DIR = os.getcwd()
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TRANSLATION_DIR = os.path.join(BASE_DIR, "translation_data")
IMAGES_DIR = os.path.join(BASE_DIR, "docs", "assets", "images")

# Ensure required directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

def copy_image_to_docs(image_filename):
    """Copy an image from the translation_data folder to the docs/assets/images folder."""
    source_path = os.path.join(TRANSLATION_DIR, image_filename)
    destination_path = os.path.join(IMAGES_DIR, image_filename)
    if os.path.exists(source_path):
        shutil.copy(source_path, destination_path)
    else:
        print(f"Warning: Image file '{image_filename}' not found in translation_data folder.")

def create_markdown_file(language, category_title, page):
    """Creates a markdown file for a given page."""
    filename = f"{page['title']['raw']}.md"
    file_path = os.path.join(OUTPUT_DIR, language, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        # Write the title
        f.write(f"# {page['title']['raw']}\n\n")
        
        # Write the paragraphs
        for paragraph in page.get("paragraphs", []):
            if "title" in paragraph and paragraph["title"]["raw"]:
                f.write(f"## {paragraph['title']['raw']}\n\n")
            if "text" in paragraph and paragraph["text"]["raw"]:
                f.write(f"{paragraph['text']['raw']}\n\n")
            if "image" in paragraph and paragraph["image"]["filename"]:
                # Copy the image to the docs/assets/images folder
                copy_image_to_docs(paragraph["image"]["filename"])
                # Adjust the image path for MkDocs
                image_path = f"assets/images/{paragraph['image']['filename']}"
                f.write(f"![{paragraph['text']['raw']}]({image_path})\n\n")

def process_language(language, language_file, config):
    """Processes a single language and generates markdown files."""
    language_dir = os.path.join(OUTPUT_DIR, language)
    os.makedirs(language_dir, exist_ok=True)

    # Load the language-specific translation data
    with open(language_file, "r", encoding="utf-8") as lang_file:
        translations = json.load(lang_file)

    # Process categories and pages
    for category in config:
        category_title = translations.get(category["title"]["raw"], category["title"]["raw"])
        for page in category["pages"]:
            create_markdown_file(language, category_title, page)

def main():
    # Load the main config file
    config_path = os.path.join(BASE_DIR, "translation_data", "config.json")
    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    # Process each language
    for language_code in os.listdir(TRANSLATION_DIR):
        language_file = os.path.join(TRANSLATION_DIR, language_code)
        if language_file.endswith(".json"):
            language = os.path.splitext(language_code)[0]
            process_language(language, language_file, config)

if __name__ == "__main__":
    main()
