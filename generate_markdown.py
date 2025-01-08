import os
import json

# Constants for directory and file paths
CONFIG_FILE = "./translation_data/config.json"
TRANSLATION_DIR = "./translation_data"
OUTPUT_DIR = "./docs"

def create_markdown_file(language, page, output_dir):
    """Creates a Markdown file with content from JSON data."""
    # File path for the Markdown file
    filename = os.path.join(output_dir, f"{page['title']['raw']}.md")
    
    # Write the Markdown file
    with open(filename, "w", encoding="utf-8") as md_file:
        # Title
        md_file.write(f"# {page['title']}\n\n")
        
        # Content: Paragraphs and Images
        for paragraph in page.get("paragraphs", []):
            if "title" in paragraph:
                md_file.write(f"## {paragraph['title']}\n\n")
            if "text" in paragraph:
                md_file.write(f"{paragraph['text']}\n\n")
            if "image" in paragraph and paragraph["image"].get("filename"):
                image_path = f"/assets/{language}/{paragraph['image']['filename']}"
                md_file.write(f"![{paragraph['text']['raw']}]({image_path})\n\n")


def generate_site():
    """Main function to generate the site content."""
    # Load the configuration file
    with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    
    # Loop through supported languages
    for language_file in os.listdir(TRANSLATION_DIR):
        if language_file.endswith(".json") and language_file != "config.json":
            language_code = language_file.split(".")[0]
            output_dir = os.path.join(OUTPUT_DIR, language_code)
            
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Load the language translation file
            with open(os.path.join(TRANSLATION_DIR, language_file), "r", encoding="utf-8") as lang_file:
                translations = json.load(lang_file)
            
            # Generate Markdown files for each page
            for page in config[0]["pages"]:
                # Translate titles and paragraphs
                page["title"] = translations.get(page["title"]["raw"], page["title"])
                for paragraph in page.get("paragraphs", []):
                    if "title" in paragraph:
                        paragraph["title"] = translations.get(paragraph["title"]["raw"], paragraph["title"])
                    if "text" in paragraph:
                        paragraph["text"] = translations.get(paragraph["text"]["raw"], paragraph["text"])
                
                # Create the Markdown file
                create_markdown_file(language_code, page, output_dir)

if __name__ == "__main__":
    generate_site()
