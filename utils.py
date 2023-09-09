import numpy as np

def beam_pattern(sound_speed = 1500,  # m/s
                num_sensors = 10,
                signal_frequency = 1000,  # Hz
                sensor_distance = 0.5):  # meters):
  lamda = sound_speed/signal_frequency
  angles = np.linspace(-np.pi/2, np.pi/2, 360)
  psy = np.pi*sensor_distance*np.sin(angles)/lamda
  D = abs(np.sin(num_sensors*psy)/(num_sensors*np.sin(psy)))
  return angles, D