#!/usr/bin/env python
# coding: utf-8
from math import log
from StringIO import StringIO
import numpy


def entropy(labels):
    label_num_dict = build_label_num_dict(labels)
    entropy_ = 0.
    total_num = len(labels)
    for label, num in label_num_dict.iteritems():
        if num:
            probability = float(num)/total_num
            entropy_ -= probability * log(probability, 2)
    return entropy_


def conditional_entropy(instances, labels, feature_index):
    """Return conditional entropy and a dict mapping feature to instance index.

    :param instances:
    :param feature_index:
    :param labels:
    :return: float, {}
    """
    total_num = len(labels)
    conditional_entropy_ = 0.
    feature_labels_dict = {}
    feature_instances_index_dict = {}
    for i, instance, label in zip(range(total_num), instances, labels):
        feature = instance[feature_index]
        try:
            feature_labels_dict[feature].append(label)
        except KeyError:
            feature_labels_dict[feature] = [label]
        try:
            feature_instances_index_dict[feature].append(i)
        except KeyError:
            feature_instances_index_dict[feature] = [i]

    for feature, feature_labels in feature_labels_dict.iteritems():
        conditional_entropy_ += float(len(feature_labels)) / total_num * \
                                entropy(feature_labels)
    return conditional_entropy_, feature_instances_index_dict


def gain(instances, feature_index, labels):
    conditional_entropy_, feature_instances_index_dict = conditional_entropy(
        instances, labels, feature_index)
    return entropy(labels) - conditional_entropy_, feature_instances_index_dict


class Branch(object):
    def __init__(self, feature_value, node):
        self.feature_value = feature_value
        self.node = node

    def __repr__(self):
        return '<Branch({}, {})>'.format(self.feature_value, self.node)


class DecisionNode(object):
    def __init__(self, feature_index):
        self.feature_index = feature_index
        self.branches = []

    def __repr__(self):
        return '<DecisionNode({}, {})>'.format(self.feature_index,
                                                   self.branches)


class LeafNode(object):
    def __init__(self, label, num):
        self.label = label
        self.num = num

    def __repr__(self):
        return '<LeafNode({}, {})>'.format(self.label, self.num)


def build_label_num_dict(labels):
    label_num_dict = {}
    for label in labels:
        try:
            label_num_dict[label] += 1
        except KeyError:
            label_num_dict[label] = 1
    return label_num_dict


def build_tree(instances, labels, feature_index_list):
    # All labels of instances are same, return left node
    label_num_dict = build_label_num_dict(labels)
    if len(label_num_dict) == 1:
        return LeafNode(labels[0], len(labels))
    # No available feature to be used to split instances
    if not feature_index_list and labels:
        # Return majority label as leaf node
        max_label = max(label_num_dict, key=lambda label: label_num_dict[label])
        return LeafNode(max_label, sum(label_num_dict.values()))

    max_gain = -1
    max_gain_feature_index = -1
    max_gain_feature_instances_index_dict = None
    for i in feature_index_list:
        gain_, feature_instances_index_dict = gain(instances, i, labels)
        if gain_ > max_gain:
            max_gain = gain_
            max_gain_feature_index = i
            max_gain_feature_instances_index_dict = feature_instances_index_dict
    new_feature_index_list = list(feature_index_list)
    new_feature_index_list.remove(max_gain_feature_index)
    root = DecisionNode(max_gain_feature_index)
    for feature_value, index_list in max_gain_feature_instances_index_dict.iteritems():
        feature_instances = []
        feature_labels = []
        for i in index_list:
            feature_instances.append(instances[i])
            feature_labels.append(labels[i])
        # Recursively build tree on branches
        tree = build_tree(feature_instances, feature_labels,
                          new_feature_index_list)
        if tree:
            root.branches.append(Branch(feature_value, tree))
    return root


class DecisionTree(object):
    root = None

    def fit(self, instances, labels):
        if not instances:
            raise RuntimeError()
        self.root = build_tree(instances, labels, range(len(instances[0])))

    def predict(self, instances):
        if not instances:
            raise RuntimeError()
        result = []
        for instance in instances:
            node = self.root
            while not isinstance(node, LeafNode):
                feature_index = node.feature_index
                feature_value = instance[feature_index]
                for branch in node.branches:
                    if branch.feature_value == feature_value:
                        node = branch.node
            if isinstance(node, LeafNode):
                result.append(node.label)
        return result

symbols = ['━', '┗', '┣']
def print_tree(tree, indent):
    if isinstance(tree, DecisionNode):
        print ' '*indent


def main():
    data_txt = StringIO('''30..40 male fair yes yes
30..40 male excellent no yes
>40 male fair no yes
>40 female fair no yes
>40 female excellent no no
<=30 male fair no no
<=30 male fair yes yes
<=30 female fair no no
30..40 female excellent yes yes
<=30 female fair no no
30..40 male fair yes yes
>40 male excellent yes no''')
    data = numpy.loadtxt(data_txt, dtype=str)
    train_instances, train_labels = data[:9, range(4)].tolist(), numpy.ndarray.flatten(data[:9, [-1]]).tolist()
    test_instances, test_labels = data[9:, range(4)].tolist(), numpy.ndarray.flatten(data[9:, [-1]]).tolist()
    decision_tree = DecisionTree()
    decision_tree.fit(train_instances, train_labels)
    result = decision_tree.predict(test_instances)
    print result


if __name__ == '__main__':
    main()