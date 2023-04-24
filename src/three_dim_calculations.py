from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class ThreeDimCalculations:
    __points: dict
    __baselines: list[dict]

    def __init__(self) -> None:
        baselines = []
        points = {}
        with open("data/baseline_deltas.txt", 'r') as f:
            lines = f.readlines()

            for line in lines:
                start, end, dx, dy, dz = line.split()
                baselines.append({
                    'start': start,
                    'end': end,
                    'dx': float(dx),
                    'dy': float(dy),
                    'dz': float(dz)
                })

        with open("data/points.txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                x, y, z, name = line.split()[1:]
                points[name] = x, y, z

        self.baselines = baselines
        self.points = points

    @property
    def points(self) -> dict:
        return self.__points

    @points.setter
    def points(self, points: dict) -> None:
        self.__points = points

    @property
    def baselines(self) -> list[dict]:
        return self.__baselines

    @baselines.setter
    def baselines(self, baselines: list[dict]) -> None:
        self.__baselines = baselines

    def calculate_avg_point(self) -> dict:
        baselines = self.baselines
        points = self.points
        unknown_points = {}

        for baseline in baselines:
            start = baseline['start']
            end = baseline['end']
            dx = baseline['dx']
            dy = baseline['dy']
            dz = baseline['dz']

            start_x, start_y, start_z = points[start]

            end_x = ThreeDimCalculations.calculate_point(start_x, dx)
            end_y = ThreeDimCalculations.calculate_point(start_y, dy)
            end_z = ThreeDimCalculations.calculate_point(start_z, dz)

            if end in unknown_points:
                unknown_points[end].append((end_x, end_y, end_z))
            else:
                unknown_points[end] = [(end_x, end_y, end_z)]

        avg_unknown_points = {}
        for name, coordinates in unknown_points.items():
            avg_x = sum([x for x, _, _ in coordinates]) / len(coordinates)
            avg_y = sum([y for _, y, _ in coordinates]) / len(coordinates)
            avg_z = sum([z for _, _, z in coordinates]) / len(coordinates)
            avg_unknown_points[name] = np.array([avg_x, avg_y, avg_z])

        return avg_unknown_points

    def create_weight_matrix(self, latex_printout: bool = False) -> None:
        data = []
        with open("data/baseline_report.txt", 'r') as f:
            lines = f.readlines()
            line_count = 1
            d = {}
            for line in lines:
                content = line.split(";")
                content = (x.strip() for x in content)
                match line_count:
                    case 1:
                        start, end = content
                        d['start'] = start
                        d['end'] = end
                    case 2:
                        M0, val = content
                        d['M0'] = float(val)
                    case 3 | 4 | 5 | 6 | 7 | 8:
                        matrix_pos, val = content
                        d[matrix_pos] = float(val)

                if line_count == 8:
                    line_count = 1
                    data.append(d)
                    d = {}
                else:
                    line_count += 1

        weight_matrixes = []
        for d in data:
            Q11 = d["Q11"]
            Q12 = d["Q12"]
            Q13 = d["Q13"]
            Q22 = d["Q22"]
            Q23 = d["Q23"]
            Q33 = d["Q33"]

            Q = np.array([
                [Q11, Q12, Q13],
                [Q12, Q22, Q23],
                [Q13, Q23, Q33]
            ])

            weight_matrixes.append(np.linalg.inv(Q))

        p = np.eye(len(weight_matrixes) * 3)
        pos = 0
        for _, wm in enumerate(weight_matrixes):
            for i in range(len(wm)):
                for j in range(len(wm)):
                    p[i + pos][j + pos] = wm[i][j]

            pos += 3

        if latex_printout:
            text = ""
            count = 1
            for wm, d in zip(weight_matrixes, data):
                start = d['start'].upper()
                end = d['end'].upper()
                df = pd.DataFrame(wm)
                text += f"\\textbf{{Baseline {count}: {start} - {end}}}\\\ \n"
                text += df.to_latex(index=False, header=False)
                text += "\n"

                text = text.replace("\\begin{tabular}{rrr}\n\\toprule\n\\midrule",
                                    "$$\np = \\left[\\begin{array}{*{3}c}")
                text = text.replace("\\bottomrule\n\\end{tabular}", "\\end{array}\\right]\n$$")

                count += 1

            print(text)

        return p

    def create_f_matrix(self) -> np.array:
        with open("data/f_equations.txt", 'r') as f:
            lines = f.readlines()

        lines = [line.strip("\n") for line in lines]
        f_vals = []
        for line in lines:
            _, content = line.split(":")

            content = content.replace("(", "").replace(")", "")
            f_vals.append(eval(content))

        return np.array(f_vals)

    def LSM(self) -> np.array:
        A_list = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [1, 0, 0, -1, 0, 0],
            [0, 1, 0, 0, -1, 0],
            [0, 0, 1, 0, 0, -1]
        ]
        A = np.array(A_list)
        p = self.create_weight_matrix()

        ATp = np.dot(A.T, p)
        ATpA = np.dot(ATp, A)
        Q = np.linalg.inv(ATpA)
        f = self.create_f_matrix()
        ATpf = np.dot(ATp, f)

        return np.dot(Q, ATpf)

    def v(self):
        A_list = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [1, 0, 0, -1, 0, 0],
            [0, 1, 0, 0, -1, 0],
            [0, 0, 1, 0, 0, -1]
        ]
        A = np.array(A_list)
        x = self.LSM()
        f = self.create_f_matrix()
        return np.dot(A, x) - f

    @staticmethod
    def calculate_point(point_component: float, delta: float) -> float:
        return float(point_component) + float(delta)
