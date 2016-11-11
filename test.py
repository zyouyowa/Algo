# -*- coding: utf-8 -*-
import sys

def test_forecast_first():
    print('forecast_first : ')    
    from main import Card, forecast_first
    check_list = [
        [Card('b'), Card('b'), Card('w'), Card('b')],
        [Card('w'), Card('w'), Card('b'), Card('w')],
        [Card('b'), Card('b'), Card('w'), Card('w')],
        [Card('w'), Card('w'), Card('b'), Card('b')],    
        [Card('w'), Card('w'), Card('w'), Card('w')],
        [Card('b'), Card('b'), Card('b'), Card('b')],
        [Card('b'), Card('w'), Card('b'), Card('w')],
        [Card('w'), Card('b'), Card('w'), Card('b')],
        [Card('b'), Card('w'), Card('w'), Card('w'), Card('b')],
        [Card('w'), Card('b'), Card('b'), Card('b'), Card('w')],
        #wbbwwbbbwwwb
        #012234566789
        [Card('w'), Card('b'), Card('b'), Card('w'), Card('w'), Card('b'), Card('b'), Card('b'), Card('w'), Card('w'), Card('w'), Card('b')],
    ]
    for to_check in check_list:
        colors = [c.color for c in to_check]
        firsts = forecast_first(to_check)
        print(colors , firsts)

def test_forecast_last():
    print('forecast_last : ')    
    from main import Card, forecast_first, forecast_last
    check_list = [
        [Card('b'), Card('b'), Card('w'), Card('b')],
        [Card('w'), Card('w'), Card('b'), Card('w')],
        [Card('b'), Card('b'), Card('w'), Card('w')],
        [Card('w'), Card('w'), Card('b'), Card('b')],    
        [Card('w'), Card('w'), Card('w'), Card('w')],
        [Card('b'), Card('b'), Card('b'), Card('b')],
        [Card('b'), Card('w'), Card('b'), Card('w')],
        [Card('w'), Card('b'), Card('w'), Card('b')],
        [Card('b'), Card('w'), Card('w'), Card('w'), Card('b')],
        [Card('w'), Card('b'), Card('b'), Card('b'), Card('w')],
        [Card('b'), Card('b'), Card('w'), Card('w'), Card('w'), Card('b'), Card('b'), Card('b'), Card('w'), Card('w'), Card('b'), Card('b'), Card('w')],
    ]
    for to_check in check_list:
        colors = [c.color for c in to_check]
        firsts = forecast_first(to_check)
        lasts = forecast_last(firsts, to_check)
        print(colors , lasts)

def test_forecast_card():
    print('forecast_card : ')
    from main import Card, forecast_card
    check_list = [
        [Card('b', 3), Card('b', 5), Card('w', 5), Card('b', 10)],
        [Card('b', 0), Card('w', 5), Card('w', 8), Card('b', 9)],
        [Card('b', 3), Card('b', 7), Card('w', 9), Card('b', 11)],
        [Card('b', 3), Card('w', 5), Card('w', 8), Card('b', 11)],
    ]
    knowns = [Card('b', 3), Card('w', 8), Card('b', 11)]
    saids = [Card('w', 5)]
    for to_check in check_list:
        colors = [c.color for c in to_check]        
        forecasts = forecast_card(to_check, knowns, saids)
        print(colors, forecasts)
    to_check = [Card('b', i) for i in range(6)]
    knowns = [Card('b', i) for i in range(3)]
    saids = [Card('b', i) for i in range(3, 7)]
    colors = [c.color for c in to_check]
    forecasts = forecast_card(to_check, knowns, saids)
    print(colors, forecasts)

def main():
    test_forecast_first()
    test_forecast_last()
    #test_forecast_card()


if __name__ == '__main__':
    sys.exit(int(main() or 0))