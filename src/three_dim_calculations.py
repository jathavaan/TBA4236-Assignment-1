from dataclasses import dataclass

@dataclass
class ThreeDimCalculations:
    @staticmethod
    def foo(delta: dict):
        with open("data/points.txt", "r") as f:
            points = f.readlines()
            for point in points:
                x, y, z, name = point.split()[1:]
                print(f"Point {name} has coordinates: {x}, {y}, {z}")

    @staticmethod
    def calculate_point(point_component: float, delta: float) -> float:
        return point_component + delta

