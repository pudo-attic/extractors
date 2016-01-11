from setuptools import setup, find_packages


setup(
    name='extractors',
    version='0.1.2',
    description="Wrapper script for data extractors.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    keywords='pdf doc data extractor',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='https://github.com/pudo/extractors',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'test']),
    namespace_packages=[],
    package_data={},
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        'pdfminer==20140328',
        'chardet>=2.3.0',
        'six'
    ]
)
