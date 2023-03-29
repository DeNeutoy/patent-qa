import json
import xmltodict
import typer
from pathlib import Path

app = typer.Typer(no_args_is_help=True)


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

            parsed = {
                "title": title,
                "metadata": metadata,
                "abstract": abstract,
                "description": description

            }
            # Write the dictionary as a JSON object to the output file
            json_file.write(json.dumps(parsed) + '\n')

if __name__ == "__main__":

    app()
