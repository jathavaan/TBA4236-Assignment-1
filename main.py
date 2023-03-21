from src.calculations import Calculations as calc


def main() -> None:
    C_hat = calc.C_hat()
    riktig = "Ja" if C_hat[0][1] == C_hat[1][0] else "Nei"
    print(f"Du har gjort oppgaven riktig: {riktig}")

if __name__ == "__main__":
    main()
