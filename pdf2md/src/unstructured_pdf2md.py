import click, re
from openai_utils import parse_table, extract_title
from pydantic import BaseModel
from unstructured.partition.pdf import partition_pdf

NUM_HEADING_PATTERN = r"^(\d+(\.\d+)*)\s+(.*)"
IGNORE_LIST = ["Page ", "Copyright "]
ALLOWED_TYPES = ["Title", "NarrativeText", "Table"]

class UnstructuredPDFParser(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def replacement(self, match):
        level = match.group(1).count('.') + 1  # Count the dots to determine the heading level
        return '#' * level
     
    def parse_pdf(self, pdf_filepath):
        try:
            rtn_text = ""
            print(f"Processing {pdf_filepath}")
            elements = partition_pdf(filename=pdf_filepath, strategy="hi_res")
            print(f"Number of elements: {len(elements)}")
            for el in elements:
                el_dict = el.to_dict()
                el_type = el_dict["type"]
                el_text = el_dict["text"]
                if el_type not in ALLOWED_TYPES:
                    continue

                if el_type == "Table":
                    rtn_text += parse_table(el_text)+ "\n\n"
                    continue
                if any(el_text.startswith(ignore) for ignore in IGNORE_LIST):
                    continue
                else:
                    match = re.match(NUM_HEADING_PATTERN, el_text)
                    if match:
                        markdown_prefix = self.replacement(match)
                        rtn_text += f"\n\n{markdown_prefix} {el_text}\n\n"
                    else:
                        rtn_text += el_text + "\n\n"
            if rtn_text != "":
                title = extract_title(rtn_text)
                return f"{title}\n\n{rtn_text}"
            else:
                return "Empty text returned."
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
def unstructured_pdf2md(input_file: str, output_file: str) -> None:
    pdf_parser = UnstructuredPDFParser()
    rtn_text = pdf_parser.parse_pdf(input_file)
    with open(output_file, "w") as f:
        f.write(rtn_text)

if __name__ == "__main__":
    unstructured_pdf2md()