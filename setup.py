"""
setup.py for config-path

https://github.com/barry-scott/config-path.git

"""

# Always prefer setuptools over distutils
import setuptools
import os.path

# Use the VERSION defined in __init__.py
import config_path

# Get the long description from the README file
with open( os.path.join( os.path.dirname( __file__ ), 'README.md'), encoding='utf-8' ) as f:
    long_description = f.read()

def getDevStatusFromVersion():
    if 'a' in config_path.VERSION:
        return 'Development Status :: 3 - Alpha'

    elif 'b' in config_path.VERSION:
        return 'Development Status :: 4 - Beta'

    else:
        return 'Development Status :: 5 - Production/Stable'

setuptools.setup(
    name='config-path',

    version=config_path.VERSION,

    description='config-path is a library to work with paths to config folders and files in an OS independent way',
    long_description=long_description,
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://github.com/barry-scott/config-path',

    # Author details
    author='Barry Scott',
    author_email='barry@barrys-emacs.org',

    # Choose your license
    license='Apache 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        getDevStatusFromVersion(),

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
    ],

    # What does your project relate to?
    keywords='development',

    packages=['config_path'],
)
