#!/usr/bin/env python
# coding: utf-8
from unittest import TestCase

from k_means import k_means, initialize_k_center, assign_points, update_centers


class TestKMeans(TestCase):
    points = [[1, 1], [1, 2], [2, 1], [2, 2], [-1, -1], [-1, -2], [-2, -1], [-2, -2]]
    k = 2
    centers = [[1, 1], [-2, -2]]

    def test_k_means(self):
        result = k_means(self.points, self.k)
        print result

    def test_initialize_k_center(self):
        result = initialize_k_center(self.points, self.k)
        print result

    def test_assign_points(self):
        clusters = assign_points(self.points, self.centers)
        print clusters

    def test_update_centers(self):
        result = update_centers([self.points[:4], self.points[4:]])
        print result