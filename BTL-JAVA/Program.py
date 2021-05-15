from Sensor import Sensor, OrderedDict
import random
import math
import sys


class Program:
    # hàm tạo
    def __init__(self, n):
        pos = 1
        # số lượng sensor
        self.quantity = n
        # danh sách sensor
        self.sensorList = list()
        # random các sensor
        while pos <= n:
            # khởi tạo 1 sensor
            sensor = Sensor()
            # random tọa độ  x và y
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            # gán số thứ tự cho mỗi sensor
            sensor.index = pos
            # gán tọa độ cho mỗi sensor
            sensor.coordinate.x = x
            sensor.coordinate.y = y

            # nếu sensor không trùng với bất kì sensor nào trong sensorList và 
            # không trùng với sink sensor
            if sensor not in self.sensorList and x != 50 and y != 50:
                self.sensorList.append(sensor)
                pos += 1

        
        for i in range(n):
            self.sensorList[i].nearSensors = self.findNearSensor(self.sensorList[i])

    def findNearSensor(self, source):
        nearSensors = OrderedDict()
        for i in range(self.quantity):
            sensor = self.sensorList[i]
            length = math.sqrt(pow(sensor.coordinate.x - source.coordinate.x, 2) +
                               pow(sensor.coordinate.y - source.coordinate.y, 2))
            if not sensor == source and length <= 2 * sensor.radius:
                nearSensors[sensor] = length

        return nearSensors

    def findPaths(self, source, destination):
        cost = 0
        pathList = list()
        pathList.append(source)
        self.findPathUntil(source, destination, pathList, cost)

    def findPathUntil(self, source, destination, localPathList, cost):
        if source == destination:
            lst = tuple(localPathList)
            source.pathToSinkSensor[lst] = cost
            return
        source.isVisited = True
        nearSensors = self.findNearSensor(source)
        if len(nearSensors) != 0:
            for sensor, length in nearSensors.items():
                if not sensor.isVisited:
                    cost += length
                    localPathList.append(sensor)
                    self.findPathUntil(sensor, destination, localPathList, cost)
                    localPathList.remove(sensor)
                    cost -= length


        source.isVisited = False

    def findShortestPath(self, pathList):
        shortestPath = None
        minCost = sys.float_info.max

        for key, value in pathList.items():
            if value < minCost:
                minCost = value
                shortestPath = list(key)
        return shortestPath

    def printSensors(self, sensorList):
        for sensor in sensorList:
            print(f"  +++STT: {sensor.index}\t(X,Y) = ({sensor.coordinate.x}, {sensor.coordinate.y})")

    def printAllPathAvailable(self, sensor):
        if len(sensor.pathToSinkSensor) != 0:
            print(f"CAC DUONG DI TU SENSOR TRUNG TAM DEN SENSOR THU {sensor.index} LA: ")
            for key, value in sensor.pathToSinkSensor.items():
                for s in key:
                    print(f"{s.index} ", end="")

                print(f"  --->cost = {value}")
            print("  ==> Duong di ngan nhat la: ")
            for s in sensor.shortestPath:
                print(f"{s.index} ", end="")
            print(end="\n")
