# Copyright 2025 Gustavo Rezende Silva
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
from launch.actions import IncludeLaunchDescription
from launch.actions import GroupAction
from launch_ros.actions import SetRemap
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable
from launch.actions import SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    world = LaunchConfiguration('world')
    world_path = PathJoinSubstitution([
        FindPackageShare('mirte_gazebo'),
        'worlds',
        'empty.world'
        ])
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=world_path,
        description='Gazebo world'
    )

    pkg_mirte_gazebo = get_package_share_directory(
        'mirte_gazebo')
    mirte_gazebo_launch_path = os.path.join(
        pkg_mirte_gazebo,
        'launch',
        'mirte_simulation_fortress.launch.py')
    mirte_gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(mirte_gazebo_launch_path),
        launch_arguments={
            'world': world,
        }.items()
    )

    pkg_mirte_navigation = get_package_share_directory("mirte_navigation")
    mirte_navigation_launch_path = os.path.join(
        pkg_mirte_navigation, "launch", "robot_navigation.launch.py"
    )

    mirte_navigation_launch = GroupAction(
        actions=[
            SetRemap(src='mirte_base_controller/cmd_vel_unstamped',dst='/cmd_vel'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(mirte_navigation_launch_path),
                launch_arguments={
                    'use_sim_time': 'true',
                }.items()
            )
        ]
    )

    
    return LaunchDescription([
        world_arg,
        mirte_navigation_launch,
        mirte_gazebo_launch,
    ])
