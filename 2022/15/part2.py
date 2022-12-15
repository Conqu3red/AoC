from typing import *
from dataclasses import dataclass
import re
import time

MAX = 4000000

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


def blank_x(sensors: List[Sensor], scan_y: int) -> int:
    ranges: List[Tuple[int, int]] = []

    for sensor in sensors:
        # mahatten distance
        dist = abs(sensor.x - sensor.beacon_x) + abs(sensor.y - sensor.beacon_y)

        y_diff = abs(sensor.y - scan_y)
        x_diff = dist - y_diff

        assert x_diff + y_diff == dist

        if x_diff > 0:
            left = sensor.x - x_diff
            right = sensor.x + x_diff # include this value!

            #print(f"{left} to {right}")

            # need to merge ranges instead of making a massive set
            ranges.append((left, right))
    
    # merge ranges
    ranges = sorted(ranges)
    #print(scan_y, ranges)

    rightmost = 0
    for r in ranges:
        if r[0] > rightmost:
            #print(r)
            return rightmost + 1
        elif r[1] > rightmost:
            rightmost = r[1]
    
    if rightmost < MAX:
        return rightmost + 1
    
    return None

s = time.time()
sensors = load()
for y in range(MAX):
    if y % 100_000 == 0:
        print(f"{y * 100 / MAX:.0f}%")
    x = blank_x(sensors, y)

    if x is not None:
        print("Found:", x, y)
        print("Part 2: ", x * 4000000 + y)
        break

e = time.time()
print(f"Completed in {e-s:.1f}s")