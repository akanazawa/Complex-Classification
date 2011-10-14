#!/usr/bin/python

import fileMaker
import wordExtractor
from cfdata import *

def yourCFExtractor(u,c):
    feats = {}
    ### TODO: YOUR CODE HERE
    util.raiseNotDefined()
    return feats


def basicCFExtractor(u,c):
    '''
    u in [0,211] is the user id
    c in [0,109] is the course id
    these match all the data in cfdata
    our job is to generate features for this user/course pair
    to try to predict if this user would have liked this course or not

    please DO NOT CHEAT.  that is, you can alwayse use
      rateCourse[u,c]
    as a feature and get pretty much perfect prediction (modulo overfitting)

    to help ensure that you don't do this, when extracting features for
    pair (u,c), the rateCourse[u,c] value has been replaced with -2.
    there are of course many ways around this, but we'll be looking at
    your code, so don't do it!!!

    a "positive" example is one with a rating >=4, a negative example
    is one with rating <4.

    the semantics of the data structures in cfdata are:

      userNames:        either student-### if they didn't enter a name or
                        the name they entered

      courseIds:        the numeric course ids (eg, 5350 for this course)
                 
      courseNames:      the official names of the courses

      courseDesc:       the catalog descriptions for each course (some are
                        blank if we couldn't find the description)

      courseLong:       a *long* description for each course (taken from the
                        course web page), or blank if we couldn't find it.

      rateCourse(u,c):  the rating of user u on course c; however:
                           -2    means never took the class, never rated it
                           -1    means took the class but didn't provide a rating
                           1..5  means rated the class 1, 2, 3, 4 or 5

      tookCourse  = rateCourse > -1.5  (all the classes that have been taken)
      ratedCourse = rateCourse > 0     (all the classes that have been rated)

    you will only train/test on ratedCourses :), since the others
    don't make sense to evaluate on.  however, you can try to use the
    extra information (from rateCourse == -2 vs -1) to do better
    feature extraction.
    '''

    numU,numC = rateCourse.shape

    feats = {}
    
    # first, list all courses this student has taken, and the ratings
    # for those (s)he has rated
    for c2 in range(numC):
        if tookCourse[u,c2]:
            feats['took-' + str(c2)] = 1
        if ratedCourse[u,c2]:
            feats['rated-' + str(c2)] = 1
            feats['rating-' + str(c2)] = rateCourse[u,c2]

    # next, list all users that have taken/rated this course
    for u2 in range(numU):
        if tookCourse[u2,c]:
            feats['took-' + str(u2)] = 1
        if ratedCourse[u2,c]:
            feats['rated-' + str(u2)] = 1
            feats['rating-' + str(u2)] = rateCourse[u2,c]
    
    # finally, generate a bag of words for this course based on its title
    for w,v in wordExtractor.wordExtractor(courseNames[c]).iteritems():
        feats['name:' + w] = v

    # return the features
    return feats



if __name__=="__main__":
    fileMaker.mainCFData(basicCFExtractor)
