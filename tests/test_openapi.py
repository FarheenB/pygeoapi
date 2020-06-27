# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2020 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

from pygeoapi.openapi import get_ogc_schemas_location
from pygeoapi.openapi import get_oas_30
import pytest
import os
from pygeoapi.util import yaml_load
import logging


LOGGER = logging.getLogger(__name__)


def test_str2bool():

    default = {
        'url': 'http://localhost:5000'
    }

    osl = get_ogc_schemas_location(default)
    assert osl == 'http://schemas.opengis.net'

    default['ogc_schemas_location'] = 'http://example.org/schemas'
    osl = get_ogc_schemas_location(default)
    assert osl == 'http://example.org/schemas'

    default['ogc_schemas_location'] = '/opt/schemas.opengis.net'
    osl = get_ogc_schemas_location(default)


def get_test_file_path(filename):
    """helper function to open test file safely"""

    if os.path.isfile(filename):
        return filename
    else:
        return 'tests/{}'.format(filename)


@pytest.fixture()
def config():
    #using custom openapi config test file with cql specifications 
    with open(get_test_file_path('pygeoapi-test-openapi-config.yml')) as fh:
        return yaml_load(fh)


@pytest.fixture()
def get_oas_30_(config):
    return get_oas_30(config)


def test_cql_filters(get_oas_30_, config):
    """added assertions here for every piece of the openapi document related to CQL extension"""

    assert isinstance(config, dict)

    #assertion for checking for support of filters
    assert 'filters' in config['resources']['obs']

    filters=['cql-text', 'cql-json'] 
    for filter_lang in filters:
        assert filter_lang in config['resources']['obs']['filters']


    assert isinstance(get_oas_30_, dict)

    #assertion for get paths
    openapi_paths=get_oas_30_.get('paths', None)
    assert openapi_paths is not None

    #assertion for components
    openapi_components=get_oas_30_.get('components', None)
    assert openapi_components is not None


    #assertion for responses
    openapi_responses=openapi_components.get('responses', None)
    assert openapi_responses is not None

    #assertion for parameters
    openapi_parameters=openapi_components.get('parameters', None)
    assert openapi_parameters is not None

    #assertion for cql schemas
    cql_schemas=openapi_components.get('schemas')
    assert cql_schemas is not None
 
    #assertion for queryables paths
    assert '/queryables' in openapi_paths is not None

    assert isinstance(openapi_paths['/queryables'], dict)
    assert isinstance(openapi_paths['/collections/obs/queryables'], dict)

    #assertion for queryables path attributes
    get_path_attributes = ['summary', 'description', 'tags', 'parameters', 'responses']
    for get_path_attribute in get_path_attributes:
        assert get_path_attribute in openapi_paths['/queryables']['get']
        assert get_path_attribute in openapi_paths['/collections/obs/queryables']['get']

    #assertion for queryables response attributes
    responses = [200, 400, 404, 500]
    for response in responses:
        assert response in openapi_paths['/queryables']['get']['responses']
        assert response in openapi_paths['/collections/obs/queryables']['get']['responses']

    #assertion for Queryables response only when queryable endpoints are present
    assert 'Queryables' in openapi_responses

    #assertion for queryables schema only when queryable endpoints are present
    assert 'queryables' in get_oas_30_['components']['schemas']



    #assertion for filter-lang parameter
    openapi_filter_lang=openapi_parameters.get('filter-lang', None)
    assert openapi_filter_lang is not None

    #assertion for filter parameter
    openapi_filter=openapi_parameters.get('filter', None)
    assert openapi_filter is not None


    #assertion for filter and filter-lang attributes
    param_attributes=['name','in', 'description','required','schema','style','explode']
    for attributes in param_attributes:
        assert attributes in openapi_filter_lang
        assert attributes in openapi_filter

    filter_lang_schemas=['type','default','enum']
    for filter_lang_schema in filter_lang_schemas:
        assert filter_lang_schema in openapi_filter_lang['schema']  
    assert openapi_filter_lang['name']=='filter-lang'
    assert openapi_filter_lang['in']=='query'
    assert openapi_filter_lang['required']==False
    assert openapi_filter_lang['schema']['type']=='string'   
    assert openapi_filter_lang['schema']['default']=='cql-text'  
    assert openapi_filter_lang['schema']['enum'] == ['cql-text', 'cql-json']     

    assert 'type' in openapi_filter['schema']
    assert openapi_filter['name']=='filter'
    assert openapi_filter['in']=='query'
    assert openapi_filter['required']==False
    assert openapi_filter['schema']['type']=='string'
    

    #assertion for logical expressions
    assert 'logicalExpression' in cql_schemas is not None
    assert cql_schemas.get('logicalExpression') is not None

    logicalExpressions = ['and', 'or', 'not']
    for logicalExpression in logicalExpressions:
        assert logicalExpression in cql_schemas['logicalExpression']['properties']

    #assertion for the definition of different logical expressions
    for logicalExpression in logicalExpressions:
        assert logicalExpression in cql_schemas is not None



    #assertion for comparison expressions
    assert 'comparisonExpressions' in cql_schemas is not None
    assert cql_schemas.get('comparisonExpressions', None) is not None

    comparisonExpressions = ['eq', 'lt', 'gt', 'lte', 'gte', 'between', 'like', 'in']
    for comparisonExpression in comparisonExpressions:
        assert comparisonExpression in cql_schemas['comparisonExpressions']['properties']

    #assertion for the definition of different comparison expressions
    for comparisonExpression in comparisonExpressions:
        assert comparisonExpression in cql_schemas is not None



    #assertion for spatial expressions
    assert 'spatialExpressions' in cql_schemas is not None
    assert cql_schemas.get('spatialExpressions', None) is not None

    spatialExpressions = ['equals', 'disjoint', 'touches', 'within', 'overlaps', 'crosses', 'intersects', 'contains']
    for spatialExpression in spatialExpressions:
        assert spatialExpression in cql_schemas['spatialExpressions']['properties']

    #assertion for the definition of different spatial expressions
    for spatialExpression in spatialExpressions:
        assert spatialExpression in cql_schemas is not None


    #assertion for temporal expressions
    assert 'temporalExpressions' in cql_schemas is not None
    assert cql_schemas.get('temporalExpressions', None) is not None

    temporalExpressions = ['after', 'before', 'begins', 'begunby', 'tcontains', 'during', 'endedby',
                        'ends', 'tequals', 'meets', 'metby', 'toverlaps', 'overlappedby']
    for temporalExpression in temporalExpressions:
        assert temporalExpression in cql_schemas['temporalExpressions']['properties']

    #assertion for the definition of different temporal expressions
    for temporalExpression in temporalExpressions:
        assert temporalExpression in cql_schemas is not None


    #assertion for arithmetic operands
    assert 'arithmeticOperands' in cql_schemas is not None
    assert cql_schemas.get('arithmeticOperands', None) is not None

    arithmeticOperands = ['property', 'function', 'value', '+', '-', '*', '/']
    for props in arithmeticOperands:
        assert props in cql_schemas['arithmeticOperands']['properties']


    #assertion for scalar operands
    assert 'scalarOperands' in cql_schemas is not None
    assert cql_schemas.get('scalarOperands', None) is not None

    scalarOperands = ['property', 'function', 'value', '+', '-', '*', '/']
    for props in scalarOperands:
        assert props in cql_schemas['scalarOperands']['properties']

    #assertion for +,-,*,/ definition
    arithmetic_operators=['add', 'sub', 'mul', 'div']
    for arithmetic_operator in arithmetic_operators:
        assert arithmetic_operator in cql_schemas is not None

    #assertion for value definition
    assert 'scalarLiteral' in cql_schemas is not None


    #assertion for spatial operands
    assert 'spatialOperands' in cql_schemas is not None
    assert cql_schemas.get('spatialOperands', None) is not None

    spatialOperands = ['property', 'function', 'value']
    for props in spatialOperands:
        assert props in cql_schemas['spatialOperands']['properties']


    #assertion for temporal operands
    assert 'temporalOperands' in cql_schemas is not None
    assert cql_schemas.get('temporalOperands', None) is not None

    temporalOperands = ['property', 'function', 'value']
    for props in temporalOperands:
        assert props in cql_schemas['temporalOperands']['properties']

    #assertion for temporal value definition
    assert 'temporalLiteral' in cql_schemas is not None
    assert 'timeLiteral' in cql_schemas is not None
    assert 'periodLiteral' in cql_schemas is not None


    #assertion for functions
    assert 'function' in cql_schemas is not None
    assert cql_schemas.get('function', None) is not None

    function = ['name', 'arguments']
    for props in function:
        assert props in cql_schemas['function']['properties']
    

    #assertion for function Object Arguments
    assert 'functionObjectArgument' in cql_schemas is not None
    assert cql_schemas.get('functionObjectArgument', None) is not None

    functionObjectArgument = ['property', 'function', 'geometry', 'bbox', 'temporalValue', '+', '-', '*', '/']
    for props in functionObjectArgument:
        assert props in cql_schemas['functionObjectArgument']['properties']

    #assertion for bbox
    assert 'bbox' in cql_schemas is not None
    #assertion for envelope definition
    assert 'envelopeLiteral' in cql_schemas is not None
    #assertion for geometry definition
    assert 'geometryLiteral' in cql_schemas is not None


    #assertion for capabilities assertion
    assert 'capabilities-assertion' in cql_schemas is not None
    assert cql_schemas.get('capabilities-assertion',None)is not None

    capabilities_assertion = ['name', 'operators', 'operands']
    for props in capabilities_assertion:
        assert props in cql_schemas['capabilities-assertion']['properties']


    #assertion for function description
    assert 'functionDescription' in cql_schemas is not None
    assert cql_schemas.get('functionDescription', None) is not None

    functionDescription = ['name', 'returns', 'arguments']
    for props in functionDescription:
        assert props in cql_schemas['functionDescription']['properties']


    #assertion for filter capabilities
    assert 'filter-capabilities' in cql_schemas is not None
    assert cql_schemas.get('filter-capabilities', None) is not None

    filter_capabilities = ['conformance-classes', 'capabilities', 'functions']
    for props in filter_capabilities:
        assert props in cql_schemas['filter-capabilities']['properties']
