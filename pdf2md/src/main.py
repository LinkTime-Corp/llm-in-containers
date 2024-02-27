import streamlit as st
import os

from llamaparse_pdf2md import LlamaParsePDFParser
from llmsherpa_pdf2md import LayoutPDFParser
from unstructured_pdf2md import UnstructuredPDFParser

INPUT_DIR = "pdf-inputs"

LLAMAPARSE_PARSER = "LlamaParse"
UNSTRUCTURED_PARSER = "Unstructured"
LLMSHERPA_PARSER = "LLMSherpa"

def clear_dirs():
    # make sure the directories exist and no files are in them
    # So this is a bit of a hack, but it works for now
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
    else:
        for file in os.listdir(INPUT_DIR):
            os.remove(os.path.join(INPUT_DIR, file))

def process_pdf(file, parser_type=LLAMAPARSE_PARSER):
    clear_dirs()

    # save the uploaded file to a directory with the same name
    filepath = f"{INPUT_DIR}/{file.name}"
    with open(filepath, "wb") as f:
        f.write(file.getbuffer())

    if parser_type == LLAMAPARSE_PARSER:
        parser = LlamaParsePDFParser()
    elif parser_type == UNSTRUCTURED_PARSER:
        parser = UnstructuredPDFParser()
    elif parser_type == LLMSHERPA_PARSER:
        parser = LayoutPDFParser()
    return parser.parse_pdf(filepath)

# Create a file uploader
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

parser_type = st.selectbox("PDF Parser Type", [LLMSHERPA_PARSER, UNSTRUCTURED_PARSER, LLAMAPARSE_PARSER])

# Create a button
if st.button("Convert PDF to Markdown"):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Convert the PDF file
        md_text = process_pdf(uploaded_file, parser_type)
        
        # Display the Markdown text
        st.markdown(md_text, unsafe_allow_html=True)
    else:
        st.write("Please upload a PDF file.")
