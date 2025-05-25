import numpy as np
import pandas as pd
from IPython.display import display
import yfinance as yf

# Calculating the Variance
# Var(x) = x^T V  x
# Constraints can be added to the energy (such as no short selling)
def energy(x, sigma):
    return x.T @ sigma @ x

# Metropolis
def metropolisMinimumVariance(sigma, numberOfStocks):

    # Random starting weight using standard Gaussian
    x = np.random.randn(numberOfStocks)
    x = np.abs(x)
    # Normalize sum to 1
    x /= x.sum()
    x *= 100

    currentVariance = energy(x, sigma)

    # Displaying initial weights
    print("=" * 80)
    print("Initial Variance: ", currentVariance)
    print("Intial Weights")
    display(x)
    print("=" * 80)


    bestX = x
    bestVariance = currentVariance

    t = 0

    # temp -> inf: uniform on all the states (explores every possibility)
    # temp -> 0: uniform on stable states (local minimums and minimums)
    temp = float(input("Enter the temperature (use 0 if no constraints): "))
    N = int(input("Enter the number of iterations (the larger the better): "))
    N10 = int(N/10)

    while (t < N):
        accept = 0
        xCand = x.copy()
        xChange = np.random.uniform(-0.5, 0.5)
        x1, x2 = np.random.choice(range(numberOfStocks), size = 2, replace = False)
        xCand[x1] += xChange
        xCand[x2] -= xChange
        candVariance = energy(xCand, sigma)

        delta = candVariance - currentVariance

        if (delta < 0):
            accept = 1
        elif (temp > 0):
            prob = np.exp(- delta / temp)
            accept = np.random.rand() < prob

        if (accept):
            x = xCand
            currentVariance = candVariance
            
            # Keeping track of best result so far
            if (candVariance < bestVariance):
                bestX = xCand
                bestVariance = candVariance

        # Report the progress periodically
        if (t%N10 == 0):
            print(f"Still thinking... on iteration {t}")
            print(f"Current variance is: {currentVariance} \n")

        t+=1

    return bestX, bestVariance

# Closed form solution is available when there is no constraints except full investment
# Covariance Matrix is invertible
def min_var_portfolio(cov_matrix):
    ones = np.ones(cov_matrix.shape[0])
    inv_cov = np.linalg.inv(cov_matrix)
    weights = inv_cov @ ones
    weights /= ones @ inv_cov @ ones
    return weights

# Getting Data from Yahoo Finance
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
data = yf.download(tickers, start='2024-01-01', end='2025-01-01')
testData = yf.download(tickers, start='2025-01-01')
dataClose = data['Close']

# Getting the returns
returnsData = np.log(dataClose / dataClose.shift(1)).dropna()
display(returnsData)

# Covariance Matrix
covarainceMatrix = returnsData.cov()
display(covarainceMatrix)

# Call our Metropolis
w, wVar = metropolisMinimumVariance(covarainceMatrix.copy(), len(tickers))

# Metropolis results
print("=" * 80)
print("Metropolis Minimum Variance Found is : ", wVar)
print("-" * 80)
w = pd.DataFrame(w, index = tickers, columns = ['Weight'])
display(w)
print("=" * 80)

# Closed-Form results
min_var_weights = min_var_portfolio(covarainceMatrix.copy())
wClosedForm = pd.DataFrame(min_var_weights, index = tickers, columns = ['Weight'])
print("=" * 80)
print("Closed Form Solution: ")
print("-" * 80)
display(wClosedForm)
print("=" * 80)
