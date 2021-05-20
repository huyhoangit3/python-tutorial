from Sensor import Sensor, OrderedDict
import random
import math
import sys


class Program:
    # hàm tạo
    def __init__(self, n):
        # số lượng sensor
        self.quantity = n
        # danh sách sensor
        self.sensorList = list()
        # khởi tạo sink sensor
        self.sinkSensor = Sensor()
        self.sinkSensor.coordinate.x = 50
        self.sinkSensor.coordinate.y = 50

        # random các sensor
        self.randSensors()

        # load dữ liệu cho từng sensor và sensor trung tâm
        self.loadData()

    # hàm random các sensor
    def randSensors(self):
        pos = 1
        while pos <= self.quantity:
            # khởi tạo 1 sensor
            sensor = Sensor()
            while True:
                flag = False
                # random tọa độ  x và y
                x = random.randint(0, 100)
                y = random.randint(0, 100)
                # gán số thứ tự cho mỗi sensor
                sensor.index = pos
                # gán tọa độ cho mỗi sensor
                sensor.coordinate.x = x
                sensor.coordinate.y = y

                length = 0
                # đảm bảo các sensor có thể kết nối với nhau
                # duyệt lần lượt từng sensor trong sensorList
                if(len(self.sensorList) == 0):
                    length = math.sqrt(pow(sensor.coordinate.x - self.sinkSensor.coordinate.x, 2) +
                                       pow(sensor.coordinate.y - self.sinkSensor.coordinate.y, 2))
                    if sensor != self.sinkSensor and length <= 2 * sensor.radius:
                        flag = True


                
                for i in range(len(self.sensorList)):
                    # lấy ra từng sensor
                    source = self.sensorList[i]
                    # tính khoảng cách giữa 2 sensor
                    length = math.sqrt(pow(sensor.coordinate.x - source.coordinate.x, 2) +
                                       pow(sensor.coordinate.y - source.coordinate.y, 2))
                    # thêm vào danh sách các sensor ở gần nếu khoảng cách <= 2 * radius
                    if sensor not in self.sensorList and x != 50 and y != 50 and length <= 2 * sensor.radius:
                        flag = True
                        break
                if flag == True:
                    break

            self.sensorList.append(sensor)
            pos += 1    


    # hàm load data cho từng sensor
    def loadData(self):
        # tìm danh sách các sensor gần sensor trung tâm
        self.findNearSensor(self.sinkSensor)
        
        for i in range(self.quantity):
            # tìm danh sách các sensor gần mỗi sensor 
            self.findNearSensor(self.sensorList[i]) 

        for i in range(self.quantity):
            # tìm danh sách đường đi tới sink sensor và chi phí của chúng nếu có
            self.findPaths(self.sinkSensor, self.sensorList[i])
            # tìm đường đi ngắn nhất từ sink sensor đến mỗi sensor (nếu có)
            self.findShortestPath(self.sensorList[i])
        

    # phương thức tìm danh sách các sensor ở gần mỗi sensor
    def findNearSensor(self, source):
        # duyệt lần lượt từng sensor trong sensorList
        for i in range(self.quantity):
            # lấy ra từng sensor
            sensor = self.sensorList[i]
            # tính khoảng cách giữa 2 sensor
            length = math.sqrt(pow(sensor.coordinate.x - source.coordinate.x, 2) +
                               pow(sensor.coordinate.y - source.coordinate.y, 2))
            # thêm vào danh sách các sensor ở gần nếu khoảng cách <= 2 * radius
            if not sensor == source and length <= 2 * sensor.radius:
                # key: sensor ở gần
                # value: khoảng cách giữa chúng
                source.nearSensors[sensor] = length

    # tìm đường đi từ sensor source đến sensor destination
    def findPaths(self, source, destination):
        # khởi tạo chi phí ban đầu là 0
        cost = 0
        # khởi tạo danh sách các sensor tạo thành đường đi
        pathList = list()
        # thêm sensor source vào danh sách các sensor tạo thành đường đi
        pathList.append(source)
        self.findPathUntil(source, destination, pathList, cost)

    # hàm đệ quy
    def findPathUntil(self, source, destination, localPathList, cost):
        # nếu sensor source bằng sensor destination
        if source == destination:
            # key: danh sách các sensor tạo thành đường đi
            lst = tuple(localPathList)
            # value: chi phí của đường đi này
            source.pathToSinkSensor[lst] = cost
            return

        source.isVisited = True
        # nếu sensor hiện tại có danh sách các senssor gần nó
        if len(source.nearSensors) != 0:
            # duyệt dictionary chứa danh sách đường đi
            # sensor: danh sách đường đi
            # lenght: chi phí đường đi đó
            for sensor, length in source.nearSensors.items():
                # nếu sensor chưa được duyệt
                if not sensor.isVisited:
                    # cộng thêm chi phí đường đi
                    cost += length
                    # thêm sensor vào localPathList
                    localPathList.append(sensor)
                    # tiếp tục tìm đến khi gặp sensor đích hoặc không tồn tại đường đi giữa 2 sensor
                    self.findPathUntil(sensor, destination, localPathList, cost)
                    # xóa sensor khỏi localPathList
                    localPathList.remove(sensor)
                    cost -= length


        source.isVisited = False

    # tìm đường đi ngắn nhất
    def findShortestPath(self, source):
        # lấy ra giá trị lớn nhất của kiểu floating point number
        minCost = sys.float_info.max

        # duyệt key và value trong dictionary pathList
        if len(source.pathToSinkSensor) != 0:
            for key, value in source.pathToSinkSensor.items():
                if value < minCost:
                    minCost = value
                    # deep copy
                    source.shortestPath = list(key)

    # in ra thông tin các sensor
    def printSensors(self, sensorList):
        for sensor in sensorList:
            print(f"  +++STT: {sensor.index}\t(X,Y) = ({sensor.coordinate.x}, {sensor.coordinate.y})")

    # in ra tất cả các đường đi
    def printAllPathAvailable(self, sensor):
        # nếu có đường đi
        if len(sensor.pathToSinkSensor) != 0:
            print(f"CAC DUONG DI TU SENSOR TRUNG TAM DEN SENSOR THU {sensor.index} LA: ")
            # duyệt dồng thời key và value trong dictionary
            for key, value in sensor.pathToSinkSensor.items():
                # duyệt lần lượt sensor trong danh sách đường đi
                for s in key:
                    # in ra số thứ tự
                    print(f"{s.index} ", end="")
                # in ra chi phí của đường đi đó
                print(f"  --->cost = {value}")
            print("  ==> Duong di ngan nhat la: ")
            # in ra đường đi ngắn nhất
            for s in sensor.shortestPath:
                print(f"{s.index} ", end="")
            print(end="\n")
