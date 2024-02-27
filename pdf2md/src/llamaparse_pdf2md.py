import click, os, sys
import nest_asyncio
nest_asyncio.apply()

from llama_parse import LlamaParse
from pydantic import BaseModel

class LlamaParsePDFParser(BaseModel):
    client: LlamaParse = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.client = LlamaParse(
            api_key=os.getenv("LLAMAPARSE_API_KEY", "your_llamaparse_api_key"),
            result_type="markdown", 
            num_workers=4,
            verbose=True)

    def parse_pdf(self, input_file: str):
        print(f"Processing {input_file}...")
        try:
            documents = self.client.load_data(input_file)
            if len(documents) > 0:
                return documents[0].text
            else:
                return ""
        except Exception as e:
            print(f"Error processing {input_file}: {e}")

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
def llamaparse_pdf2md(input_file: str, output_file: str) -> None:
    pdf_parser = LlamaParsePDFParser()
    md_text = pdf_parser.parse_pdf(input_file)
    with open(output_file, "w") as f:
        f.write(md_text)        

if __name__ == "__main__":
    llamaparse_pdf2md()()
