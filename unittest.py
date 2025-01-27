import unittest
from improved import *

#tests #thankyou gpt 
class TestKDTree(unittest.TestCase):
    def setUp(self):
        # Initialize test data
        self.simple_points = [[2,3], [5,4], [9,6], [4,7], [8,1]]
        self.geo_points = [
            [42.3601, -71.0589],  # Boston
            [40.7128, -74.0060],  # NYC
            [34.0522, -118.2437], # LA
            [41.8781, -87.6298],  # Chicago
            [29.7604, -95.3698]   # Houston
        ]
        self.dest_points = [
            [42.2626, -71.8023],  # Worcester (near Boston)
            [40.7357, -74.1724],  # Newark (near NYC)
            [34.1478, -118.1445], # Pasadena (near LA)
            [41.8339, -87.8722],  # Oak Park (near Chicago)
            [29.7355, -95.2308],  # Pasadena TX (near Houston)
            [39.9526, -75.1652],  # Philadelphia
            [38.9072, -77.0369]   # Washington DC
        ]
        
    def test_tree_construction(self):
        root = None
        for point in self.simple_points:
            root = insert(root, point)
        self.assertEqual(root.point, [2,3])
        self.assertEqual(root.right.point, [5,4])
        
    def test_empty_tree(self):
        root = None
        result = closestPoint(root, [1,1])
        self.assertIsNone(result)
        
    def test_single_node(self):
        root = None
        root = insert(root, [1,1])
        result = closestPoint(root, [2,2])
        self.assertEqual(result.point, [1,1])
        
    def test_nearest_neighbor_simple(self):
        root = None
        for point in self.simple_points:
            root = insert(root, point)
        target = [3,4]
        result = closestPoint(root, target)
        self.assertEqual(result.point, [2,3])
        
    def test_nearest_neighbor_geo(self):
        root = None
        for point in self.geo_points:
            root = insert(root, point)
        # Query point near NYC
        target = [40.7, -74.0]
        result = closestPoint(root, target)
        self.assertEqual(result.point, [40.7128, -74.0060])
    def test_nearest_city_matching(self):
        root = None
        # Build KD-tree with destination points
        for point in self.dest_points:
            root = insert(root, point)
            
        # Test each source point
        matches = []
        for source in self.geo_points:
            nearest = closestPoint(root, source)
            matches.append((source, nearest.point))
            
        # Verify expected matches
        self.assertEqual(matches[0][1], [42.2626, -71.8023])  # Boston -> Worcester
        self.assertEqual(matches[1][1], [40.7357, -74.1724])  # NYC -> Newark
        self.assertEqual(matches[2][1], [34.1478, -118.1445]) # LA -> Pasadena