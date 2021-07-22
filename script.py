#Here is the script version of the jupyter notebook for reading the code easier.

# Solution by Kerem Tezcan.
# I make some asssumptions regarding what the question wants:
# 1. I treat two names connected with a hyphen as seperate, i.e. "John-Sam" -> John and Sam seperated
# 2. I look for names which are given in any part of the name, in paranthesis or other special characters as well
# 3. I assume lowercase and uppercase does not matter
# 4. I assume the questions wants a list of unique names: some names are found multiple times, I return the name only once

import pandas as pd
import numpy as np
import re

#read the data
data = pd.read_csv(r"C:\Users\ktezcan\Downloads\20210103_hundenamen.csv")

#search parameters:
search_string = "Luca"
search_dist = 1
verbose = False # set this if you want to see the intermediate results

search_string = search_string.lower()
print("Looking for the names which have a distance of "+str(search_dist)+" to the name: " + search_string)

#look at it to get an understanding
data.head()


#I define here the function for calculating the Levenshtein distance
#taken from: https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/

def levenshteinDistanceDP(token1, token2):
    distances = np.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    #printDistances(distances, len(token1), len(token2))
    return distances[len(token1)][len(token2)]


# here I parse the dog names and make sure there are no special characters etc left
for name in data.HUNDENAME:
    if verbose: print(name, " >>> ", re.split(' |-|\'', name.replace('(','').replace(')','').replace('""','').replace('""','')))


#now I loop through the parsed name lists and check if any of the names
#has a Levenshtein distance of 1 to any of the lower case names in the list:
for name in data.HUNDENAME:
    parsed_name = re.split(' |-|\'', name.replace('(','').replace(')','').replace('""','').replace('""',''))
    for pn in parsed_name:
        dist = levenshteinDistanceDP(search_string, pn.lower())
        if dist ==1:
            if verbose: print(name, " >>> ", parsed_name)

#The question asks us to return the names close to the search string,
#so I will only return that particular name and not the full name:
#now I loop through the parsed name lists and check if any of the names
#has a Levenshtein distance of 1 to any of the lower case names in the list:
all_names = []
for name in data.HUNDENAME:
    parsed_name = re.split(' |-|\'', name.replace('(','').replace(')','').replace('""','').replace('""',''))
    for pn in parsed_name:
        dist = levenshteinDistanceDP(search_string, pn.lower())
        if dist ==search_dist:
            if verbose: print(name," >>> ", parsed_name," >>> ", pn)
            all_names.append(pn)


#We can look at all names that fullfill our condition:
if verbose: print(all_names)


#It does not make much sense to return the same name multiple times, I assume
#the question is not asking for that, so I will just return each name only once:
all_names_unique = list(set(all_names))
print("Solution is:")
for name in all_names_unique:
    print(name + ", ")













