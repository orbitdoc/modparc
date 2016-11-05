# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from funcparserlib.parser import (many, maybe, Parser)
from .syntax import keyword, op, token_type

from .expressions import name, comment, expression, array_subscript

# pylint: disable=no-name-in-module
from .syntax_elements import (TypePrefix, TypeSpecifier, ConditionAttribute,
                              Declaration, ComponentDeclaration, ComponentList,
                              ComponentClause)
# pylint: enable=no-name-in-module

kw = keyword

type_prefix = (maybe(kw("flow") | kw("stream")) +
               maybe(kw("discrete") | kw("parameter") | kw("constant")) +
               maybe(kw("input") | kw("output"))) >> TypePrefix

type_specifier = name >> TypeSpecifier

condition_attribute = keyword('if') + expression >> ConditionAttribute


@Parser
def declaration(tokens, state):
    from .modification import modification
    parser = (token_type('ident') + maybe(array_subscript)
              + maybe(modification)) >> Declaration
    return parser.run(tokens, state)

component_declaration = (declaration + maybe(condition_attribute) + comment
                         >> ComponentDeclaration)

component_list = (component_declaration + maybe(many(op(",") +
                                                     component_declaration))
                  >> ComponentList)

component_clause = (type_prefix + type_specifier + maybe(array_subscript)
                    + component_list) >> ComponentClause
