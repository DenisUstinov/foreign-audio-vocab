from setuptools import setup, find_packages

setup(
    name='foreign-audio-vocab',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'gtts',
        'pydub'
    ],
    description='Проект для создания аудиофайлов на основе текстовых переводов',
    author='Denis Ustinov',
    author_email='revers-06-checkup@icloud.com',
    url='https://github.com/DenisUstinov/foreign-audio-vocab',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
