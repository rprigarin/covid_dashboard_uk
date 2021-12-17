from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='covid-dashboard-rprigarin',
    version='0.9.0',
    author='Ruslan Prigarin',
    author_email='rp641@exeter.ac.uk',
    license='MIT',
    description='Just some covid dashboard written using a couple API libraries and Flask.',
    long_description=read('README.md'),
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operationg System :: OS Independent",
    ],
    python_requires='>=3.6'

)