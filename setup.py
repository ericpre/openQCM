import codecs
import os.path
from setuptools import setup, find_packages


# https://packaging.python.org/guides/single-sourcing-package-version/
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


install_requires = ['h5py',
                    'lxml',
                    'numpy',
                    'pandas',
                    'progressbar',
                    'pyserial',
                    'pyqtgraph',
                    'scipy',
                    ]

setup(name='openQCM',
      version=get_version("openQCM/__init__.py"),
      description='Real Time Frequency and Dissipation Monitoring for the openQCM Q-1 device',
      url='https://openqcm.com',
      license='GPL-3.0-or-later',
      package_data={'openQCM':['*.txt'],
                    },
      entry_points={
          'gui_scripts': [
              'openQCM = openQCM.__main__:main',
              ]
          },
      packages=find_packages(),
      python_requires='~=3.6',
      install_requires=install_requires,
      zip_safe=False
      )
