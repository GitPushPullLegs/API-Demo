from setuptools import setup

setup(
    name='demoapi',
    version='0.0.1',
    description="This is a flexible API that generates dynamic SQL queries.",
    url='https://github.com/GitPushPullLegs/demoapi',
    author='Joe Aguilar',
    author_email='Jose.Aguilar.6694@gmail.com',
    license='GNU General Public License',
    packages=['mft'],
    install_requires=['flask'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)