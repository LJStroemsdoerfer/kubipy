from setuptools import setup

setup(name='kubipy',
      version='0.0.0.0.1',
      description='a simply library to orchestrate local kubernetes clusters from python',
      url='https://github.com/LJStroemsdoerfer/kubipy',
      author='Lukas Jan Stroemsdoerfer',
      author_email='ljstroemsdoerfer@gmail.com',
      license='MIT',
      packages=['kubipy'],
      install_requires=[
          'requests'
      ],
      zip_safe=False)