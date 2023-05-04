from setuptools import setup, find_packages

setup(
    name='ipfs_dict_chain',
    version='1.0.2',
    description='A Python package that provides IPFSDict and IPFSDictChain objects, which are dictionary-like data structures that store their state on IPFS and keep track of changes.',
    author='Wouter Glorieux',
    author_email='info@valyrian.tech',
    url='https://github.com/ValyrianTech/ipfs_dict_chain',
    packages=find_packages(),
    install_requires=[
        'aioipfs>=0.6.3',
        'multiaddr>=0.0.9',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
)
