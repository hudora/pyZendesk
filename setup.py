from setuptools import setup, find_packages

setup(name='zendesk',
      maintainer='',
      maintainer_email='md@hudora.de',
      version='0.1',
      url='https://github.com/hudora/pyZendesk/',
      description='pyZendesk',
      long_description="Python Module for Zendesk automation",
      license='BSD',
      #classifiers=['Intended Audience :: Developers',
      #             'Programming Language :: Python'],
      
      
      py_modules=['zendesk'],
      #packages = find_packages(),
      package_data = {
      },
      install_requires = [],
      zip_safe = True,
)
