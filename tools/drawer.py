
import numpy as np 
import matplotlib.pyplot as plt

def main():
    price = []
    state = []
    choosenBullPrice = []
    choosenBearPrice = []
    isBull = True
    currentPrice = 0

    stateMA = []
    stateMAperiod = 1500
    
    stateMA2 = []
    stateMAperiod2 = 1000

    priceMultiplyState = []

    f = open("./binance_5m.log", "r")
    for i, x in enumerate(f):
        if "price" in x:
            currentPrice = float(x.split("price: ", 1)[1].rstrip())
            price.append(currentPrice)
            
        if "state" in x:
            currentState = float(x.split("state: ", 1)[1].rstrip())
            state.append(currentState)
            priceMultiplyState.append (currentState * currentPrice)

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
                avgState = sumState/stateMAperiod2
                stateMA2.append(avgState)
            else:
                stateMA2.append(0)

            if not isBull and currentState < -0.5:
                isBull = True
                choosenBullPrice.append(currentPrice)
                print("bull")
                print(i/2, ",", currentPrice)
            
            if isBull and currentState > 0.5:
                isBull = False
                choosenBearPrice.append(currentPrice)
                print("bear")
                print(i/2, ",", currentPrice)
                print("\n")

    print("choosenBullPrices", choosenBullPrice)
    
    print("choosenBearPrices", choosenBearPrice)
            
    plt.plot(price)
    plt.ylabel('Price')
    plt.show()

    plt.plot(state)
    plt.ylabel('State')
    plt.plot(stateMA)
    plt.ylabel('stateMA')
    plt.plot(stateMA2)
    plt.ylabel('stateMA2')
    plt.show()

    print("HELLO")
    
    price.append(price[len(price)-1])

    x = np.array(list(range(1, len(state)+1)))
    y1 = np.array(price)
    y2 = np.array(state)

    
    print(len(x), len(y1), len(y2))

    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.plot(x, y1, 'g-')
    ax2.plot(x, y2, 'b-')

    ax1.set_xlabel('X data')
    ax1.set_ylabel('Price', color='g')
    ax2.set_ylabel('State', color='b')

    plt.show()

if __name__ == "__main__":
    main()