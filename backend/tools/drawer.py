import numpy as np
import matplotlib.pyplot as plt

# pylint: skip-file


def calculate_average(state, state_ma_period):
    avg_state = 0
    if len(state) > state_ma_period:
        sum_state = 0
        for past_state in state[len(state) - state_ma_period:]:
            sum_state += past_state
        avg_state = sum_state / state_ma_period
    return avg_state


def handle_data_in_file(file_name, price, state, state_ma, state_ma2,
                        state_ma_period, state_ma_period2, bull_buy_trigger,
                        bull_sell_trigger, bear_buy_trigger,
                        bear_sell_trigger):

    money = 100
    token = "usd"
    current_price = 0
    state_or_price = "state"
    num_lines = sum(1 for line in open(file_name))
    choosen_bull_buy_price = []
    choosen_bear_buy_price = []
    choosen_bull_sell_price = []
    choosen_bear_sell_price = []

    input_file = open(file_name, "r")
    for i, j in enumerate(input_file):

        if state_or_price == "price" and "price" in j:
            current_price = float(j.split("Current price: ", 1)[1].rstrip())
            price.append(current_price)
            state_or_price = "state"

        if state_or_price == "state" and "state" in j:
            current_state = float(j.split("Current state: ", 1)[1].rstrip())
            state.append(current_state)
            state_or_price = "price"

            state_ma.append(calculate_average(state, state_ma_period))
            state_ma2.append(calculate_average(state, state_ma_period2))

            if token == "usd" and current_price > 0 and state_ma[
                    -2] <= bull_buy_trigger and state_ma[
                        -1] >= bull_buy_trigger:
                token = "bull"
                choosen_bull_buy_price.append(current_price)
                print(token, i / 3, current_price)

            if token == "bull" and (current_price > 0
                                    and state_ma[-2] >= bull_sell_trigger
                                    and state_ma[-1] <= bull_sell_trigger
                                    or i > num_lines - 4):
                token = "usd"
                choosen_bull_sell_price.append(current_price)
                if len(choosen_bull_buy_price) > 0:
                    money = money * 0.998 * current_price / choosen_bull_buy_price[
                        -1]
                    print(token, i / 3, current_price,
                          current_price / choosen_bull_buy_price[-1] * 0.998)

            if token == "usd" and current_price > 0 and state_ma[
                    -2] >= bear_buy_trigger and state_ma[
                        -1] <= bear_buy_trigger:
                token = "bear"
                choosen_bear_buy_price.append(current_price)
                print(token, i / 3, current_price)

            if token == "bear" and (current_price > 0
                                    and state_ma[-2] <= bear_sell_trigger
                                    and state_ma[-1] >= bear_sell_trigger
                                    or i > num_lines - 4):
                token = "usd"
                choosen_bear_sell_price.append(current_price)
                if len(choosen_bear_buy_price) > 0:
                    money = money * 0.998 * choosen_bear_buy_price[
                        -1] / current_price
                    print(token, i / 3, current_price,
                          choosen_bear_buy_price[-1],
                          choosen_bear_buy_price[-1] / current_price * 0.998)

    print("choosen_bull_buy_price", choosen_bull_buy_price,
          "choosen_bull_sell_price", choosen_bull_sell_price)
    print("choosen_bear_buy_price", choosen_bear_buy_price,
          "choosen_bear_sell_price", choosen_bear_sell_price)
    print("money", money)


def main():
    file_name = "./trading_view_bot_5m.log"
    file_name2 = "./trading_view_bot.log"

    bull_buy_trigger = -0.2
    bull_sell_trigger = 0.1
    bear_buy_trigger = 0.2
    bear_sell_trigger = -0.1

    state_ma_period = 900
    state_ma_period2 = 300

    price_5m = []
    state_5m = []

    state_ma_5m = []
    state_ma2_5m = []

    price_1h = []
    state_1h = []

    state_ma_1h = []
    state_ma2_1h = []

    handle_data_in_file(file_name, price_5m, state_5m, state_ma_5m,
                        state_ma2_5m, state_ma_period, state_ma_period2,
                        bull_buy_trigger, bull_sell_trigger, bear_buy_trigger,
                        bear_sell_trigger)

    handle_data_in_file(file_name2, price_1h, state_1h, state_ma_1h,
                        state_ma2_1h, state_ma_period, state_ma_period2,
                        bull_buy_trigger, bull_sell_trigger, bear_buy_trigger,
                        bear_sell_trigger)

    fig, ax1 = plt.subplots()
    # ax2 = ax1.twinx()
    ax1.plot(np.array(list(range(1,
                                 len(price_1h) + 1))), np.array(price_1h),
             'g-')
    # ax2.plot(np.array(list(range(1, len(state_1h)+1))), np.array(state_1h), 'r-')

    ax1.set_xlabel('Length')
    ax1.set_ylabel('Price_1h')
    # ax2.set_ylabel('State_1h')

    plt.plot(state_ma_1h)
    plt.ylabel('state_ma_1h')
    plt.plot(state_ma_5m)
    plt.ylabel('state_ma_5m')

    plt.show()


if __name__ == "__main__":
    main()
