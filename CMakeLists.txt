cmake_minimum_required(VERSION 3.15)
project(mirte_gazebo)

set(CMAKE_CXX_STANDARD 20)
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(mirte_msgs REQUIRED)
find_package(std_srvs REQUIRED)

add_executable(convert_ir src/convert_ir.cpp)
ament_target_dependencies(convert_ir rclcpp std_msgs sensor_msgs mirte_msgs std_srvs)
install(TARGETS convert_ir
  DESTINATION lib/${PROJECT_NAME})

foreach(X IN ITEMS "config" "launch" "urdf" "media" "models" "worlds")
    install(DIRECTORY ${X}
      DESTINATION share/${PROJECT_NAME}/)
endforeach()

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
