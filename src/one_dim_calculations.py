from dataclasses import dataclass

import numpy as np


@dataclass
class OneDimCalculations:
    @staticmethod
    def A() -> np.array:
        table = [
            [0, 1],
            [0, 0],
            [0, 0],
            [0, 1],
            [1, 0],
            [0, 0],
            [0, 0],
            [1, 0],
            [0, 1],
            [-1, 1],
            [1, 0],
        ]

        return np.array(table)

    @staticmethod
    def f_and_p() -> np.array:
        baselines = {
            "L1": (-23.1545, 0.0010),
            "L2": (-61.4324, 0.0010),
            "L3": (64.7888, 0.0008),
            "L4": (-88.1397, 0.0005),
            "L5": (-89.6963, 0.0003),
            "L6": (-0.1990, 0.0002),
            "L7": (-126.4255, 0.0002),
            "L8": (-89.8950, 0.0002),
            "L9": (38.2770, 0.0006),
            "L10": (1.7519, 0.0005),
            "L11": (-24.8742, 0.0003),
        }

        heights = {
            "HM": 170.8390,
            "HH": 171.0560,
            "HØ": 44.6180,
            "HF": 106.0470,
        } # Ellipsoidal heights

        f = np.array([
            heights["HF"] + baselines["L1"][0],
            heights["HF"] - heights["HØ"] + baselines["L2"][0],
            heights["HF"] - heights["HM"] + baselines["L3"][0],
            heights["HH"] + baselines["L4"][0],
            heights["HM"] + baselines["L5"][0],
            heights["HH"] - heights["HM"] + baselines["L6"][0],
            heights["HH"] - heights["HØ"] + baselines["L7"][0],
            heights["HH"] + baselines["L8"][0],
            heights["HØ"] + baselines["L9"][0],
            baselines["L10"][0],
            heights["HF"] + baselines["L11"][0]
        ])

        s_0 = 0.0002
        p = np.eye(len(baselines))
        for i in range(len(baselines)):
            p[i][i] = s_0 ** 2 / baselines[f"L{i + 1}"][1] ** 2

        return f, p

    @staticmethod
    def x_hat() -> np.array:
        A = OneDimCalculations.A()
        f, p = OneDimCalculations.f_and_p()

        ATP = np.dot(A.T, p)
        ATPA = np.dot(ATP, A)
        N = np.linalg.inv(ATPA)  # Normal matrix
        NAT = np.dot(N, A.T)
        NATp = np.dot(NAT, p)
        x_hat = np.dot(NATp, f)

        return x_hat

    @staticmethod
    def v() -> np.array:
        A = OneDimCalculations.A()
        f, p = OneDimCalculations.f_and_p()
        x_hat = OneDimCalculations.x_hat()

        return np.dot(A, x_hat) - f

    @staticmethod
    def var_hat() -> np.array:
        v = OneDimCalculations.v()
        p = OneDimCalculations.f_and_p()[1]
        vTp = np.dot(v.T, p)
        vTpv = np.dot(vTp, v)
        return np.sqrt(vTpv / (11 - 2))

    @staticmethod
    def C_hat() -> np.array:
        var = OneDimCalculations.var_hat()
        A = OneDimCalculations.A()
        p = OneDimCalculations.f_and_p()[1]
        ATP = np.dot(A.T, p)
        ATPA = np.dot(ATP, A)
        N = np.linalg.inv(ATPA)  # Normal matrix

        return var * N

    @staticmethod
    def s_xx() -> np.array:
        var = OneDimCalculations.var_hat()
        return np.sqrt(var[0][0])

    @staticmethod
    def s_yy() -> np.array:
        var = OneDimCalculations.var_hat()
        return np.sqrt(var[1][1])

    @staticmethod
    def weighted_mean() -> np.array:
        pass
