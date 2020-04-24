# load libs
from setuptools import setup
import kubipy

# read in README.md
with open("README.md", "r") as fh:
    long_description = fh.read()

# catch the version
current_version = kubipy.__version__

# define the setup
setup(name='kubipy',
      version=current_version,
      description='a simply library to orchestrate local kubernetes clusters from python',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/LJStroemsdoerfer/kubipy',
      author='Lukas Jan Stroemsdoerfer',
      author_email='ljstroemsdoerfer@gmail.com',
      license='MIT',
      packages=['kubipy'],
      install_requires=[
          'requests'
      ],
      zip_safe=False)