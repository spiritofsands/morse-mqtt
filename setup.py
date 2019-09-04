from setuptools import setup

setup(name='morse-mqrr-rcv',
      version='0.1',
      install_requires=[
          'paho-mqtt',
          'morse-talk',
          ],
      zip_safe=False)
