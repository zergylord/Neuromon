import sys

import rlglue.RLGlue as RLGlue
print "\n\nExperiment starting up!"
taskSpec = RLGlue.RL_init()
print "RL_init called, the environment sent task spec: " + taskSpec
#We could run one step at a time instead of one episode at a time */
#Start the episode */
startResponse = RLGlue.RL_start()

firstObservation = startResponse.o.intArray[0]
firstAction = startResponse.a.intArray[0]
print "First observation and action were: " + str(firstObservation) + " and: " + str(firstAction)

#Run one step */
stepResponse = RLGlue.RL_step()

#Run until the episode ends*/
while (stepResponse.terminal != 1):
    stepResponse = RLGlue.RL_step()

print "\n\n----------Summary----------"

totalSteps = RLGlue.RL_num_steps()
totalReward = RLGlue.RL_return()
print "It ran for " + str(totalSteps) + " steps, total reward was: " + str(totalReward)
RLGlue.RL_cleanup()



