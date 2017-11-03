from jellyfish import jaro_winkler

#def validWord(word, dictionary):

rmvpunc = str.maketrans('','','.,")(}{][/?><~=+-_;\':!@#$%^&`*')

def closestWord(word, dictionary):
    word = word.translate(rmvpunc)
    word = word.lower()
    #DO NOT REMOVE IDK WHY THIS MAKES IT WORK
    if word == 'i':
        return 'i'
    #would return 'is' for some reason
    if((any(char.isdigit() for char in word))):
        return
    maxWord = ''
    maxDist = -1.0
    for w in dictionary:
        dist = jaro_winkler(w, word)
        if dist > maxDist:
            maxDist = dist
            maxWord = w
    if(maxDist < .5):
        return
    return maxWord