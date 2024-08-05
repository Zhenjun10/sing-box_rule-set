class RuleManual:
    def __init__(self):
        self.DirectRules = {
            'version': 1,
            'rules': [
                {
                    'ip_cidr': [],
                    'domain': [],
                    'domain_suffix': [],
                    'domain_keyword': [],
                    'domain_regex': []
                }
            ]
        }
        self.ProxyRules = {
            'version': 1,
            'rules': [
                {
                    'ip_cidr': [],
                    'domain': [],
                    'domain_suffix': [],
                    'domain_keyword': [],
                    'domain_regex': []
                }
            ]
        }

    @property
    def direct_rules(self):
        return self.DirectRules["rules"][0]

    @property
    def proxy_rules(self):
        return self.ProxyRules["rules"][0]

    def log(self, log_type: str, string):
        if log_type == 'INFO':
            print("\033[34mINFO\033[0m", string)  # blue
        elif log_type == 'ERROR':
            print("\033[31mERROR\033[0m", string)  # red
        elif log_type == 'DONE':
            print("\033[32mDONE\033[0m", string)  # green

    def add_custom_direct_rules(self, filename: str):
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            if line[0] == "#":
                continue
            else:
                line = line.split()
                if line[0] == "-":
                    try:
                        self.direct_rules[line[1]].remove(line[2])
                        self.log("INFO", f"Remove {line[2]} from {line[1]}")
                    except:
                        self.log("ERROR", f"{line[2]} not in {line[1]}")
                elif line[0] == "+":
                    self.direct_rules[line[1]].append(line[2])
                    self.log("INFO", f"Add {line[2]} to {line[1]}")
                self.direct_rules[line[1]].sort()

    def add_custom_proxy_rules(self, filename: str):
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            if line[0] == "#":
                continue
            else:
                line = line.split()
                if line[0] == "-":
                    try:
                        self.proxy_rules[line[1]].remove(line[2])
                        self.log("INFO", f"Remove {line[2]} from {line[1]}")
                    except:
                        self.log("ERROR", f"{line[2]} not in {line[1]}")
                elif line[0] == "+":
                    self.proxy_rules[line[1]].append(line[2])
                    self.log("INFO", f"Add {line[2]} to {line[1]}")
                self.proxy_rules[line[1]].sort()

    def add_direct_rules(self, filename: str):
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip().split(":")
            length = len(line)
            if length == 1:
                self.direct_rules["domain_suffix"].append(line[0])
            elif length == 2:
                if line[0] == 'full':
                    self.direct_rules["domain"].append(line[1])
                elif line[0] == 'regexp':
                    self.direct_rules["domain_regex"].append(line[1])
        self.log('DONE', f"Add {filename} to DirectRules")

    def add_proxy_rules(self, filename: str):
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip().split(":")
            length = len(line)
            if length == 1:
                self.proxy_rules["domain_suffix"].append(line[0])
            elif length == 2:
                if line[0] == 'full':
                    self.proxy_rules["domain"].append(line[1])
                elif line[0] == 'regexp':
                    self.proxy_rules["domain_regex"].append(line[1])
        self.log('DONE', f"Add {filename} to ProxyRules")

    def gen_rule_files(self):
        import json
        json.dump(self.DirectRules, open("DirectRules", "w+", encoding="utf-8"), indent=2)
        json.dump(self.ProxyRules, open("ProxyRules", "w+", encoding="utf-8"), indent=2)

    def uniq_rule_files(self):
        for key in self.direct_rules:
            self.direct_rules[key] = list(set(self.direct_rules[key]))
            self.direct_rules[key].sort()
        for key in self.proxy_rules:
            self.proxy_rules[key] = list(set(self.proxy_rules[key]))
            self.proxy_rules[key].sort()
        self.log('DONE', "uniq and sort complete")


if __name__ == "__main__":
    rm = RuleManual()
    rm.add_direct_rules("direct-list")
    rm.add_direct_rules("china-list")
    rm.add_direct_rules("apple-cn")
    rm.add_direct_rules("google-cn")
    rm.add_proxy_rules("proxy-list")
    rm.add_proxy_rules("gfw")
    rm.add_custom_direct_rules("custom-DirectRules")
    rm.add_custom_proxy_rules("custom-ProxyRules")
    rm.uniq_rule_files()
    rm.gen_rule_files()


