from setuptools import setup, find_packages
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('podfs/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
	name='podfs',
	version=main_ns['__version__'],
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
        "scipy"
        ]
	)
