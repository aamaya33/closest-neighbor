# If the user gives you two arrays of geo location, match each point in the 
# first array to the closest one in the second array

#distance between longitude and latitude given by (found on geek4geeks)
#d = d = 3963.0 * arccos[(sin(lat1) * sin(lat2)) + cos(lat1) * cos(lat2) * cos(long2 – long1)]
# where long and lat are in radians


#Could use K-D Tree and use nearest neighbors query to find the closest point, but would i have to remake the tree every time? recalculating distance for each point in arrA?
#plan is to use k-d tree, find k nearest neighbors and run distance formula on that. ripping most of implementation from geek4geeks
import math 
import unittest

k=2 #dimension of the k tree (2 since just long and lat)

class Node: 
    def __init__(self, point): 
        self.point = point 
        self.left = None
        self.right = None 

def newNode(point): #create new node in kd tree
    return Node(point)

def insertRec(root, point, depth): #insert node into kd tree
    if not root:
        return newNode(point)
    
    cd = depth % k
 
    # geek4geeks magic 
    if point[cd] < root.point[cd]:
        root.left = insertRec(root.left, point, depth + 1)
    else:
        root.right = insertRec(root.right, point, depth + 1)
 
    return root

def insert(root, point):
    return insertRec(root, point, 0)

def closest(temp,root,target):
    if not root: 
        return temp 

    if not temp: 
        return root 

    lat1, long1 = temp.point[0] * math.pi / 180, temp.point[1] * math.pi / 180
    lat2, long2 = target[0] * math.pi / 180, target[1] * math.pi / 180
    lat3, long3 =root.point[0] * math.pi / 180, root.point[1] * math.pi / 180

    d1 = 3963.0 * math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(long2 - long1))
    d2 = 3963.0 * math.acos(math.sin(lat3) * math.sin(lat2) + math.cos(lat3) * math.cos(lat2) * math.cos(long2 - long3))
    
    
    return temp if d1 < d2 else root
    
#Credits to Andre Violentyev (https://bitbucket.org/StableSort/)
def closestPoint(root, target, depth=0):
    if not root: 
        return None

    cd = depth % k

    if target[cd] < root.point[cd]:
        next_branch = root.left
        opposite_branch = root.right
    else: 
        next_branch = root.right
        opposite_branch = root.left

    temp = closestPoint(next_branch, target, depth + 1)
    best = closest(temp, root, target)

    #check to see if we should traverse down the other branch 
    rprime = 3963.0 * math.acos(math.sin(target[0] * math.pi / 180) * math.sin(root.point[0] * math.pi / 180) + math.cos(target[0] * math.pi / 180) * math.cos(root.point[0] * math.pi / 180) * math.cos(root.point[1] * math.pi / 180 - target[1] * math.pi / 180))
    dist = target[cd] - root.point[cd]

    if rprime >= dist * dist: 
        temp = closestPoint(opposite_branch, target, depth + 1)
        best = closest(temp, best, target)
    
    return best


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

if __name__ == '__main__':
    unittest.main()








