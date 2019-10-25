from setuptools import find_packages, setup

setup(
    name='elefant',
    version='1.0.0',
    url='https://elefant.augustbonds.com',
    description='A personal microblog/bookmark app',
    author='August Bonds',
    author_email='august.bonds@protonmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
