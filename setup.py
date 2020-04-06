from setuptools import setup, find_packages

setup(name='gofixit',
      version='0.0.0',
      description=u"Basic maintenance tracking software.",
      author=u"Julian Irwin",
      author_email='julian.irwin@gmail.com',
      url='https://github.com/julianirwin/gofixit',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['tinydb'],
      setup_requires=[],
      extras_require={
          'test': [],
      },
      test_suite = '',
      entry_points = {
          # 'console_scripts': ['bpl4_quickplot=batchplotlib4.bpl4_quickplot:main'],
          # 'console_scripts': ['hloopy=hloopy.cli:main'],
          }
      )
