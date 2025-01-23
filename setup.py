from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name = 'smartMutator',
    version = '0.0.1',
    author = 'Spencer White',
    author_email = '',
    license = 'MIT',
    description = 'Use Anthropic Claude to convert files',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = '<github url where the tool code will remain>',
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        smartmutator=src.cli:cli
    '''
)