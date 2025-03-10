from common.numpy_fast import interp
from selfdrive.controls.lib.latcontrol_helpers import model_polyfit, calc_desired_path, compute_path_pinv
import selfdrive.kegman_conf as kegman
import numpy as np

CAMERA_OFFSET = float(kegman.conf['cameraOffset'])  # m from center car to camera


class ModelParser(object):
  def __init__(self):
    self.lane_width_array = np.zeros(50)
    self.lane_width_array_counter = 0
    self.fullarray = False
    self.d_poly = [0., 0., 0., 0.]
    self.c_poly = [0., 0., 0., 0.]
    self.r_poly = [0., 0., 0., 0.]
    self.l_poly = [0., 0., 0., 0.]
    self.c_prob = 0.
    self.last_model = 0.
    self.lead_dist, self.lead_prob, self.lead_var = 0, 0, 1
    self._path_pinv = compute_path_pinv()

    self.lane_width_estimate = 2.85
    self.lane_width_certainty = 1.0
    self.lane_width = 2.85
    self.l_prob = 0.
    self.r_prob = 0.

  def update(self, v_ego, md):
    if md is not None:
      p_poly = model_polyfit(md.model.path.points, self._path_pinv)  # predicted path
      l_poly = model_polyfit(md.model.leftLane.points, self._path_pinv)  # left line
      r_poly = model_polyfit(md.model.rightLane.points, self._path_pinv)  # right line

      # only offset left and right lane lines; offsetting p_poly does not make sense
      l_poly[3] += CAMERA_OFFSET
      r_poly[3] += CAMERA_OFFSET

      p_prob = 1.  # model does not tell this probability yet, so set to 1 for now
      l_prob = md.model.leftLane.prob  # left line prob
      r_prob = md.model.rightLane.prob  # right line prob

      # Find current lanewidth
      lr_prob = l_prob * r_prob
      self.lane_width_certainty += 0.05 * (lr_prob - self.lane_width_certainty)
      current_lane_width = abs(l_poly[3] - r_poly[3])
      self.lane_width_array[self.lane_width_array_counter] = current_lane_width
      self.lane_width_array_counter = (self.lane_width_array_counter + 1 ) % 50
      if self.lane_width_array_counter == 0 and self.fullarray == False:
        self.fullarray = True
      self.lane_width_estimate += 0.005 * (current_lane_width - self.lane_width_estimate)
      speed_lane_width = interp(v_ego, [0., 14., 20.], [2.5, 3., 3.5]) # German Standards
      self.lane_width = self.lane_width_certainty * self.lane_width_estimate + \
                        (1 - self.lane_width_certainty) * speed_lane_width
      if self.fullarray:
        lane_width_diff = abs(np.mean(self.lane_width_array) - current_lane_width)
        if abs(self.lane_width - current_lane_width) > lane_width_diff:
          lane_width_diff = abs(self.lane_width - current_lane_width)
      else:
        lane_width_diff = abs(self.lane_width - current_lane_width)
      lane_prob = interp(lane_width_diff, [0.3, 1.0], [1.0, 0.0])

      if abs(self.r_poly[3] - self.c_poly[3]) - abs(self.l_poly[3] - self.c_poly[3]) > 0.3 and \
         abs(self.r_poly[3] - r_poly[3]) > abs(self.l_poly[3] - l_poly[3]):
        r_prob *= lane_prob
      elif abs(self.l_poly[3] - self.c_poly[3]) - abs(self.r_poly[3] - self.c_poly[3]) > 0.3 and \
         abs(self.l_poly[3] - l_poly[3]) > abs(self.r_poly[3] - r_poly[3]):
        l_prob *= lane_prob      

      self.lead_dist = md.model.lead.dist
      self.lead_prob = md.model.lead.prob
      self.lead_var = md.model.lead.std**2

      # compute target path
      self.d_poly, self.c_poly, self.c_prob = calc_desired_path(
        l_poly, r_poly, p_poly, l_prob, r_prob, p_prob, v_ego, self.lane_width)

      self.r_poly = r_poly
      self.r_prob = r_prob

      self.l_poly = l_poly
      self.l_prob = l_prob

      self.p_poly = p_poly
      self.p_prob = p_prob
