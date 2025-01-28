import pytest
from improved import Node, newNode, insert, closest, closestPoint, clean_string_csv

def test_node_creation():
    point = [1.0, 2.0]
    node = Node(point)
    assert node.point == point
    assert node.left is None
    assert node.right is None

def test_new_node():
    point = [1.0, 2.0]
    node = newNode(point)
    assert node.point == point
    assert isinstance(node, Node)

def test_insert():
    root = None
    point1 = [1.0, 2.0]
    point2 = [3.0, 4.0]

    root = insert(root, point1)
    assert root.point == point1

    root = insert(root, point2)
    assert root.right.point == point2

def test_closest_point():
    # Create a small tree
    root = None
    points = [
        [40.7128, -74.0060],  # New York
        [34.0522, -118.2437], # Los Angeles
        [41.8781, -87.6298],  # Chicago
    ]

    for point in points:
        root = insert(root, point)

    target = [42.3601, -71.0589]  # Boston
    result = closestPoint(root, target)
    assert result.point == [40.7128, -74.0060]  # Should be closest to New York


def test_closest_calculation():
    point1 = [40.7128, -74.0060]  # New York
    point2 = [34.0522, -118.2437]  # Los Angeles
    target = [41.8781, -87.6298]  # Chicago

    node1 = Node(point1)
    node2 = Node(point2)

    result = closest(node1, node2, target)
    assert result.point == point1  # NY should be closer to Chicago than LA

def test_edge_cases():
    # Test with None values
    assert closest(None, None, [0, 0]) is None

    # Test with same points
    point = [1.0, 1.0]
    node = Node(point)
    result = closest(node, node, point)
    assert result.point == point

@pytest.mark.parametrize("point", [
    [90.0, 180.0],    # Maximum valid coordinates
    [-90.0, -180.0],  # Minimum valid coordinates
    [0.0, 0.0],       # Zero coordinates
])
def test_coordinate_bounds(point):
    node = Node(point)
    assert node.point == point