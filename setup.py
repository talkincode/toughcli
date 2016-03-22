#!/usr/bin/python


from setuptools import setup, find_packages
import toughcli

version = toughcli.__version__

install_requires = [ 'Click']
install_requires_empty = []
package_data={}


setup(name='toughcli',
      version=version,
      author='jamiesun',
      author_email='jamiesun.net@gmail.com',
      url='https://github.com/talkincode/toughcli',
      license='BSD',
      description='ToughSTRUCT Software Tools',
      long_description=open('README.md').read(),
      classifiers=[
       'Development Status :: 6 - Mature',
       'Intended Audience :: Developers',
       'Programming Language :: Python :: 2.7',
       'Topic :: Software Development :: Libraries :: Python Modules',
       'Topic :: System :: Systems Administration :: Authentication/Directory',
       ],
      packages=find_packages(),
      package_data=package_data,
      keywords=['radius', 'AAA','authentication','accounting','authorization','toughradius','toughguy'],
      zip_safe=True,
      include_package_data=True,
      eager_resources=['toughcli'],
      install_requires=install_requires,
      entry_points={
          'console_scripts': [
              'toughcli = toughcli.toughclis:cli'
          ]
      }
)