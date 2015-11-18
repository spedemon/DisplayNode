
# Display Node - Python and Javascript plotting and data visualisation. 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# 20 Oct 2013, Helsinki 


import multiprocessing
from setuptools import setup, Extension
from glob import glob 


setup(
    name='DisplayNode',
    version='0.3.0',
    author='Stefano Pedemonte',
    author_email='stefano.pedemonte@gmail.com',
    packages=['DisplayNode', 'DisplayNode.examples', 'DisplayNode.tests'], 
    data_files=[('DisplayNode/static', glob('DisplayNode/static/*.*')),
                ('DisplayNode/static/openseadragon', glob('DisplayNode/static/openseadragon/*.*')),
                ('DisplayNode/static/openseadragon/images', glob('DisplayNode/static/openseadragon/images/*.*')),
                ('DisplayNode/static/tipix', glob('DisplayNode/static/tipix/*.*')),
                ('DisplayNode/static/tipix/js', glob('DisplayNode/static/tipix/js/*.*')),
                ('DisplayNode/static/tipix/style', glob('DisplayNode/static/tipix/style/*.*')),
                ('DisplayNode/static/tipix/images', glob('DisplayNode/static/tipix/images/*.*')),
    ],
    test_suite = "DisplayNode.tests", 
    url='http://www.occiput.io/',
    license='LICENSE.txt',
    description='Web-based plotting and data visualisation package.',
    long_description=open('README.rst').read(),
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[], 
)

