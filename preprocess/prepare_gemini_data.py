import glob
import os

import pandas as pd

from apis import gemini

if __name__ == "__main__":
    data_path = "./data/ready_to_label_data/"
    files = glob.glob(f"{data_path}/**/*", recursive=True)
    files = [f for f in files if not os.path.isdir(f)]
    files = [f for f in files if "/excel/" in f.lower()]  # or "/eml/" in f.lower()]

    for path in files:
        xls = pd.ExcelFile(path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name)
            html_bytes = df.to_html(index=False).encode("utf-8")

            text, token = gemini.call_gemini(html_bytes)

            path = path.replace("ready_to_label_data", "gemini_prediction")
            directory = os.path.dirname(path)

            os.makedirs(directory, exist_ok=True)

            with open(path, "a") as f:
                f.write(text)
        break
