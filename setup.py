from setuptools import setup
from setuptools import find_packages

setup(
		name = "clingo",
		packages = find_packages(),
		version = "0.1",
		description = "just an experimental tool",
		author = "Khirod Kant Naik",
		url = "https://github.com/shinigamiryuk/clingo",
		scripts = ["scripts/clingo", "scripts/runFS", "scripts/clingosearch"],
)