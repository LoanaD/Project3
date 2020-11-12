"""
    Searches deep inside a directory structure, looking for duplicate file.
    Duplicates aka copies have the same content, but not necessarily the same name.
"""
__author__ = "Loana Davis"
__email__ = "DAVISL41@my.erau.edu"
__version__ = "1.0"

# noinspection PyUnresolvedReferences
from os.path import getsize, join
from time import time

# noinspection PyUnresolvedReferences
from typing import List, Any

from p1utils import all_files, compare


def search(file_list):
    """Looking for duplicate files in the provided list of files

       :returns a list of lists, where each list contains files with the same content

       Basic search strategy goes like this:
       - until the provided list is empty.
       - remove the 1st item from the provided file_list
       - search for its duplicates in the remaining list and put the item and all its duplicates into a new list
       - if that new list has more than one item (i.e. we did find duplicates) save the list in the list of lists
       As a result we have a list, each item of that list is a list,
       each of those lists contains files that have the same content
       """
    lol = []
    while file_list:
        a = file_list.pop()
        l = []
        for x in range(len(file_list) - 1, -1, -1):
            if compare(a, file_list[x]):
                l.append(file_list.pop(x))
        if len(l) > 0:
            l.append(a)
            lol.append(l)
    return lol


def faster_search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Here's an idea: executing the compare() function seems to take a lot of time.
    Therefore, let's optimize and try to call it a little less often.
    """
    lol = []
    file_sizes = list(map(getsize, file_list))
    file_list = list(filter(lambda file: 1 < file_sizes.count(getsize(file)), file_list))

    while 0 < len(file_list):
        duplicate = [file_list.pop(0)]
        for i in range(len(file_list) - 1, -1, -1):
            if compare(duplicate[0], file_list[i]):
                duplicate.append(file_list.pop(i))
        if 1 < len(duplicate):
            lol.append(duplicate)
    return lol


def report(lol):
    """ Prints a report
    :param lol: list of lists (each containing files with equal content)
    :return: None
    Prints a report:
    - longest list, i.e. the files with the most duplicates
    - list where the items require the largest amount or disk-space
    """
    print("== == Duplicate File Finder Report == ==")
    if 0 < len(lol):
        large = max(lol, key=len)
        large.sort()
        print(f"The file with the most duplicates is: \n {large[0]}")
        print(f"Here are its {len(large) - 1} copies.")
        for x in range(1, len(large)):
            print(large[x])

        large = max(lol, key=lambda a: len(a) * getsize(a[0]))
        large.sort()

        print(f"\nThe most disk space ({(len(large) - 1) * getsize(large[0])}) could be recovered, by deleting copies "
              f"of this file:\n {large[0]}")
        print(f""
              f"Here are its {len(large) - 1} copies")
        for x in range(1, len(large)):
            print(large[x])
        print("\n")
    else:
        print("No duplicates found")


if __name__ == '__main__':
    path = join(".", "images")

    # measure how long the search and reporting takes:
    t0 = time()
    report(search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")

    print("\n\n .. and now w/ a faster search implementation:")

    # measure how long the search and reporting takes:
    t0 = time()
    report(faster_search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")
