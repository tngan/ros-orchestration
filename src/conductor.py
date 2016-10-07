#!/usr/bin/env python

__version__ = '1.0.0'

from suite import Suite

# this is a very simple state conductor
class Conductor:

    state = None

    def __init__(self, cfg):
        self.state = Suite.getInitialState(cfg)
        self.history = []
        self.suite = Suite.parseFromYml(cfg)
        self.lock = False
        self.terminate = False

    def step_over(self):
        self.state = self.next_state()
        self.history.push(self.state)
        self.unlock()

    # TODO pending ... dangerous for retry action
    def roll_back(self):
        self.state = self.history.pop() if (len(self.history) > 0) else None
        self.unlock()

    # see if it is good to publish as a topic
    def get_state(self):
        return self.state

    # mainly for debug use and not recommend to be a topic
    def get_history(self):
        return self.history

    def lock(self):
        self.lock = True

    def unlock(self):
        self.lock = False
        # unlock only the task is being done
        if next_state() == None:
            self.terminate = True

    def is_lock(self):
        return self.lock

    def is_end(self):
        return self.terminate

    def next_state(self):
        return self.suite[self.state].next

    def get_kickstart_topic(self):
        state_info = self.suite[self.state]
        if state_info.has_key('kickstart_topic'):
            return state_info.kickstart_topic
        else:
            return self.state + '/kickstart'
