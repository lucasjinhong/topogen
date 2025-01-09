from setuptools import setup, find_packages

setup(
    name='topogen',
    version='0.4.2',
    description='A simple tool to generate the network topology',
    author = "lucasjh",
    author_email = "jinhongkh@gmail.com",
    url = "https://github.com/lucasjinhong/topogen.git",
    packages=find_packages(),
    package_data={'topogen': ['config/*.yaml']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)