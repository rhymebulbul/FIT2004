### Rhyme Bulbul 31865224 ###
#
"""
References: Monash FIT2004 Week 3 Studio Material
https://www.youtube.com/watch?v=XiuSW_mEn7g
https://www.youtube.com/watch?v=OKd534EWcdk
"""


def analyze(results, roster, score):
    """
    High level description about the approach taken
    :param results: List of lists, containing each match
    :param roster: Number length of character set teams are formed of
    :param score: The minimum score to look for in a match
    :return:
    :Time complexity:
    :Aux Space complexity:
    """

    resultsB = []
    for each in results:
        resultsB.append(each)

    # # Add opposites to mix
    # opposites = addOpposites(results)
    #
    # # Call function to sort matches in required order
    # sort(opposites, roster)
    #
    # temp = sameScoreDuplicates(opposites, roster)
    #
    # uniques = []
    # for i in range(temp[1]):
    #     uniques.append(temp[0][i])

    # Get matches with at least the searched score
    searchedMatches = getSearchedMatches(resultsB, roster, score)

    # Get the top ten matches for this data set
    topTenMatches = getTopTenMatches(results, roster)

    return [topTenMatches, searchedMatches]

def getTopTenMatches(array, roster):
    topTenMatches = []
    print(len(array))
    # Add opposites to mix
    addOpposites(array)
    # # Call function to sort matches in required order
    sort(array, roster)
    # Remove duplicates so all are unique
    uniques = sameScoreDuplicates(array, roster)

    for i in range(len(uniques) - 1, len(uniques) - 11, -1):
        topTenMatches.append(uniques[i])

    sortTeam(topTenMatches)

    return topTenMatches


def getSearchedMatches(array, roster, score):
    searchedMatches = []
    # Call function to sort matches in required order
    sort(array, roster)
    # Remove duplicates so all are unique
    uniques = sameScoreDuplicates(array, roster)

    for match in uniques:
        # TODO: Check same team different match
        if match[2] >= score:
            searchedMatches.append(match)
        elif match[2] <= 100 - score:
            searchedMatches.append(getRotatedMatch(match))

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
    for i in range(j):
        #print(array[i])
        output.append(array[i])
    #print(len(output))
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


if __name__ == '__main__':
    results = [['EAE', 'BCA', 85], ['EEE', 'BDB', 17], ['EAD', 'ECD', 21],
               ['ECA', 'CDE', 13], ['CDA', 'ABA', 76], ['BEA', 'CEC', 79],
               ['EAE', 'CED', 8], ['CBE', 'CEA', 68], ['CDA', 'CEA', 58],
               ['ACE', 'DEE', 24], ['DDC', 'DCA', 61], ['CDE', 'BDE', 67],
               ['DED', 'EDD', 83], ['ABC', 'CAB', 54], ['AAB', 'BDB', 15],
               ['BBE', 'EAD', 28], ['ACD', 'DCD', 50], ['DEB', 'CAA', 21],
               ['EBE', 'AAC', 24], ['EBD', 'BCD', 48]]

    results = [['AAB', 'AAB', 35], ['AAB', 'BBA', 49], ['BAB', 'BAB', 42],
     ['AAA', 'AAA', 38], ['BAB', 'BAB', 36], ['BAB', 'BAB', 36],
     ['ABA', 'BBA', 57], ['BBB', 'BBA', 32], ['BBA', 'BBB', 49],
     ['BBA', 'ABB', 55], ['AAB', 'AAA', 58], ['ABA', 'AAA', 46],
     ['ABA', 'ABB', 44], ['BBB', 'BAB', 32], ['AAA', 'AAB', 36],
     ['ABA', 'BBB', 48], ['BBB', 'ABA', 33], ['AAB', 'BBA', 30],
     ['ABB', 'BBB', 68], ['BAB', 'BBB', 52]]

    out = analyze(results, 2, 63)

    for i in out[0]:
        print(i)
    print(out[1])
