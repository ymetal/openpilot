import selfdrive.messaging as messaging
from selfdrive.services import service_list
import zmq

def start():
  context = zmq.Context()
  while True:
    dynamic_follow_sock = messaging.sub_sock(context, service_list['dynamicFollowData'].port, conflate=True)