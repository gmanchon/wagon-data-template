from setuptools import setup, find_packages

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name="project",
      version="1.0",
      description="Package description",
      packages=find_packages(),
      install_requires=requirements)
