import selfdrive.messaging as messaging
from selfdrive.services import service_list
import zmq
import sys

import time
f = '%4i %%'
len_to_clear = len(f)+1
clear = '\x08'* len_to_clear
print 'Progress in percent:'+' '*(len_to_clear),
for i in range(123):
    print clear+f % (i*100//123),
    time.sleep(0.4)
raw_input('\nDone')

context = zmq.Context()
poller = zmq.Poller()
dynamic_follow_sock = messaging.sub_sock(context, service_list['dynamicFollowData'].port, conflate=True, poller=poller)
while True:
  dynData = messaging.recv_one(dynamic_follow_sock)
  if dynData is not None:
    #print("Gas: {}\nBrake: {}".format(dynData.dynamicFollowData.gas, dynData.dynamicFollowData.brake), end="\r")
    #sys.stdout.flush()
    pass
