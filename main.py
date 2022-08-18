### Rhyme Bulbul 31865224 ###
#
"""
References: Monash FIT2004 Week 2,3 Studio and Lecture Material
https://www.youtube.com/watch?v=XiuSW_mEn7g
https://www.youtube.com/watch?v=OKd534EWcdk
"""


def analyze(results, roster, score):
    """
    Basic function to consider opposite matches, sort data, remove duplicates
    and then call appropriate functions to retrieve top ten matches and searched matches
    :param results: List of lists, containing each match
    :param roster: Number length of character set teams are formed of
    :param score: The minimum score to look for in a match
    :return: List of lists containing top ten matches and searched matches
    :Time complexity: O(NM)
    :Aux Space complexity: O(NM)
    """
    # Add opposites to mix
    addOpposites(results)
    # # Call functions to sort matches in required order
    sort(results, roster)
    # Remove duplicates so all are unique
    uniques = sameScoreDuplicates(results, roster)
    # Get matches with at least the searched score
    searchedMatches = getSearchedMatches(uniques, score)
    # Get the top ten matches for this data set
    topTenMatches = getTopTenMatches(uniques)
    return [topTenMatches, searchedMatches]

def getTopTenMatches(array):
    """
    Gets the top ten matches with highest scores
    Takes the first ten matches from the sorted array
    Sorts each team name into lexicographical order
    :Input:
        argv1: array of results
    :Return: List of top ten matches with highest scores
    :Time complexity: O(NM)
    :Aux space complexity: O(NM)
    """
    topTenMatches = []
    # Iterates over array and adds first ten, which are actually greatest ten scores
    for i in range(len(array) - 1, len(array) - 11, -1):
        topTenMatches.append(array[i])
    # Sorts each team name into lexicographical order
    sortTeam(topTenMatches)
    return topTenMatches


def getSearchedMatches(array, score):
    """
    Get all matches with target score, or nearest higher score if not found.
    Iterates array for target score or higher,
    Once found, appends and sets that to target score, and only looks for exact score
    Sorts each team name into lexicographical order
    :Input:
        argv1: array of results
        argv2: minimum score we are targeting
    :Return: list of matches with at least the target score
    :Time complexity: O(NM)
    :Aux space complexity: O(NM)
    """
    matchFound = False
    searchedMatches = []
    # Iterate over array until the score or greater is found
    for j in range(len(array)):
        if array[j][2] >= score and not matchFound: # Once score or greater is found
            score = array[j][2] # set that to target score
            matchFound = True # stop looking for at least score, and look for exact score only
            searchedMatches.append(array[j]) # add element to list
        elif array[j][2] == score and matchFound: # Only look for exact score
            searchedMatches.append(array[j]) # add element to list
    searchedMatches.reverse() # Reverse order of list as appended in reverse
    # Sorts each team name into lexicographical order
    sortTeam(searchedMatches)
    return searchedMatches

def addOpposites(array):
    """
    Adds in scores of the opposite teams to the array
    Calls getRotatedMatch() to get the opposite match and
    appends to end of array
    :Input:
        argv1: array of results
    :Output, return or postcondition:
    :Time complexity: O(N)
    :Aux space complexity: O(N)
    """
    for j in range(len(array)):
        array.append(getRotatedMatch(array[j]))

def sameScoreDuplicates(array, roster):
    """
    Removes duplicate data from the array ie. same teams with the same score.
    Iterates over array and compares previous element. Copies over if unique.
    Does not if duplicate
    :Input:
        argv1: array of results
        argv2: Character set team is formed from
    :Return: array of unique elements
    :Time complexity: O(N)
    :Aux space complexity: O(N)
    """
    j = 0
    # Iterate over matches in results array and compare team and score with previous ones
    for i in range(1, len(array)):
        if not isTeamSame(array[i][0], array[i - 1][0], roster) or not isTeamSame(array[i][1], array[i - 1][1], roster) \
                or array[i][2] != array[i - 1][2]: # copy over match if unique
            array[j + 1] = array[i] # Uniques[0...j], Duplicates[j+1...n]
            j += 1
    # Create new array with uniques only
    output = []
    for i in range(j+1): # Only copy upto j, which are unique elements
        output.append(array[i])
    return output

def sort(array, roster):
    """
    Sorts results array as per requirements.
    Firsts sort in lexicographical order of team2 so that it remains in place
    Then team1, which also remains in place when finally sorted in order of scores
    :Input:
        argv1: array of results
        argv2: Character set team is formed from
    :Postcondition: array is sorted as per requirements
    :Time complexity: O(NM)
    :Aux space complexity: O(NM)
    """
    # Sort in lexicographical order of second team
    radixSortRoster(array, roster, 1)
    # Sort in lexicographical order of first team
    radixSortRoster(array, roster, 0)
    # Now sort in order of scores with inplace sort
    radixSort(array)

def countingSort(array, place):
    """
    Implements counting sort. Counts number of occurence of each number
    Turns count into cumulative count. Moves each element in array to position as denoted by cumulative count
    :Input:
        argv1: Array to be sorted
        argv2: The ones, tens or hundreds place we are sorting by
    :Postcondition: Array is sorted at given place
    :Time complexity: O(M)
    :Aux space complexity: O(M)
    """
    size = len(array) # Size of array
    output = [0] * size  # Prepare empty array of same size for output
    count = [0] * 10 # Initialize all elements of counting array to zero
    # Iterate over array
    for i in range(0, size):
        index = array[i][2] // place # get place of element
        count[index % 10] += 1  # Increment count of that integer
    # Make count array represent cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]
    # Write elements in sorted order
    i = size - 1
    while i >= 0:
        index = array[i][2] // place # get place of element
        output[count[index % 10] - 1] = array[i]  # Store each element at index denoted by count array
        count[index % 10] -= 1 # Decrement count for element written
        i -= 1
    # Rewrite output to original array
    for i in range(0, size):
        array[i] = output[i]

def radixSort(array):
    """
    Uses Counting sort to implement radix sort
    Calls counting sort on each place of team score till array is sorted
    :Input:
        argv1: Array of results to sort
    :Postcondition: Array is sorted
    :Time complexity: O(M)
    :Aux space complexity: O(M)
    """
    max_element = 100 # Largest element in list, score of 100
    place = 1
    # Continue to call counting sort on each place of the numbers until sorted
    while max_element // place > 0:
        countingSort(array, place)
        place *= 10 # Increment place to the next 10s

def countingSortRoster(array, roster, place, team):
    """
    Implements counting sort. Counts number of occurence of each number
    Turns count into cumulative count. Moves each element in array to position as denoted by cumulative count
    :Input:
        argv1: Array to be sorted
        argv2: Character set team is formed from
        argv1: The ones, tens or hundreds place we are sorting by
        argv2: Team we want to sort based on
    :Postcondition: Array is sorted at given place
    :Time complexity: O(M)
    :Aux space complexity: O(M)
    """
    size = len(array) # Size of array
    output = [0] * size  # Prepare empty array of same size for output
    count = [0] * roster # Initialize all elements of counting array to zero
    # Iterate over array
    for i in range(0, size):
        index = ord(array[i][team][place]) # get place of element
        count[index % roster] += 1 # Increment count of that integer
    # Make count array represent cumulative count
    for i in range(1, roster):
        count[i] += count[i - 1]
    # Write elements in sorted order
    i = size - 1
    while i >= 0:
        index = ord(array[i][team][place]) # get place of element
        output[count[index % roster] - 1] = array[i] # Store each element at index denoted by count array
        count[index % roster] -= 1 # Decrement count for element written
        i -= 1
    # Rewrite output to original array
    for i in range(0, size):
        array[i] = output[i]

def radixSortRoster(array, roster, team):
    """
    Uses Counting sort to implement radix sort
    Calls counting sort on each place of team name till array is sorted
    :Input:
        argv1: Array of results to sort
        argv2: Character set team is formed from
        argv3: Team we want to sort based on
    :Postcondition: Array is sorted
    :Time complexity: O(NM)
    :Aux space complexity: O(NM)
    """
    place = len(array[0][0]) - 1
    # Continue to call counting sort on each place of the numbers until sorted
    while place >= 0:
        countingSortRoster(array, roster, place, team)
        place -= 1 # Decrement place to the next

def countingSortTeam(array, place):
    """
    Implements counting sort. Counts number of occurence of each number
    Turns count into cumulative count. Moves each element in array to position as denoted by cumulative count
    :Input:
        argv1: Array to be sorted
        argv2: The ones, tens or hundreds place we are sorting by
    :Postcondition: Array is sorted at given place
    :Time complexity: O(M)
    :Aux space complexity: O(M)
    """
    size = len(array) # Size of array
    output = [0] * size # Prepare empty array of same size for output
    count = [0] * 10 # Initialize all elements of counting array to zero
    # Iterate over array
    for i in range(0, size):
        index = array[i] // place # get place of element
        count[index % 10] += 1 # Increment count of that integer
    # Make count array represent cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]
    # Write elements in sorted order
    i = size - 1
    while i >= 0:
        index = array[i] // place # get place of element
        output[count[index % 10] - 1] = array[i] # Store each element at index denoted by count array
        count[index % 10] -= 1 # Decrement count for element written
        i -= 1
    # Rewrite output to original array
    for i in range(0, size):
        array[i] = (output[i])

def radixSortTeam(array):
    """
    Uses Counting sort to implement radix sort
    Calls counting sort on each place of numbers till array is sorted
    :Input:
        argv1: Team name we want to sort
    :Postcondition: Array is sorted
    :Time complexity: O(M)
    :Aux space complexity: O(M)
    """
    max_element = 122   # Largest element in list, ASCII value of z
    place = 1
    # Continue to call counting sort on each place of the numbers until sorted
    while max_element // place > 0:
        countingSortTeam(array, place)
        place *= 10 # Increment place to the next 10s

def sortByChar(team):
    """
    Takes a team name and sorts in lexicographical order
    :Input:
        argv1: Team name we want to sort
    :Return: Team name sorted in lexicographical order
    :Time complexity: O(M)
    :Aux space complexity: O(M)
    """
    converted = []
    # Append ASCII values of each char to list
    for i in range(len(team)):
        converted.append(ord(team[i]))
    # Use radix sort to sort list
    radixSortTeam(converted)
    # changing ASCII values in sorted list to characters
    for i in range(len(converted)):
        converted[i] = (chr(converted[i]))
    # Return a string from joining sorted characters in list
    return ''.join(converted)

def sortTeam(array):
    """
    Sorts individual team names in alpahabetical order
    Iterates list and calls sort on each team name
    :Input:
        argv1: The results list we want the team characters rearranged
    :Postcondition: The given list now has team names sorted in lexicographical order
    :Time complexity: O(NM)
    :Aux space complexity: O(NM)
    """
    for i in range(len(array)):
        array[i][0] = sortByChar(array[i][0])
        array[i][1] = sortByChar(array[i][1])

def getRotatedMatch(match):
    """
    Gets the match score the other way around for the opposite team
    Simply switches the positions of teams in the record and
    calculates score for that team as the remainder of 100
    :Input:
        argv1: The match we want opposite scores for
    :Return: Opposite scores for this match
    :Time complexity: O(1)
    :Aux space complexity: O(1)
    """
    return [match[1], match[0], 100 - match[2]]

def isTeamSame(a, b, roster):
    """
    Compares two teams to check if they are the same.
    Uses counting sort to count number of times each character appears in each team.
    Then compare the count records of each team character by character to deem if same
    :Input:
        argv1: First team to compare
        argv2: Second team to compare
    :Return: Boolean whether they are the same team
    :Time complexity: O(1)
    :Aux space complexity: O(1)
    """
    # Arrays to store counts of each character
    countA = [0] * roster
    countB = [0] * roster
    size = len(a)
    for i in range(0, size):
        # Iterate over team A
        indexA = ord(a[i])
        # Increment counts of each character
        countA[indexA % roster] += 1
        # Iterate over team B
        indexB = ord(b[i])
        # Increment counts of each character
        countB[indexB % roster] += 1
    # Compare counts of each character
    for i in range(0, roster):
        if countA[i] != countB[i]:
            return False
    return True

if __name__ == '__main__':
    # results = [['EAE', 'BCA', 85], ['EEE', 'BDB', 17], ['EAD', 'ECD', 21],
    #            ['ECA', 'CDE', 13], ['CDA', 'ABA', 76], ['BEA', 'CEC', 79],
    #            ['EAE', 'CED', 8], ['CBE', 'CEA', 68], ['CDA', 'CEA', 58],
    #            ['ACE', 'DEE', 24], ['DDC', 'DCA', 61], ['CDE', 'BDE', 67],
    #            ['DED', 'EDD', 83], ['ABC', 'CAB', 54], ['AAB', 'BDB', 15],
    #            ['BBE', 'EAD', 28], ['ACD', 'DCD', 50], ['DEB', 'CAA', 21],
    #            ['EBE', 'AAC', 24], ['EBD', 'BCD', 48]]

    results = [['AAB', 'AAB', 35], ['AAB', 'BBA', 49], ['BAB', 'BAB', 42],
     ['AAA', 'AAA', 38], ['BAB', 'BAB', 36], ['BAB', 'BAB', 36],
     ['ABA', 'BBA', 57], ['BBB', 'BBA', 32], ['BBA', 'BBB', 49],
     ['BBA', 'ABB', 55], ['AAB', 'AAA', 58], ['ABA', 'AAA', 46],
     ['ABA', 'ABB', 44], ['BBB', 'BAB', 32], ['AAA', 'AAB', 36],
     ['ABA', 'BBB', 48], ['BBB', 'ABA', 33], ['AAB', 'BBA', 30],
     ['ABB', 'BBB', 68], ['BAB', 'BBB', 52]]

    out = analyze(results, 2, 63)
    print("------------")
    for i in out[0]:
        print(i)
    print(out[1])
