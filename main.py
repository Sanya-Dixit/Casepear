from urllib.parse import urljoin, urlparse
import gradio as gr
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS
import os
import requests
from bs4 import BeautifulSoup

# Function to download and save a file
def download_file(url, folder, headers):
    try:
        local_filename = os.path.join(folder, os.path.basename(urlparse(url).path))
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
    except requests.exceptions.RequestException as e:
        return f"Failed to download file: {e}"

def clone_website(url, clone_media_only=False):
    base_dir = 'resources'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        os.makedirs(base_dir, exist_ok=True)
        domain_name = urlparse(url).netloc
        if clone_media_only:
            output_dir = os.path.join(base_dir, 'media', domain_name)
        else:
            output_dir = os.path.join(base_dir, 'websites', domain_name)
        os.makedirs(output_dir, exist_ok=True)

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        tags_to_clone = ['img', 'video'] if clone_media_only else ['link', 'script', 'img', 'video']

        for tag in soup.find_all(tags_to_clone):
            if tag.name == 'link' and tag.get('rel') == ['stylesheet']:
                file_url = urljoin(url, tag['href'])
                attr = 'href'
            elif tag.name == 'script' and tag.get('src'):
                file_url = urljoin(url, tag['src'])
                attr = 'src'
            elif tag.name == 'img' and tag.get('src'):
                file_url = urljoin(url, tag['src'])
                attr = 'src'
            elif tag.name == 'video' and tag.get('src'):
                file_url = urljoin(url, tag['src'])
                attr = 'src'
            else:
                continue

            local_file_path = download_file(file_url, output_dir, headers)
            if local_file_path.startswith("Failed"):
                raise Exception(local_file_path)
            tag[attr] = os.path.basename(local_file_path)

        if not clone_media_only:
            with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as file:
                file.write(str(soup))

        return f"Successfully cloned {'media' if clone_media_only else 'the complete website'} from {url} to {output_dir}"

    except Exception as e:
        return f"Failed to clone website: {e}"

def extract_metadata(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if not exif_data:
            return "No EXIF metadata found.", None
        metadata = {TAGS.get(tag_id, tag_id): value for tag_id, value in exif_data.items()}
        metadata_str = "\n".join(f"{tag}: {value}" for tag, value in metadata.items())
        return metadata_str, image_path
    except FileNotFoundError:
        return "Error: File not found.", None
    except UnidentifiedImageError:
        return "Error: Cannot identify image file. Please upload a valid image.", None
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", None

def clear_metadata(image_path):
    try:
        img = Image.open(image_path)
        img.save(image_path, exif=b'')
        return image_path
    except Exception as e:
        return f"An error occurred while clearing metadata: {str(e)}"

def process_image(image_path, clear_metadata_option):
    metadata_str, image_path = extract_metadata(image_path)
    if clear_metadata_option and image_path:
        cleared_image_path = clear_metadata(image_path)
        if isinstance(cleared_image_path, str) and cleared_image_path.startswith("Error"):
            return cleared_image_path, gr.update(visible=False), None
        return "Metadata cleared successfully. Download the image below.", gr.update(value=cleared_image_path, visible=True), None
    else:
        if metadata_str and image_path:
            metadata_file_path = os.path.splitext(image_path)[0] + "_metadata.txt"
            with open(metadata_file_path, 'w') as f:
                f.write(metadata_str)
            return metadata_str, gr.update(visible=False), metadata_file_path
        return metadata_str, gr.update(visible=False), None

# Create separate interfaces for website cloning and image metadata processing
website_cloner_interface = gr.Interface(
    fn=clone_website,
    inputs=[
        gr.Textbox(lines=1, placeholder="Enter URL here", label="Website URL"),
        gr.Checkbox(label="Clone Media Only")
    ],
    outputs=[gr.Textbox(label="Cloning Result")],
    title="Website Cloner",
    description="Enter the URL of the website you want to clone."
)

image_metadata_interface = gr.Interface(
    fn=process_image,
    inputs=[
        gr.Image(type="filepath"), 
        gr.Checkbox(label="Clear Metadata")
    ],
    outputs=[
        gr.Textbox(), 
        gr.File(label="Download Image", visible=False),
        gr.File(label="Download Metadata", visible=True)
    ],
    title="Image Metadata Processor",
    description="Upload an image to extract its metadata. Optionally clear the metadata and download the modified image."
)

# Combine the interfaces into a tabbed interface
iface = gr.TabbedInterface(
    [website_cloner_interface, image_metadata_interface],
    ["Website Cloner", "Image Metadata Processor"],
    title="CasePear"
)

if __name__ == "__main__":
    iface.launch()