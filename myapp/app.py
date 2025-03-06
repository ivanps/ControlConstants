from shiny.express import input, render, ui
from scipy.stats import norm
from scipy.integrate import quad
from scipy.special import gammaln
import numpy as np

ui.h1("Shewhart control charts constants")
ui.input_numeric("n", "Select the group sample size:", 5, min=2, max=100)

def compute_d2(n):
    def integrand(x):
        return 1 - (1 - norm.cdf(x)) ** n - (norm.cdf(x)) ** n

    result, _ = quad(integrand, -np.inf, np.inf)
    return result

def compute_c4(n):
    # To avoid overflow, use gammaln() instead of gamma()
    # Compute the exponential of the difference of the logs
    gamma_ratio = np.exp(gammaln(n / 2) - gammaln((n - 1) / 2))
    return np.sqrt(2 / (n - 1)) * gamma_ratio

@render.code
def txt():
    return f"c4 = {compute_c4(input.n())}\nd2 = {compute_d2(input.n())}"
