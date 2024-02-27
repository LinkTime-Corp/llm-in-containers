import os
from openai import OpenAI

TABLE_PROMPT = """
Given the following piece of text obtained from a PDF file, which represents a table, 
please return a table in markdown format without changing its content.
If it is not a table, then return the text as is. Don't return anything else.

If the first line of this text starts with something like this: "| 1.1.1 introduction name | ...", 
please extract "1.1.1 introduction" as a heading in the markdown format and put
it at the beginning of the table. The "name" should be treated as part of the table header.
So "| 1.1.1 introduction name | ..." will be converted to:
### 1.1.1 introduction
| name | ...

If the first line starts like "| introduction name | ..." then there is no heading to extract.
So "| introduction name | ..." will be converted to:
|introduction name | ...

The extracted text from PDF you need to process is:
{table_text}
"""

TITLE_PROMPT = """
Given the following first few lines of text obtained from a PDF file. 
Please extract the title and return it in markdown format, 
remembering to add only one # in front of the title text:
# Some Title

Some Examples:
----------------
1. If the first few lines of the text are:
```
Prodcut Name
Version 1.0
Manual
```
Then the title to be extracted is "Product Name Version 1.0 Manual".
----------------
2. If the first few lines of the text are:
```
# Some unrelated text

We are presenting a new product called VWP 1.0, its ...
```
Then the title to be extracted is "Introducing VWP 1.0", which means you need to look into
the paragraph for the purpose of this article.
----------------
3. If the first few lines of the text are:
```
We, Company ABC, provide product CDF, as a major product in our line of products...
```
Then the title to be extracted is "Introducing CDF from ABC", which means you need to look into
the paragraph for the purpose of this article.
----------------


The extracted text you need to process is:
{text}
"""

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo-0125")
EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_title(text: str) -> str:
    # get the first 5 lines of the text
    lines = text.split("\n")[:5]
    title_prompt = TITLE_PROMPT.format(text="\n".join(lines))
    if OPENAI_API_KEY is None or OPENAI_API_KEY == "":
        return lines[0]
    else:
        return query_openai(title_prompt)

def parse_table(table_text: str) -> str:
    chat_prompt = TABLE_PROMPT.format(table_text=table_text)
    if OPENAI_API_KEY is None or OPENAI_API_KEY == "":
        return table_text
    else:
        return query_openai(chat_prompt)

def query_openai(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
                {
                "role": "user",
                "content": prompt,
            }
        ], model=OPENAI_MODEL)
    return chat_completion.choices[0].message.content

def embed(text: str) -> list[float]:
    response =  client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL)
    return response.data[0].embedding
