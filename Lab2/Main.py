import string

listOfUpperCase = []
listOfLowerCase = []
listOfDigits = []

for letter in string.ascii_uppercase:
    listOfUpperCase.append(letter)

for letter in string.ascii_lowercase:
    listOfLowerCase.append(letter)

for i in range(0, 10):
    listOfDigits.append(i)


def createDictFromList(theList):
    dict = {}
    for i in range(0, len(theList)):
        if theList[i] in listOfLowerCase or theList[i] in listOfUpperCase or theList[i] in listOfDigits:
            dict[theList[i]] = i + 1
    return dict


def printMenu1():
    str = "Press 1 for regular grammar\n"
    str += "Press 2 for finite automata\n"
    str += "Press 0 to quit\n"
    print(str)


def printMenu2():
    str = "Press 1 to read from keyboard\n"
    str += "Press 2 to read from file\n"
    str += "Press -1 to go back\n"
    str += "Press 0 to quit\n"
    print(str)


def regularGrammarOptionsMenu():
    str = "Press 1 for the set of non-terminals\n"
    str += "Press 2 for the set of terminals\n"
    str += "Press 3 for the set of productions\n"
    str += "Press 4 for the productions of a given non-terminals\n"
    str += "Press 5 to turn into finite automata\n"
    str += "Press 6 to verify if is regular grammar\n"
    str += "Press -1 to go back\n"
    str += "Press 0 to quit\n"
    print(str)


def finiteAutomataOptionsMenu():
    str = "Press 1 for the set of states\n"
    str += "Press 2 for the alphabet\n"
    str += "Press 3 for all the transitions\n"
    str += "Press 4 for the set of final states\n"
    str += "Press 5 to turn into regular grammar\n"
    str += "Press -1 to go back\n"
    str += "Press 0 to quit\n"
    print(str)


def readRegularGrammarfromKeyboard():
    regularGrammar = []
    userInput = ""
    print("Input the regular grammar rules. Write 'done' when you're done.")
    while userInput != "done":
        userInput = input()
        regularGrammar.append(userInput.strip())
    regularGrammar = regularGrammar[:len(regularGrammar) - 1]
    return regularGrammar


def readRegularGrammarFromFile(filename):
    regularGrammar = []
    with open(filename) as f:
        for line in f:
            regularGrammar.append(line.strip())
    return regularGrammar


def readFiniteAutomataFromKeyboard():
    finiteAutomata = []
    q = input("Input the initial state: ")
    F = input("Input the final state(s): ")
    F = F.split(", ")
    userInput = ""
    print("Input the transition table. Write 'done' when you're done.")
    while userInput != "done":
        userInput = input()
        finiteAutomata.append(userInput.strip().split("|"))
    finiteAutomata = finiteAutomata[:len(finiteAutomata) - 1]
    return q, F, finiteAutomata


def readFiniteAutomataFromFile(filename):
    finiteAutomata = []
    q = ""
    F = []
    with open(filename) as f:
        q = f.readline().strip().strip("q = ")
        F = f.readline().strip().strip("F = {").strip("}").split(", ")
        for line in f:
            finiteAutomata.append(line.strip().split("|"))
    return q, F, finiteAutomata


def getNonTerminals(str):
    nonTerminals = []
    for st in str:
        for s in st:
            if s in listOfUpperCase:
                nonTerminals.append(s)
    return list(set(nonTerminals))


def getTerminals(str):
    terminals = []
    for st in str:
        st = st.replace("|epsilon", "")
        print(st)
        for s in st:
            if s in listOfLowerCase or s in listOfDigits:
                terminals.append(s)
    return list(set(terminals))


def getProductions(str):
    return str


def getProductionsOfNonTerminal(str, nonTerminal):
    prodsOfNonTerm = []
    for prod in str:
        if prod.find(nonTerminal) != -1:
            prodsOfNonTerm.append(prod)
    return prodsOfNonTerm


def getSetOfStates(str):
    states = []
    for st in str:
        states.append(st[0])
    return states[1:]


def getAlphabet(str):
    alphabet = []
    for s in str[0]:
        alphabet.append(s.strip(" "))
    return alphabet[1:]


def getTransitions(str):
    transitions = "  "
    for st in str:
        for i in range(0, len(st)):
            transitions += st[i]
            if i != len(st) - 1:
                transitions += "|"
        transitions += "\n"
    return transitions


def getSetOfFinalStates(str):
    return str


def fromRegularGrammarToFiniteAutomata(str):
    finiteAutomata = []
    terminals = [" "] + getTerminals(str)  # lowerCase
    terminals_Dict = createDictFromList(getTerminals(str))
    nonTerminals = getNonTerminals(str)  # upperCase
    nonTerminals_Dict = createDictFromList(nonTerminals)
    finiteAutomata.append(terminals)
    for nonTerminal in nonTerminals:
        finiteAutomata.append([nonTerminal] + ([""] * (len(terminals) - 1)))
    productions = getProductions(str)
    for production in productions:
        for i in range(3, len(production) - 1):
            if production[i] in terminals:
                if production[i + 1] in nonTerminals:
                    finiteAutomata[nonTerminals_Dict[production[0]]
                                   ][terminals_Dict[production[i]]] += production[i + 1]
                elif production[i + 1] == '|':
                    finiteAutomata[nonTerminals_Dict[production[0]]
                                   ][terminals_Dict[production[i]]] = 'epsilon'
        if production[len(production) - 1] in terminals:
            finiteAutomata[nonTerminals_Dict[production[0]]
                           ][terminals_Dict[production[i + 1]]] = 'epsilon'
    finiteAutomata = getTransitions(finiteAutomata)
    return finiteAutomata


# def frmRegToFinite(regularGrammar):
#     finiteAutomata = []
#     terminals = getTerminals(regularGrammar)
#     terminals_Dict = createDictFromList(terminals)
#     nonTerminals = getNonTerminals(regularGrammar)
#     return terminals_Dict


def fromFiniteAutomataToRegularGrammar(finiteAutomata, setOfFinalStates):
    regularGrammar = []
    alphabet = getAlphabet(finiteAutomata)
    setOfStates = getSetOfStates(finiteAutomata)
    for i in range(0, len(setOfStates)):
        production = setOfStates[i] + "->"
        for j in range(0, len(alphabet)):
            listOfState = finiteAutomata[i+1][j+1].split(",")
            for state in listOfState:
                production += alphabet[j] + state + "|"
        if production[len(production)-1] == '|':
            production = production[:-1]
        regularGrammar.append(production)
    for i in range(0, len(regularGrammar)):
        if regularGrammar[i].split("->")[0] in setOfFinalStates:
            regularGrammar[i] += "|epsilon"
    return regularGrammar


def checkIfRegularGrammar(regularGrammar):
    ok = False
    okEpsilon = False
    okInitial = True
    setOfProductions = getProductions(regularGrammar)
    for production in setOfProductions:
        if "epsilon" in production:
            okEpsilon = True
        if production.split("->")[0] != "S":
            if "S" in production:
                okInitial = False
    if okEpsilon and okInitial:
        ok = True
    return "Is regular grammar" if ok else "Is not regular grammar"


def runRegularGrammarLogistics(regularGrammar):
    while(True):
        regularGrammarOptionsMenu()
        y = input("Your choice: ")
        if y == "1":
            print(getNonTerminals(regularGrammar))
        elif y == "2":
            print(getTerminals(regularGrammar))
        elif y == "3":
            print(getProductions(regularGrammar))
        elif y == "4":
            z = input("Enter the non-terminal whose productions you'd like: ")
            if z not in listOfUpperCase:
                print("What you've entered isn't a non-terminal.")
            else:
                print(getProductionsOfNonTerminal(regularGrammar, z))
        elif y == "5":
            print(frmRegToFinite(regularGrammar))
        elif y == "6":
            print(checkIfRegularGrammar(regularGrammar))
        elif y == "-1":
            break
        elif y == "0":
            exit()
        else:
            print("Invalid choice")


def runRegularGrammar():
    while(True):
        regularGrammar = []
        printMenu2()
        x = input("Your choice: ")
        if x == "1":
            regularGrammar = readRegularGrammarfromKeyboard()
        elif x == "2":
            regularGrammar = readRegularGrammarFromFile("rg.txt")
        elif x == "-1":
            break
        elif x == "0":
            exit()
        else:
            print("Invalid choice")
        runRegularGrammarLogistics(regularGrammar)


def runFiniteAutomataLogistics(q, F, finiteAutomata):
    while(True):
        finiteAutomataOptionsMenu()
        y = input("Your choice: ")
        if y == "1":
            print(getSetOfStates(finiteAutomata))
        if y == "2":
            print(getAlphabet(finiteAutomata))
        if y == "3":
            print(getTransitions(finiteAutomata))
        if y == "4":
            print(getSetOfFinalStates(F))
        if y == "5":
            print(fromFiniteAutomataToRegularGrammar(finiteAutomata, F))
        elif y == "-1":
            break
        elif y == "0":
            exit()
        else:
            print("Invalid choice")


def runFiniteAutomata():
    while(True):
        q, F, finiteAutomata = [], [], []
        printMenu2()
        x = input("Your choice: ")
        if x == "1":
            q, F, finiteAutomata = readFiniteAutomataFromKeyboard()
        elif x == "2":
            q, F, finiteAutomata = readFiniteAutomataFromFile("fa.txt")
        elif x == "-1":
            break
        elif x == "0":
            exit()
        else:
            print("Invalid choice")
        runFiniteAutomataLogistics(q, F, finiteAutomata)


def runProgram():
    printMenu1()
    x = input("Your choice: ")
    if x == "0":
        exit()
    elif x == "1":
        runRegularGrammar()
    elif x == "2":
        runFiniteAutomata()


while(True):
    runProgram()
