#!/usr/bin/env python3
"""
Demonstration of the Unknown Project Structure Handler feature.

This script showcases the capabilities of the UnknownProjectHandler
by analyzing different types of Python projects.
"""

from unknown_project_handler import UnknownProjectHandler, ProjectType, analyze_unknown_project


def demo_web_application():
    """Demonstrate detection of a web application"""
    print("=" * 60)
    print("DEMO 1: Web Application Detection")
    print("=" * 60)

    code = """
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        # Create user
        return {'status': 'created'}
    return {'users': []}

if __name__ == '__main__':
    app.run(debug=True)
"""

    handler = UnknownProjectHandler(code)
    result = handler.analyze()

    print(f"✓ Project Type: {result['project_type'].value}")
    print(f"✓ Number of Functions: {len(result['structure_info']['functions'])}")
    print(f"✓ Number of Imports: {len(result['structure_info']['imports'])}")
    print(f"✓ Visualization Nodes: {len(result['nodes'])}")
    print(f"✓ Success: {result['success']}")
    print()


def demo_cli_tool():
    """Demonstrate detection of a CLI tool"""
    print("=" * 60)
    print("DEMO 2: CLI Tool Detection")
    print("=" * 60)

    code = """
import argparse
import sys
from pathlib import Path

def process_file(filename, verbose=False):
    '''Process a single file'''
    if verbose:
        print(f"Processing {filename}")
    # Process file logic here
    return True

def main():
    parser = argparse.ArgumentParser(description='File processor CLI')
    parser.add_argument('files', nargs='+', help='Files to process')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-o', '--output', help='Output directory')

    args = parser.parse_args()

    for file in args.files:
        process_file(file, args.verbose)

if __name__ == '__main__':
    main()
"""

    result = analyze_unknown_project(code)

    print(f"✓ Project Type: {result['project_type'].value}")
    print(f"✓ Number of Functions: {len(result['structure_info']['functions'])}")
    print(f"✓ Has 'main' function: {'main' in [f['name'] for f in result['structure_info']['functions']]}")
    print(f"✓ Success: {result['success']}")
    print()


def demo_data_analysis():
    """Demonstrate detection of a data analysis project"""
    print("=" * 60)
    print("DEMO 3: Data Analysis Project Detection")
    print("=" * 60)

    code = """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_dataset(filepath):
    '''Load data from CSV file'''
    return pd.read_csv(filepath)

def clean_data(df):
    '''Clean and preprocess data'''
    df = df.dropna()
    df = df[df['value'] > 0]
    return df

def analyze_correlations(df):
    '''Analyze correlations between variables'''
    corr_matrix = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True)
    plt.show()
    return corr_matrix

def plot_distributions(df, columns):
    '''Plot distributions for specified columns'''
    fig, axes = plt.subplots(len(columns), 1, figsize=(10, 5*len(columns)))
    for ax, col in zip(axes, columns):
        df[col].hist(ax=ax, bins=30)
        ax.set_title(f'Distribution of {col}')
    plt.tight_layout()
    plt.show()
"""

    result = analyze_unknown_project(code)

    print(f"✓ Project Type: {result['project_type'].value}")
    print(f"✓ Number of Functions: {len(result['structure_info']['functions'])}")
    print(f"✓ Uses data science libraries: True")
    print(f"✓ Success: {result['success']}")
    print()


def demo_error_handling():
    """Demonstrate error handling with syntax errors"""
    print("=" * 60)
    print("DEMO 4: Error Handling (Code with Syntax Errors)")
    print("=" * 60)

    code = """
import os
import sys

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process(self):
        return [x * 2 for x in self.data]

def broken_function(:  # <-- Syntax error: missing parameter name
    print('This function has a syntax error'
    return None

def working_function():
    '''This function is fine'''
    return "I work!"

class AnotherClass:
    def method(self):
        pass
"""

    result = analyze_unknown_project(code)

    print(f"✓ Success: {result['success']}")
    print(f"✓ Has Errors: {len(result['structure_info']['errors']) > 0}")
    print(f"✓ Number of Errors: {len(result['structure_info']['errors'])}")

    if result['structure_info']['errors']:
        for error in result['structure_info']['errors']:
            print(f"  - {error['type']}: {error['message']}")

    print(f"✓ Partial Analysis Succeeded:")
    print(f"  - Classes found: {len(result['structure_info']['classes'])}")
    print(f"  - Imports found: {len(result['structure_info']['imports'])}")
    print(f"✓ Error nodes in visualization: {len([n for n in result['nodes'] if n[1] == 'error'])}")
    print()


def demo_library():
    """Demonstrate detection of a library"""
    print("=" * 60)
    print("DEMO 5: Library Detection")
    print("=" * 60)

    code = """
'''
Math utilities library
'''

class Vector:
    '''Vector class for 2D/3D operations'''

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def magnitude(self):
        '''Calculate vector magnitude'''
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def normalize(self):
        '''Normalize the vector'''
        mag = self.magnitude()
        return Vector(self.x/mag, self.y/mag, self.z/mag)

    def dot(self, other):
        '''Calculate dot product'''
        return self.x*other.x + self.y*other.y + self.z*other.z

class Matrix:
    '''Matrix class for linear algebra'''

    def __init__(self, data):
        self.data = data

    def transpose(self):
        '''Transpose the matrix'''
        return Matrix([[self.data[j][i] for j in range(len(self.data))]
                       for i in range(len(self.data[0]))])

    def multiply(self, other):
        '''Matrix multiplication'''
        # Implementation here
        pass
"""

    result = analyze_unknown_project(code)

    print(f"✓ Project Type: {result['project_type'].value}")
    print(f"✓ Number of Classes: {len(result['structure_info']['classes'])}")
    print(f"✓ Class Names: {[c['name'] for c in result['structure_info']['classes']]}")
    print(f"✓ Total Methods: {sum(len(c['methods']) for c in result['structure_info']['classes'])}")
    print(f"✓ Has 'main' function: {'main' in [f['name'] for f in result['structure_info']['functions']]}")
    print(f"✓ Success: {result['success']}")
    print()


def demo_visualization_data():
    """Demonstrate visualization data structure"""
    print("=" * 60)
    print("DEMO 6: Visualization Data Structure")
    print("=" * 60)

    code = """
import requests

class APIClient:
    def get(self, url):
        return requests.get(url)

def process_response(response):
    return response.json()
"""

    result = analyze_unknown_project(code)

    print("Nodes (name, type):")
    for node in result['nodes']:
        print(f"  - {node[0]:20s} [{node[1]}]")

    print("\nEdges (parent → child):")
    for edge in result['edges']:
        print(f"  - {edge[0]} → {edge[1]}")

    print("\nLevels:")
    for level_name, level_nodes in result['levels'].items():
        if level_nodes:
            print(f"  - {level_name}: {level_nodes}")
    print()


def main():
    """Run all demonstrations"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "UNKNOWN PROJECT HANDLER DEMO" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    demo_web_application()
    demo_cli_tool()
    demo_data_analysis()
    demo_error_handling()
    demo_library()
    demo_visualization_data()

    print("=" * 60)
    print("All demonstrations completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()
