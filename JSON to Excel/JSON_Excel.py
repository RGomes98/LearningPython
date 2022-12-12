import json
import pandas as pd


def convert_json_to_excel(json_file_path, excel_file_path):
    json_arr = json.load(open(json_file_path, encoding="utf-8"))
    json_arr_obj_keys = list(json_arr[0])

    new_json_table = {}

    for obj in json_arr:
        for i in range(len(obj)):

            if json_arr_obj_keys[i] not in new_json_table:
                new_json_table[json_arr_obj_keys[i]] = []

            if list(new_json_table)[i] == json_arr_obj_keys[i]:
                new_json_table[json_arr_obj_keys[i]] += [obj[json_arr_obj_keys[i]]]

    json_dataframe = pd.DataFrame(new_json_table)
    json_dataframe.to_excel(excel_file_path)
    print(f"Successfully written to Excel file located in: {excel_file_path}.")


convert_json_to_excel(
    ".\json_input\data.json",
    ".\excel_output\output.xlsx",
)
