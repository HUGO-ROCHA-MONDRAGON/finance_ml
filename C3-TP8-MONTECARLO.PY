import numpy as np

class MonteCarloSimulator:
    def __init__(self, S0, r, sigma, T):
        self.S0 = S0      # Initial stock price
        self.r = r        # Risk-free rate
        self.sigma = sigma  # Volatility
        self.T = T        # Time to maturity

    def simulate_paths(self, num_simulations, num_steps):
        dt = self.T / num_steps
        paths = np.zeros((num_simulations, num_steps + 1))
        paths[:, 0] = self.S0
        
        for i in range(1, num_steps + 1):
            z = np.random.standard_normal(num_simulations)
            paths[:, i] = paths[:, i-1] * np.exp((self.r - 0.5 * self.sigma**2) * dt + 
                                                 self.sigma * np.sqrt(dt) * z)
        return paths

    def price_option(self, num_simulations, num_steps):
        paths = self.simulate_paths(num_simulations, num_steps)
        payoffs = self.payoff(paths[:, -1])
        option_price = np.exp(-self.r * self.T) * np.mean(payoffs)
        return option_price

    def payoff(self, ST):
        raise NotImplementedError("Subclasses must implement payoff method")
    

def option_pricer(payoff_func):
    def wrapper(**outer_kwargs):  # **kwargs collects all keyword arguments into a dictionary.
        class OptionPricer(MonteCarloSimulator):
            def payoff(self, ST):
                return payoff_func(ST, **outer_kwargs)
        return OptionPricer
    return wrapper



@option_pricer
def european_call_payoff(ST, K=100):
    return np.maximum(ST - K, 0)

@option_pricer
def european_put_payoff(ST, K=100):
    return np.maximum(K - ST, 0)

# Usage
if __name__ == "__main__":
    call_pricer = european_call_payoff(K=100)(S0=100, r=0.05, sigma=0.2, T=1)
    call_price = call_pricer.price_option(num_simulations=100000, num_steps=252)
    print(f"European Call Option Price: {call_price:.4f}")

    put_pricer = european_put_payoff(K=100)(S0=100, r=0.05, sigma=0.2, T=1)
    put_price = put_pricer.price_option(num_simulations=100000, num_steps=252)
    print(f"European Put Option Price: {put_price:.4f}")