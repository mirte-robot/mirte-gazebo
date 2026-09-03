# todos

PIoneer:
- [x] cmd vel, topic: /cmd_vel
- [ ] sensors
  - [ ] depth cam
  - [x] intensity: topic /mirte/intensity/{left,right}{,_digital}
  - [x] sonar: topic /mirte/distance/{left,right}, max dist not rep117 okay
    - [ ] doesnt work nicely when also having realsense depth cam
  - [ ] lidar 
- [ ] urdf config
- [ ] worlds
- [ ] state broadcasting

[21:29, 27-08-2026] Jasper van Brakel (TU): https://github.com/SuperJappie08/brum-ros-packages/blob/ed7a7d4a196393e2b5f34b5debc1f103ce9c9b1f/brum_description/urdf/brum.urdf.xacro#L58-L66 Joint state publisher example
[21:29, 27-08-2026] Jasper van Brakel (TU): (Dit is for Jazzy/GZ-sim Harmonic)
[21:30, 27-08-2026] Jasper van Brakel (TU): https://github.com/SuperJappie08/brum-ros-packages/blob/ed7a7d4a196393e2b5f34b5debc1f103ce9c9b1f/brum_description/urdf/wheels.urdf.xacro#L123-L132
[21:32, 27-08-2026] Jasper van Brakel (TU): https://github.com/gazebosim/gz-sim/blob/ign-gazebo6/src/systems/velocity_control/VelocityControl.hh
[21:32, 27-08-2026] Jasper van Brakel (TU): Is ook voor fortress
[21:33, 27-08-2026] Jasper van Brakel (TU): Stopt alleen niet vanzelf met rijden
[21:33, 27-08-2026] Jasper van Brakel (TU): wat een beetje hinderlijk is
[21:33, 27-08-2026] Jasper van Brakel (TU): je moet een 0 sturen
[21:33, 27-08-2026] Jasper van Brakel (TU): https://github.com/SuperJappie08/brum-ros-packages/blob/ed7a7d4a196393e2b5f34b5debc1f103ce9c9b1f/brum_description/urdf/wheels.urdf.xacro#L123-L132
maar met die andere plugin in deze, kan je odom faken
[21:34, 27-08-2026] Jasper van Brakel (TU): https://github.com/gazebosim/gz-sim/blob/ign-gazebo6/src/systems/odometry_publisher/OdometryPublisher.hh
Deze, ook available voor fortress
[21:36, 27-08-2026] Jasper van Brakel (TU): Dit is de GZ bridge voor die plugins https://github.com/SuperJappie08/brum-ros-gz/blob/e89728458b3f277c8f7843096dbe0072d156a88a/brum_gz/launch/spawn_brum.launch.xml#L76-L103
[21:37, 27-08-2026] Jasper van Brakel (TU): dit gebruikt GEEN ros2_control
[21:39, 27-08-2026] Jasper van Brakel (TU): Dit is de GZ bridge voor die plugins https://github.com/SuperJappie08/brum-ros-gz/blob/e89728458b3f277c8f7843096dbe0072d156a88a/brum_gz/launch/spawn_brum.launch.xml#L76-L103
Je moet wel een normale parameter bridge defineren in plaats van dit, de launch action/extension is pas vanaf Jazzy (of Iron)
[21:40, 27-08-2026] Jasper van Brakel (TU): Als je nog meer Gazebo hulp nodig hebt, laat je maar wetebn
[21:40, 27-08-2026] Jasper van Brakel (TU): Ik heb bekend in Gazebo Hell