#!/usr/bin/env python
# coding: utf-8
from unittest import TestCase
from decision_tree import build_tree

train_instances = [
    ['30..40', 'male', 'fair', 'yes'],
    ['30..40', 'male', 'excellent', 'no'],
    ['>40', 'male', 'fair', 'no'],
    ['>40', 'female', 'fair', 'no'],
    ['>40', 'female', 'excellent', 'no'],
    ['<=30', 'male', 'fair', 'no'],
    ['<=30', 'male', 'fair', 'yes'],
    ['<=30', 'female', 'fair', 'no'],
    ['30..40', 'female', 'excellent', 'yes']
]
train_labels = [
    'yes',
    'yes',
    'yes',
    'yes',
    'no',
    'no',
    'yes',
    'no',
    'yes'
]


class TestBuildTree(TestCase):
    def test_build_tree(self):
        node = build_tree(train_instances, train_labels,
                          range(len(train_instances[0])))
        print node
