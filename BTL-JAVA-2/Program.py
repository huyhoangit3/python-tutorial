from Sensor import Sensor, OrderedDict
import random
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize


class Program:
    # hàm tạo
    def __init__(self, length, width, mode):
        self.length = length
        self.width = width
        self.mode = mode
        # danh sách sensor
        self.sensor_list = list()
        # khởi tạo sink sensor
        self.sink_sensor = Sensor()
        self.sink_sensor.coordinate.x = self.length // 2
        self.sink_sensor.coordinate.y = self.width // 2
    

    # hàm đọc file
    def read_file(self, file_path):
        file = open(file_path, 'r')
        line_number = 0
        while True:
            line = file.readline()
            if line_number == 0:
                line_number += 1
                continue
            if not line:
                break
            line = line.rstrip('\n')
            result = line.split(',')
            result = [int(x) for x in result]
            sensor = Sensor()
            sensor.coordinate.x = result[0]
            sensor.coordinate.y = result[1]
            sensor.index = result[2]
            self.sink_sensor.radius = sensor.radius = result[3]
            self.sensor_list.append(sensor)
        file.close()

    # hàm load data cho từng sensor
    def load_data(self):
        # tìm danh sách các sensor gần sensor trung tâm
        self.find_near_sensor(self.sink_sensor)
        
        for sensor in self.sensor_list:
            # tìm danh sách các sensor gần mỗi sensor 
            self.find_near_sensor(sensor) 

        for sensor in self.sensor_list:
            # tìm danh sách đường đi tới sink sensor và chi phí của chúng nếu có
            self.find_paths(self.sink_sensor, sensor)
            # tìm đường đi ngắn nhất từ sink sensor đến mỗi sensor (nếu có)
            self.find_shortest_path(sensor)
        

    # phương thức tìm danh sách các sensor ở gần mỗi sensor
    def find_near_sensor(self, source):
        # duyệt lần lượt từng sensor trong sensor_list
        for sensor in self.sensor_list:
            # tính khoảng cách giữa 2 sensor
            length = sensor.distance_to_sensor(source)
            # thêm vào danh sách các sensor ở gần nếu khoảng cách <= 2 * radius
            if length != 0 and length <= 2 * sensor.radius:
                # key: sensor ở gần
                # value: khoảng cách giữa chúng
                source.near_sensors[sensor] = length

    # tìm đường đi từ sensor source đến sensor destination
    def find_paths(self, source, destination):
        # khởi tạo chi phí ban đầu là 0
        cost = 0
        # khởi tạo danh sách các sensor tạo thành đường đi
        path_list = list()
        # thêm sensor source vào danh sách các sensor tạo thành đường đi
        path_list.append(source)
        self.find_path_until(source, destination, path_list, cost)

    # hàm đệ quy
    def find_path_until(self, source, destination, local_path_list, cost):
        # nếu sensor source bằng sensor destination
        if source == destination:
            # key: danh sách các sensor tạo thành đường đi
            lst = tuple(local_path_list)
            # value: chi phí của đường đi này
            source.path_to_sinksensor[lst] = cost
            return

        source.is_visited = True
        # nếu sensor hiện tại có danh sách các senssor gần nó
        if len(source.near_sensors) != 0:
            # duyệt dictionary chứa danh sách đường đi
            # sensor: danh sách đường đi
            # lenght: chi phí đường đi đó
            for sensor, length in source.near_sensors.items():
                # nếu sensor chưa được duyệt
                if not sensor.is_visited:
                    # cộng thêm chi phí đường đi
                    cost += length
                    # thêm sensor vào localPathList
                    local_path_list.append(sensor)
                    # tiếp tục tìm đến khi gặp sensor đích hoặc không tồn tại đường đi giữa 2 sensor
                    self.find_path_until(sensor, destination, local_path_list, cost)
                    # xóa sensor khỏi localPathList
                    local_path_list.remove(sensor)
                    cost -= length


        source.is_visited = False

    # tìm đường đi ngắn nhất
    def find_shortest_path(self, source):
        # lấy ra giá trị lớn nhất của kiểu floating point number
        min_cost = sys.float_info.max

        # duyệt key và value trong dictionary pathList
        if len(source.path_to_sinksensor) != 0:
            for key, value in source.path_to_sinksensor.items():
                if value < min_cost:
                    min_cost = value
                    # deep copy
                    source.shortest_path = list(key)


    def simulate2(self, xlim, ylim):
        # fill color in Circle
        cmap = cm.jet   # Select colormap U want
        # Declare for set range of value for normalization
        vmin = 0 
        vmax = 1
        # Normalize value for cmap
        norm = Normalize(vmin, vmax)

        # danh sách các tọa độ x
        x_values = list()
        # danh sách các tọa độ y
        y_values = list()
        # danh sách các lable là số thứ tự của từng sensor
        labels = list()

        # vẽ sink sensor
        drawing_sink_sensor = plt.Circle((self.sink_sensor.coordinate.x, 
            self.sink_sensor.coordinate.y), self.sink_sensor.radius, color=cmap(norm(0.7)))
        # vẽ danh sách các sensor
        drawing_circle_list = list()

        list_len = len(self.sensor_list)
        for i in range(list_len):
            sensor = self.sensor_list[i]
            # nếu sensor có đường đi tới sink sensor
            # thì set màu cho sensor đó
            if i <= list_len // 2 - 1:
                drawing_circle = plt.Circle((sensor.coordinate.x, sensor.coordinate.y), sensor.radius, color=cmap(norm(0.5)))
            else:
                drawing_circle = plt.Circle((sensor.coordinate.x, sensor.coordinate.y), sensor.radius, color=cmap(norm(0.3)))
            
            drawing_circle_list.append(drawing_circle)

            x_values.append(sensor.coordinate.x)
            y_values.append(sensor.coordinate.y)
            labels.append(sensor.index)

        # thêm tọa độ sink sensor vào danh sách tọa độ
        x_values.append(self.sink_sensor.coordinate.x)
        y_values.append(self.sink_sensor.coordinate.y)

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
        plt.xlim([0, xlim])
        plt.ylim([0, ylim])
        plt.show()


    def simulate1(self, xlim, ylim):
        # fill color in Circle
        cmap = cm.jet   # Select colormap U want
        # Declare for set range of value for normalization
        vmin = 0 
        vmax = 1
        # Normalize value for cmap
        norm = Normalize(vmin, vmax)

        # danh sách các sensor có đường đi tới sink sensor
        # dùng set thay vì list để loại bỏ các sensor trùng nhau
        colored_sensor = set()

        for sensor in self.sensor_list:
            if len(sensor.path_to_sinksensor) != 0:
                for s in sensor.path_to_sinksensor.keys():
                    for i in s:
                        colored_sensor.add(i)
        # danh sách các tọa độ x
        x_values = list()
        # danh sách các tọa độ y
        y_values = list()
        # danh sách các lable là số thứ tự của từng sensor
        labels = list()

        # vẽ sink sensor
        drawing_sink_sensor = plt.Circle((self.sink_sensor.coordinate.x, 
            self.sink_sensor.coordinate.y), self.sink_sensor.radius, color=cmap(norm(0.7)))
        # vẽ danh sách các sensor
        drawing_circle_list = list()

        for sensor in self.sensor_list:
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
        x_values.append(self.sink_sensor.coordinate.x)
        y_values.append(self.sink_sensor.coordinate.y)

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
        plt.xlim([0, xlim])
        plt.ylim([0, ylim])
        plt.show()
