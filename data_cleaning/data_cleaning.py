import os
import json

directory = './data'


# Splits a long string into chunks of around 25k characters
def split_contents(s: str):
    split_content = s.split("\n\n")
    curr_str = ""
    result = []
    for substr in split_content:
        curr_str += "\n\n" + substr
        if len(curr_str) > 25_000:
            result.append(curr_str)
            curr_str = ""
    if curr_str != "":
        result.append(curr_str)
    return result


file_contents = []
for file_name in os.listdir(directory):
    if file_name.endswith('.txt'):
        with open(os.path.join(directory, file_name), mode='r', encoding='utf-8-sig') as f:
            content = f.read()
            if len(content) < 32768:
                file_contents.append({"file_name": file_name, "contents": content})
            else:
                for idx, piece in enumerate(split_contents(content)):
                    file_contents.append({"file_name": f"(Part {idx + 1}) {file_name}", "contents": piece})

for i in file_contents:
    print(f"{i['file_name']}, length: {len(i['contents'])}")

result_file = open("data.json", "w")
result_file.write(json.dumps(file_contents))
