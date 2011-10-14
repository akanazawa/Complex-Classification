#!/usr/bin/python

import re
import fileMaker

def pixelExtractor(line):
    # get all the pixel values and normalize them to be in [0,1] instead of [0,255]
    vals = [ float(v) / 255 for v in line.split() ]

    # the layout is row-major, so pixels 0..27 are the first line, 28..55 are the second line and so on
    feats = {}
    for i in range(len(vals)):
        feats["px" + repr(i)] = vals[i]

    return feats


if __name__=="__main__":
    fileMaker.mainExtractor(pixelExtractor)
