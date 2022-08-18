
def analyse(results, roster, score):
    """
    >>> results = [['AAB', 'AAB', 35], ['AAB', 'BBA', 49], ['BAB', 'BAB', 42], ['AAA', 'AAA', 38], ['BAB', 'BAB', 36],
    ...             ['BAB', 'BAB', 36], ['ABA', 'BBA', 57], ['BBB', 'BBA', 32], ['BBA', 'BBB', 49], ['BBA', 'ABB', 55],
    ...             ['AAB', 'AAA', 58], ['ABA', 'AAA', 46], ['ABA', 'ABB', 44], ['BBB', 'BAB', 32], ['AAA', 'AAB', 36],
    ...             ['ABA', 'BBB', 48], ['BBB', 'ABA', 33], ['AAB', 'BBA', 30], ['ABB', 'BBB', 68], ['BAB', 'BBB', 52]]
    >>> analyse(results, 2, 64)
    [[['ABB', 'AAB', 70], ['ABB', 'BBB', 68], ['AAB', 'BBB', 67], ['AAB', 'AAB', 65], ['AAB', 'AAA', 64], ['ABB', 'ABB', 64], ['AAA', 'AAA', 62], ['AAB', 'AAA', 58], ['ABB', 'ABB', 58], ['AAB', 'ABB', 57]], [['AAB', 'AAA', 64], ['ABB', 'ABB', 64]]]

    >>> results = [['AAB', 'AAB', 35],['AAB', 'BBA', 49], ['BAB', 'BAB', 42], ['AAA', 'AAA', 38], ['BAB', 'BAB', 36],
    ...             ['BAB', 'BAB', 36], ['ABA', 'BBA', 57], ['BBB', 'BBA', 32], ['BBA', 'BBB', 49], ['BBA', 'ABB', 55],
    ...             ['AAB', 'AAA', 58], ['ABA', 'AAA', 46], ['ABA', 'ABB', 44], ['BBB', 'BAB', 32], ['AAA', 'AAB', 36],
    ...             ['ABA', 'BBB', 48], ['BBB', 'ABA', 33], ['AAB', 'BBA', 30], ['ABB', 'BBB', 68], ['BAB', 'BBB', 52]]
    >>> analyse(results, 2, 63)
    [[['ABB', 'AAB', 70], ['ABB', 'BBB', 68], ['AAB', 'BBB', 67], ['AAB', 'AAB', 65], ['AAB', 'AAA', 64], ['ABB', 'ABB', 64], ['AAA', 'AAA', 62], ['AAB', 'AAA', 58], ['ABB', 'ABB', 58], ['AAB', 'ABB', 57]], [['AAB', 'AAA', 64], ['ABB', 'ABB', 64]]]

    >>> results = [['AAB', 'AAB', 35], ['AAB', 'BBA', 49], ['BAB', 'BAB', 42], ['AAA', 'AAA', 38], ['BAB', 'BAB', 36],
    ...             ['BAB', 'BAB', 36], ['ABA', 'BBA', 57], ['BBB', 'BBA', 32], ['BBA', 'BBB', 49], ['BBA', 'ABB', 55],
    ...             ['AAB', 'AAA', 58], ['ABA', 'AAA', 46], ['ABA', 'ABB', 44], ['BBB', 'BAB', 32], ['AAA', 'AAB', 36],
    ...             ['ABA', 'BBB', 48], ['BBB', 'ABA', 33], ['AAB', 'BBA', 30], ['ABB', 'BBB', 68], ['BAB', 'BBB', 52]]
    >>> analyse(results, 2, 71)
    [[['ABB', 'AAB', 70], ['ABB', 'BBB', 68], ['AAB', 'BBB', 67], ['AAB', 'AAB', 65], ['AAB', 'AAA', 64], ['ABB', 'ABB', 64], ['AAA', 'AAA', 62], ['AAB', 'AAA', 58], ['ABB', 'ABB', 58], ['AAB', 'ABB', 57]], []]

    >>> results = [['AAB', 'AAB', 35], ['AAB', 'BBA', 49], ['BAB', 'BAB', 42], ['AAA', 'AAA', 38], ['BAB', 'BAB', 36],
    ...             ['BAB', 'BAB', 36], ['ABA', 'BBA', 57], ['BBB', 'BBA', 32], ['BBA', 'BBB', 49], ['BBA', 'ABB', 55],
    ...             ['AAB', 'AAA', 58], ['ABA', 'AAA', 46], ['ABA', 'ABB', 44], ['BBB', 'BAB', 32], ['AAA', 'AAB', 36],
    ...             ['ABA', 'BBB', 48], ['BBB', 'ABA', 33], ['AAB', 'BBA', 30], ['ABB', 'BBB', 68], ['BAB', 'BBB', 52]]
    >>> analyse(results, 2, 0)
    [[['ABB', 'AAB', 70], ['ABB', 'BBB', 68], ['AAB', 'BBB', 67], ['AAB', 'AAB', 65], ['AAB', 'AAA', 64], ['ABB', 'ABB', 64], ['AAA', 'AAA', 62], ['AAB', 'AAA', 58], ['ABB', 'ABB', 58], ['AAB', 'ABB', 57]], [['AAB', 'ABB', 30]]]
    """

    ### Your code here ###

    # Add opposites to mix
    addOpposites(results)
    # # Call function to sort matches in required order
    sort(results, roster)
    # Remove duplicates so all are unique
    uniques = sameScoreDuplicates(results, roster)

    # Get matches with at least the searched score
    searchedMatches = getSearchedMatches(uniques, score)

    # Get the top ten matches for this data set
    topTenMatches = getTopTenMatches(uniques, roster)

    return [topTenMatches, searchedMatches]


def getTopTenMatches(array, roster):
    topTenMatches = []

    for i in range(len(array) - 1, len(array) - 11, -1):
        topTenMatches.append(array[i])

    sortTeam(topTenMatches)

    return topTenMatches


def getSearchedMatches(array, score):
    matchFound = False
    searchedMatches = []

    for match in array:
        if match[2] >= score and not matchFound:
            score = match[2]
            matchFound = True
            searchedMatches.append(match)
        elif match[2] == score and matchFound:
            searchedMatches.append(match)

    sortTeam(searchedMatches)
    return searchedMatches


def addOpposites(array):
    # opposites = []
    for i in range(len(array)):
        # array.append(match)
        # print(getRotatedMatch(array[i]))
        array.append(getRotatedMatch(array[i]))

    # return array


def sameScoreDuplicates(array, roster):
    j = 0
    for i in range(1, len(array)):
        if not isTeamSame(array[i][0], array[i - 1][0], roster) or not isTeamSame(array[i][1], array[i - 1][1], roster) \
                or array[i][2] != array[i - 1][2]:
            array[j + 1] = array[i]
            j += 1
    output = []
    for i in range(j + 1):
        # print(array[i])
        output.append(array[i])
    # print(len(output))
    return output


def sort(array, roster):
    # Sort in alphabetical order of second team
    radixSortRoster(array, roster, 1)
    # Sort in alphabetical order of first team
    radixSortRoster(array, roster, 0)
    # Now sort in order of scores with inplace sort
    radixSort(array)


def countingSort(array, place):
    size = len(array)
    output = [0] * size
    count = [0] * 10

    for i in range(0, size):
        index = array[i][2] // place
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = size - 1
    while i >= 0:
        index = array[i][2] // place
        output[count[index % 10] - 1] = array[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(0, size):
        array[i] = output[i]


def radixSort(array):
    max_element = 100

    place = 1
    while max_element // place > 0:
        countingSort(array, place)
        place *= 10


def countingSortRoster(array, roster, place, team):
    size = len(array)
    output = [0] * size
    count = [0] * roster

    for i in range(0, size):
        index = ord(array[i][team][place])
        count[index % roster] += 1

    for i in range(1, roster):
        count[i] += count[i - 1]

    i = size - 1
    while i >= 0:
        index = ord(array[i][team][place])
        output[count[index % roster] - 1] = array[i]
        count[index % roster] -= 1
        i -= 1

    for i in range(0, size):
        array[i] = output[i]


def radixSortRoster(array, roster, team):
    place = len(array[0][0]) - 1
    while place >= 0:
        countingSortRoster(array, roster, place, team)
        place -= 1


def countingSortTeam(array, place):
    size = len(array)
    output = [0] * size
    count = [0] * 10

    for i in range(0, size):
        index = array[i] // place
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = size - 1
    while i >= 0:
        index = array[i] // place
        output[count[index % 10] - 1] = array[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(0, size):
        array[i] = (output[i])


def radixSortTeam(array):
    max_element = 100

    place = 1
    while max_element // place > 0:
        countingSortTeam(array, place)
        place *= 10


def sortByChar(team):
    converted = []
    for i in range(len(team)):
        converted.append(ord(team[i]))

    radixSortTeam(converted)

    for i in range(len(converted)):
        converted[i] = (chr(converted[i]))

    return ''.join(converted)


def sortTeam(array):
    for i in range(len(array)):
        array[i][0] = sortByChar(array[i][0])
        array[i][1] = sortByChar(array[i][1])


def getRotatedMatch(match):
    return [match[1], match[0], 100 - match[2]]


def rotateMatch(array, result):
    temp = [array[result][1], array[result][0], 100 - array[result][2]]
    array[result] = temp


def isTeamSame(a, b, roster):
    countA = [0] * roster
    countB = [0] * roster
    size = len(a)

    for i in range(0, size):
        indexA = ord(a[i])
        countA[indexA % roster] += 1
        indexB = ord(b[i])
        countB[indexB % roster] += 1

    for i in range(0, roster):  # for i in range(0, size):
        if countA[i] != countB[i]:
            return False
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)