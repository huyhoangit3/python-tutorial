from Program import Program, Sensor
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import sys

def main():
    mode, length, width, file_path = load_data()
    
    program = Program(length, width, mode)
    program.read_file(file_path)

    if mode == 1:
        program.load_data()
        program.simulate1(length, width)
    elif mode == 2:
        program.simulate2(length, width)

def load_data():
    arguments = sys.argv
    mode = int(arguments[1])
    file_path = arguments[2]

    file = open(file_path, 'r')
    length = width = 0
    while True:
        line = file.readline()
        line = line.rstrip("\n")
        result = line.split(",")
        length = int(result[0])
        width = int(result[1])
        break;
    file.close()
    return [mode, length, width, file_path]

if __name__ == "__main__":

    main()
    
