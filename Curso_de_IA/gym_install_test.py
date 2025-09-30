# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 19:25:00 2018

@author: Pinotronic
"""

import gym

environment = gym.make("MountainCar-v0")

environment.reset()
for _ in range(2000):
    environment.render()
    environment.step(environment.action_space.sample())
    
    
