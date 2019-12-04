#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a trial loop Step 2
Use this template to turn Step 1 into a loop
@author: katherineduncan
"""
#%%
#In the task, there are 8 trials. To begin a trial, press the space bar. After a
#short delay, a face will be shown. After another brief delay, a second face will
#be shown. If the second face is the same as the first, press 1. If different,
#press 0. Once you submit your response to the second image, the screen will go 
#blank and you can begin the next trial by pressing the space bar. Once you 
#complete the last trial, the program will close automatically. The script outputs
#a 'test_data' text file that contains the correct answer to each trial, and the 
#participant's response in separate columns. 

#%%
import numpy as np
import pandas as pd
import os, sys
import random
from psychopy import visual, core, event

#Initialize answer and response arrays
correct_answer = []
response = []
accuracy = []
rt = []

#Initialize stim lists
target = list(range(1,9))
probe = list(range(1,9))
np.random.shuffle(target)
np.random.shuffle(probe)

# Determine correct answers 
for i in range(len(target)):
    if target[i] == probe[i]:
        correct_answer.append(1)
    else:
        correct_answer.append(0)

# Set durations
iti = 0.5 #Pre-trial fixation
t_dur = 0.5 #Target stimulus presentation duration
isi = 3.0 #Maintenance period delay
f_dur = 1.0 #Duration of feedback screen
e_dur = 1.0 #Duration following subject response and beginning of new trial

#%%Task Procedure

#Open new window
win = visual.Window(fullscr=True, 
        allowGUI=True, 
        color='white', 
        unit='height'
        ) 

for x in range(len(target)):
    # Pre-trial fixation
    fixation = visual.GratingStim(win=win, 
                              size=0.01, 
                              pos=[0,0], 
                              sf=0, 
                              rgb='black')
    fixation.draw()
    event.Mouse(visible=False)
    
    keys = event.waitKeys(keyList =['space']) # Wait for space bar press to begin trial

    win.flip()
    
    clock = core.Clock()
    while clock.getTime() < iti:
        core.wait(0.001)
    
    #%%Present target face image
    temp = target[x]
    file = '/Users/jmsaito/Documents/GitHub/trialloops-jmsaito25/faces/face' + str(temp) + '.jpg'
    current_face = visual.ImageStim(win, image=file, pos=(0,0))

    current_face.draw()
    event.Mouse(visible=False)
    win.flip()
    
    clock.reset()
    while clock.getTime() < t_dur:
        current_face.draw()
        win.flip()

    #%%Delay Period
    
    fixation.draw()
    event.Mouse(visible=False)
    
    win.flip()

    clock.reset()
    while clock.getTime() < isi:
        fixation.draw()
        win.flip()
        
    #%%Present probe face
    temp2 = probe[x]
    file = '/Users/jmsaito/Documents/GitHub/trialloops-jmsaito25/faces/face' + str(temp2) + '.jpg'
    current_face = visual.ImageStim(win, image=file, pos=(0,0))

    current_face.draw()
    event.Mouse(visible=False)
    win.flip()

    #Gather participant same/different response & RT
    clock.reset()
    keys = event.waitKeys(keyList =['1','0'], timeStamped=clock)

    #%%Feedback period
    c_text = visual.TextStim(win=win, text="Correct!", color = 'black', pos = (0, 0))
    ic_text = visual.TextStim(win=win, text="Incorrect.", color = 'black', pos = (0, 0))
    
    temp_key = int(keys[0][0])
    temp_RT = keys[0][1]
    
    if temp_key==correct_answer[x]:
        response.append(temp_key) # Record response
        accuracy.append(1) #Record accuracy
        rt.append(temp_RT) #Record RT
        c_text.draw() #Write feedback
        print('accuracy: ',np.mean(accuracy),'\n'
              'rt: ',np.mean(rt))
    else:
        response.append(temp_key)# Record response
        accuracy.append(0)#Record accuracy
        rt.append(temp_RT)#Record RT
        ic_text.draw() #Write feedback
        print('accuracy: ',np.mean(accuracy),'\n'
              'rt: ',np.mean(rt))
    
    win.flip()
    clock.reset()
    while clock.getTime() < f_dur:
        core.wait(0.001)

    win.flip()
    
#%% Close window and end experiment
win.close()
    
#%% Save participant data

data = pd.DataFrame({'answer':correct_answer,
                     'response':response,
                     'accuracy':accuracy,
                     'rt':rt})
data.to_csv('test_data.csv')