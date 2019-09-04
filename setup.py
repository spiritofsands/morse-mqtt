from setuptools import setup

setup(name='morse-mqrr-rcv',
      version='0.1',
      install_requires=[
          'morse-talk',
          'numpy',
          'paho-mqtt',
          'scipy',
          ],
      zip_safe=False)
