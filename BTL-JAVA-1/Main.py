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

    # # in ra các sensor đã random
    # print("CAC SENSOR DA RANDOM LA: ")
    # program.printSensors(program.sensorList)
    # print("**************************************")

    # # in ra các sensor có thể giao tiếp với sensor trung tâm
    # print("CAC SENSOR CO THE GIAO TIEP VOI SENSOR TRUNG TAM")
    # if len(program.sinkSensor.nearSensors) != 0:
    #     program.printSensors(program.sinkSensor.nearSensors.keys())
    # print("======================================")

    # ##########################
    # print("CAC SENSOR VA DS SENSOR CO THE GIAO TIEP VOI NO")
    # for sensor in program.sensorList:
    #     print(f"STT: {sensor.index}\t(X,Y) = ({sensor.coordinate.x}, {sensor.coordinate.y})")
    #     if len(sensor.nearSensors) != 0:
    #         program.printSensors(sensor.nearSensors)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    for sensor in program.sensorList:
        if len(sensor.pathToSinkSensor) != 0:
            program.findShortestPath(sensor)
    
    for sensor in program.sensorList:
        program.printAllPathAvailable(sensor)
    ###########################

    # danh sách các sensor có đường đi tới sink sensor
    # dùng set thay vì list để loại bỏ các sensor trùng nhau
    colored_sensor = set()

    for sensor in program.sensorList:
        if len(sensor.pathToSinkSensor) != 0:
            for s in sensor.pathToSinkSensor.keys():
                for i in s:
                    colored_sensor.add(i)
    # danh sách các tọa độ x
    x_values = list()
    # danh sách các tọa độ y
    y_values = list()
    # danh sách các lable là số thứ tự của từng sensor
    labels = list()

    # vẽ sink sensor
    drawing_sink_sensor = plt.Circle((program.sinkSensor.coordinate.x, 
        program.sinkSensor.coordinate.y), sensor.radius, color=cmap(norm(0.7)))
    # vẽ danh sách các sensor
    drawing_circle_list = list()
    # duyệt lần lượt sensorList
    for sensor in program.sensorList:
        # nếu sensor có đường đi tới sink sensor
        # thì set màu cho sensor đó
        if sensor in colored_sensor:
            drawing_circle = plt.Circle((sensor.coordinate.x, sensor.coordinate.y), sensor.radius, color=cmap(norm(0.5)))
        # ngược lại màu mặc định
        else:
            drawing_circle = plt.Circle((sensor.coordinate.x, sensor.coordinate.y), sensor.radius, color=cmap(norm(0.3)))
        
        drawing_circle_list.append(drawing_circle)

        x_values.append(sensor.coordinate.x)
        y_values.append(sensor.coordinate.y)
        labels.append(sensor.index)

    # thêm tọa độ sink sensor vào danh sách tọa độ
    x_values.append(program.sinkSensor.coordinate.x)
    y_values.append(program.sinkSensor.coordinate.y)

    # danh sách các điểm để vẽ
    x_points = np.array(x_values)
    y_points = np.array(y_values)

    figure, axes = plt.subplots()
    axes.scatter(x_points, y_points)
    axes.set_aspect(1)

    
    for i in drawing_circle_list:
        # vẽ danh sách các sensor đã random
        axes.add_artist(i)

    # vẽ sink sensor
    axes.add_artist(drawing_sink_sensor)

    # vẽ các số thứ tự tương ứng
    for i, txt in enumerate(labels):
        axes.annotate(txt, (x_points[i], y_points[i]))

    # vẽ các điểm ứng với các tọa độ các sensor đã random không có đường nối
    plt.plot(x_points, y_points, "o")
    # set giá trị limit cho trục x và y
    plt.xlim([0, 100])
    plt.ylim([0, 100])
    plt.show()

    
    
    
    
    # print("CAC SENSOR VA DS SENSOR CO THE GIAO TIEP VOI NO")
    # for sensor in program.sensorList:
    #     print(f"STT: {sensor.index}\t(X,Y) = ({sensor.coordinate.x}, {sensor.coordinate.y})")
    #     if len(sensor.nearSensors) != 0:
    #         program.printSensors(sensor.nearSensors)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # for sensor in program.sensorList:
    #     if len(sensor.pathToSinkSensor) != 0:
    #         program.findShortestPath(sensor.pathToSinkSensor)
    
    # for sensor in program.sensorList:
    #     program.printAllPathAvailable(sensor)
