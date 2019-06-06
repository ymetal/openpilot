import selfdrive.messaging as messaging
from selfdrive.services import service_list
import zmq

def start():
  context = zmq.Context()
  poller = zmq.Poller()
  dynamic_follow_sock = messaging.sub_sock(context, service_list['dynamicFollowData'].port, conflate=True, poller=poller)
  while True:
    dynData = messaging.recv_one(dynamic_follow_sock)
    if dynData is not None:
      print("Gas: {}".format(dynData.dynamicFollowData.gas))
      print("Brake: {}".format(dynData.dynamicFollowData.brake))