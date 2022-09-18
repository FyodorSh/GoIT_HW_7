from setuptools import setup, find_namespace_packages

setup(name='Sort folder',
      version='1.0',
      description='Sort folder',
      author='Fyodor Shevchenko',
      author_email='fyodor.shevchenko@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      install_requires=['py7zr', 'patool'],
      entry_points={'console_scripts': ['clean-folder = sort_folder.sort_folder:clean']}
     )