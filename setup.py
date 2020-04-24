from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='kubipy',
      version='0.1',
      description='a simply library to orchestrate local kubernetes clusters from python',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/LJStroemsdoerfer/kubipy',
      author='Lukas Jan Stroemsdoerfer',
      author_email='ljstroemsdoerfer@gmail.com',
      license='MIT',
      packages=['kubipy'],
      install_requires=[
          'requests',
          'subprocess'
      ],
      zip_safe=False)