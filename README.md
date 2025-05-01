# Installation

The simulation will not run on the MIRTE robot, but on your own machine.
We assume you have ros-humble-base installed. To get the simulation up and
running you need to install a couple of packages:

```sh
# In your ROS2 workspace (eg ~/ros2_ws/)
vcs import src/ < src/mirte-gazebo/sources.repos
cd src/mirte_ros_packages
shopt -s extglob
rm -rf !("mirte_msgs"|"mirte_control"|"mirte_description"|"mirte_moveit_config")
cd ../..
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

# MIRTE master examples

```sh
ros2 launch mirte_gazebo gazebo_mirte_master_empty.launch.xml
```

The following sequence of commands will let you pick up a cylinder, drive it somewhere else, and place it.

Spawn a cylinder:
```sh
ros2 run gazebo_ros spawn_entity.py -file $(pwd)/src/mirte-gazebo/urdf/cylinder.sdf -entity cylinder -x 1.39 -y .51
```

Gripper close:
```sh
ros2 action send_goal /mirte_master_gripper_controller/gripper_cmd control_msgs/action/GripperCommand "{command: {position: 0.1}}"
```

Arm up:
```sh
ros2 topic pub --once /mirte_master_arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{joint_names: ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_joint'], points: [{positions: [0.0, 0.0, -1.56, 1.56], time_from_start:{ sec: 3, nanosec: 0}}]}"
```

Driving around:
```sh
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/mirte_base_controller/cmd_vel_unstamped
```

Arm down:
```sh
ros2 topic pub --once /mirte_master_arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{joint_names: ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_joint'], points: [{positions: [0.0, -1.56, -1.56, 1.56], time_from_start:{ sec: 3, nanosec: 0}}]}"
```

Gripper open:
```sh
ros2 action send_goal /mirte_master_gripper_controller/gripper_cmd control_msgs/action/GripperCommand "{command: {position: -0.1}}"
```




