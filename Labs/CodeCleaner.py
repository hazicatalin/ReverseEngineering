import re


def remove_comments(codeLine):
    if "//" in codeLine:
        codeLine = codeLine[:codeLine.find("//")]
    if "/*" in codeLine:
        codeLine = codeLine[:codeLine.find("/*")] + codeLine[codeLine.find("*/") + 2:]
    return codeLine


def add_endline(codeLine):
    stringReplacer = 0
    openedBraces = 0
    length = len(codeLine)
    for element in range(0, length):
        if codeLine[element] == "{":
            if codeLine[element - 1] != "$":
                openedBraces += 1
                codeLine = codeLine[:element + 1] + "\n" + "    " * openedBraces + codeLine[element + 1:]
                length += 4 * openedBraces + 1
            else:
                stringReplacer = 1
        if codeLine[element] == "}":
            if stringReplacer == 1:
                stringReplacer = 0
            else:
                openedBraces -= 1
                codeLine = codeLine[:element] + "}\n" + codeLine[element + 1:]
                length += 2
    return codeLine


def add_spaces(codeLine):
    length = len(codeLine)
    for element in range(0, length):
        if codeLine[element] == ";" and element + 1 < length and codeLine[element + 1] != " ":
            codeLine = codeLine[:element + 1] + " " + codeLine[element + 1:]
            length += 1
    return codeLine


def concatenate(codeLine, previous):
    variableNames = re.search("[a-zA-Z0-9]+\+[a-zA-Z0-9]+", re.sub("\s*", "", codeLine))
    while variableNames:
        variableNames = variableNames.group(0).split("+")
        variableValue = re.search(variableNames[0] + "\s*=\s*\".+\"", previous).group(0).split("\"")[1]
        codeLine = re.sub(variableNames[0], "\"" + variableValue + "\"", codeLine)
        variableValue = re.search(variableNames[1] + "\s*=\s*\".+\"", previous).group(0).split("\"")[1]
        codeLine = re.sub(variableNames[1], "\"" + variableValue + "\"", codeLine)
        variableNames = re.search("[a-zA-Z0-9]+\+[a-zA-Z0-9]+", re.sub("\s*", "", codeLine))
    variableName = re.search("[a-zA-Z0-9]+\+\"", re.sub("\s*", "", codeLine))
    if variableName:
        variableName = variableName.group(0)[:-2]
        variableValue = re.search(variableName + "\s*=\s*\".+\"", previous).group(0).split("\"")[1]
        codeLine = re.sub(variableName, "\"" + variableValue + "\"", codeLine)
    variableName2 = re.search("\"\+[a-zA-Z0-9]+", re.sub("\s*", "", codeLine))
    if variableName2:
        variableName2 = variableName2.group(0)[2:]
        variableValue = re.search(variableName2 + "\s*=\s*\".+\"", previous).group(0).split("\"")[1]
        codeLine = re.sub(variableName2, "\"" + variableValue + "\"", codeLine)
    codeLine = re.sub("\"\s*\+\s*\"", "", codeLine)
    return codeLine


def main():
    # change path for cleaning other file
    f = open("D:/Facultate/Reverse Engineering/lab2_1.js", "r")
    line = f.readline()
    fileText = ""
    while line:
        # line = remove_comments(line)
        # line = add_endline(line)
        # line = add_spaces(line)
        line = concatenate(line, fileText)
        fileText += line
        line = f.readline()
    print(fileText)


if __name__ == "__main__":
    main()
