from setuptools import setup

setup(name='morse-mqrr-rcv',
      version='0.1',
      install_requires=[
          'morse-talk',
          'opencv-python',
          'paho-mqtt',
          ],
      zip_safe=False)
