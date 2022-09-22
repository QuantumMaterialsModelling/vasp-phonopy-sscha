import distutils.core
from distutils.core import setup
import setuptools
from setuptools import find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='vasp-phonopy-sscha',  
     version='1.0',
     packages=['vasp-phonopy-sscha'] ,
     author="Ranalli Luigi",
     author_email="luigi.ranalli@univie.ac.at",
     description="An interface between VASP, PHONOPY and SSCHA",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/luigiranalli96/vasp-phonopy-sscha",
     install_requires=['numpy','pandas','scipy','ase','cellconstructor','phonopy','python-sscha'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
