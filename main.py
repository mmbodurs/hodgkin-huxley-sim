import numpy as np
import matplotlib.pyplot as plt
#TODO: Add ModelDB/NeuroElectro preset loader
DEFAULT_PARAMS = {
    "C_M":1.0,  # Membrane capacitance ($C_m$)
    "G_NA":120,      #Max sodium conductance ($\bar{g}_{Na}$)
    "G_K":36,       #Max potassium conductance ($\bar{g}_K$)
    "G_L":0.3,       #Leak conductance ($\bar{g}_L$)
    "E_NA":50,      #Sodium reversal potential ($E_{Na}$)
    "E_K":-77,       #Potassium reversal potential ($E_K$) 
    "E_L":-54.387,     #Leak reversal potential ($E_L$)
}

#Functions
def alpha_m(V):
    if np.isclose(V, -40):
        return 1.0  
    sodium_activation = (0.1 * (V + 40)) / (1 - np.exp(-(V + 40) / 10))
    return sodium_activation

def beta_m(V):
    sodium_activation = 4 * np.exp(-(V + 65) / 18)
    return sodium_activation

def alpha_h(V):
    sodium_inactivation = 0.07 * np.exp(-(V + 65) / 20)
    return sodium_inactivation

def beta_h(V):
    sodium_inactivation = 1 / (1 + np.exp(-(V + 35) / 10))
    return sodium_inactivation

def alpha_n(V):
    if np.isclose(V, -55):
        return 0.1
    potassium_activation = (0.01 * (V + 55)) / (1 - np.exp(-(V + 55) / 10))
    return potassium_activation 

def beta_n(V):
    potassium_activation = 0.125 * np.exp(-(V + 65) / 80)
    return potassium_activation

#Taking derivatives
def derivatives(state, I_ext, params=DEFAULT_PARAMS):
    state = np.array(state)
    V, m, h, n = state

    I_Na = params["G_NA"] * (m**3) * h * (V - params["E_NA"])
    I_K = params["G_K"] * (n**4) * (V - params["E_K"])
    I_L = params["G_L"] * (V - params["E_L"])

    dV = (I_ext - I_Na - I_K - I_L) / params["C_M"]
    dm = alpha_m(V) * (1 - m) - beta_m(V) * m
    dh = alpha_h(V) * (1 - h) - beta_h(V) * h
    dn = alpha_n(V) * (1 - n) - beta_n(V) * n
    return np.array([dV, dm, dh, dn])
