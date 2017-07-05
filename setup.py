from setuptools import find_packages
from setuptools import setup

setup(
    name='ros2_launch_util',
    version='0.0.0',
    packages=find_packages('src', exclude=['test']),
    package_dir={'': 'src'},
    install_requires=['setuptools', 'imp', 'xacro', 'ros2run', 'ament_index_python'],
    author='Brett Ponsler',
    author_email='ponsler@gmail.com',
    maintainer='Brett Ponsler',
    maintainer_email='ponsler@gmail.com',
    url='https://github.com/bponsler/ros2_launch_util',
    download_url='https://github.com/bponsler/ros2_launch_util',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='ROS 2 launch utility functions.',
    long_description=('Provides utility functions for use in the ROS 2 launch system'),
    license='Apache License, Version 2.0',
)
