from os.path import basename, exists, join, splitext

from imp import load_source

from ros2run.api import get_executable_path
from ament_index_python.packages import get_package_share_directory


def find_share_file(package_name, file_dir, file_name):
    """Locate the path to a file within a package's share directory.

    Locate the path to a file within a package's share directory.

    * package_name -- is the name of the package
    * file_dir -- is the package directory containing the file (or None)
    * file_name -- is the name of the file to find

    """
    if file_dir is None: file_dir = ""
    return join(get_package_share_directory(package_name), file_dir, file_name)


def find_executable(package_name, executable_name):
    """Locate the path to a node within a package.

    Locate the path to a node within a package.

    * package_name -- is the name of the package
    * executable_name -- is the name of the executable

    """
    return get_executable_path(
        package_name=package_name,
        executable_name=executable_name)


def add_node(ld, package_name, node_name, args=None):
    """Add a node to the launch tree.

    Add a node to the launch tree.

    * ld -- is the launch descriptor object
    * package_name -- is the name of the package
    * node_name -- is the name of the node within the package
    * args -- the args to pass to the node
    """
    # Get the path to the executable
    executable = find_executable(package_name, node_name)

    # Make sure the node exists
    if not exists(executable):
        raise Exception("Failed to find '%s' node in package '" %
                        (node_name, package_name))
    
    # Add the node to the launch tree
    if args is None: args = []
    ld.add_process(cmd=[executable] + args)

    
def add_static_transform_publisher(
        ld, parent_frame, child_frame,
        x=0, y=0, z=0,
        roll=0, pitch=0, yaw=0):
    """Add a static transform publisher node to the launch tree.

    Add a static transform publisher node to the launch tree.

    * ld -- is the launch descriptor object
    * parent_frame -- is the name of the parent tf frame
    * child_frame -- is the name of the child tf frame
    * x -- the x offset for the transform
    * y -- the y offset for the transform
    * z -- the z offset for the transform
    * roll -- the roll offset for the transform
    * pitch -- the pitch offset for the transform
    * yaw -- the yaw offset for the transform

    """
    STATIC_TRANSFORM_PUBLISHER = get_executable_path(
        package_name="tf2_ros",
        executable_name="static_transform_publisher")
    
    ld.add_process(cmd=[
        STATIC_TRANSFORM_PUBLISHER,
        str(x), str(y), str(z),
        str(yaw), str(pitch), str(roll),
        parent_frame,
        child_frame
    ])


def add_launch_file(
        ld, package_name, launch_file, launch_dir="launch", argv=None):
    """Add a launch file to the launch tree.

    Add a launch file to the launch tree.

    * ld -- is the launch descriptor object
    * package_name -- is the name of the package containing the launch file
    * launch_file -- is the name of the launch file
    * launch_dir -- is the package directory containing the launch file
    * argv -- is the dictionary of input arguments

    """
    # Locate the launch file
    if launch_dir is None: launch_dir = ""
    package_launch_file = find_share_file(package_name, launch_dir, launch_file)

    if not exists(package_launch_file):
        raise Exception("Failed to locate launch file: %s" %
                        package_launch_file)

    # Import the launch module
    module_name = splitext(basename(package_launch_file))[0]
    launch_module = load_source(module_name, package_launch_file)
    if launch_module is None:
        raise Exception("Failed to import launch module: %s" %
                        package_launch_file)

    # Make sure the launch function exists in the module
    if not hasattr(launch_module, "launch"):
        raise Exception("Imported invalid launch module: %s" %
                        package_launch_file)

    try:
        if argv is None: args = {}
        launch_module.launch(ld, argv)
    except Exception as e:
        raise Exception("Failed to add launch file: %s, error: %s" %
                        (package_launch_file, e))

    
def xacro_to_urdf(package_name, xacro_dir, xacro_file, urdf_file=None):
    """Convert a xacro file to URDF.

    Convert a xacro file to URDF.

    * package_name -- is the name of the package that contains the xacro file
    * xacro_dir -- the name of the directory containing the xacro file
    * xacro_file -- is the name of xacro file
    * urdf_file -- the path to the URDF file to save (None to use a temporary file)

    """
    # Locate the xacro file
    xacroFile = find_share_file(package_name, xacro_dir, xacro_file)

    # Convert the xacro file to urdf, and return the path
    # to the urdf file
    import xacro
    return xacro.to_urdf(xacroFile, urdf_path=urdf_file)
    
   
def add_robot_state_publisher_urdf(ld, urdf_package, urdf_dir, urdf_file):
    """Add a robot state publisher node to the launch tree.

    Add a robot state publisher node to the launch tree using the given
    urdf file.

    * urdf_package -- is the name of the package that contains the urdf file
    * urdf_dir -- the name of the directory containing the urdf file
    * urdf_file -- is the name of urdf file

    """
    # Find the URDF file
    urdf = find_share_file(urdf_package, urdf_dir, urdf_file)

    # Launch the robot state publisher with the desired URDF
    add_node(ld, "robot_state_publisher", "robot_state_publisher", [urdf])

    
def add_robot_state_publisher_xacro(ld, xacro_package, xacro_dir, xacro_file):
    """Add a robot state publisher node to the launch tree.

    Add a robot state publisher node to the launch tree using the given
    xacro file.

    * xacro_package -- is the name of the package that contains the xacro file
    * xacro_dir -- the name of the directory containing the xacro file
    * xacro_file -- is the name of xacro file

    """
    # Convert the xacro file to URDF
    urdf = xacro_to_urdf(xacro_package, xacro_dir, xacro_file)

    # Launch the robot state publisher with the desired URDF
    add_node(ld, "robot_state_publisher", "robot_state_publisher", [urdf])
