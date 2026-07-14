# mirte-gazebo

This package provides the ROS2 package for the [MIRTE robot](https://mirte.org)
gazebo simulation. This includes the MIRTE Pioneer and the MIRTE Master.
Please read the [MIRTE documentation](https://docs.mirte.org/develop/doc/simulation/install_simulation.html) 
on how to use this simulation.

## Install

We assuem you have cloned this repository in your ROS2 workspace (eg. ~/ros_ws/src).

```sh
vcs import src/ < src/mirte-gazebo/sources.repos
rosdep install -y --from-paths src/ --ignore-src --rosdistro humble
colcon build --symlink-install
```

## License

This work is licensed under a Apache-2.0 OSS license.
