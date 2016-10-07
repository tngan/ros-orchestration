#!/usr/bin/env python
__version__ = '1.0.0'

from machine import Machine
import rospy
import yaml
import os

from bailey_flow.srv import *

def bailey_controller_node():

    # initiate a ros node
    rospy.init_node('bailey_controller_node', anonymous=True)

    # get ros parameters from launch file
    recipe_config = rospy.get_param('~recipe', 'default.yml')
    node_rate = rospy.get_param('~rate', 50.0)
    step_over_srv_name = rospy.get_param('~step_over_srv_name', '/step_over')
    roll_back_srv_name = rospy.get_param('~roll_back_srv_name', '/roll_back')

    # load the recipe
    recipe = yaml.load(open(recipe_config))

    # configure a state machine with the yaml file
    machine = Machine(recipe)

    # configure the rate
    rate = rospy.Rate(node_rate)

    # configure the service server # currying
    step_over_srv = rospy.Service(step_over_srv_name, StepOver, machine.step_over)
    roll_back_srv = rospy.Service(roll_back_srv_name, RollBack, machine.roll_back)

    # main loop
    while not rospy.is_shutdown():
        # kickstart the bailey node with current state
        # terminate when the recipe is played successfully
        # TODO timeout may need to make the machine more reliable
        # TODO the services should shutdown itself after issuing the service request to step_over

        if machine.is_end():
            break

        # only execute if lock is open
        if machine.is_lock():
            print("machine is locked")
        else:
            # only kickstart to a new one without lock (waiting for new state)
            kickstart = rospy.ServiceProxy(machine.get_kickstart_topic(), KickstartNode)
            try:
                response = kickstart()
                # this lock will be unlock until the step_over call from bailey node is made
                machine.lock()
            except rospy.ServiceException as exc:
                print("service did not process request: " + str(exc))

        # some logger here
        rate.sleep()

if __name__ == "__main__":
    try:
        bailey_controller_node()
    except rospy.ROSInterruptException:
        pass
