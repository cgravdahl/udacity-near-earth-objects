"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""
from functools import lru_cache,cache,reduce
import time
import re

from models import NearEarthObject


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches
        self.neo_set = {}


        # TODO: What additional auxiliary data structures will be useful?

        # TODO: Link together the NEOs and their close approaches.
        @cache
        def get_neo(approach):
            for neo in neos:
                # if neo.fullname is not self.neo_set:
                #     self.neo_set[neo.fullname] = neo
                if neo.designation == approach._designation:
                    approach.neo = neo.designation
                    neo.approaches.append(approach)
                    self.neo_set[neo.fullname] = neo
                    # if neo.designation in self.neo_set:
                    #     self.neo_set[neo.designation][neo.approaches].append(approach)
                    # else:
                    #
                    #     # self.neo_set[neo.designation] = {
                    #     #     'diameter': neo.diameter,
                    #     #     'hazardous': neo.hazardous,
                    #     #     'approaches': [approach.__str__()]
                    #     # }
                    #     # if neo.name:
                    #     #     self.neo_set[neo.designation]['name'] = neo.name
                    return neo.designation

        def set_approaches():
            start = time.time()
            for approach in approaches:
                approach.neo = get_neo(approach)
            end = time.time()
            print(end - start)
        set_approaches()


    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        # TODO: Fetch an NEO by its primary designation.
        print(self.neo_set[designation],designation)
        if designation in self.neo_set:
            return self.neo_set[designation]
        else:
            return None
        # return self.neo_set[designation]


    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        # TODO: Fetch an NEO by its name.
        values = [val for key, val in self.neo_set.items() if re.search(name.lower(), key.lower())]
        if any(name in key for key in self.neo_set.keys()):
            return values[0]
        else:
            return None

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # TODO: Generate `CloseApproach` objects that match all of the filters.
        for approach in self._approaches:
            yield approach
