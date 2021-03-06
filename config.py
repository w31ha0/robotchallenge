import brickpi

SensorPort = 0
interface = brickpi.Interface()
interface.initialize()
interface.sensorEnable(SensorPort, brickpi.SensorType.SENSOR_ULTRASONIC)

touchPort = [2, 3]

touchDetected = 0
test1 = 12

interface.sensorEnable(touchPort[0], brickpi.SensorType.SENSOR_TOUCH)
interface.sensorEnable(touchPort[1], brickpi.SensorType.SENSOR_TOUCH)

motors = [0, 1, 2]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])
interface.motorEnable(motors[2])

motorParams = interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = 6.0
motorParams.maxRotationSpeed = 12.0
motorParams.feedForwardGain = 255 / 20.0
motorParams.minPWM = 27.0
motorParams.pidParameters.minOutput = -255
motorParams.pidParameters.maxOutput = 255
motorParams.pidParameters.k_p = 500.0
motorParams.pidParameters.k_i = 300.0
motorParams.pidParameters.k_d = 15.0

interface.setMotorAngleControllerParameters(motors[0], motorParams)
interface.setMotorAngleControllerParameters(motors[1], motorParams)

motorParams_sonic = interface.MotorAngleControllerParameters()
motorParams_sonic.maxRotationAcceleration = 6.0
motorParams_sonic.maxRotationSpeed = 12.0
motorParams_sonic.feedForwardGain = 255 / 20.0
motorParams_sonic.minPWM = 27.0
motorParams_sonic.pidParameters.minOutput = -255
motorParams_sonic.pidParameters.maxOutput = 255
motorParams_sonic.pidParameters.k_p = 400.0
motorParams_sonic.pidParameters.k_i = 300.0
motorParams_sonic.pidParameters.k_d = 15.0
interface.setMotorAngleControllerParameters(motors[2], motorParams_sonic)

numberOfParticles = 100

initialPosition = (84.0, 30.0, 0.0, 1.0 / numberOfParticles)

mean_x = 0.0
# sd_x = 0.35728
sd_x = 1.0
mean_y = 0.0
#sd_y = 0.35178
sd_y = 0.45178
# sd_y = 0.1
mean_theta = 0.0
# sd_theta = 0.3
sd_theta = 2

mean_theta_g = 0.0
sd_theta_g = 2.5

sonarToCenter = 3.0

numberOfScans = 72
angleToRotateScans = 5.0
