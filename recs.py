# recs.py

import matplotlib
from math import sqrt

# create dict of user preferences (in this case, movie critics and
# their rating of movies)

critics = {'Lisa Rose': {'Lady in the Water': 2.5,
                         'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0,
                         'Superman Returns': 3.5,
                         'You, Me, and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0,
                            'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5,
                            'Superman Returns': 5.0,
                            'You, Me, and Dupree': 3.5,
                            'The Night Listener': 3.0},
           'Michael Phillips': {'Lady in the Water': 2.5,
                                'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5,
                                'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5,
                            'Just My Luck': 3.0,
                            'Superman Returns': 4.0,
                            'You, Me, and Dupree': 2.5,
                            'The Night Listener': 4.5},
           'Mick LaSalle': {'Lady in the Water': 3.0,
                            'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0,
                            'Superman Returns': 3.0,
                            'You, Me, and Dupree': 2.0,
                            'The Night Listener': 3.0},
           'Jack Matthews': {'Lady in the Water': 3.0,
                             'Snakes on a Plane': 4.0,
                             'Superman Returns': 5.0,
                             'You, Me, and Dupree': 3.5,
                             'The Night Listener': 3.0},
           'Toby': {'Snakes on a Plane': 4.5,
                    'Superman Returns': 4.0,
                    'You, Me, and Dupree': 1.0}
           }

# returns a distance-based similarity score between 1 and 0
# (a value of 1 means that two people have identical preferences)
# between two people

def sim_distance(prefs, person1, person2):
    # Get list of shared tems
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    #if they have no ratings in common, return 0
    if len(si)==0: return 0;

    # add up the squares of all the differences
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                        for item in prefs[person1] if item in prefs[person2]])

    return 1/(1+sqrt(sum_of_squares))

# returns the pearson correlation coefficient between two people
# (measure of the /strength /of the association between the two variables)

def sim_pearson(prefs,p1,p2):
    # Get the list of mutually rated items
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1

    # Find the number of elements
    n=len(si)

    # If there are no ratings in common, return 0
    if n==0: return 0

    # Add up all the preferences
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])

    # Sum up the squares
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

    # Sum up the products
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

    # Calculate Pearson score
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0

    r=num/den

    return r

# to get an ordered list of people with similar tastes to the
# specified person, use topMatches

# returns the best matches for person from the prefs dictionary
# number of results and similarity function are optional params

def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other)
            # this function uses a list comprehension to compare
            # toby to every other user in the dictionary using one
            # of the previously defined distance metrics
            for other in prefs if other!=person]

    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]

# to get recommendations for a specified person, call getRecommendations

def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        # don't compare toby to himself
        if other==person: continue
        sim=similarity(prefs,person,other)

        # ignore scores of zero or lower
        if sim<=0: continue
        for item in prefs[other]:
            # only score movies toby hasn't seen yet
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * Score
                totals.setdefault(item,0)
                # how the final score for an item is calculated--score for
                # each item is multiplied by the similarity and these
                # products are all added together
                totals[item]+=prefs[other][item]*sim
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim

        # Creating the normalize list
        rankings=[(total/simSums[item],item) for item,total in totals.items()]       

        # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

# to match similar products, you can begin by looking at who liked a
# particular item and seeing the other things that they liked
# this is the same method we used earlier to determine similarity
# between people--we need only to swap the people and the items

def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            # flip item and person
            result[item][person]=prefs[person][item]

    return result
