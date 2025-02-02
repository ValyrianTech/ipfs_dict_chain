from setuptools import setup

# Read README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ipfs_dict_chain',
    version='1.0.8',
    description='A Python package that provides IPFSDict and IPFSDictChain objects, which are dictionary-like data structures that store their state on IPFS and keep track of changes.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Wouter Glorieux',
    author_email='info@valyrian.tech',
    url='https://github.com/ValyrianTech/ipfs_dict_chain',
    packages=['ipfs_dict_chain'],
    install_requires=[
        'aioipfs>=0.6.3',
        'multiaddr>=0.0.9',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
