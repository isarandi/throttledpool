from setuptools import setup

setup(
    name='throttledpool',
    version='0.1.0',
    author='István Sárándi',
    author_email='istvan.sarandi@uni-tuebingen.de',
    packages=['throttledpool'],
    license='LICENSE',
    description='Parallel process pool that throttles the task producer thread to avoid '
                'out-of-memory issues',
    python_requires='>=3.6',
)
