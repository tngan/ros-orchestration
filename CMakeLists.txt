cmake_minimum_required(VERSION 2.8.3)
project(ros_orchestration)

find_package(catkin REQUIRED COMPONENTS
  rospy
  message_generation
  std_msgs
)

add_message_files(DIRECTORY msg FILES)
add_service_files(DIRECTORY srv FILES KickstartNode.srv RollBack.srv StepOver.srv)

generate_messages(DEPENDENCIES std_msgs)

catkin_package(CATKIN_DEPENDS message_runtime std_msgs)

catkin_install_python(PROGRAMS
  src/conductor.py
  src/suite.py
  src/orchestration.py
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/orchestration
)
install(FILES
  src/orchestration.launch
  suites/*.yml
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/orchestration
)
