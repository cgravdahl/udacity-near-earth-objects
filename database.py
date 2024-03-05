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
from functools import cache

import re


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
        self.neo_dict = {}
        self.approaches_dict = {}
        """Tried to get a better understanding of caching for Python, leveraged Dicts to cache
         inspect get methods. There can be improvements to get_neo and get approaches. With a refactor could
         be leveraged elsewhere as well. 
         """
        def set_approaches():
            self.approaches_dict = self.get_approaches()
        set_approaches()

    @cache
    def get_neo(self, approach):
        cache_neos = {}
        for neo in self._neos:
            if neo.designation == approach._designation:
                approach.neo = neo
                neo.approaches.append(approach)
                cache_neos[neo.fullname] = neo
                return cache_neos

    @cache
    def get_approaches(self, **kwargs):
        cache_approaches = {}
        if len(kwargs) == 0:
            for approach in self._approaches:
                self.neo_dict.update(self.get_neo(approach))
                cache_approaches[approach.neo] = approach
            return cache_approaches

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        # print(self.neo_dict[designation], designation)
        values = [val for key, val in self.neo_dict.items() if re.search(designation.lower(), key.lower())]
        if any(designation in key for key in self.neo_dict.keys()):
            for value in values:
                if value.designation.lower() == designation.lower():
                    return value

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
        values = [val for key, val in self.neo_dict.items() if re.search(name.lower(), key.lower())]
        if any(name in key for key in self.neo_dict.keys()):
            for value in values:
                if value.name.lower() == name.lower():
                    return value
            # return values[0]
        else:
            return None

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        asked_filters = []
        for asked_filter in filters:
            if asked_filter.value is not None:
                asked_filters.append(asked_filter)
        for approach in self._approaches:
            filtered_results = []
            if len(asked_filters) >= 1:
                for asked_filter in asked_filters:
                    if asked_filter(approach):
                        filtered_results.append(approach)
                    else:
                        filtered_results = []
                if len(filtered_results) == len(asked_filters):
                    yield approach
            else:
                yield approach
