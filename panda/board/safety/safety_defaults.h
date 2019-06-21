void default_rx_hook(CAN_FIFOMailBox_TypeDef *to_push) {}

int default_ign_hook() {
  return -1; // use GPIO to determine ignition
}

// *** no output safety mode ***

static void nooutput_init(int16_t param) {
  controls_allowed = 0;
<<<<<<< HEAD
  #ifdef PANDA
    lline_relay_release();
  #endif
=======
>>>>>>> 7d5332833b11570db288f35657a963ed0d8cad0a
}

static int nooutput_tx_hook(CAN_FIFOMailBox_TypeDef *to_send) {
  return false;
}

static int nooutput_tx_lin_hook(int lin_num, uint8_t *data, int len) {
  return false;
}

static int nooutput_fwd_hook(int bus_num, CAN_FIFOMailBox_TypeDef *to_fwd) {
  return -1;
}

<<<<<<< HEAD
static int nooutput_relay_hook(int to_set) {
  return false;
}

=======
>>>>>>> 7d5332833b11570db288f35657a963ed0d8cad0a
const safety_hooks nooutput_hooks = {
  .init = nooutput_init,
  .rx = default_rx_hook,
  .tx = nooutput_tx_hook,
  .tx_lin = nooutput_tx_lin_hook,
  .ignition = default_ign_hook,
  .fwd = nooutput_fwd_hook,
<<<<<<< HEAD
  .relay = nooutput_relay_hook,
=======
>>>>>>> 7d5332833b11570db288f35657a963ed0d8cad0a
};

// *** all output safety mode ***

static void alloutput_init(int16_t param) {
  controls_allowed = 1;
<<<<<<< HEAD
  #ifdef PANDA
    lline_relay_release();
  #endif
=======
>>>>>>> 7d5332833b11570db288f35657a963ed0d8cad0a
}

static int alloutput_tx_hook(CAN_FIFOMailBox_TypeDef *to_send) {
  return true;
}

static int alloutput_tx_lin_hook(int lin_num, uint8_t *data, int len) {
  return true;
}

static int alloutput_fwd_hook(int bus_num, CAN_FIFOMailBox_TypeDef *to_fwd) {
  return -1;
}

<<<<<<< HEAD
static int alloutput_relay_hook(int to_set) {
  return true;
}

=======
>>>>>>> 7d5332833b11570db288f35657a963ed0d8cad0a
const safety_hooks alloutput_hooks = {
  .init = alloutput_init,
  .rx = default_rx_hook,
  .tx = alloutput_tx_hook,
  .tx_lin = alloutput_tx_lin_hook,
  .ignition = default_ign_hook,
  .fwd = alloutput_fwd_hook,
<<<<<<< HEAD
  .relay = alloutput_relay_hook,
=======
>>>>>>> 7d5332833b11570db288f35657a963ed0d8cad0a
};
