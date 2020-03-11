
import numpy as np 
import matplotlib.pyplot as plt

def main():
    file = "./trading_view_bot.log"
    price = []
    state = []
    amount = []
    bullTrigger = -0.2
    bearTrigger = 0.2
    choosenBullPrice = []
    choosenBearPrice = []
    isBull = True
    currentPrice = 0
    money = 100
    btc = 0

    stateMA = []
    stateMAperiod = 1200
    
    stateMA2 = []
    stateMAperiod2 = 900

    avgState = 0
    avgState2 = 0
    num_lines = sum(1 for line in open(file))
    

    f = open(file, "r")
    for i, x in enumerate(f):

        if "price" in x:
            currentPrice = float(x.split("price: ", 1)[1].rstrip())
            price.append(currentPrice)
            if len(price) == 1:
                btc= money/currentPrice
            
        if "state" in x:
            currentState = float(x.split("state: ", 1)[1].rstrip())
            state.append(currentState)

            if len(state) > stateMAperiod:
                sumState = 0
                for pastState in state[len(state) - stateMAperiod:]: 
                    sumState += pastState
                avgState = sumState/stateMAperiod
                stateMA.append(avgState)
            else:
                stateMA.append(0)

            if len(state) > stateMAperiod2:
                sumState = 0
                for pastState in state[len(state) - stateMAperiod2:]: 
                    sumState += pastState
                avgState2 = sumState/stateMAperiod2
                stateMA2.append(avgState2)
            else:
                stateMA2.append(0)

            if not isBull and (currentPrice > 0 and stateMA2[-2] <= bullTrigger and stateMA2[-1] >= bullTrigger or i > num_lines - 4):
                isBull = True
                choosenBullPrice.append(currentPrice)
                print("bull", i/3, currentPrice)
                if len(choosenBearPrice) > 0:
                    money = money + money - (money / choosenBearPrice[-1] * 0.999) * currentPrice * 0.999
            
            if isBull and (currentPrice > 0 and stateMA2[-2] >= bearTrigger and stateMA2[-1] <= bearTrigger or i > num_lines - 4):
                isBull = False
                choosenBearPrice.append(currentPrice)
                print("bear", i/3, currentPrice)
                if len(choosenBullPrice) > 0:
                    money = (money / choosenBullPrice[-1] * 0.999) * currentPrice * 0.999

    print("choosenBullPrices", choosenBullPrice)
    print("choosenBearPrices", choosenBearPrice)

    print("BTC", btc)
    print("money", money)
    
    price.append(price[len(price)-1])
    price.append(price[len(price)-1])
    price.append(price[len(price)-1])

    x = np.array(list(range(1, len(state)+1)))
    y1 = np.array(price)
    y2 = np.array(state)

    print(len(x), len(y1), len(y2))

    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.plot(x, y1, 'g-')
    # ax2.plot(x, y2, 'r-')

    ax1.set_xlabel('X data')
    ax1.set_ylabel('Price')
    # ax2.set_ylabel('State')
    
    plt.plot(stateMA)
    plt.ylabel('stateMA')
    plt.plot(stateMA2)
    plt.ylabel('stateMA2')

    plt.show()

if __name__ == "__main__":
    main()