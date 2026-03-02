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
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
  # Use simulation time
  world = LaunchConfiguration('world')
  use_sim_time = LaunchConfiguration('use_sim_time')

  headless_arg = DeclareLaunchArgument(
    'headless',
    default_value='False',
    description='headless simulation'
  )

  use_sim_time_arg = DeclareLaunchArgument(
    'use_sim_time',
    default_value='True',
    description='Use simulation (Gazebo) clock if true'
  )

  world_path = PathJoinSubstitution([
    FindPackageShare('aws_robomaker_small_warehouse_world'),
    'worlds',
    'no_roof_small_warehouse/no_roof_small_warehouse.world'
  ])
  world_arg = DeclareLaunchArgument(
    'world',
    default_value=world_path,
    description='Gazebo world'
  )

  gz_sim = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
      PathJoinSubstitution([
        FindPackageShare('ros_gz_sim'),
        'launch',
        'gz_sim.launch.py',
      ])
    ),
    launch_arguments={'gz_args' : ['-r ', world, ' -v 4']}.items(),
  )

  pkg_mirte_gazebo = get_package_share_directory(
        'mirte_gazebo')
  spawn_mirte_master_path = os.path.join(
      pkg_mirte_gazebo,
      'launch',
      'spawn_mirte_master.launch.xml')
  spawn_mirte_master = IncludeLaunchDescription(
    XMLLaunchDescriptionSource(spawn_mirte_master_path),
    launch_arguments={'use_sim_time': use_sim_time}.items()
  )

  arm_nav_home_publisher_node = Node(
    package='mirte_master_arm_control',
    executable='arm_home_publisher',
    parameters=[
      PathJoinSubstitution([
        get_package_share_directory('mirte_master_arm_control'),
        'config', 'arm_nav_home_position.yml',
      ])],
  )

  return LaunchDescription([
    headless_arg,
    use_sim_time_arg,
    world_arg,
    gz_sim,
    spawn_mirte_master,
    # arm_nav_home_publisher_node,
  ])
