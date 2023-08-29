## dependencies:

Requires ```mirte-ros-packages```, change ```mirte_teleop/launch/teleopkey.lauch```:
```/mobile_base_controller/cmd_vel``` to ```/mirte/base_controller/cmd_vel```

Requires ros-control packages:
```apt install ros-noetic-ros-control ros-noetic-ros-controllers```
## running:

```sh
roslaunch mirte_gazebo gazebo_all.launch
```

Controlling the Mirte:
```sh
roslaunch mirte_teleop teleopkey.launch
```

Change world by changing the `duckietown` argument in `launch/gazebo_duckietown_world.launch` to any map in the maps folder.

The map file is converted to `urdf/generated.world` by `scripts/buildMap.py` and converted to `worlds/generated.world` by xacro before launching Gazebo.


## Format
Format xml (.launch, .xacro and .world) by running 
```sh
./scripts/xmlformat.sh # uses xmllint
```
and Python files:
```sh
./scripts/pythonformat.sh # uses black
```
and yaml files:
```sh
./scripts/yamlformat.sh # uses yamlfmt
```