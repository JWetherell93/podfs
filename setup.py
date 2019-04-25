from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='podfs',
      version='0.1',
      description='Library for PODFS decomposition for Boundary Condition Reconstruction',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='pod fourier cfd decomposition',
      url='https://github.com/JWetherell93/podfs',
      author='JWetherell93',
      author_email='jwetherell93@gmail.com',
      license='UTC',
      packages=['podfs'],
      install_requires=[
            'numpy',
            ],
      include_package_data=True,
      zip_safe=False)
