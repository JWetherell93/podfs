from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
	name='podfs',
	version='0.1',
	description='Library for PODFS decomposition for Boundary Condition Reconstruction',
	long_description=readme(),
	url='https://github.com/JWetherell93/podfs',
	author='JWetherell93',
	author_email='jwetherell93@gmail.com',
	packages=['podfs'],
	entry_points = {
		"console_scripts": ['podfs = podfs.podfs:main']
			},
    install_requires = [
        "numpy",
        ]
	)
