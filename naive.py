# If the user gives you two arrays of geo location, match each point in the 
# first array to the closest one in the second array

#distance between longitude and latitude given by (found on geek4geeks)
#d = d = 3963.0 * arccos[(sin(lat1) * sin(lat2)) + cos(lat1) * cos(lat2) * cos(long2 – long1)]
# where long and lat are in radians
import math
import unittest

def findClosest(arr1, arr2):
    #arr1 and arr2 are gonna be arrays of arrays, we turn the points into radians 
    closest = []
    for long1, lat1 in arr1: 
        min_distance = float('inf')
        closest_point = None

        long1Rad = long1 * math.pi / 180
        lat1Rad = lat1 * math.pi / 180

        for long2, lat2 in arr2:
            long2Rad = long2 * math.pi / 180
            lat2Rad = lat2 * math.pi / 180

            distance = 3963.0 * math.acos((math.sin(lat1Rad) * math.sin(lat2Rad)) + math.cos(lat1Rad) * math.cos(lat2Rad) * math.cos(long2Rad - long1Rad))
            if distance < min_distance:
                min_distance = distance
                closest_point = [long2, lat2]

        closest.append(closest_point)

    return closest

#test cases
class TestNaive(unittest.TestCase):
    def test_single_point(self):
        arr1 = [[-71.0589, 42.3601]]  # Boston
        arr2 = [[-74.0060, 40.7128]]  # NYC
        result = findClosest(arr1, arr2)
        self.assertEqual(result, [[-74.0060, 40.7128]])

    def test_multiple_points(self):
        arr1 = [
            [-71.0589, 42.3601],  # Boston
            [-118.2437, 34.0522]  # Los Angeles
        ]
        arr2 = [
            [-74.0060, 40.7128],  # NYC
            [-122.4194, 37.7749], # San Francisco
        ]
        result = findClosest(arr1, arr2)
        self.assertEqual(result[0], [-74.0060, 40.7128])
        self.assertEqual(result[1], [-122.4194, 37.7749])

    def test_same_locations(self):
        arr1 = [[0, 0]]
        arr2 = [[0, 0], [1, 1]]
        result = findClosest(arr1, arr2)
        self.assertEqual(result, [[0, 0]])

if __name__ == '__main__':
    unittest.main()

            
           
            