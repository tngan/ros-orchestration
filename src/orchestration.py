#!/usr/bin/env python
__version__ = '1.0.0'

from conductor import Conductor
import rospy
import yaml
import os

from ros_orchestration.srv import *

def orchestration_controller_node():

    # initiate a ros node
    rospy.init_node('orchestration_controller_node', anonymous=True)

    # get ros parameters from launch file
    suite_config = rospy.get_param('~suite', 'default.yml')
    node_rate = rospy.get_param('~rate', 50.0)
    step_over_srv_name = rospy.get_param('~step_over_srv_name', '/step_over')
    roll_back_srv_name = rospy.get_param('~roll_back_srv_name', '/roll_back')

    # load the suite
    suite = yaml.load(open(suite_config))

    # configure a state conductor with the yaml file
    conductor = Conductor(suite)

    # configure the rate
    rate = rospy.Rate(node_rate)

    # configure the service server # currying
    step_over_srv = rospy.Service(step_over_srv_name, StepOver, conductor.step_over)
    roll_back_srv = rospy.Service(roll_back_srv_name, RollBack, conductor.roll_back)

    # main loop
    while not rospy.is_shutdown():
        # kickstart the orchestration node with current state
        # terminate when the suite is played successfully
        # TODO timeout may need to make the conductor more reliable
        # TODO the services should shutdown itself after issuing the service request to step_over

        if conductor.is_end():
            break

        # only execute if lock is open
        if conductor.is_lock():
            print("conductor is locked")
        else:
            # only kickstart to a new one without lock (waiting for new state)
            kickstart = rospy.ServiceProxy(conductor.get_kickstart_topic(), KickstartNode)
            try:
                response = kickstart()
                # this lock will be unlock until the step_over call from orchestration node is made
                conductor.lock()
            except rospy.ServiceException as exc:
                print("service did not process request: " + str(exc))

        # some logger here
        rate.sleep()

if __name__ == "__main__":
    try:
        orchestration_controller_node()
    except rospy.ROSInterruptException:
        pass
