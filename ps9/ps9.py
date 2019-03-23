# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#
from copy import deepcopy
from operator import itemgetter
from itertools import combinations

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
SAMPLE_FILENAME = "sample_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    subjects_map = {}
    inputFile = open(filename)
    for line in inputFile:
        line = line.split(',')
        subjects_map[line[0]] = (int(line[1].strip()), int(line[2].strip()))
    return subjects_map
 
    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).
	
def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\tRatio\n======\t=====\t=====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        ratio = float(subjects[s][VALUE]) / subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\t' + '{:2.2f}'.format(ratio) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    # TODO...
    if subInfo1[VALUE] > subInfo2[VALUE]:
        return True
    else:
        return False

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    # TODO...
    if subInfo1[WORK] < subInfo2[WORK]:
        return True
    else:
        return False

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    # TODO...
    if float(subInfo1[VALUE]) / subInfo1[WORK] > float(subInfo2[VALUE]) / subInfo2[WORK]:
        return True
    else:
        return False

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: string 'value', 'work' or 'ratio'
	
    """
    # TODO...
    temp_subjects = deepcopy(subjects)
    res = {}
    totalValue = 0.0
    totalWork = 0.0
    numOfSubjects = len(temp_subjects)
    i = 0
    while totalWork <= maxWork and i < numOfSubjects:
        if comparator == 'value':
            # searching for key (course name) that maps to the tuple (learning-value, work) with the max learning-value
            name = max(temp_subjects.iteritems(), key = itemgetter(1))[0]
      
        if comparator == 'work':
            # searching for key (course name) that maps to the tuple (learning-value, work) with the max work
            name = max(temp_subjects.keys(), key=(lambda k: temp_subjects[k][1]))

        if comparator == 'ratio':
            # searching for key (course name) that maps to the tuple with max learning-value/work ratio
            name = max(temp_subjects.keys(), key=(lambda k: (float(temp_subjects[k][0])/temp_subjects[k][1])))
        
        subInfo = temp_subjects.pop(name)
        if maxWork >= subInfo[1] + totalWork:
            res[name] = subInfo
            totalWork += subInfo[1]
            totalValue += subInfo [0]	
        i += 1
    return res

#
# Problem 3: Subject Selection By Brute Force
#

# Helper functions:
def dToB(n, numDigits):
    """requires: n is a natural number less than 2**numDigits
      returns a binary string of length numDigits representing the
              the decimal number n."""
    assert type(n)==int and type(numDigits)==int and\
           n >=0 and n < 2**numDigits
    bStr = ''
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n//2
    while numDigits - len(bStr) > 0:
        bStr = '0' + bStr
    return bStr

def genPset(subjects):
    """
    Generate a list of lists representing the power set of courseNames
    subjects - dictonary of subjects
	"""
    subjNames = subjects.keys()
    numSubsets = 2**len(subjNames)
    templates = []
    for i in range(numSubsets):
        templates.append(dToB(i, len(subjNames)))
    pset = []
    for t in templates:
        elem = []
        for j in range(len(t)):
            if t[j] == '1':
                elem.append(subjNames[j])
        pset.append(elem)
    return pset
	
def genPset2(subjects):
    """
    Generate a list of lists representing the power set of courseNames
    subjects - dictonary of subjects
	"""
    subjNames = subjects.keys()
    pset = []
    for i in range(len(subjNames) + 1):
        for subset in combinations(subjNames, i):
            pset.append(subset)
    return pset

def chooseBest(pset, subjects, maxWork):
    bestVal = 0.0
    bestSet = None
    for subSets in pset:
        setVal = 0.0
        setWork = 0.0
        for courseName in subSets:
            setVal += subjects[courseName][VALUE]
            setWork += subjects[courseName][WORK]
        if setWork <= maxWork and setVal > bestVal:
            bestVal = setVal
            bestSet = subSets
    return (bestSet, bestVal, setWork)

# end of helper functions

def bruteForceAdvisor(subjects, maxWork):
    """ 
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    bestSubjects = {}
    courseNames = subjects.keys()
    pset = genPset2(subjects)
    bestSet, setVal, setWork = chooseBest(pset, subjects, maxWork)
    # print ('Total value of courses taken = ' + str(setVal))
    # for course in bestSet:
        # print '  ', course
    for courseName in bestSet:
        bestSubjects[courseName] = (subjects[courseName][VALUE], subjects[courseName][WORK])
    return bestSubjects


maxWork = 50
print 'GREEDY ALGORITHM - max Work:'
printSubjects(greedyAdvisor(loadSubjects(SAMPLE_FILENAME), maxWork, 'work'))

print 'GREEDY ALGORITHM - max Value:'
printSubjects(greedyAdvisor(loadSubjects(SAMPLE_FILENAME), maxWork, 'value'))

print 'GREEDY ALGORITHM - max Ratio:'
printSubjects(greedyAdvisor(loadSubjects(SAMPLE_FILENAME), maxWork, 'ratio'))

print 'BRUTE FORCE ALGORITHM:'
    """
    May cause overFlowError depending on the size of sample
    Solutions:
    a) instead of creating the list of possible combinations, calculate in place value of set and replace it if better found
    b) be break the pset list using chunking, for example, do the first 1000 elements of the list, pickle and save them to disk
    and then do the next 1000. To work with them, unpickle one chunk at a time, this is essentially the same technique
    that databases use to work with more data than will fit in RAM.
    see: https://stackoverflow.com/questions/5537618/memory-errors-and-list-limits
    """
printSubjects(bruteForceAdvisor(loadSubjects(SAMPLE_FILENAME), maxWork))


