import os
from json_to_sql.j2s import J2S

path_input = "./input/"
path_output = "./output/"

count = 1
total = len(os.listdir(path_input))
for file in os.listdir(path_input):
    if file.endswith(".json"):
        file_name = os.path.basename(file)
        json_data = open(path_input + file, "r")

        print("JSON to SQL process for : {file_name} ({count}/{total})".format(file_name=file_name, count=count, total=total))

        j2s = J2S(os.path.splitext(file_name)[0], json_data)
        j2s.process()
        query = j2s.get_query()

        print("Writing to file...")
        sql_output = open(path_output + file_name.replace("json", "sql"), "w", encoding="utf-8")
        sql_output.write(query)

        print("Next file\n")
        count += 1

print("Done !")
