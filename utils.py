import re


def get_document_ai_result(entities):
    sample = {}
    sample["booking"] = []
    for entity in entities:
        if "booking" not in entity["type"]:
            sample[entity["type"]] = entity["mentionText"]
        else:
            booking = {}
            booking["booking_record"] = []
            booking_amount = 0
            for prop in entity["properties"]:
                if "booking_record" not in prop["type"]:
                    booking[prop["type"]] = prop["mentionText"]
                else:
                    _rec = {}
                    for p in prop["properties"]:
                        _rec[p["type"]] = p["mentionText"]
                    record_money = re.sub(r"\D", "", _rec["record_money"])
                    booking_amount += float(record_money)
                    booking["booking_record"].append(_rec)
            booking["booking_amount"] = booking_amount
            sample["booking"].append(booking)

    return sample


# def traverse_json(obj) -> dict | list:
#     temp_d = {}
#     if isinstance(obj, dict):
#         for k, v in obj.items():
#             if k == "mentionText":
#                 temp_d[obj["type"]] = obj["mentionText"]
#             elif k == "properties" and obj["properties"]:
#                 res = traverse_json(v)
#                 if res:
#                     temp_d["properties"] = res
#
#     elif isinstance(obj, list):
#         temp_l = []
#         for item in obj:
#             temp_l.append(traverse_json(item))
#         return temp_l
#     return temp_d


# def get_document_ai_label(entities):
#     # Get labels
#     sample = {}
#     sample["booking"] = []
#     for entity in entities:
#         res = traverse_json(entity)
#         # Get booking info
#         if "booking" in res:
#             booking = {}
#             booking["booking_record"] = []
#             for ele in res["properties"]:
#                 # Merge booking record
#                 if "booking_record" in ele:
#                     e_dict = {}
#                     for e in ele["booking_record"]:
#                         e_dict.update(e)
#                     booking["booking_record"].append(e_dict)
#
#                 elif ele not in sample["booking"]:
#                     booking.update(ele)
#             sample["booking"].append(booking)
#         # Get other info
#         else:
#             for k, v in res.items():
#                 sample[k] = v
#     return sample
