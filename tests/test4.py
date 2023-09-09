
import numpy as np
import matplotlib.pyplot as plt

frequencies=[1000,5000]
def calculate_beam_pattern(sound_speed, num_sensors, sensor_distance, angle_range):
    angular_range = np.radians(angle_range)
    theta = np.linspace(-angular_range/2, angular_range/2, 1000)
    wavelength = sound_speed / np.mean(frequencies)  # Assuming you have a list of frequencies
    
    steering_vector = np.exp(1j * 2 * np.pi * sensor_distance / wavelength * np.sin(theta))
    beam_pattern = np.abs(np.sum(steering_vector, axis=1))
    
    return theta, beam_pattern

# Parameters
sound_speed = 1500  # m/s
num_sensors = 8
sensor_distance = 0.5  # meters
angle_range = 90  # degrees

# Calculate beam pattern
theta, beam_pattern = calculate_beam_pattern(sound_speed, num_sensors, sensor_distance, angle_range)

# Plot beam pattern
plt.plot(np.degrees(theta), beam_pattern)
plt.title('Beam Pattern of Linear Sonar Array')
plt.xlabel('Angle (degrees)')
plt.ylabel('Beam Pattern Magnitude')
plt.grid(True)
plt.show()
