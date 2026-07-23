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


def generate_launch_description():
  # Use simulation time
  world = LaunchConfiguration('world')

  headless_arg = DeclareLaunchArgument(
    'headless',
    default_value='False',
    description='headless simulation'
  )

  use_sim_time_arg = DeclareLaunchArgument(
    'use_sim_time',
    default_value='true',
    description='Use simulation (Gazebo) clock if true'
  )

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

  gz_sim = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
      PathJoinSubstitution([
        FindPackageShare('ros_gz_sim'),
        'launch',
        'gz_sim.launch.py',
      ])
    ),
    launch_arguments={'gz_args' : ['-r ', world, ' --verbose']}.items(),
  )

  pkg_mirte_gazebo = get_package_share_directory(
        'mirte_gazebo')
  spawn_mirte_pioneer_path = os.path.join(
      pkg_mirte_gazebo,
      'launch',
      'spawn_mirte_pioneer.launch.xml')
  spawn_mirte_pioneer = IncludeLaunchDescription(
    XMLLaunchDescriptionSource(spawn_mirte_pioneer_path),
    launch_arguments={'use_sim_time' : LaunchConfiguration('use_sim_time')}.items(),
  )

  return LaunchDescription([
    headless_arg,
    use_sim_time_arg,
    world_arg,
    gz_sim,
    spawn_mirte_pioneer,
  ])