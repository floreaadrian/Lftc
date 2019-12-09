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


def getNonTerminals(gr):
    return list(set(gr[0].split(",")))


def getTerminals(gr):
    return list(set(gr[1].split(",")))


def getProductions(gr):
    return gr[2:]


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


def getProductinosContainingNonTerminal(rg, nonTerminal):
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
        prodFoundIn = getProductinosContainingNonTerminal(rg, i)
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
    print(nextFollow)


rg = readRegularGrammarFromFile("rg1.txt")
first = constructFirst(rg)
follow = constructFollow(rg, first)
