import base64
import json
import os
from pathlib import Path

import utils
from tqdm import tqdm

parent_dir = "./data/raw_data"
output_dir = "./data/preprocess_data"
Path(output_dir).mkdir(parents=True, exist_ok=True)
Path(os.path.join(output_dir), "labels").mkdir(parents=True, exist_ok=True)
Path(os.path.join(output_dir), "images").mkdir(parents=True, exist_ok=True)

files = os.listdir(parent_dir)


# ignore: 'uri', 'docid', 'mimeType', 'textStyles', 'entityRelations', 'textChanges', 'blobAssets'
# info:
#   - 'text': text in document
#   - 'pages': raw images
#   - 'entities': labels
# revisions: [{'id': 'af4686550f414aaa', 'createTime': '2025-06-26T07:35:49.219296261Z', 'agent': 'console_ui@google.com', 'parentIds': ['709c2ae87c47ea22'], 'parent': []}]


for file in tqdm(files):
    with open(os.path.join(parent_dir, file), "r") as f:
        raw = json.load(f)
        data = json.loads(raw)
        file_name = file.split(".")[0]

        # Get label
        sample = utils.get_document_ai_result(data["entities"])
        with open(
            os.path.join(output_dir, f"labels/{file_name}.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(sample, f, indent=4)

        # Save images
        for page in data["pages"]:
            page_number = page["pageNumber"]
            extension = page["image"]["mimeType"].split("/")[1]
            image = base64.b64decode(page["image"]["content"])
            with open(
                os.path.join(
                    output_dir, f"images/{file_name}_{page_number}.{extension}"
                ),
                "wb",
            ) as f:
                f.write(image)
