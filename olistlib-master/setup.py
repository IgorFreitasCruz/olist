import os
from distutils.core import setup
import setuptools

BASE_DIR = os.path.dirname( os.path.abspath(__file__) )
with open( os.path.join( BASE_DIR, 'requirements.txt' ), 'r' ) as reqs_file:
      reqs = [i.strip("\n") for i in reqs_file.readlines() ]

setup(name='olistlib',
      version='0.1',
      description='Biblioteca para suporte de módulos nos projetos da empresa Olist',
      author='Téo Calvo',
      author_email='teocalvo2@gmail.com',
      packages=setuptools.find_packages(),
      install_requires=reqs,
     )