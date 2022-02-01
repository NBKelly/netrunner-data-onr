import ast
import fileinput

with open("onr_out/art_inter.txt", "r") as file:
    art_dict_str = file.read()
    dict = ast.literal_eval(art_dict_str)

    for line in fileinput.input():
        line = line.strip()
        #print("line: " + line)
        if line in dict:
            print(dict[line][1])
        else:
            print("unknown")

#print(dict)
