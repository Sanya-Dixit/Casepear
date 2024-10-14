# CasePear

CasePear is a tool that allows you to clone websites and process image metadata. It provides a user-friendly interface to perform these tasks using Gradio.

## Features

- Clone websites by providing a URL.
- Extract and optionally clear metadata from images.
- Download the extracted metadata as a `.txt` file.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository:**

    ```sh
    git clone https://github.com/kshuxx/casepear.git
    cd casepear
    ```

2. **Create a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```sh
        source venv/bin/activate
        ```

4. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. **Run the main script:**

    ```sh
    python main.py
    ```

2. **Open your web browser and navigate to the URL provided by Gradio (usually `http://127.0.0.1:7860`).

## Usage

### Website Cloner

1. Go to the "Website Cloner" tab.
2. Enter the URL of the website you want to clone.
3. Click the "Submit" button.
4. The cloning result will be displayed, and the cloned website will be saved in the [cloned_website](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5Cgit%5C%5Cweb_scrapper%5C%5Ccloned_website%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FE%3A%2Fgit%2Fweb_scrapper%2Fcloned_website%22%2C%22scheme%22%3A%22file%22%7D%7D) directory.

### Image Metadata Processor

1. Go to the "Image Metadata Processor" tab.
2. Upload an image file.
3. (Optional) Check the "Clear Metadata" checkbox if you want to clear the metadata from the image.
4. Click the "Submit" button.
5. The extracted metadata will be displayed, and you can download the metadata as a `.txt` file. If you chose to clear the metadata, you can also download the modified image.

## .gitignore

A [.gitignore](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5Cgit%5C%5Cweb_scrapper%5C%5C.gitignore%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FE%3A%2Fgit%2Fweb_scrapper%2F.gitignore%22%2C%22scheme%22%3A%22file%22%7D%7D) file is included to exclude unnecessary files from the repository. It includes common patterns for Python projects, such as:

- Byte-compiled files
- Distribution files
- Virtual environment directories
- IDE and tool-specific files

## Acknowledgements

- [Gradio](https://gradio.app/) for providing the user interface framework.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping.
- [Pillow](https://python-pillow.org/) for image processing.
- [Requests](https://docs.python-requests.org/en/latest/) for making HTTP requests.
