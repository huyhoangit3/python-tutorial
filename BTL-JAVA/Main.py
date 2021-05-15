from Program import Program, Sensor
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize

if __name__ == "__main__":
    # fill color in Circle
    cmap = cm.jet   # Select colormap U want
    # Declare for set range of value for normalization
    vmin = 0        
    vmax = 1
    # Normalize value for cmap
    norm = Normalize(vmin, vmax)

    # số lượng sensor
    n = 20
    program = Program(n)
    # khởi tạo sink sensor
    sinkSensor = Sensor()
    sinkSensor.coordinate.x = 50
    sinkSensor.coordinate.y = 50

    # in ra các sensor đã random
    print("CAC SENSOR DA RANDOM LA: ")
    program.printSensors(program.sensorList)
    print("**************************************")

    # in ra các sensor có thể giao tiếp với sensor trung tâm
    print("CAC SENSOR CO THE GIAO TIEP VOI SENSOR TRUNG TAM")
    nearSinkSensors = program.findNearSensor(sinkSensor)
    if len(nearSinkSensors) != 0:
        program.printSensors(nearSinkSensors.keys())
    print("======================================")

    for i in range(n):
        program.findPaths(sinkSensor, program.sensorList[i])
    colored_sensor = set()
    for sensor in program.sensorList:
        if len(sensor.pathToSinkSensor) != 0:
            for s in sensor.pathToSinkSensor.keys():
                for i in s:
                    colored_sensor.add(i)

    print(len(colored_sensor))
    x_values = list()
    y_values = list()
    labels = list()
    Drawing_sink_sensor = plt.Circle((sinkSensor.coordinate.x, sinkSensor.coordinate.y), sensor.radius, color=cmap(norm(0.7)))
    Drawing_uncolored_circle_list = list()
    for sensor in program.sensorList:
        if sensor in colored_sensor:
            Drawing_uncolored_circle = plt.Circle((sensor.coordinate.x, sensor.coordinate.y), sensor.radius, color=cmap(norm(0.5)))
        else:
            Drawing_uncolored_circle = plt.Circle((sensor.coordinate.x, sensor.coordinate.y), sensor.radius)
        Drawing_uncolored_circle_list.append(Drawing_uncolored_circle)
        x_values.append(sensor.coordinate.x)
        y_values.append(sensor.coordinate.y)
        labels.append(sensor.index)

    x_values.append(sinkSensor.coordinate.x)
    y_values.append(sinkSensor.coordinate.y)

    x_points = np.array(x_values)
    y_points = np.array(y_values)

    figure, axes = plt.subplots()
    axes.scatter(x_points, y_points)
    axes.set_aspect(1)
    axes.add_artist(Drawing_sink_sensor)
    for i in Drawing_uncolored_circle_list:
        axes.add_artist(i)

    for i, txt in enumerate(labels):
        axes.annotate(txt, (x_points[i], y_points[i]))

    plt.plot(x_points, y_points, ".")
    plt.xlim([0, 100])
    plt.ylim([0, 100])
    plt.show()

    
    
    
    #
    # print("CAC SENSOR VA DS SENSOR CO THE GIAO TIEP VOI NO")
    # for sensor in program.sensorList:
    #     print(f"STT: {sensor.index}\t(X,Y) = ({sensor.coordinate.x}, {sensor.coordinate.y})")
    #     if len(sensor.nearSensors) != 0:
    #         program.printSensors(sensor.nearSensors)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # for i in range(n):
    #     program.findPaths(sinkSensor, program.sensorList[i])
    # for sensor in program.sensorList:
    #     if len(sensor.pathToSinkSensor) != 0:
    #         sensor.shortestPath = program.findShortestPath(sensor.pathToSinkSensor)
    #
    # for sensor in program.sensorList:
    #     program.printAllPathAvailable(sensor)
