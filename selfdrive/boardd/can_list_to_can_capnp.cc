#include <vector>
#include <tuple>
#include <string>
#include "common/timing.h"
#include <capnp/serialize.h>
#include "cereal/gen/cpp/log.capnp.h"
#include "cereal/gen/cpp/car.capnp.h"

typedef struct {
	long address;
	std::string dat;
	long busTime;
	long src;
} can_frame;

extern "C" {

void can_list_to_can_capnp_cpp(const std::vector<can_frame> &can_list, std::string &out, bool sendCan) {
  capnp::MallocMessageBuilder msg;
  cereal::Event::Builder event = msg.initRoot<cereal::Event>();
  event.setLogMonoTime(nanos_since_boot());

  auto canData = sendCan ? event.initSendcan(can_list.size()) : event.initCan(can_list.size());
<<<<<<< HEAD
  int i = 0;
  for (auto it = can_list.begin(); it != can_list.end(); it++, i++) {
    canData[i].setAddress(it->address);
    canData[i].setBusTime(it->busTime);
    canData[i].setDat(kj::arrayPtr((uint8_t*)it->dat.data(), it->dat.size()));
    canData[i].setSrc(it->src);
=======
  int j = 0;
  for (auto it = can_list.begin(); it != can_list.end(); it++, j++) {
    canData[j].setAddress(it->address);
    canData[j].setBusTime(it->busTime);
    canData[j].setDat(kj::arrayPtr((uint8_t*)it->dat.data(), it->dat.size()));
    canData[j].setSrc(it->src);
>>>>>>> 7d5332833b11570db288f35657a963ed0d8cad0a
  }
  auto words = capnp::messageToFlatArray(msg);
  auto bytes = words.asBytes();
  out.append((const char *)bytes.begin(), bytes.size());
}

}
