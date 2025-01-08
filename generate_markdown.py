import os
import json

# Constants for paths
CURRENT_DIR = os.getcwd()
CONFIG_FILE = os.path.join(CURRENT_DIR, "translation_data", "config.json")
TRANSLATION_DIR = os.path.join(CURRENT_DIR, "translation_data")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "docs")

def create_markdown_file(language_code, page, output_dir):
    """
    Creates a markdown file for a given page in a specific language.
    """
    # Use the raw title for the file name
    file_name = f"{page['raw_title']}.md"
    file_path = os.path.join(output_dir, file_name)
    
    with open(file_path, "w", encoding="utf-8") as md_file:
        # Write the page title
        md_file.write(f"# {page['title']}\n\n")
        
        # Write paragraphs
        for paragraph in page.get("paragraphs", []):
            if paragraph["title"]:
                md_file.write(f"## {paragraph['title']}\n\n")
            if paragraph["text"]:
                md_file.write(f"{paragraph['text']}\n\n")
            if paragraph["image"]["filename"]:
                image_path = os.path.join("images", paragraph["image"]["filename"])
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
                
                # Generate Markdown files for each page
                for page in pages:
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
                    create_markdown_file(language_code, page_data, language_output_dir)
                    
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    generate_site()
