# ros2_launch_util
This package provides a python module that contains functions that make composing a ROS 2 launch tree easier.

**NOTE**: this package uses the ROS 2 xacro package found [here](https://github.com/bponsler/xacro/tree/ros2-devel)

This module contains the following functions:

- **find_share_file**(package_name, file_dir, file_name)
- **find_executable**(package_name, executable_name)
- **add_node**(ld, package_name, node_name, args=None)
- **add_static_transform_publisher**(ld, parent_frame, child_frame, x=0, y=0, z=0, roll=0, pitch=0, yaw=0)
- **add_launch_file**(ld, package_name, launch_file, launch_dir="launch", argv=None)
- **xacro_to_urdf**(package_name, xacro_dir, xacro_file, urdf_file=None)
- **add_robot_state_publisher_urdf**(ld, urdf_package, urdf_dir, urdf_file)
- **add_robot_state_publisher_xacro**(ld, xacro_package, xacro_dir, xacro_file)
- **create_args_list**(arg_map)

Examples:

    from ros2_launch_util import *
    
    def launch(ld, argv):
        # Launch a robot state publisher using URDF
        #     my_robot_description/urdf/my_robot.urdf
        add_robot_state_publisher_urdf(
            ld, "my_robot_description", "urdf", "my_robot.urdf")
        
        # Or use xacro (which will be converted to urdf)
        #     my_robot_description/urdf/my_robot.urdf.xacro
        add_robot_state_publisher_xacro(
            ld, "my_robot_description", "urdf", "my_robot.urdf.xacro")
        
        # Include a launch file: other_package/launch/other_package.py
        add_launch_file(ld, "other_package", "other_package.py")
        
        # Add a static transform publisher with an x offset
        add_static_transform_publisher(ld, "world", "map", x=1.0)

	# Create a list of arguments for a node
	nodeArgs = create_args_list({
	    "--my_int": 10,
	    "--my_topic": "hello",
	})

        # Easily launch the my_node node within the my_package package
        add_node("my_package", "my_node", args=nodeArgs)
        
        # Find a file in the package's share directory:
        #     my_package/config/info.cfg
        configFile = find_share_file("my_package", "config", "info.cfg")
        
        # Find an executable within a package:
        execPath = find_executable("my_package", "my_executable")
        
        # Convert an xacro file to a URDF file, returns the path to
        # the resulting URDF file as a temporary file
        # (e.g., /tmp/my_robot.urdf.xacro_siu_qyii)
        urdfFile = xacro_to_urdf(
            "my_robot_description", "urdf", "my_robot.urdf.xacro")
        
        # Convert an xacro file to a specific URDF file
        urdfFile = xacro_to_urdf(
            "my_robot_description", "urdf", "my_robot.urdf.xacro",
            urdf_file="/tmp/my_robot.urdf")
