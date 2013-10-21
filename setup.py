
# Display Node - Python and Javascript plotting and data visualisation. 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# 20 Oct 2013, Helsinki 


from setuptools import setup, Extension
from glob import glob 


setup(
    name='DisplayNode',
    version='0.1.0',
    author='Stefano Pedemonte',
    author_email='stefano.pedemonte@gmail.com',
    packages=['DisplayNode', 'petlink.examples', 'petlink.tests'], 
    ext_modules=[petlink32_c_module, ],
    test_suite = "DisplayNode.tests", 
    url='http://niftyrec.scienceontheweb.com/',
    license='LICENSE.txt',
    description='Python and Javascript plotting and data visualisation.',
    long_description=open('README.txt').read(),
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[], 
)

