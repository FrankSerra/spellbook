from setuptools import setup

setup(
    name='spellbook',
    packages=['spellbook'],
    include_package_data=True,
    install_requires=[
        'flask',
		'flask-sqlalchemy'
    ]
)