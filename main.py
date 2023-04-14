from src.one_dim_calculations import OneDimCalculations
from src.three_dim_calculations import ThreeDimCalculations


def one_dim_calculation() -> None:
    print(OneDimCalculations.x_hat())


def three_dim_calculation() -> None:
    ThreeDimCalculations.foo({})


def main() -> None:
    one_dim_calculation()
    three_dim_calculation()


if __name__ == "__main__":
    main()
