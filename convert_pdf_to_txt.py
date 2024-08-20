import os
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import glob

import nest_asyncio

# Apply nest_asyncio to handle the event loop issue
nest_asyncio.apply()

# Set up your environment variables
os.environ["LLAMA_CLOUD_API_KEY"] = ""

parser = LlamaParse(
    api_key=os.getenv("LLAMA_CLOUD_API_KEY"),  # Fetch from environment variable
    result_type="markdown"  # "markdown" and "text" are available
)

# Define the file extractor
file_extractor = {".pdf": parser}

# Initialize the SimpleDirectoryReader with the directory containing your PDF files
directory = "pdf_files/pdf_documents"  # Directory containing the PDF files
reader = SimpleDirectoryReader(directory, file_extractor=file_extractor)

# Load data from the directory
documents = reader.load_data()

# Ensure the output directory exists
output_directory = "pdf_files/convertedmd_doc"
os.makedirs(output_directory, exist_ok=True)

# Save the parsed content as markdown files
for i, doc in enumerate(documents):
    output_path = os.path.join(output_directory, f"parsed_document_{i + 1}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(doc.text)  # Assuming `doc.text` contains the parsed markdown content

print("Parsing and saving completed.")

import os
import glob

# Define the output directory containing your markdown files
output_directory = "pdf_files/convertedmd_doc"

# Get all markdown files in the directory
markdown_files = glob.glob(os.path.join(output_directory, "*.md"))

# Define the paths for the combined markdown file and the resulting text file
combined_markdown_path = "pdf_files/markdown/combined_document.md"
combined_text_path = "ragtest/input/combined_document.txt"

# Open the combined markdown file for writing
with open(combined_markdown_path, "w", encoding="utf-8") as combined_file:
    # Iterate over each markdown file and append its content to the combined file
    for markdown_file in markdown_files:
        with open(markdown_file, "r", encoding="utf-8") as f:
            combined_file.write(f.read())
            combined_file.write("\n\n")  # Add a newline between files for separation

# Read the combined markdown file and write its content to a text file
with open(combined_markdown_path, "r", encoding="utf-8") as combined_file:
    content = combined_file.read()

with open(combined_text_path, "w", encoding="utf-8") as text_file:
    text_file.write(content)

print(f"All markdown files have been combined into {combined_markdown_path}.")
print(f"The combined markdown file has been converted to {combined_text_path}.")

