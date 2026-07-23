# Use the official ROS 2 Humble base image with Gazebo Fortress pre-installed
FROM osrf/ros:humble-desktop-full

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install additional dependencies if needed
RUN apt-get update && apt-get install -y \
    ros-humble-gazebo-ros-pkgs \
    python3-vcstool \
    python3-rosdep \
    ignition-fortress \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directories
RUN mkdir -p /mirte_ws/src

# Copy dependencies.repos into the container
COPY dependencies.repos /mirte_ws/

# Use vcs to import and clone all packages
RUN vcs import /mirte_ws/src < /mirte_ws/dependencies.repos
RUN touch /mirte_ws/src/mirte-ros-packages/mirte_telemetrix_cpp/COLCON_IGNORE

# Initialize rosdep
# RUN rosdep update && apt update

# Source ROS 2 setup script, install dependencies, and build the workspace
WORKDIR /mirte_ws
# RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
#     rosdep install --from-paths src --ignore-src -r -y"

RUN ["/bin/bash", "-c", "source /opt/ros/humble/setup.bash \
    && apt update \
    && rosdep update \
    && rosdep install --from-paths src --ignore-src -r -y \
    && sudo rm -rf /var/lib/apt/lists/"]

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install"

# RUN rm -rf /var/lib/apt/lists/*

# Set the default entrypoint
ENTRYPOINT ["/bin/bash"]