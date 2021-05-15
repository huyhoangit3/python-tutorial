from Point import Point
from collections import OrderedDict


class Sensor:
    def __init__(self):
        # số thứ tự của sensor
        self.index = -1
        # bán kính của sensor
        self.radius = 10
        # tọa độ Oxy của sensor
        self.coordinate = Point()
        # danh sách các sensor gần nó và khoảng cách giữa chúng
        self.nearSensors = OrderedDict()
        # trạng thái duyệt của sensor
        self.isVisited = False
        # danh sách các đường đi và chi phí của nó
        self.pathToSinkSensor = OrderedDict()
        # đường đi ngắn nhất từ sink sensor đến mỗi sensor
        self.shortestPath = tuple()

    # override equal method
    def __eq__(self, other):
        return isinstance(other, Sensor) and self.coordinate == other.coordinate

    # make Sensor object hashable
    def __hash__(self):
        return hash((self.index,self.coordinate))
