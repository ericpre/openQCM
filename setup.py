from setuptools import setup, find_packages

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
      version='2.1',
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
