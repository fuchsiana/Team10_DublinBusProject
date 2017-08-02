from setuptools import setup

setup(name='dublin_bus_travel_predictor',
      version='0.1',
      description='Dublin Bus Web Application Project',
      author = 'Emma Byrne, Wen-Ting Chang, Ian Fuchs, Willie Delaney',
      url='https://github.com/wjdelaney/Team-10',
      license = 'GNU',
      packages = ['web_app'],
      entry_points = {
          'console_scripts': [
              'run = web_app.run:run'
            ]
          }
      )