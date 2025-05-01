# Dennis Tislin, Period 5, 2026
import sys; args = sys.argv[1:]

nodes = {"g": 0.9, "o1": 0.5, "~o1": 0.05, "o2": 0.75, "~o2": 0.25} # dictionary of given probabilities

def formula(to_find, problem):
    if problem == "e":
        return (nodes["o2"] * nodes["o1"] * nodes["g"] + nodes["~o2"] * nodes["~o1"] * (1 - nodes["g"])) / (nodes["~o1"] * (1 - nodes["g"]) + nodes["o1"] * nodes["g"])
    
    stl = to_find.split("|")
    find = stl[0].replace("(", "")
    stp = stl[len(stl) - 1].replace(")", "")
    stp_list = stp.split(",")
    stp_list[0].replace(" ", "")
    stp_list[1].replace(" ", "")
    finding = find.split(" ")[0]
    fgiven = stp_list[0].split(" ")[1] if " " in stp_list[0] else stp_list[0]
    sgiven = stp_list[1].split(" ")[1] if " " in stp_list[1] else stp_list[1]
    
    # print(finding)
    # print(fgiven)
    # print(sgiven)
    
    if problem == "a":
        return ((1 - nodes[sgiven]) * nodes[fgiven] * nodes[finding]) / ((1 - nodes[sgiven]) * nodes[fgiven])

    elif problem == "b":
        return (nodes[fgiven] * nodes[sgiven] * nodes[finding]) / (nodes[fgiven] * nodes[sgiven] * nodes[finding] + nodes["~o1"] * nodes["~o2"] * (1 - nodes[finding]))

    elif problem == "c":
        return ((1 - nodes["o1"]) * nodes[sgiven] * nodes[finding]) / ((1 - nodes["o1"]) * nodes[sgiven] * nodes[finding] + (1 - nodes["~o1"]) * nodes["~o2"] * (1 - nodes[finding]))

    elif problem == "d":
        return ((1 - nodes["o1"]) * (1 - nodes["o2"]) * nodes[finding]) / ((1 - nodes["o1"]) * (1 - nodes["o2"]) * nodes[finding] + (1 - nodes["~o1"]) * (1 - nodes["~o2"]) * (1 - nodes[finding]))

def main():
    to_find = input("please give the probability expression you want to find (ex; (x | y, z) or (x | y)):\n")
    print()
    
    if "P" in to_find or "p" in to_find:
        if "P" in to_find:
            find = to_find.replace("P", "")
        else:
            find = to_find.replace("p", "")
    else: 
        find = to_find
        
    problem = input("please give the lowercase letter of the problem (ex; a):\n")
    # given = args[1]
    print()
    print("Probability of problem " + problem + " " + to_find + ":")
    print(formula(find, problem))

if __name__ == "__main__":
    main()

# Dennis Tislin, Period 5, 2026
