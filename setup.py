from setuptools import setup, find_packages


setup(
    name='colour-runner',
    version='0.1.0',
    description='Colour formatting for unittest tests',
    url='https://github.com/meshy/colour-runner',
    author='Charlie Denton',
    author_email='charlie@meshy.co.uk',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Testing',
    ],
    keywords='unittest colour color output',
    packages=find_packages(),
    install_requires=['blessings', 'pygments'],
)
