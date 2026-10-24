import os
import sys
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_prefix

# As soon as we have updated to a newer Gazebo version,
# we need to check if this is still needed, or that
# we can use the default spawn_entity.py again
# on windows.

def generate_launch_description():

    ns = LaunchConfiguration('ns_1')

    if os.name == "nt":
        # Windows: launch_ros cannot correctly execute spawn_entity.py
        gazebo_prefix = get_package_prefix("gazebo_ros")
        spawn_entity_script = os.path.join(
            gazebo_prefix,
            "lib",
            "gazebo_ros",
            "spawn_entity.py"
        )

        spawn_entity = ExecuteProcess(
            cmd=[
                sys.executable,
                spawn_entity_script,
                "-topic", "robot_description",
                "-entity", "mirte",
                "-b",
                "-unpause"
            ],
            output="screen"
        )

    else:
        # Linux: standard ROS way
        spawn_entity = Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            output="screen",
            arguments=[
                "-topic", "robot_description",
                "-entity", "mirte",
                "-b",
                "-unpause"
            ]
        )


    return LaunchDescription([
        spawn_entity,
    ])