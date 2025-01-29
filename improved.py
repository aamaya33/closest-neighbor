# If the user gives you two arrays of geo location, match each point in the
# first array to the closest one in the second array
# distance between longitude and latitude given by haversine (geek4geeks)
# use k-d tree, find k nearest neighbors, calculate distance (geeks4geeks).
# use basemap to plot the points on a map

# TO BE DONE plot out the points from array A in one color and B in another color.
# for the closest points, change the color of the point in array B to a
# differernt color and draw a line between the two points
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import filedialog

k = 2  # dimension of the k tree (2 since just long and lat)
arrayA = None
arrayB = None
count = 0  # count of files uploaded
calculate_button = None


class Node:
    def __init__(self, point):
        self.point = point
        self.left = None
        self.right = None


def newNode(point):  # create new node in kd tree
    return Node(point)


def insertRec(root, point, depth):  # insert node into kd tree
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


def closest(temp, root, target):
    if not root:
        return temp

    if not temp:
        return root

    lat1, long1 = temp.point[0] * math.pi / 180, temp.point[1] * math.pi / 180
    lat2, long2 = target[0] * math.pi / 180, target[1] * math.pi / 180
    lat3, long3 = root.point[0] * math.pi / 180, root.point[1] * math.pi / 180

    expression1 = (math.sin(lat1) * math.sin(lat2) + math.cos(lat1) *
                   math.cos(lat2) * math.cos(long2 - long1))
    expression2 = (math.sin(lat3) * math.sin(lat2) + math.cos(lat3) *
                   math.cos(lat2) * math.cos(long2 - long3))

    # FIXME: if there is a locaiton in both of the arrays, out of bounds error
    d1 = 3963.0 * math.acos(expression1)
    d2 = 3963.0 * math.acos(expression2)

    return temp if d1 < d2 else root


# Credits to Andre Violentyev (https://bitbucket.org/StableSort/)
def closestPoint(root, target, depth=0):
    if not root:
        return None

    cd = depth % k

    # Compare the target point and the current point
    if target[cd] < root.point[cd]:
        next_branch = root.left
        opposite_branch = root.right
    else:
        next_branch = root.right
        opposite_branch = root.left

    # Recursively search down the tree
    temp = closestPoint(next_branch, target, depth + 1)
    best = closest(temp, root, target)

    # check to see if the distance of the other branch is less than the distance of the current best
    expression = (math.sin(target[0] * math.pi / 180) * math.sin(root.point[0] * math.pi / 180) +
                  math.cos(target[0] * math.pi / 180) * math.cos(root.point[0] * math.pi / 180) *
                  math.cos(root.point[1] * math.pi / 180 - target[1] * math.pi / 180))

    if expression >= 1:
        expression = 0.98

    # FIXME: if there is a locaiton in both of the arrays, you'll get an out of bounds error here
    rprime = (3963.0 * math.acos(math.sin(target[0] * math.pi / 180) *
                                 math.sin(root.point[0] * math.pi / 180) + math.cos(target[0] * math.pi / 180) *
                                 math.cos(root.point[0] * math.pi / 180) * math.cos(root.point[1] * math.pi / 180 -
                                                                                    target[1] * math.pi / 180)))
    dist = target[cd] - root.point[cd]

    if rprime >= dist * dist:
        temp = closestPoint(opposite_branch, target, depth + 1)
        best = closest(temp, best, target)

    return best


# FIXME: Add functionality to handle degree minute seconds for coordinates (currently it just says to make it long and lat)
def openFile() -> list:
    '''
    Opens file (csv, json, txt) and parses it to find longitude and latitude

    Returns array which will then be used to find the closest point in arrayB for each point in arrayA

    '''
    global arrayA
    global arrayB
    global count
    array = []

    filetypes = (
        ('CSV files', '*.csv'),
        ('JSON files', '*.json'),
        ('Text files', '*.txt')
    )
    filepath = filedialog.askopenfilename(
        filetypes=filetypes
    )
    if not filepath:
        return
    # parse file and find longitude and latitude
    try:
        with open(filepath, 'r') as file:
            file_extension = filepath.split('.')[-1]

            if file_extension == 'txt':
                # parse text file
                # go through each line, split by comma, first element is latitude, second is longitude
                # country, name, lat, lng
                print("TXT file successfully read")
                for line in file:
                    try:
                        line = line.strip().split(',')
                        lat, long = float(line[2]), float(line[3])
                        array.append([lat, long])
                    except Exception:
                        try:
                            lat, long = float(line[3]), float(line[4])
                            array.append([lat, long])
                        except Exception:
                            print("Error parsing line: ", line, "\nThis line will be ignored. Please make sure to format the line correctly (e.g. -22.1892, 29.1269).")
                count += 1
            if file_extension == 'csv':
                # parse csv file
                print("CSV successfully read")
                for line in file:
                    # print(line)
                    try:
                        # here we're going to assume that the long, lat is at the end of the line
                        line = [clean_string_csv(value) for value in line.strip().split(',')]
                        # print(line)
                        lat, long = float(line[-2]), float(line[-1])
                        array.append([lat, long])
                    except Exception as e:
                        print("Error: ", e, "this line will be ignored. Please make sure to format the line correctly (e.g. -22.1892, 29.1269).")
                count += 1
    except Exception as e:
        print("Error: ", e)
    finally:
        file.close()

    if count == 1:
        arrayA = array
        print("ArrayA updated")
    elif count == 2:
        arrayB = array
        calculate_button.config(state=tk.NORMAL)
        plot_button.config(state=tk.NORMAL)
        print("ArrayB updated")
    else:
        print("Error: too many files uploaded. Please upload only 2 files. Terminating program.")
        window.quit()
        return
    return array


def find_closest_point(arrayA, arrayB):
    '''
    Find the closest point in arrayB for each point in arrayA

    Returns array of tuples where each tuple contains the point in arrayA and the closest point in arrayB
    '''
    root = None
    for point in arrayB:
        root = insert(root, point)
    matches = []
    for source in arrayA:
        nearest = closestPoint(root, source)
        matches.append((source, nearest.point))

    # FIXME: Actually tell the user what two places are closest instead of just printing the coordinates (readability)
    print("Here are the closest points: \n\n", matches)
    # FIXME: Plot the new points (call the plot function)
    return matches


def clean_string_csv(value):
    '''
    Removes quotations from string
    '''
    return value.strip().replace('"', '')

def plot_coordinates(arrayA, arrayB):
    '''
    Plots the coordinates on a map
    '''
    dfA = pd.DataFrame(arrayA, columns=['Latitude', 'Longitude'])
    dfB = pd.DataFrame(arrayB, columns=['Latitude', 'Longitude'])
    fig = px.scatter_map(dfA, lat="Latitude", lon="Longitude", color_discrete_sequence=["red"], zoom=4)
    fig.update_layout(map_style="carto-darkmatter")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()


if __name__ == '__main__':
    # assume second input will be arrayb
    window = tk.Tk()
    upload_button = tk.Button(text="Open File", command=openFile)
    status = tk.Label(text="Upload two files to find the closest point in the second array for each point in the first array.")
    # FIXME: once the calculate button is pressed, reset file count to 0
    # FIXME: add a clear button to reset the program
    # FIXME: plot the coordinates on a map?
    calculate_button = tk.Button(text="Calculate", command=lambda: print(find_closest_point(arrayA, arrayB)), state=tk.DISABLED)
    close_button = tk.Button(text="Quit", command=window.quit)
    plot_button = tk.Button(text="Plot", command=lambda: plot_coordinates(arrayA, arrayB), state=tk.DISABLED)
    status.pack()
    calculate_button.pack()
    plot_button.pack()
    upload_button.pack()
    close_button.pack()
    window.mainloop()