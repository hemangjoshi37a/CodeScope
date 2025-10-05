"""
Setup configuration for CodeScope
Python Code Visualization Tool
"""

from setuptools import setup, find_packages
import os


def read_file(filename):
    """Read contents of a file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ''


def read_requirements():
    """Read requirements from requirements.txt"""
    requirements = []
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    requirements.append(line)
    except FileNotFoundError:
        # Fallback to hardcoded requirements
        requirements = [
            'PyQt6>=6.0.0',
            'pyqtgraph>=0.12.0',
            'networkx>=2.5',
        ]
    return requirements


# Read long description from README
long_description = read_file('README.md')

# Read version from a VERSION file or set default
version = '1.0.0'
if os.path.exists('VERSION'):
    version = read_file('VERSION').strip()

setup(
    name='codescope',
    version=version,
    author='Hemang Joshi',
    author_email='hemangjoshi37a@gmail.com',
    description='Transform complex Python codebases into intuitive, interactive visual representations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hemangjoshi37a/CodeScope',
    project_urls={
        'Bug Reports': 'https://github.com/hemangjoshi37a/CodeScope/issues',
        'Source': 'https://github.com/hemangjoshi37a/CodeScope',
        'Documentation': 'https://github.com/hemangjoshi37a/CodeScope#readme',
    },

    # Package discovery
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    py_modules=['app', 'unknown_project_handler', 'demo_unknown_project', 'minimal_example'],

    # Python version requirement
    python_requires='>=3.7',

    # Dependencies
    install_requires=read_requirements(),

    # Optional dependencies for development
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=22.0',
            'flake8>=4.0',
            'mypy>=0.950',
        ],
        'test': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'pytest-qt>=4.0',
        ],
    },

    # Entry points for command-line scripts
    entry_points={
        'console_scripts': [
            'codescope=app:main',
        ],
    },

    # Package data to include
    include_package_data=True,

    # Classification metadata
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Environment :: X11 Applications :: Qt',
        'Natural Language :: English',
    ],

    # Keywords for discoverability
    keywords='visualization code-analysis ast python pyqt6 graph networkx development-tools',

    # License
    license='MIT',

    # Package metadata
    zip_safe=False,
)
