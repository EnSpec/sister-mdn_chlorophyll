from setuptools import setup,find_packages
from pathlib import Path
from __version__ import __version__

# We can't reference the local requirements file within itself,
# which means installing with e.g. pip install -r MDN/requirements.txt
# won't work if we have requirements listed here, and only a '.' in
# the requirements file.
# Instead, we can reference the local path here, and parse the requirements
with Path(__file__).parent.joinpath('requirements.txt').open() as f:
        requirements = [line.strip() for line in f.readlines()]

setup(
    name='MDN',
    version=__version__,
    description='Mixture Density Network',
    author='Brandon Smith',
    author_email='b.smith@nasa.gov',
    url='https://github.com/BrandonSmithJ/MDN',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
)
