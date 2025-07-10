from dotenv import load_dotenv

load_dotenv()
# ruff: noqa: E402

import json
import warnings
from pathlib import Path

from apis import document_ai
from google.cloud import documentai_v1beta3 as documentai
from tqdm import tqdm

warnings.filterwarnings("ignore", category=UserWarning)

if __name__ == "__main__":
    project_id = "staging-servers-157416"
    location = "eu"
    processor_id = "cf1645a6dce688ee"
    processor_version = "rc"
    mime_type = "application/pdf"
    directory_path = Path("./data/raw_data/")
    directory_path.mkdir(parents=True, exist_ok=True)

    res = document_ai.list_documents(
        project_id=project_id, location=location, processor=processor_id, page_size=100
    )

    # Get all docs per page
    docs = res.document_metadata
    while len(docs) != res.total_size:
        page_token = res.next_page_token
        res = document_ai.list_documents(
            project_id,
            location,
            processor_id,
            page_token=page_token,
        )
        docs.extend(res.document_metadata)
    print(f"Number of docs: {len(docs)}")

    # Download docs
    for doc in tqdm(docs):
        doc_id = doc.document_id
        split_type = doc.dataset_type
        if split_type == 3:
            split = "unassigned"
        elif split_type == 2:
            split = "test"
        elif split_type == 1:
            split = "train"
        else:
            split = "unknown"
        file_name = doc.display_name

        res = document_ai.get_document(
            project_id=project_id,
            location=location,
            processor=processor_id,
            doc_id=doc_id,
        )
        json_data = documentai.Document.to_json(res.document)

        # Save to file
        with open(f"./data/raw_data/{file_name}.json", "w") as f:
            json.dump(json_data, f, indent=4)

    # get_document(project_id=project_id, location=location, processor=processor_id, doc_id=)
