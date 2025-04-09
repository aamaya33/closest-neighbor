# EC530-Assignment1
[![Python Tests](https://github.com/aamaya33/closest-neighbor/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/aamaya33/closest-neighbor/actions/workflows/python-package-conda.yml)

**Collaborator:** Logan Lechuga

## Problem Statement
Given two arrays of geographic coordinates, match each point in the first array to the closest point in the second array.

## Solutions

### 1. Naive Approach
- Iterate through each point in array A.
- For each point in A, calculate the distance to every point in array B.
- Return an array containing the closest point in B for each point in A.

### 2. Improved Approach: KD Tree
- Construct a KD Tree using array B to reduce the number of distance calculations.
- Perform a K-Nearest Neighbors (KNN) query on the tree to identify the closest points.
- Use longitude and latitude for the KD Tree queries, followed by the distance formula for final validation.

### Resources
The KD Tree implementation was found on geeksforgeeks and KNN query was inspired by StableSort’s video tutorial and code.

GPT used to create some base test cases. 
