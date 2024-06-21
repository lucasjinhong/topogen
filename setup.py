from setuptools import setup, find_packages

setup(
    name='topogen',
    version='0.3.0.beta',
    author = "lucasjh",
    author_email = "jinhongkh@gmail.com",
    url = "https://github.com/lucasjinhong/topogen.git",
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here.
    ],
    tests_require=[
        'pytest',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    entry_points={
        'console_scripts': [
            'topogen=topogen.topo_generator:main',  # Assuming topo_generator.py has a main function
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)