#!/usr/bin/env python

import keyword
import re


def make_python_identifier(string):
    """
    Takes an arbitrary string and creates a valid Python identifier.

    Identifiers must follow the convention outlined here:
        https://docs.python.org/2/reference/lexical_analysis.html#identifiers
    """

    s = string.lower()
    s = s.strip()
    s = re.sub('[\\s\\t\\n]+', '_', s)
    s = re.sub('[^0-9a-zA-Z_]', '', s)

    # Remove leading characters until we find a letter or underscore
    s = re.sub('^[^a-zA-Z_]+', '', s)

    # Check that the string is not a python identifier
    while s in keyword.kwlist:
        if re.match(".*?_\d+$", s):
            i = re.match(".*?_(\d+)$", s).groups()[0]
            s = s.strip('_'+i) + '_'+str(int(i)+1)
        else:
            s += '_1'

    return s
