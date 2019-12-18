import json
import copy


def areEqual(arr1, arr2, n, m):
    if (n != m):
        return False
    arr1.sort()
    arr2.sort()
    for i in range(0, n - 1):
        if (arr1[i] != arr2[i]):
            return False
    return True


def checkIfDictsAreEqual(dict1, dict2):
    for key in dict1:
        arr1 = dict1[key]
        arr2 = dict2[key]
        if not areEqual(arr1, arr2, len(arr1), len(arr2)):
            return False
    return True


def readRegularGrammarFromFile(filename):
    regularGrammar = []
    with open(filename) as f:
        for line in f:
            regularGrammar.append(line.strip())
    return regularGrammar


def getNonTerminals(rg):
    return list(set(rg[0].split(",")))


def getTerminals(rg):
    return list(set(rg[1].split(",")))


def getProductions(rg):
    newOne = rg[3:]
    newOne.pop()
    return newOne


def getStartingSymbol(rg):
    return rg[2]


def getSeq(rg):
    return rg[-1].split(" ")


def divideProduction(prod):
    left = prod.split("->")[0]
    right = prod.split("->")[1].split(" ")
    return left, right


def createDictionaryFromNonTerminals(nonTerminals):
    table = {}
    for i in nonTerminals:
        table[i] = []
    return table


def getTerminalsFromRight(right, terminals):
    for i in right:
        if i in terminals:
            return i


def getTerminalsFromFirstNonTerminals(right, nonTerminals, firstFirst):
    for i in right:
        if i in nonTerminals:
            if firstFirst[i] == [None]:
                return []
            else:
                return firstFirst[i]
    return []


def getNextFirst(rg, firstFirst):
    productions = getProductions(rg)
    nonTerminals = getNonTerminals(rg)
    nextFirst = copy.deepcopy(firstFirst)
    for prod in productions:
        left, right = divideProduction(prod)
        if "eps" in nextFirst[left]:
            pass
        else:
            nextFirst[left] += getTerminalsFromFirstNonTerminals(
                right, nonTerminals, firstFirst)
        nextFirst[left] = list(set(nextFirst[left]))
    return nextFirst


def constructFirst(rg):
    terminals = getTerminals(rg)
    nonTerminals = getNonTerminals(rg)
    productions = getProductions(rg)
    firstFirst = createDictionaryFromNonTerminals(nonTerminals)
    nextFirst = createDictionaryFromNonTerminals(nonTerminals)
    for prod in productions:
        left, right = divideProduction(prod)
        terminalsFromRight = getTerminalsFromRight(right, terminals)
        if terminalsFromRight == None:
            pass
        else:
            nextFirst[left].append(terminalsFromRight)
    while not checkIfDictsAreEqual(firstFirst, nextFirst):
        firstFirst = copy.deepcopy(nextFirst)
        nextFirst = getNextFirst(rg, firstFirst)
    return nextFirst


def getProductionsContainingNonTerminal(rg, nonTerminal):
    listToReturn = []
    nonTerminals = getNonTerminals(rg)
    productions = getProductions(rg)
    for i in productions:
        left, right = divideProduction(i)
        if left == nonTerminal:
            listToReturn.append(i)
        elif nonTerminal in right:
            listToReturn.append(i)
    return listToReturn


def rule1(prod, nonTerminal):
    if nonTerminal == "S":
        return True
    return False


def rule2(prod, nonTerminal):
    left, right = divideProduction(prod)
    if right[len(right) - 1] == nonTerminal:
        return True
    return False


def rule3(prod, nonTerminal):
    left, right = divideProduction(prod)
    for i in range(1, len(right) - 1):
        if right[i] == nonTerminal:
            return True
    return False


def applyRule3(prod, follow, first, nonTerminal, listOfTerminals):
    left, right = divideProduction(prod)
    listToWorkOn = []
    listToReturn = []
    for i in range(1, len(right) - 1):
        if right[i] == nonTerminal:
            listToWorkOn = right[i+1:]
    for i in listToWorkOn:
        if i in listOfTerminals:
            listToReturn.append(i)
        else:
            if "eps" in first[i]:
                listToReturn += first[i]
                listToReturn.remove("eps")
                listToReturn += follow[left]
            else:
                listToReturn += first[i]
    return listToReturn


def applyRulesOnProds(prods, follow, first, nonTerminal, listOfTerminals):
    listOfResults = []
    for i in prods:
        left, right = divideProduction(i)
        if rule1(i, nonTerminal):
            listOfResults += ["eps"]
        if rule2(i, nonTerminal):
            listOfResults += follow[left]
        elif rule3(i, nonTerminal):
            listOfResults += applyRule3(i, follow,
                                        first, nonTerminal, listOfTerminals)
    return listOfResults


def constructFollowRule(rg, first, followBefore):
    terminals = getTerminals(rg)
    nonTerminals = getNonTerminals(rg)
    productions = getProductions(rg)
    follow = createDictionaryFromNonTerminals(nonTerminals)
    for i in nonTerminals:
        prodFoundIn = getProductionsContainingNonTerminal(rg, i)
        follow[i] += applyRulesOnProds(prodFoundIn, followBefore, first,
                                       i, terminals)
        follow[i] = list(set(follow[i]))
    return follow


def constructFollow(rg, first):
    terminals = getTerminals(rg)
    nonTerminals = getNonTerminals(rg)
    productions = getProductions(rg)
    firstFollow = createDictionaryFromNonTerminals(nonTerminals)
    nextFollow = createDictionaryFromNonTerminals(nonTerminals)
    nextFollow = constructFollowRule(rg, first, firstFollow)
    while not checkIfDictsAreEqual(firstFollow, nextFollow):
        firstFollow = copy.deepcopy(nextFollow)
        nextFollow = constructFollowRule(rg, first, firstFollow)
    return nextFollow


def findProduction(nonTerminal, terminal, rg):
    foundProduction = ""
    prodNumber = 0
    productions = getProductions(rg)
    for i in range(len(productions)):
        left, right = divideProduction(productions[i])
        if left == nonTerminal:
            if foundProduction == "":
                foundProduction = right
                prodNumber = i
            if terminal in right:
                foundProduction = right
                prodNumber = i
    return (foundProduction, prodNumber + 1)


def constructTableV2(rg, first, follow):
    table = {}
    terminals = getTerminals(rg)
    terminals.remove("eps")
    nonTerminals = getNonTerminals(rg)
    terminals += "$"
    combined = terminals + nonTerminals
    productions = getProductions(rg)
    for i in range(len(productions)):
        epsInFirst = False
        left, right = divideProduction(productions[i])
        elem = right[0]
        if elem != "eps":
            if elem in terminals:
                if (left, elem) in table:
                    raise Exception(
                        "There is an ambiguous value between %s and %s" % (left, elem))
                table[(left, elem)] = (right, i+1)
            else:
                for fr in first[elem]:
                    if fr != "eps":
                        if (left, fr) in table:
                            raise Exception(
                                "There is an ambiguous value between %s and %s" % (left, fr))
                        table[(left, fr)] = (right, i+1)
                    else:
                        epsInFirst = True
        else:
            for fr in follow[left]:
                if fr != "eps":
                    if (left, fr) in table:
                        raise Exception(
                            "There is an ambiguous value between %s and %s" % (left, fr))
                    table[(left, fr)] = (right, i+1)
                else:
                    if (left, "$") in table:
                        raise Exception(
                            "There is an ambiguous value between %s and $" % left)
                    table[(left, "$")] = (right, i + 1)
    for terminal in terminals:
        for term2 in terminals:
            if terminal == term2 and terminal == "$":
                table[(terminal, terminal)] = "acc"
            elif terminal == term2:
                table[(terminal, terminal)] = "pop"
    return table


def syntacticAnalysis(rg, table, seq):
    alfa = copy.deepcopy(seq)
    alfa.append("$")
    alfa.reverse()
    beta = ["$", getStartingSymbol(rg)]
    pi = ["eps"]
    isAccepted = False
    while True:
        top_alfa = alfa[-1]
        top_beta = beta[-1]
        top_pi = pi[-1]
        print("-"*30)
        print(alfa)
        print(beta)
        print(pi)
        if (top_beta, top_alfa) in table:
            if table[(top_beta, top_alfa)] == "pop":
                alfa.pop()
                beta.pop()
            elif table[(top_beta, top_alfa)] == "acc":
                beta.pop()
                isAccepted = True
                break
            else:
                b, i = table[(top_beta, top_alfa)]
                b = copy.deepcopy(b)
                beta.pop()
                b.reverse()
                if b[0] != "eps":
                    beta += b
                pi.append(i)
        elif top_beta == "$":
            beta.pop()
        else:
            break

    if isAccepted == True:
        return True, pi
    else:
        return False, []


def writeFromResult(rg, result):
    productions = getProductions(rg)
    nonTerminals = getNonTerminals(rg)
    result.reverse()
    result.pop()
    left, right = divideProduction(productions[result[-1] - 1])
    rewr = right
    while(len(result) > 0):
        top_result = result[-1] - 1
        found = False
        left, right = divideProduction(productions[top_result])
        for j in range(len(rewr)):
            if rewr[j] == left:
                if right == ["eps"]:
                    del rewr[j]
                    found = True
                    break
                else:
                    del rewr[j]
                    rewr[j:j] = right
                    found = True
                    break
        result.pop()
    return rewr


rg = readRegularGrammarFromFile("miniLang.txt")
first = constructFirst(rg)
follow = constructFollow(rg, first)
table = constructTableV2(rg, first, follow)
print(table)
isAccepted, result = syntacticAnalysis(rg, table, getSeq(rg))
print(isAccepted, result)
if isAccepted:
    rewriten = writeFromResult(rg, result)
    print(rewriten)
    print(" ".join(rewriten))
