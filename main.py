import json


cnip = json.load(open("cnip", "r", encoding="utf-8"))["rules"][0]
cnsite = json.load(open("cnsite", "r", encoding="utf-8"))["rules"][0]

geocn = {'version': 1, 'rules': [{}]}
rules = geocn["rules"][0]
rules["ip_cidr"] = cnip["ip_cidr"]
rules["domain"] = cnsite["domain"]
rules["domain_suffix"] = cnsite["domain_suffix"]

with open("custom-rules", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    if line[0] == "#":
        continue
    else:
        line = line.split()
        if line[0] == "-":
            try:
                rules[line[1]].remove(line[2])
                print("\033[34mINFO\033[0m", "Remove", line[2], "from", line[1])  # blue
            except:
                print("\033[31mERROR\033[0m", line[2], "not in", line[1])  # red
        elif line[0] == "+":
            rules[line[1]].append(line[2])
            print("\033[34mINFO\033[0m", "Add", line[2], "to", line[1])  # blue
        rules[line[1]].sort()
json.dump(geocn, open("geocn", "w+", encoding="utf-8"), indent=2)

