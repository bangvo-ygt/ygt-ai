import json
import os
import time
import warnings

import apis.document_ai as local_docai
import utils
# from google.cloud import documentai_v1 as documentai
from google.cloud import documentai_v1beta3 as documentai
from tqdm import tqdm

warnings.filterwarnings("ignore", category=UserWarning)

if __name__ == "__main__":
    folder_path = "../data/invoices/"

    project_id = "staging-servers-157416"
    location = "eu"
    processor_id = "cf1645a6dce688ee"
    processor_version = "rc"
    # file_path = "./YGT Cost/YGT Sample Invoices/BF0003944130.pdf"
    mime_type = "application/pdf"

    all_files = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            all_files.append(os.path.join(dirpath, filename))

    average_time = {}

    for dir in tqdm(all_files):
        file_name = os.path.basename(dir).split(".")[0]
        start = time.time()
        data = local_docai.process_document(
            project_id=project_id,
            location=location,
            processor_id=processor_id,
            processor_version=processor_version,
            file_path=dir,
            mime_type=mime_type,
        )
        end = time.time() - start
        data = documentai.Document.to_json(data)
        data = json.loads(data)

        sample = utils.get_document_ai_result(data["entities"])
        with open(f"./results/document_ai/{file_name}.json", "w") as f:
            json.dump(sample, f, indent=4)
        average_time[dir] = end

    with open("./benchmark_results/time.txt", "w") as f:
        total = 0
        for k, v in average_time.items():
            total += v
            f.write(f"{k}: {v} (s)")
            f.write("\n")
        f.write(f"Average time: {total / len(average_time)} (s)")
