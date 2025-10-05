"""
Demo script to showcase main.py entry point usage.

This script creates a sample Python file and demonstrates
how to launch CodeScope with different command-line options.
"""

import os
import tempfile
import subprocess
import sys

# Sample Python code to visualize
SAMPLE_CODE = '''
"""
Sample Python Module for CodeScope Visualization
Demonstrates various Python structures.
"""

class DataProcessor:
    """Process and analyze data."""

    def __init__(self, name):
        self.name = name
        self.data = []

    def add_data(self, item):
        """Add an item to the data list."""
        self.data.append(item)
        return len(self.data)

    def process(self):
        """Process the collected data."""
        return [self._transform(item) for item in self.data]

    def _transform(self, item):
        """Internal transformation method."""
        return str(item).upper()


class DataAnalyzer(DataProcessor):
    """Analyze processed data."""

    def analyze(self):
        """Perform analysis on data."""
        processed = self.process()
        return {
            'count': len(processed),
            'items': processed
        }


def create_processor(name):
    """Factory function to create a data processor."""
    return DataProcessor(name)


def main():
    """Main execution function."""
    processor = create_processor("demo")
    processor.add_data("hello")
    processor.add_data("world")

    analyzer = DataAnalyzer("analyzer")
    analyzer.add_data("test")
    results = analyzer.analyze()

    print(f"Analysis results: {results}")


if __name__ == "__main__":
    main()
'''


def create_sample_file():
    """Create a temporary sample Python file."""
    temp_file = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        prefix='codescope_sample_',
        delete=False
    )
    temp_file.write(SAMPLE_CODE)
    temp_file.close()
    return temp_file.name


def demo_basic_usage():
    """Demonstrate basic usage without arguments."""
    print("=" * 60)
    print("Demo 1: Basic Usage (No Arguments)")
    print("=" * 60)
    print("\nCommand: python main.py")
    print("\nThis launches CodeScope with default sample code.")
    print("You can paste your own Python code in the editor.")
    print("\nPress Ctrl+C to skip actual launch...")
    print()


def demo_with_file():
    """Demonstrate usage with a file argument."""
    print("=" * 60)
    print("Demo 2: Opening a Specific File")
    print("=" * 60)

    # Create sample file
    sample_file = create_sample_file()
    print(f"\nCreated sample file: {sample_file}")
    print(f"\nCommand: python main.py --file {sample_file}")
    print("\nThis launches CodeScope with the specified file loaded.")
    print("\nPress Ctrl+C to skip actual launch...")
    print()

    return sample_file


def demo_with_debug():
    """Demonstrate usage with debug flag."""
    print("=" * 60)
    print("Demo 3: Debug Mode")
    print("=" * 60)
    print("\nCommand: python main.py --debug")
    print("\nThis enables detailed debug logging to the console.")
    print("Useful for troubleshooting visualization issues.")
    print("\nPress Ctrl+C to skip actual launch...")
    print()


def demo_help():
    """Demonstrate help command."""
    print("=" * 60)
    print("Demo 4: Getting Help")
    print("=" * 60)
    print("\nCommand: python main.py --help")
    print("\nOutput:")
    print("-" * 60)

    # Actually run the help command
    result = subprocess.run(
        [sys.executable, 'main.py', '--help'],
        capture_output=True,
        text=True
    )
    print(result.stdout)


def demo_version():
    """Demonstrate version command."""
    print("=" * 60)
    print("Demo 5: Version Information")
    print("=" * 60)
    print("\nCommand: python main.py --version")
    print("\nOutput:")
    print("-" * 60)

    # Actually run the version command
    result = subprocess.run(
        [sys.executable, 'main.py', '--version'],
        capture_output=True,
        text=True
    )
    print(result.stdout)


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "CodeScope Main Entry Point Demo" + " " * 16 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    sample_file = None

    try:
        # Run demonstrations
        demo_basic_usage()
        input("Press Enter to continue...")
        print("\n")

        sample_file = demo_with_file()
        input("Press Enter to continue...")
        print("\n")

        demo_with_debug()
        input("Press Enter to continue...")
        print("\n")

        demo_help()
        input("Press Enter to continue...")
        print("\n")

        demo_version()

        print("\n" + "=" * 60)
        print("Demo Complete!")
        print("=" * 60)
        print("\nTo launch CodeScope:")
        print("  1. python main.py                    # Default mode")
        print("  2. python main.py --file script.py   # Load specific file")
        print("  3. python main.py --debug            # Debug mode")
        print(f"  4. python main.py -f {sample_file}  # With sample file")
        print("\nThe sample file has been kept for testing.")
        print(f"Location: {sample_file}")

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    finally:
        # Clean up (optional - keep sample file for testing)
        if sample_file and os.path.exists(sample_file):
            print(f"\nSample file available at: {sample_file}")
            print("Delete it manually when done: rm " + sample_file)


if __name__ == "__main__":
    main()
