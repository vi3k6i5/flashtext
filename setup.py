from setuptools import setup, Command
from sphinx.setup_command import BuildDoc
import subprocess


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call(['py.test'])
        raise SystemExit(errno)

name = 'flashtext'
version = '1.3'

setup(
    name=name,
    version=version,
    url='http://github.com/vi3k6i5/flashtext',
    author='Vikash Singh',
    author_email='vikash.duliajan@gmail.com',
    description='Extract/Replaces keywords in sentences.',
    long_description=open('README.rst').read(),
    packages=['flashtext'],
    install_requires=[],
    platforms='any',
    cmdclass={'test': PyTest, 'build_sphinx': BuildDoc},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', version)
        }
    }
)
