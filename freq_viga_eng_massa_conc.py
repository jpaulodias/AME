# -*- coding: utf-8 -*-
"""
@autor: jpdsp
24.11.22

Código para encontrar a frequência natural de uma viga engastada-livre com uma massa concentrada na ponta.

"""

import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt


def f(x, alpha):
    # Expressão das frequências naturais de uma viga engastada-livre com uma
    # massa m_a concentrada na ponta, tal que alpha = m_a / (rho * A * L)

    y = 1 + np.cosh(x) * np.cos(x) + alpha * x * (np.sinh(x) * np.cos(x) - np.cosh(x) * np.sin(x))

    return y


'''
Entrada dos parâmetros físicos e geométricos do sistema
'''
m_a = 5e-3              # Massa concentrada na ponta da viga (kg)
rho = 1050              # Massa específica da viga (kg/m³)
b = 0.0335              # Largura da seção transversal da viga (m)
h = 0.003               # Altura da seção transversal da viga (m)
A = b * h               # Área da seção transversal da viga (m²)
L = 0.25                # Comprimento da viga (m)
E = 2.78e9              # Módulo de elasticidade do material da viga (Pa)
I = b * h ** 3 / 12     # Momento de inércia da seção transversal (m^4)

print('\nComprimento da viga:', L, 'm')
print('Massa da viga:', round(rho * A * L, 3), 'kg')
print('Massa concentrada na ponta da viga:', m_a, 'kg\n')

alpha = m_a / (rho * A * L)

# print(alpha)

'''
Plotagem da função para identificação visual das raízes e escolha do chute inicial
'''
x = np.linspace(-7.5, 7.5, 201)

plt.plot(x, f(x, alpha))
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid()
# plt.show()

x_chute_inicial = 1.5
x_solucao = fsolve(f, x_chute_inicial, args=(alpha))

# print(x_solucao)

'''
Cálculo da frequência natural
'''
omega_w = np.sqrt(E * I / (rho * A * L ** 4))
omega = x_solucao ** 2 * omega_w        # Frequência natural angular da viga
f_n = omega / (2 * np.pi)               # Frequência natural linear da viga

# print('Frequência angular:', round(omega [0], 2), 'Hz\n')
print('Frequência natural:', round(f_n[0], 2), 'Hz\n')
