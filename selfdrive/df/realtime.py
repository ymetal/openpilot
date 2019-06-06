from __future__ import print_function
import selfdrive.messaging as messaging
from selfdrive.services import service_list
import zmq

context = zmq.Context()
poller = zmq.Poller()
dynamic_follow_sock = messaging.sub_sock(context, service_list['dynamicFollowData'].port, conflate=True, poller=poller)
while True:
  dynData = messaging.recv_one(dynamic_follow_sock)
  if dynData is not None:
    print("Gas: {}\nBrake: {}".format(dynData.dynamicFollowData.gas, dynData.dynamicFollowData.brake), end="\r")
