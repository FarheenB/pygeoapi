"""
For evaluating CQL filter queries from Abstract Syntax Tree
"""

import logging
from typing import Tuple
import enum

from pygeoapi.exception import (CQLExceptionAttribute,
                                CQLExceptionCombination,
                                CQLExceptionComparison,
                                CQLExceptionComparator
                                )

LOGGER = logging.getLogger(__name__)


class Combinator(enum.Enum):
    """ Enum for logical operators """
    AND = "AND"
    OR = "OR"


def combine(sub_filters: Tuple, combination: Combinator = Combinator.AND):
    """
    Combine filters using a logical combinator

    :param sub_filters: the filters to combine
    :param combinator: a string: "AND" / "OR"
    :type sub_filters: tuple of multiple sub-filter result

    :return: the combined filter
    :rtype: filtered dict
    """

    try:
        mapping_list = []
        intersection = []
        union = []

        for row in sub_filters[0]:
            if row in sub_filters[1]:
                intersection.append(row)
            else:
                union.append(row)

        # perform combination operation
        if combination == "AND":
            mapping_list = intersection
        else:
            mapping_list = union + sub_filters[1]

        return mapping_list

    except IndexError as err:
        LOGGER.error(err)
        raise CQLExceptionCombination()


def negate(sub_filter):  # TODO!!
    """ Negate a filter, opposing its meaning.

        :param sub_filter: the filter to negate
        :type sub_filter: query
        :return: the negated filter
        :rtype:
    """
    pass


# Comparison operators dictionary
Comparator = {
    "<": "<",
    "<=": "<=",
    ">": ">",
    ">=": ">=",
    "<>": "!=",
    "=": "=="
}


def compare(lhs, rhs, op, mapping_choices=None, field_mapping=None):
    """ Compare a filter with an expression using a comparison operation

        :param lhs: the field to compare
        :type lhs: string
        :param rhs: the filter expression
        :type rhs: literal
        :param op: a string denoting the operation. one of ``"<"``, ``"<="``,
                   ``">"``, ``">="``, ``"<>"``, ``"="``
        :type op: str
        :param mapping_choices: a list of dict to lookup potential choices
                                for a certain field.
        :type mapping_choices: list
        :return: a comparison expression filter
        :rtype: dict
    """

    try:
        comp = Comparator[op]
        mapping_list = []
        if comp:
            for row in mapping_choices:
                # perform comparison operation
                if eval(row[lhs] + comp + str(rhs)):
                    mapping_list.append(row)

        return mapping_list

    except KeyError as err:
        LOGGER.error("Invalid field name or operator %s " % err)
        raise CQLExceptionComparison()


def between(lhs, low, high, not_=False):  # TODO!!
    """ Create a filter to match elements that have a value within a certain
        range.

        :param lhs: the field to compare
        :type lhs:
        :param low: the lower value of the range
        :type low:
        :param high: the upper value of the range
        :type high:
        :param not_: whether the range shall be inclusive (the default) or
                     exclusive
        :type not_: bool
        :return:
        :rtype:
    """
    pass


def like(lhs, rhs, case=False, not_=False, mapping_choices=None):  # TODO!!
    """ Create a filter to filter elements according to a string attribute using
        wildcard expressions.

        :param lhs: the field to compare
        :type lhs:
        :param rhs: the wildcard pattern: a string containing any number of '%'
                    characters as wildcards.
        :type rhs: str
        :param case: whether the lookup shall be done case sensitively or not
        :type case: bool
        :param not_: whether the range shall be inclusive (the default) or
                     exclusive
        :type not_: bool
        :param mapping_choices: a list of dict to lookup potential choices
                                for a certain field.
        :type mapping_choices: list
        :return: a comparison expression result
        :rtype:
    """
    pass


def contains(lhs, items, not_=False, mapping_choices=None):  # TODO!!
    """ Create a filter to match elements attribute to be in a list of choices.

        :param lhs: the field to compare
        :type lhs:
        :param items: a list of choices
        :type items: list
        :param not_: whether the range shall be inclusive (the default) or
                     exclusive
        :type not_: bool
        :param mapping_choices: a list of dict to lookup potential choices
                                for a certain field.
        :type mapping_choices: list
        :return: a comparison expression result
        :rtype:
    """
    pass


def null(lhs, not_=False):  # TODO!!
    """ Create a filter to match elements whose attribute is (not) null

        :param lhs: the field to compare
        :type lhs:
        :param not_: whether the range shall be inclusive (the default) or
                     exclusive
        :type not_: bool
        :return: a comparison expression result
        :rtype:
    """
    pass


def temporal(lhs, time_or_period, op):  # TODO!!
    """ Create a temporal filter for the given temporal attribute.

        :param lhs: the field to compare
        :type lhs:
        :param time_or_period: the time instant or time span to use as a filter
        :type time_or_period: :class:`datetime.datetime` or a tuple of two
                              datetimes or a tuple of one datetime and one
                              :class:`datetime.timedelta`
        :param op: the comparison operation. one of ``"BEFORE"``,
                   ``"BEFORE OR DURING"``, ``"DURING"``, ``"DURING OR AFTER"``,
                   ``"AFTER"``.
        :type op: str
        :return: a comparison expression result
        :rtype:
    """
    pass


def time_interval(time_or_period, containment='overlaps',
                  begin_time_field='begin_time',
                  end_time_field='end_time'):  # TODO!!
    """
    """
    pass


UNITS_LOOKUP = {
    "kilometers": "km",
    "meters": "m"
}


def spatial(lhs, rhs, op, pattern=None, distance=None, units=None):  # TODO!!
    """ Create a spatial filter for the given spatial attribute.

        :param lhs: the field to compare
        :type lhs:
        :param rhs: the time instant or time span to use as a filter
        :type rhs:
        :param op: the comparison operation. one of ``"INTERSECTS"``,
                   ``"DISJOINT"``, `"CONTAINS"``, ``"WITHIN"``,
                   ``"TOUCHES"``, ``"CROSSES"``, ``"OVERLAPS"``,
                   ``"EQUALS"``, ``"RELATE"``, ``"DWITHIN"``, ``"BEYOND"``
        :type op: str
        :param pattern: the spatial relation pattern
        :type pattern: str
        :param distance: the distance value for distance based lookups:
                         ``"DWITHIN"`` and ``"BEYOND"``
        :type distance: float
        :param units: the units the distance is expressed in
        :type units: str
        :return: a comparison expression result
        :rtype:
    """
    pass


def bbox(lhs, minx, miny, maxx, maxy, crs=None, bboverlaps=True):  # TODO!!
    """ Create a bounding box filter for the given spatial attribute.

        :param lhs: the field to compare
        :param minx: the lower x part of the bbox
        :type minx: float
        :param miny: the lower y part of the bbox
        :type miny: float
        :param maxx: the upper x part of the bbox
        :type maxx: float
        :param maxy: the upper y part of the bbox
        :type maxy: float
        :param crs: the CRS the bbox is expressed in
        :type crs: str
        :type lhs:
        :return: a comparison expression result
        :rtype:
    """
    pass


def attribute(name, field_mapping=None):
    """
    Create an attribute lookup expression using a field mapping dictionary.

    :param name: the field filter name
    :type name: str
    :param field_mapping: the dictionary to use as a lookup.
    :type mapping_choices:

    :return: field name
    :rtype:
    """

    try:
        if name in field_mapping:
            field = name
            return field
        else:
            raise CQLExceptionAttribute("Invalid field value %s " % name)

    except CQLExceptionAttribute as err:
        LOGGER.error(err)


def literal(value):
    """
    Returns the literal value of the node

    :param value: data value
    :type name: str, int, float

    :return: data value
    :rtype: str, int, float
    """

    return value


# OP_TO_FUNC = {
#     "+": add,
#     "-": sub,
#     "*": mul,
#     "/": truediv
# }


def arithmetic(lhs, rhs, op):  # TODO!!
    """ Create an arithmetic filter

        :param lhs: left hand side of the arithmetic expression.
                    either a scalar or a field lookup or another
                    type of expression
        :param rhs: same as `lhs`
        :param op: the arithmetic operation. one of
                    ``"+"``, ``"-"``, ``"*"``, ``"/"``
        :rtype:
    """
    pass
