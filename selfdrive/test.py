import zmq
from selfdrive.services import service_list
import selfdrive.messaging as messaging
context = zmq.Context()
thermal_sock = messaging.pub_sock(context, service_list['thermal'].port)

data = messaging.new_message()
data.init('phantomData')
data.phantomData.status = status
data.phantomData.speed = speed
data.phantomData.angle = angle
data.phantomData.time = time
self.phantomData_sock.send(data.to_bytes())