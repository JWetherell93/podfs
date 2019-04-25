from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='ofreader',
      version='0.1',
      description='Python reader for native openfoam files',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='openfoam reader python',
      url='https://github.com/JWetherell93/ofreader',
      author='JWethere93',
      author_email='jwetherell93@gmail.com',
      license='UTC',
      packages=['ofreader'],
      install_requires=[
            'numpy',
            ],
      include_package_data=True,
      zip_safe=False)
