import json
import xmltodict
import typer
from pathlib import Path

app = typer.Typer(no_args_is_help=True)


def extract_text(json_data):
    text_list = []
    if isinstance(json_data, dict):

        text = json_data.get("#text", None)
        if text is not None:
            text_list.append(text)
        claim_text = json_data.get("claim-text")
        if claim_text is not None:
            text_list.extend(extract_text(claim_text))
    elif isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, str):
                text_list.append(item)
            else:
                text_list.extend(extract_text(item))
    return text_list



@app.command()
def main(input_path: Path, output_path: Path):
    # Open the input file with concatenated XML data
    with open(input_path, 'r') as xml_file:
        xml_data = xml_file.read()

    # Split the concatenated XML data into individual XML documents
    xml_docs = xml_data.split('<?xml version="1.0" encoding="UTF-8"?>\n')

    # Convert each XML document to a JSON object and write to output file
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as json_file:
        for i, xml_doc in enumerate(xml_docs):
            # Ignore empty documents
            if xml_doc.strip() == '':
                continue

            # Convert the XML document to a dictionary
            doc_dict = xmltodict.parse(xml_doc)

            metadata = doc_dict['us-patent-grant']['us-bibliographic-data-grant']
            title = metadata['invention-title']['#text']
            abstract = doc_dict['us-patent-grant']['abstract']['p']['#text']

            description = []
            for p in doc_dict['us-patent-grant']['description']['p']:
                # Sometimes there are tables, for now just grab if it is text only.
                if p.get("#text") is not None:
                    description.append(p.get("#text"))

            claims = []
            for p in doc_dict['us-patent-grant']['claims']['claim']:
                claim_parts = extract_text(p)

                claims.append(" ".join(claim_parts))
            
            print(claims)

            parsed = {
                "title": title,
                "metadata": metadata,
                "abstract": abstract,
                "description": description,
                "claims": claims

            }
            # Write the dictionary as a JSON object to the output file
            json_file.write(json.dumps(parsed) + '\n')

if __name__ == "__main__":

    app()
