import glob
import os
import random
import re
import shutil

import pandas as pd


def clean_data(data_path, dest_path):
    # Remove duplicates with the (1) in the name
    files = glob.glob(f"{data_path}/**/*", recursive=True)
    files = [f for f in files if not os.path.isdir(f)]
    print(f"Number of original files: {len(files)}")
    base_files = set()
    duplicates = []

    # Collect base filenames (without the (1) part)
    for file in files:
        # Match pattern like "name(1).pdf"
        match = re.match(r"(.+)\(\d+\)(\.\w+)$", file)
        if match:
            base_name = match.group(1) + match.group(2)
            if base_name in files:
                duplicates.append(file)
        else:
            base_files.add(file)

    print(f"Number of files to be removed: {len(duplicates)}")
    original_files = [f for f in files if f not in duplicates]

    for file in original_files:
        filename = os.path.basename(file)
        foldername = file.split("/")[-2]
        os.makedirs(os.path.join(dest_path, foldername), exist_ok=True)
        shutil.copy2(file, os.path.join(dest_path, foldername, filename))


def update_data_info(df: pd.DataFrame, data_path: str = ""):
    files = glob.glob(f"{data_path}/**/*", recursive=True)
    files = [f for f in files if not os.path.isdir(f)]

    for file in sorted(files):
        file_name = os.path.basename(file)
        folder_name = os.path.dirname(file).split("/")[-1]
        extension = file_name.split(".")[-1].lower()
        code = folder_name.split(" ")[0]
        extension_mapping = ""
        # Get file type mapping
        if extension in ["xlsx", "xls", "xlsb"]:
            extension_mapping = "excel"
        elif extension in ["pdf"]:
            extension_mapping = "pdf"
        elif extension in ["doc", "docx"]:
            extension_mapping = "word"
        elif extension in ["eml"]:
            extension_mapping = "eml"
        elif extension in ["html"]:
            extension_mapping = "html"

        exists = (
            (df["folder_name"] == folder_name) & (df["file_name"] == file_name)
        ).any()
        if not exists:
            df.loc[len(df)] = {
                "code": code,
                "folder_name": folder_name,
                "file_name": file_name,
                "idx": len(df),
                "file_type": extension.lower(),
                "file_type_mapping": extension_mapping,
                "split": -1,
                "in_use": False,
            }

    return df


def split_by_type(df: pd.DataFrame, clean_path: str = "", dest_path: str = ""):
    for idx, row in df.iterrows():
        os.makedirs(
            os.path.join(dest_path, row["file_type_mapping"], row["folder_name"]),
            exist_ok=True,
        )
        shutil.copy2(
            os.path.join(clean_path, row["folder_name"], row["file_name"]),
            os.path.join(
                dest_path,
                row["file_type_mapping"],
                row["folder_name"],
                row["file_name"],
            ),
        )


def get_data_to_label(
    df: pd.DataFrame, num_sample=50, split=0, src_path="", dest_path=""
):
    df_available = df[df["in_use"] == False]
    customers = df_available["code"].unique().tolist()
    if num_sample > len(customers):
        num_sample = len(customers)
    customers = random.sample(customers, k=num_sample)

    for customer in customers:
        df.loc[df["code"] == customer, "in_use"] = True
        df.loc[df["code"] == customer, "split"] = split
        for idx, row in df[df["code"] == customer].iterrows():
            full_src_path = os.path.join(src_path, row["folder_name"])
            full_dest_path = os.path.join(
                dest_path, str(split), row["file_type_mapping"], row["folder_name"]
            )
            os.makedirs(full_dest_path, exist_ok=True)
            shutil.copy2(
                os.path.join(full_src_path, row["file_name"]),
                os.path.join(full_dest_path, row["file_name"]),
            )

    return df


def analyze(df):
    num_customers = df["code"].unique()
    num_samples = len(df)
    num_available = len(df[df["in_use"] == False])
    file_type_value_counts = df["file_type"].value_counts()
    file_type_mapping_value_counts = df["file_type_mapping"].value_counts()

    print(f"Number of customers: {len(num_customers)}")
    print(f"Number of files: {num_samples}")
    print(f"Number of unlabeled files: {num_available}")
    print(f"File types: {str(file_type_value_counts)}")
    print(f"File types mapping: {str(file_type_mapping_value_counts)}")


if __name__ == "__main__":
    # Read path
    original_data_path = "./data/original_data/invoices/"
    ready_to_label_path = "./data/ready_to_label_data/"
    clean_data_path = "./data/clean_data/"
    split_path = "./data/split_data/"

    os.makedirs(ready_to_label_path, exist_ok=True)
    os.makedirs(clean_data_path, exist_ok=True)
    os.makedirs(split_path, exist_ok=True)
    data_info = "./data_info.csv"

    df = None
    is_save = True
    is_create_split = True
    is_clean_data = True
    is_update_data_info = True
    is_analyze = True
    is_split_by_type = True

    # Remove duplicates
    if is_clean_data:
        clean_data(original_data_path, clean_data_path)

    # Load data
    if os.path.exists(data_info):
        df = pd.read_csv(data_info, index_col=False)
    else:
        df = pd.DataFrame(
            columns=[
                "idx",
                "code",
                "folder_name",
                "file_name",
                "file_type",
                "file_type_mapping",
                "split",
                "in_use",
            ]
        )

    if is_update_data_info:
        df = update_data_info(df, clean_data_path)

    if is_analyze:
        analyze(df)

    if is_split_by_type:
        split_by_type(df, clean_data_path, split_path)

    # Create split
    if is_create_split:
        num_customers = 50

        while len(df[df["in_use"] == False]["code"].unique().tolist()) > num_customers:
            max_idx = df["split"].max()

            df = get_data_to_label(
                df,
                num_sample=num_customers,
                split=max_idx + 1,
                src_path=clean_data_path,
                dest_path=ready_to_label_path,
            )

    # Store data information
    if is_save:
        df = df.to_csv(data_info, index=False)
