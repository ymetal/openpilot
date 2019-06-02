import zmq
from selfdrive.services import service_list
import selfdrive.messaging as messaging
context = zmq.Context()
thermal_sock = messaging.pub_sock(context, service_list['thermal'].port)

data = messaging.new_message()
data.init('thermal')
data.thermal.remoteUpdate = True
thermal_sock.send(data.to_bytes())