from setuptools import (
    setup,
    find_packages,
)

# Install requirements 
with open('README.md') as fh:
    long_description = fh.read()

with open('core/requirements.txt') as rf:
    requires = rf.read().splitlines()
    print(requires)

setup(name='OPSE',
    version='0.1.0',
    description='Collect person profile base on information provide by user',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/opse-dev/opse-framework/',
    install_requires=requires,
    packages=find_packages(),
    include_package_data=True,
    author='OPSE-dev',
    author_email='',
    license='MIT',
    zip_safe=False)
