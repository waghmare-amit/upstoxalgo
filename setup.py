import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'upstoxalgo',
    packages = setuptools.find_packages(),
    version = '0.3',
    include_package_data = True,
    description = 'Unofficial Python library for Upstox',
    long_description = long_description,
    long_description_content_type = "text/markdown", 
    author = 'waghmare-amit',
    author_email = 'wamit066@gmail.com',
    license="GPLv3",
    license_files=['LICENSE'],
    url = 'https://github.com/waghmare-amit/algotrading-upstoxapi',
    install_requires = ['pandas', 'requests', 'curlify'],
    keywords = ['upstox', 'uplink', 'python', 'nse', 'trading', 'stock markets'],
    classifiers = [
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3', 
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.6'
)