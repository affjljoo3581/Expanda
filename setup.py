from setuptools import dist, setup, find_packages

# `Cython` is used when installing `kss` library.
dist.Distribution().fetch_build_eggs(['Cython'])

setup(
    name='Expanda',
    version='1.1.2',

    author='Jungwoo Park',
    author_email='affjljoo3581@gmail.com',

    description='Integrated Corpus-Building Environment',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',

    keywords=['expanda', 'corpus', 'dataset', 'nlp'],
    url='https://github.com/affjljoo3581/Expanda',
    license='Apache-2.0',

    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires='>=3.6.0',
    install_requires=[
        'nltk',
        'ijson',
        'tqdm>=4.46.0',
        'mwparserfromhell>=0.5.4',
        'tokenizers>=0.7.0',
        'kss==1.3.1'
    ],

    entry_points={
        'console_scripts': [
            'expanda = expanda:_main',
            'expanda-shuffling = expanda.shuffling:_main',
            'expanda-tokenization = expanda.tokenization:_main'
        ]
    },

    classifiers=[
        'Environment :: Console',
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ]
)
