import click, json, os, re, sys
from llmsherpa.readers import LayoutPDFReader
from llmsherpa.readers import Paragraph, Table, ListItem, Section, Block
from openai_utils import parse_table, extract_title
from pydantic import BaseModel
import re

UPPERCASE_LINE_PATTERN = r"^[A-Z\s]+$"
UPPERCASE_FIRST_PATTERN = r'^([A-Z][a-z]+)(\s[A-Z][a-z]+)*$'
NUM_HEADING_PATTERN = r"^(\d+(\.\d+)*)\s+(.*)"
SECTION_HEADING_PATTERN = r"^SECTION \d+:"
START_HEADING_LEVEL = 1

LLMSHERPA_API_URL = "http://nlm-ingestor:5001/api/parseDocument?renderFormat=all"

class LayoutPDFParser(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    pdf_reader : LayoutPDFReader = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pdf_reader = LayoutPDFReader(LLMSHERPA_API_URL)

    def convert_line_to_markdown(self, line: str, previous_heading_level) -> str:
        prefix = ""
        # Use regular expressions to check if the line matches heading or subheading
        if prefix == "":
            match = re.match(SECTION_HEADING_PATTERN, line)
            if match:
                # Convert to main heading if it matches "SECTION <number>:"
                prefix = "#" * (previous_heading_level + 1)

        if prefix == "":
            match = re.match(NUM_HEADING_PATTERN, line)
            if match:
                prefix = self.replacement(match, previous_heading_level)

        if prefix == "":
            match = re.match(UPPERCASE_LINE_PATTERN, line)
            if match:
                prefix = "#" * (previous_heading_level + 1)

        if prefix == "":
            match = re.match(UPPERCASE_FIRST_PATTERN, line)
            if match:
                prefix = "#" * (previous_heading_level + 1)

        if prefix != "":
            line = f"{prefix} {line}"   
            previous_heading_level += 1     
        return (line, previous_heading_level)

    def replacement(self, match, previous_heading_level: int):
        level = match.group(1).count('.') + previous_heading_level + 1  # Count the dots to determine the heading level
        return '#' * level

    def traversal_doc(self, node: Block, previous_heading_level: int) -> str: 
        md_text = ""
        node_type = ""
        if isinstance(node, Section):
            node_type = "Section"
            (node_text_with_heading, previous_heading_level) = \
                self.convert_line_to_markdown(node.to_text(), previous_heading_level)
            md_text += node_text_with_heading + "\n\n"
        elif isinstance(node, Table):
            node_type = "Table"
            table_content = parse_table(node.to_text())
            md_text += table_content + "\n\n"
        elif isinstance(node, Paragraph):
            node_type = "Paragraph"
            md_text += node.to_text() + "\n\n"
        elif isinstance(node, ListItem):
            node_type = "ListItem"
            md_text += node.to_html() + "\n\n"
        elif isinstance(node, Block):
            node_type = "Block"
        else:
            print(type(node))
            raise ValueError("Unknown node type")

        if node_type not in ['ListItem', 'Paragraph', 'Table']:
            for child in node.children:
                md_text += self.traversal_doc(child, previous_heading_level)
        return md_text

    def parse_pdf(self, pdf_filepath: str) -> str:
        try:
            doc = self.pdf_reader.read_pdf(pdf_filepath)
            md_text = self.traversal_doc(doc.root_node, START_HEADING_LEVEL)
            title = extract_title(md_text)
            return f"{title}\n\n{md_text}"
        except Exception as e:
            print(f"Error processing {pdf_filepath}: {e}")

@click.command()
@click.option(
    "-i",
    "--input_file",
    "input_file",
    required=True,
    help="The input pdf file to parse.",
)
@click.option(
    "-o",
    "--output_file",
    "output_file",
    required=True,
    help="The output markdown file.",
)
def llmsherpa_pdf2md(input_file, output_file):
    pdf_parser = LayoutPDFParser()
    md_content = pdf_parser.parse_pdf(input_file)
    with open(output_file, "w") as f:
        f.write(md_content)
if __name__ == "__main__":
    llmsherpa_pdf2md()