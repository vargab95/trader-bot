import matplotlib.pyplot as plt

def main():
    price = []
    state = []
    f = open("./binance_5m.log", "r")
    for x in f:
        if "price" in x:
            price.append(float(x.split("price: ", 1)[1].rstrip()))
            
        if "state" in x:
            state.append(float(x.split("state: ", 1)[1].rstrip()))
            
    plt.plot(price)
    plt.ylabel('Price')
    plt.show()

    
    plt.plot(state)
    plt.ylabel('State')
    plt.show()

if __name__ == "__main__":
    main()