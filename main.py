from src.one_dim_calculations import OneDimCalculations as odc
from src.three_dim_calculations import ThreeDimCalculations


def bmatrix(a):
    text = r'$\left[\begin{array}{*{'
    text += str(len(a[0]))
    text += r'}c}'
    text += '\n'
    for x in range(len(a)):
        for y in range(len(a[x])):
            text += str(a[x][y])
            text += r' & '
        text = text[:-2]
        text += r'\\'
        text += '\n'
    text += r'\end{array}\right]$'

    return text


def one_dim_calculation() -> None:
    v = odc.v()
    print(v)


def three_dim_calculation() -> None:
    tdc = ThreeDimCalculations()
    x_hat = tdc.LSM()
    v = tdc.v()
    f = tdc.create_f_matrix()
    print(x_hat * 1000)


def main() -> None:
    # one_dim_calculation()
    three_dim_calculation()


if __name__ == "__main__":
    main()
