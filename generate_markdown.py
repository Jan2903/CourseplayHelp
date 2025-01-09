import os
import json
import shutil

# Constants for paths
CURRENT_DIR = os.getcwd()
CONFIG_FILE = os.path.join(CURRENT_DIR, "translation_data", "config.json")
TRANSLATION_DIR = os.path.join(CURRENT_DIR, "translation_data")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "docs")
IMAGES_DIR = os.path.join(CURRENT_DIR, "docs", "assets", "images")

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

def format_text_with_line_breaks(text):
    """Format text by replacing detected newlines with Markdown-compatible line breaks."""
    return text.replace("\n", "  \n")

def create_markdown_file(language_code, page, output_dir, file_index):
    """
    Creates a markdown file for a given page in a specific language.
    """
    # Format the file name with a numbered prefix
    file_name = f"{file_index:02d}_page_{page['raw_title']}.md"
    file_path = os.path.join(output_dir, file_name)
    
    with open(file_path, "w", encoding="utf-8") as md_file:
        # Write the page title
        md_file.write(f"# {page['title']}\n\n")
        
        # Write paragraphs
        for paragraph in page.get("paragraphs", []):
            if paragraph["title"]:
                md_file.write(f"## {paragraph['title']}\n\n")
            if paragraph["text"]:
                # Format text with forced line breaks
                formatted_text = format_text_with_line_breaks(paragraph["text"])
                md_file.write(f"{formatted_text}\n\n")
            if paragraph["image"]["filename"]:
                # Copy the image to the docs/assets/images folder
                copy_image_to_docs(paragraph["image"]["filename"])
                # Adjust the image path for MkDocs
                image_path = f"../assets/images/{paragraph['image']['filename']}"
                md_file.write(f"![Image]({image_path})\n\n")

def generate_site():
    """
    Main function to generate markdown files for a multi-language site.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Load the configuration file
        with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        
        # Ensure config is a list and contains valid data
        if not isinstance(config, list) or not isinstance(config[0].get("pages", []), list):
            raise ValueError("Invalid config.json format. Ensure it has a list with 'pages' key.")
        
        # Load the pages from the configuration
        pages = config[0]["pages"]
        
        # Loop through supported languages
        for language_file in os.listdir(TRANSLATION_DIR):
            if language_file.endswith(".json") and language_file != "config.json":
                language_code = language_file.split(".")[0]
                language_output_dir = os.path.join(OUTPUT_DIR, language_code)
                
                # Ensure the language-specific output directory exists
                os.makedirs(language_output_dir, exist_ok=True)
                
                # Load the language translation file
                with open(os.path.join(TRANSLATION_DIR, language_file), "r", encoding="utf-8") as lang_file:
                    translations = json.load(lang_file)
                    if not isinstance(translations, dict):
                        raise ValueError(f"Invalid {language_file} format. Ensure it is a JSON object.")
                
                # Generate Markdown files for each page with numbering
                for index, page in enumerate(pages, start=1):
                    # Translate titles and paragraphs
                    page_data = {
                        "raw_title": page["title"]["raw"],
                        "title": translations.get(page["title"]["raw"], page["title"]["raw"]),
                        "paragraphs": []
                    }
                    
                    for paragraph in page.get("paragraphs", []):
                        translated_paragraph = {
                            "title": translations.get(paragraph["title"]["raw"], paragraph["title"]["raw"]) if paragraph["title"]["raw"] else "",
                            "text": translations.get(paragraph["text"]["raw"], paragraph["text"]["raw"]) if paragraph["text"]["raw"] else "",
                            "image": paragraph["image"]  # Images are the same across all languages
                        }
                        page_data["paragraphs"].append(translated_paragraph)
                    
                    # Create the Markdown file
                    create_markdown_file(language_code, page_data, language_output_dir, index)
                    
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    generate_site()
