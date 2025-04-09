from setuptools import setup, find_packages

setup(
    name="closest-neighbor",
    version="0.1.0",
    description="Tool for matching geographical points to their closest neighbors using k-d trees",
    author="aamaya3",
    author_email="aamaya3@bu.edu",
    packages=find_packages(),
    install_requires=[
        "pandas >= 2.2.2",
        "plotly >= 5.22",
        "matplotlib >= 3.8.4",
        "tk >= 0.1.0",
    ],
    tests_require=[
        "pytest >= 7.0.0",
    ],
    entry_points={
        "console_scripts": [
            "closest-neighbor=improved:main",
        ],
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: GIS",
    ],
)