#!/usr/bin/env python
# coding: utf-8
from math import sqrt
import random
from StringIO import StringIO
import numpy


def initialize_k_center(points, k):
    """Randomly choose k points as initial centers."""
    index_list = random.sample(range(0, len(points)), k)
    centers = [points[i] for i in index_list]
    return centers


def distance(a, b):
    """Calculate Euclidean distance between a and b."""
    sum_ = 0
    for x, y in zip(a, b):
        sum_ += (x-y)**2
    return sqrt(sum_)


def assign_points(points, centers):
    clusters = [[] for i in range(len(centers))]
    for point in points:
        min_ = min([(i, distance(center, point)) for i, center in enumerate(centers)], key=lambda x: x[1])
        clusters[min_[0]].append(point)
    return clusters


def update_centers(clusters):
    centers = []
    for cluster in clusters:
        dimensions = len(cluster[0])
        cluster_size = len(cluster)
        center = [.0]*dimensions
        for point in cluster:
            for i, v in enumerate(point):
                center[i] += v
        for i in range(dimensions):
            center[i] /= cluster_size
        centers.append(center)
    return centers


def k_means(points, k):
    centers = initialize_k_center(points, k)
    while True:
        clusters = assign_points(points, centers)
        new_centers = update_centers(clusters)
        if new_centers == centers:
            return clusters
        else:
            centers = new_centers


def main():
    k = 2
    data = StringIO('''0 2
    0 0
    1.5 0
    5 0
    5 2''')
    points = numpy.loadtxt(data)
    print k_means(points.tolist(), k)


if __name__ == '__main__':
    main()