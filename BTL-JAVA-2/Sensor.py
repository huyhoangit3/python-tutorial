from Point import Point
from collections import OrderedDict
import math


class Sensor:
    def __init__(self):
        # số thứ tự của sensor
        self.index = -1
        # bán kính của sensor
        self.radius = 0
        # tọa độ Oxy của sensor
        self.coordinate = Point()
        # danh sách các sensor gần nó và khoảng cách giữa chúng
        self.near_sensors = OrderedDict()
        # trạng thái duyệt của sensor
        self.is_visited = False
        # danh sách các đường đi và chi phí của nó
        self.path_to_sinksensor = OrderedDict()
        # đường đi ngắn nhất từ sink sensor đến mỗi sensor
        self.shortest_path = list()

    # override equal method
    def __eq__(self, other):
        return isinstance(other, Sensor) and self.coordinate == other.coordinate

    # make Sensor object hashable
    def __hash__(self):
        return hash((self.index,self.coordinate))
    # 
    def distance_to_sensor(self, other):
        return math.sqrt(pow(self.coordinate.x - other.coordinate.x, 2) +
                                       pow(self.coordinate.y - other.coordinate.y, 2))

