import json
import os


# Check supplier_name, invoice_id, booking_id, booking_amount, total_amount
def validate_per_doc(target, prediction):
    if (
        "supplier_name" in target
        and target["supplier_name"] != prediction["supplier_name"]
    ):
        return False
    if "invoice_id" in target and target["invoice_id"] != prediction["invoice_id"]:
        return False
    if (
        "supplier_name" in target
        and target["total_amount"] != prediction["total_amount"]
    ):
        return False

    if "booking_id" in target:
        target_booking = {
            ele["booking_id"]: ele["booking_amount"] for ele in target["booking"]
        }
        prediction_booking = {
            ele["booking_id"]: ele["booking_amount"] for ele in prediction["booking"]
        }
        if target_booking != prediction_booking:
            return False

    return True


if __name__ == "__main__":
    target_path = "./data/preprocess_data/labels/"
    predict_path = "./results/document_ai/"

    all_files = []
    for dirpath, dirnames, filenames in os.walk(target_path):
        for filename in filenames:
            all_files.append(os.path.join(dirpath, filename))

    total = len(all_files)
    true = 0
    for file in all_files:
        file_name = os.path.basename(file)
        target_data = json.load(open(file, "r"))
        predict_data = json.load(open(os.path.join(predict_path, file_name), "r"))
        result = validate_per_doc(target_data, predict_data)
        if result is False:
            print(f"Wrong file: {file}")
            print(f"Target data: {target_data}")
            print(f"Predict data: {predict_data}")

        true += int(result)

    print(f"Result: {true}/{total}, {true / total}")
