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
    # Call function to sort matches in required order
    sort(results, roster)
    print('-------------')
    print("Check: all")
    for i in results:
        print(i)
    print('-------------')
    # Get matches with at least the searched score
    searchedMatches = getSearchedMatches(results, score)

    # Get the top ten matches for this data set
    topTenMatches = getTopTenMatches(results, roster)

    topTenMatches.append(searchedMatches)
    # Testing
    print('-------------')
    print("Check: topTenMatches")
    for i in topTenMatches:
        print(i)
    print('-------------')
    return topTenMatches


# def addOpposites():
#     for match in results:
#         if match[2] >= score:
#             searchedMatches.append(match)
#         elif match[2] <= 100 - score:
#             searchedMatches.append(getRotatedMatch(match))
#

def removeDuplicates(array, roster):
    # for searched matches
    j = 1
    for i in range(2, len(array)):
        if isTeamSame(array[i][0], array[i - 1][0], roster) or isTeamSame(array[i][1], array[i - 1][1], roster):
            array[j + 1] = array[i]
            j = j + 1
            # Unique : 1....j
            # Duplicate : j + 1....n


def getTopTenMatches(results, roster):
    topTenMatches = []
    # TODO: add 85-100=15 scores
    # for i in range(len(results) - 1, len(results) - 11, -1):
    #     # TODO: Omit same teams same score
    #     if not isTeamSame(results[i], roster):
    #         topTenMatches.append(results[i])
    return topTenMatches


def getSearchedMatches(results, score):
    searchedMatches = []

    for match in results:
        # TODO: Check if this versus has been p
        if match[2] >= score:
            searchedMatches.append(match)
        elif match[2] <= 100 - score:
            searchedMatches.append(getRotatedMatch(match))
    return searchedMatches


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
    analyze(results, 5, 70)

    print(isTeamSame("ECA", "ACE", 5))
    print(isTeamSame("ECb", "ACE", 5))

    # import doctest
    #
    # doctest.testmod(verbose=True)
