# Copyright 2020 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

import xacro


def generate_launch_description():

    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros')
    world_file_name = 'sonar_demo.world'
    world_path = os.path.join(pkg_gazebo_ros, 'worlds', world_file_name)

    gazebo = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
              launch_arguments={
                'world': os.path.join(os.path.join(get_package_share_directory('mirte_gazebo')), 'test_world.world'),
                'extra_gazebo_args': '-s libgazebo_ros_camera.so -s libgazebo_ros_ray_sensor.so -s libgazebo_ros2_control.so --verbose'
              }.items()
        )

    gazebo_ros2_control_demos_path = os.path.join(
        get_package_share_directory('mirte_gazebo'))

    xacro_file = os.path.join(gazebo_ros2_control_demos_path,
                              'urdf',
                              'mirte.xacro')

    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    params = {'robot_description': doc.toxml()}

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-x', '0.0',
                                   '-y', '0.0',
                                   '-Y', '0.0',
                                   '-entity', 'mirte'],
                        output='screen')

    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_diff_drive_base_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'diff_drive_base_controller'],
        output='screen'
    )

    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_entity,
                on_exit=[load_joint_state_controller],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[load_diff_drive_base_controller],
            )
        ),
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
    ])