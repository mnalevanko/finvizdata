from pprint import PrettyPrinter

from controller import KeyStatsController

pp = PrettyPrinter(indent=4)


if __name__ == '__main__':
    symbol = input('Enter symbol of the stock: ')
    symbol = symbol.upper()
    if len(symbol) == 0:
        print('No symbol was provided.')

    ctrl = KeyStatsController(symbol)
    res = ctrl.update()
    print(res)
