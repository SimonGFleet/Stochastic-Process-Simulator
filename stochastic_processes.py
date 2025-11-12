import numpy as np
from numpy import random



# Base Class
class StochasticProcess:
    '''Parent class for stochastic processes, contains required structure for individual stochastic processes.'''
    name = "Base"
    def __init__(self):
        self.dim=1

    def simulate(self, params):
        raise NotImplementedError

    def ui_spec(self):
        return {}
    
class BrownianMotion(StochasticProcess):
    def __init__(self):
        self.dim = 1
    name = "Brownian Motion"
    
    def simulate(self, params):
        N=params["Number of Steps"]
        mu=params["Drift"]
        sigma=params["Volatility"]
        dt = 1 / N
        std = dt ** 0.5
        Z = random.normal(mu * dt, sigma * std, size=(N))
        return Z.cumsum()

    def ui_spec(self):
        return {
            "Number of Steps":     {"min": 10,   "max": 100000, "default": 100,   "scale": "log"},
            "Drift":    {"min": -10,  "max": 10, "default": 0,   "scale": "linear"},
            "Volatility": {"min": 0.1, "max": 3, "default": 1,   "scale": "linear"},
            "Number of Paths": {"min": 1,   "max": 10, "default": 1,   "scale": "int"}
        }



class BrownianSheet(StochasticProcess):
    def __init__(self):
        self.dim = 2
    name = "Brownian Sheet"

    def simulate(self, params):
        """
        Simulates a Brownian sheet on an NxN grid.
        Args:
            N: grid size
            T: total extent (used symmetrically in both dimensions)
        """
        N=params["Number of Steps"]
        mu=params["Drift"]
        sigma=params["Volatility"]
        dt = 1 / N
        #This is sqrt(dt) * sqrt(dt) since 2 dimensional, so standard deviation is just dt
        std = dt

        # Generate independent increments
        Z = np.random.normal(mu * dt, sigma * std, size=(N, N))
        
        # 2D cumulative sum: sum over rectangles
        sheet = np.cumsum(np.cumsum(Z, axis=0), axis=1)
        
        return sheet
    
    def ui_spec(self):
        return {
            "Number of Steps":     {"min": 10,   "max": 1000000, "default": 1000,   "scale": "log"},
            "Drift":    {"min": -10,  "max": 10, "default": 0,   "scale": "linear"},
            "Volatility": {"min": 0.1, "max": 3, "default": 1,   "scale": "linear"}
        }

    


class RandomWalk(StochasticProcess):
    def __init__(self):
        self.dim = 1
    name = "Random Walk"

    def simulate(self, params):
        N=params["Number of Steps"]
        mu=params["Drift"]
        sigma=params["Volatility"]
        k = (1 / N) * sigma
        p_pos = 0.5 + mu / (2 * sigma)
        p_neg = 1 - p_pos

        steps = np.random.choice([-k, k], size=N, p=[p_neg, p_pos])
        walk = np.cumsum(steps)
        return walk
    
    def ui_spec(self):
        return {
            "Number of Steps":     {"min": 10,   "max": 100000, "default": 100,   "scale": "log"},
            "Drift":    {"min": -1,  "max": 1, "default": 0,   "scale": "linear"},
            "Volatility": {"min": 0.1, "max": 3, "default": 1,   "scale": "linear"},
            "Number of Paths": {"min": 1,   "max": 10, "default": 1,   "scale": "int"}
        }



class GeometricBrownianMotion(StochasticProcess):
    def __init__(self):
        self.dim = 1
    name = "Geometric Brownian Motion"
    
    def simulate(self, params):
        N=params["Number of Steps"]
        mu=params["Drift"]
        sigma=params["Volatility"]
        dt = 1 / N
        dW = random.normal(0, np.sqrt(dt), size=N)
        
        # cumulative Brownian motion
        W = np.cumsum(dW)
        
        t = np.linspace(0, 1, N)
        
        S0 = 1
        S = S0 * np.exp((mu - 0.5 * sigma**2) * t + sigma * W)
        return S
    
    def ui_spec(self):
        return {
            "Number of Steps":     {"min": 10,   "max": 100000, "default": 100,   "scale": "log"},
            "Drift":    {"min": -1,  "max": 1, "default": 0,   "scale": "linear"},
            "Volatility": {"min": 0.1, "max": 3, "default": 1,   "scale": "linear"},
            "Number of Paths": {"min": 1,   "max": 10, "default": 1,   "scale": "int"}
        }






class OrnsteinUhlenbeck(StochasticProcess):
    def __init__(self):
        self.dim = 1
    name = "Ornstein Uhlenbeck"

    def simulate(self, params):
        N=params["Number of Steps"]
        mu=params["Drift"]
        sigma=params["Volatility"]
        theta=params["Reversion Factor"]
        X = np.zeros(N)
        X[0] = 0
        
        dt = 1 / N

        # Pre-draw noise
        noise = np.random.normal(0, np.sqrt(dt), N)
        
        for t in range(1, N):
            X[t] = X[t-1] + theta*(mu - X[t-1])*dt + sigma*noise[t]

        return X
    
    def ui_spec(self):
        return {
            "Number of Steps":     {"min": 10,   "max": 100000, "default": 100,   "scale": "log"},
            "Drift":    {"min": -1,  "max": 1, "default": 0,   "scale": "linear"},
            "Volatility": {"min": 0.1, "max": 3, "default": 1,   "scale": "linear"},
            "Number of Paths": {"min": 1,   "max": 10, "default": 1,   "scale": "int"},
            "Reversion Factor": {"min": 0, "max": 2, "default": 1, "scale": "linear"}
        }
    


class EmptyPlot(StochasticProcess):
    name = "Empty Plot"

    def default_params(self):
        return {}

    def simulate(self, params):
        raise NotImplementedError
    
    
    def ui_spec(self):
        return {}







processes = {
    "Select a Path" : EmptyPlot, 
    "Brownian Motion" : BrownianMotion, 
    "Geometric Brownian Motion" : GeometricBrownianMotion, 
    "Random Walk" : RandomWalk, 
    "Brownian Sheet" : BrownianSheet,
    "Ornstein Uhlenbeck" : OrnsteinUhlenbeck
    }