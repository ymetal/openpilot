import zmq
import math
import numpy as np

from common.realtime import sec_since_boot
from selfdrive.services import service_list
from selfdrive.swaglog import cloudlog
from selfdrive.controls.lib.lateral_mpc import libmpc_py
from selfdrive.controls.lib.drive_helpers import MPC_COST_LAT
from selfdrive.controls.lib.model_parser import ModelParser
import selfdrive.messaging as messaging

_DT_MPC = 0.05
_DT_HALF_MPC = 0.025

def calc_states_after_delay(states, v_ego, steer_angle, curvature_factor, steer_ratio, delay):
  states[0].x = v_ego * delay
  states[0].psi = v_ego * curvature_factor * math.radians(steer_angle) / steer_ratio * delay
  return states


class PathPlanner(object):
  def __init__(self, CP):
    self.MP = ModelParser()

    self.l_poly = [0., 0., 0., 0.]
    self.r_poly = [0., 0., 0., 0.]
    
    self.last_cloudlog_t = 0

    context = zmq.Context()
    self.latControl_sock = messaging.pub_sock(context, service_list['latControl'].port)
    self.plan = messaging.pub_sock(context, service_list['pathPlan'].port)
    self.livempc = messaging.pub_sock(context, service_list['liveMpc'].port)

    self.setup_mpc(CP.steerRateCost)
    self.invalid_counter = 0

  def setup_mpc(self, steer_rate_cost):
    self.libmpc = libmpc_py.libmpc
    self.libmpc.init(MPC_COST_LAT.PATH, MPC_COST_LAT.LANE, MPC_COST_LAT.HEADING, steer_rate_cost)

    self.mpc_solution = libmpc_py.ffi.new("log_t *")
    self.cur_state = libmpc_py.ffi.new("state_t *")
    self.cur_state[0].x = 0.0
    self.cur_state[0].y = 0.0
    self.cur_state[0].psi = 0.0
    self.cur_state[0].delta = 0.0
    self.mpc_angles = [0.0, 0.0, 0.0]
    self.mpc_times = [0.0, 0.0, 0.0]
    
    self.angle_steers_des = 0.0
    self.angle_steers_des_mpc = 0.0
    self.angle_steers_des_prev = 0.0
    self.angle_steers_des_time = 0.0

  def update(self, rcv_times, CP, VM, CS, md, live100, live_parameters):
    v_ego = CS.carState.vEgo
    angle_steers = CS.carState.steeringAngle
    active = live100.live100.active
    cur_time = sec_since_boot()

    angle_offset_average = live_parameters.liveParameters.angleOffsetAverage
    angle_offset_bias = live100.live100.angleModelBias + angle_offset_average

    self.MP.update(v_ego, md)

    VM.update_params(live_parameters.liveParameters.stiffnessFactor, live_parameters.liveParameters.steerRatio)
    curvature_factor = VM.curvature_factor(v_ego)

    l_poly = libmpc_py.ffi.new("double[4]", list(self.MP.l_poly))
    r_poly = libmpc_py.ffi.new("double[4]", list(self.MP.r_poly))
    p_poly = libmpc_py.ffi.new("double[4]", list(self.MP.p_poly))

    # account for actuation delay
    self.cur_state = calc_states_after_delay(self.cur_state, v_ego, angle_steers - angle_offset_average, curvature_factor, VM.sR, CP.steerActuatorDelay)
    self.angle_steers_des_prev = np.interp(cur_time, self.mpc_times, self.mpc_angles)

    # reset to current steer angle if not active or overriding
    if active:
      self.cur_state[0].delta = math.radians(self.angle_steers_des_prev - angle_offset_bias) / VM.sR
    else:
      rate_desired = 0.0
      self.cur_state[0].delta = math.radians(angle_steers - angle_offset_bias) / VM.sR

    v_ego_mpc = max(v_ego, 5.0)  # avoid mpc roughness due to low speed
    self.libmpc.run_mpc(self.cur_state, self.mpc_solution,
                        l_poly, r_poly, p_poly,
                        self.MP.l_prob, self.MP.r_prob, self.MP.p_prob, curvature_factor, v_ego_mpc, self.MP.lane_width)

    #  Check for infeasable MPC solution
    mpc_nans = np.any(np.isnan(list(self.mpc_solution[0].delta)))
    if not mpc_nans:
      self.mpc_angles = [self.angle_steers_des_prev,
                        float(math.degrees(self.mpc_solution[0].delta[1] * VM.sR) + angle_offset_bias),
                        float(math.degrees(self.mpc_solution[0].delta[2] * VM.sR) + angle_offset_bias)]

      self.mpc_times = [cur_time,
                        cur_time + _DT_HALF_MPC,
                        cur_time + _DT_HALF_MPC + _DT_MPC]

      self.angle_steers_des_mpc = self.mpc_angles[1]
      rate_desired = math.degrees(self.mpc_solution[0].rate[0] * VM.sR)
    else:
      self.libmpc.init(MPC_COST_LAT.PATH, MPC_COST_LAT.LANE, MPC_COST_LAT.HEADING, CP.steerRateCost)
      self.cur_state[0].delta = math.radians(angle_steers) / VM.sR

      if cur_time > self.last_cloudlog_t + 5.0:
        self.last_cloudlog_t = cur_time
        cloudlog.warning("Lateral mpc - nan: True")

    if self.mpc_solution[0].cost > 20000. or mpc_nans:   # TODO: find a better way to detect when MPC did not converge
      self.invalid_counter += 1
    else:
      self.invalid_counter = 0

    cur_time = sec_since_boot()
    model_dead = cur_time - rcv_times['model'] > 0.5
    plan_valid = self.invalid_counter < 2

    plan_send = messaging.new_message()
    plan_send.init('pathPlan')
    plan_send.pathPlan.laneWidth = float(self.MP.lane_width)
    plan_send.pathPlan.dPoly = [float(x) for x in self.MP.d_poly]
    plan_send.pathPlan.cPoly = [float(x) for x in self.MP.c_poly]
    plan_send.pathPlan.cProb = float(self.MP.c_prob)
    plan_send.pathPlan.lPoly = [float(x) for x in l_poly]
    plan_send.pathPlan.lProb = float(self.MP.l_prob)
    plan_send.pathPlan.rPoly = [float(x) for x in r_poly]
    plan_send.pathPlan.rProb = float(self.MP.r_prob)
    plan_send.pathPlan.angleSteers = float(self.angle_steers_des_mpc)
    plan_send.pathPlan.mpcAngles = map(float, self.mpc_angles)
    plan_send.pathPlan.mpcTimes = map(float, self.mpc_times)
    plan_send.pathPlan.rateSteers = float(rate_desired)
    plan_send.pathPlan.angleOffset = float(angle_offset_average)
    plan_send.pathPlan.valid = bool(plan_valid)
    plan_send.pathPlan.paramsValid = bool(live_parameters.liveParameters.valid)
    plan_send.pathPlan.modelValid = bool(not model_dead)

    self.plan.send(plan_send.to_bytes())

    dat = messaging.new_message()
    dat.init('liveMpc')
    dat.liveMpc.x = list(self.mpc_solution[0].x)
    dat.liveMpc.y = list(self.mpc_solution[0].y)
    dat.liveMpc.psi = list(self.mpc_solution[0].psi)
    dat.liveMpc.delta = list(self.mpc_solution[0].delta)
    dat.liveMpc.cost = self.mpc_solution[0].cost
    self.livempc.send(dat.to_bytes())
    
    dat2 = messaging.new_message()
    dat2.init('latControl')
    dat2.latControl.anglelater = math.degrees(list(self.mpc_solution[0].delta)[-1])
    self.latControl_sock.send(dat2.to_bytes())
    
    self.l_poly = l_poly
    self.r_poly = r_poly
