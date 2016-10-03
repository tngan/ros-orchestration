cmake_minimum_required(VERSION 2.8.3)
project(bailey_flow)

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
  bailey_controller/machine.py
  bailey_controller/bailey_controller_node.py
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/bailey_controller
)
install(FILES
  bailey_controller/bailey_controller.launch
  recipes/*.yml
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/bailey_controller
)
