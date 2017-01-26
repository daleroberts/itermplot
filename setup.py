from setuptools import setup, find_packages

setup(name='itermplot',
      packages=find_packages(),
      install_requires=[
        'matplotlib',
        'six',
        'numpy'
      ],
      version='0.19',
      description='An awesome iTerm2 backend for Matplotlib, so you can plot directly in your terminal.',
      url='http://github.com/daleroberts/itermplot',
      author='Dale Roberts',
      author_email='dale.o.roberts@gmail.com',
      license='MIT',
      zip_safe=False)
