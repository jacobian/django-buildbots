from setuptools import setup, find_packages

setup(
    name = "django-buildbot-recipes",
    version = "1.0",
    author = 'Jacob Kaplan-Moss',
    packages = find_packages(),
    install_requires = ['collective.buildbot'],
    entry_points = {
        'zc.buildout': ['master = django_buildbot_recipes.master_recipe:Recipe']
    }
)