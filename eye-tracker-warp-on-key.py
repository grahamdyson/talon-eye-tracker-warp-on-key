import logging

from talon import actions, app, Module, tracking_system, ui
from talon.track import tobii

class WarpOnKeyEyeTracker:
	def register(self):
		tracking_system.register("gaze", self._on_gaze);
		logging.info("WarpOnKeyEyeTracker: registered")

	def _on_gaze(self, frame: tobii.GazeFrame):
		if frame:
			self.lastGaze = frame.gaze

	def warp(self):
		pixel = _gaze_to_pixel(self.lastGaze) if self.lastGaze else ui.active_window().rect.center
		actions.mouse_move(pixel.x, pixel.y)

def _gaze_to_pixel(gaze):
	screen_rectangle = ui.main_screen().rect
	gaze_screen_offset = gaze * screen_rectangle.size
	return screen_rectangle.clamp(screen_rectangle.pos + gaze_screen_offset)

def on_ready():
	global warpOnKeyEyeTracker
	warpOnKeyEyeTracker = WarpOnKeyEyeTracker()
	warpOnKeyEyeTracker.register()

app.register("ready", on_ready)

mod = Module()

@mod.action_class
class EyeTrackerWarpOnkey:
	def warpEyeTracker():
		"'Warps' mouse to last gaze position or screen center"
		global warpOnKeyEyeTracker
		if warpOnKeyEyeTracker:
			warpOnKeyEyeTracker.warp()