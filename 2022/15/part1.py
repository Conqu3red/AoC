from typing import *
from dataclasses import dataclass
import re
import time

@dataclass
class Sensor:
    x: int
    y: int
    beacon_x: int
    beacon_y: int

LINE_PATTERN = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"

def load() -> List[Sensor]:
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    sensors = []
    for line in lines:
        sensor_x, sensor_y, beacon_x, beacon_y = map(int, re.match(LINE_PATTERN, line).groups())

        sensors.append(Sensor(sensor_x, sensor_y, beacon_x, beacon_y))
    
    return sensors


def no_beacons(sensors: List[Sensor], scan_y: int) -> int:
    #ranges: List[Tuple[int, int]] = []

    numbers: Set[int] = set()

    for sensor in sensors:
        # mahatten distance
        dist = abs(sensor.x - sensor.beacon_x) + abs(sensor.y - sensor.beacon_y)

        y_diff = abs(sensor.y - scan_y)
        x_diff = dist - y_diff

        if x_diff > 0:
            left = sensor.x - x_diff
            right = sensor.x + x_diff # include this value!

            #print(f"{left} to {right}")

            numbers |= set(range(left, right + 1))
            
            # might need to merge ranges instead of making a massive set
    
    for sensor in sensors:
        if sensor.beacon_y == scan_y and sensor.beacon_x in numbers:
            numbers.remove(sensor.beacon_x)
    
    return len(numbers)

s = time.time()
sensors = load()
print("Part 1:", no_beacons(sensors, 2000000))
e = time.time()
print(e - s)