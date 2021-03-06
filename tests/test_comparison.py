#! /usr/bin/env python
# coding: utf-8
#
# Copyright (c) 2020 JR Oakes
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Test Cases for Comparison Module"""

import pytest

from seodeploy.lib import comparison


@pytest.fixture
def diff():
    return comparison.CompareDiffs()


EXAMPLES = {
    "integer": {
        "items": (1, 2),
        "result": [
            {
                "type": "change",
                "item": "integer",
                "element": "",
                "production": 1,
                "staging": 2,
            }
        ],
    },
    "float": {
        "items": (1.1, 2.2),
        "result": [
            {
                "type": "change",
                "item": "float",
                "element": "",
                "production": 1.1,
                "staging": 2.2,
            }
        ],
    },
    "text": {
        "items": ("this", "that"),
        "result": [
            {
                "type": "change",
                "item": "text",
                "element": "",
                "production": "this",
                "staging": "that",
            }
        ],
    },
    "list": {
        "items": ([1, 2, 3], [1, 2, 4]),
        "result": [
            {
                "type": "add",
                "item": "list",
                "element": "",
                "production": "",
                "staging": 4,
            },
            {
                "type": "remove",
                "item": "list",
                "element": "",
                "production": 3,
                "staging": "",
            },
        ],
    },
    "dict_num": {
        "items": ({"a": 1, "b": 2}, {"a": 3, "b": 4}),
        "result": [
            {
                "type": "change",
                "item": "dict_num",
                "element": "a",
                "production": 1,
                "staging": 3,
            },
            {
                "type": "change",
                "item": "dict_num",
                "element": "b",
                "production": 2,
                "staging": 4,
            },
        ],
    },
    "dict_text": {
        "items": ({"element": "a", "content": "a"}, {"element": "a", "content": "b"}),
        "result": [
            {
                "type": "change",
                "item": "dict_text",
                "element": "content",
                "production": "a",
                "staging": "b",
            }
        ],
    },
    "dict_list_num": {
        "items": ([{"a": 1, "b": 2}], [{"a": 3, "b": 4}]),
        "result": [
            {
                "type": "change",
                "item": "dict_list_num",
                "element": "0.a",
                "production": 1,
                "staging": 3,
            },
            {
                "type": "change",
                "item": "dict_list_num",
                "element": "0.b",
                "production": 2,
                "staging": 4,
            },
        ],
    },
    "dict_list_text": {
        "items": (
            [{"element": "a", "content": "a"}],
            [{"element": "a", "content": "b"}],
        ),
        "result": [
            {
                "type": "change",
                "item": "dict_list_text",
                "element": "0.content",
                "production": "a",
                "staging": "b",
            }
        ],
    },
}


def test_comparison_add_diffs(diff):
    path = "/path/"
    diffs = [
        {
            "type": "change",
            "item": "float",
            "element": "",
            "production": 1,
            "staging": 2,
        }
    ]
    diff.add_diffs(path, diffs)
    assert diff.diffs == [
        {
            "path": "/path/",
            "diffs": [
                {
                    "type": "change",
                    "item": "float",
                    "element": "",
                    "production": 1,
                    "staging": 2,
                }
            ],
        }
    ]


def test_comparison_compare(diff):
    path = "/path/"
    for k, v in EXAMPLES.items():
        item = k
        result = {"path": path, "diffs": v["result"]}
        d1, d2 = v["items"]
        diff.compare(path, item, d1, d2)
        assert diff.diffs[-1] == result


def test_comparison_l2d(diff):
    l1, l2 = EXAMPLES["dict_list_text"]["items"]
    d1, d2 = diff._l2d(l1, l2, "element", "content")
    assert (d1, d2) == ({"a": ["a"]}, {"a": ["b"]})
