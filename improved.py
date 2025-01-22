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

def closestPoint()





