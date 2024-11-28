# -*- coding: utf-8 -*-
"""
@autor: jpdsp
24.11.21

Aplicação da transformada discreta de Fourier (DFT) em um sinal temporal.
O algoritmo da transformada rápida de Fourier (FFT) pode ser utilizado caso
o número de amostras seja uma potência de 2 (N = 2^k, k = 1, 2, 3...).

"""

import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
import time
import os

# Início da contagem do tempo do programa.
start_time = time.time()
from datetime import datetime
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
np.set_printoptions(suppress=True)
np.seterr(divide='ignore', invalid='ignore')


def ler_CSV(path):
    # Retorna uma numpy.array com os dados do arquivo .CSV, com a
    # primeira linha referente ao tempo e a segunda às medições.

    with open(path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        data_array = np.transpose(np.array(data, dtype = float))

    return data_array


def converter_tempo(data, const):
    # Converte a unidade de tempo multiplicando por uma constante.
    # Obs.: não afeta os valores da medição.
    
    data[0,:] *= const

    return data


def converter_medicao(data, const):
    # Converte a unidade da medição multiplicando por uma constante.
    # Obs.: não afeta o vetor de tempo.
    
    data[1,:] *= const

    return data


def interpolar(data, T):
    # Interpola as medições considerando um vetor de tempo com Δt uniforme.

    t = data[0]
    x = data[1]
    N = len(t)

    t_unif = np.linspace(0, T, N)

    med_unif = np.interp(t_unif, t, x)

    data_unif = np.array([t_unif, med_unif])

    return data_unif


def dft(x):
    # Converte os dados temporais para o domínio da frequência usando
    # a Transformada Discreta de Fourier (DFT).

    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(-2j * np.pi * k * n / N)
    dft = np.dot(M, x)

    return dft


def fft(x):
    # Aplica o algoritmo de otimização da Transformada Rápida de Fourier para
    # converter os dados temporais para o domínio da frequência.
    # Obs.: o vetor de dados precisa ter comprimento igual a 2^k, k = 1, 2, 3...
    
    N = len(x)

    if N == 1:
        return x
    else:
        X_par = fft(x[::2])
        X_impar = fft(x[1::2])
        C = np.exp(-2j * np.pi * np.arange(N)/N)

        X = np.concatenate([X_par + C[:int(N/2)] * X_impar, X_par + C[int(N/2):] * X_impar])
        
        return X


def PSD(data, T):
    # Converte a transformada de Fourier para densidade espectral.

    x = data[1]

    N = len(x)                                      # Comprimento do sinal
    f_s = N/T                                       # Frequência de amostragem (Hz)
    print('\nIntervalo de análise: T = ', T, " s\n")
    print('Número de amostras: N = ', N, "\n")
    print('Frequência de amostragem: f_s =', f_s, " Hz\n")
    df = 1/T                                        # Resolução de frequência (Hz)
    f_i = 0                                         # Frequência inicial considerada (Hz)
    f_f = f_s / 2                                   # Frequência final considerada (Hz)
    f = np.linspace(f_i, f_s, N, endpoint=False)    # Vetor de frequências (Hz)

    X = dft(x)                                   # Conversão do sinal para o domínio da frequência

    n_oneside = N // 2
    f_oneside = f[:n_oneside]
    X_oneside = X[:n_oneside]
    abs = np.abs(X_oneside)                         # Valor absoluto da transformada (desconsideração da parcela complexa)

    A = 2 * abs / N                                 # Amplitudes

    PSD =  abs**2 / (N * f_s)                       # Conversão para densidade espectral

    X = np.array([f_oneside, PSD])

    return X


def plot_tempo(data, T, titulo, path):
    # Plota o sinal medido no domínio do tempo.

    now = datetime.now()

    t = data[0]
    y = data[1]

    lim_x = T
    lim_y = int(y[np.argmax(np.abs(y))])
    
    plt.figure(1, figsize=(6, 5.25))
    plt.style.use('classic')
    plt.grid(True)
    # plt.title(titulo)
    plt.ylabel(r'$a_z\,(t)\;\;[g]$', fontsize=20)
    plt.text(0.025 * lim_x, 1.1 * lim_y, "$a_{{z,max}} = {0}".format(round(y[np.argmax(np.abs(y))], 1)) +
        r"\,g" + "$\n$t_{{max}}={0}".format(round(t[np.argmax(np.abs(y))], 2)) +
        r"\,s$" # + "\n" + r"$\sigma={0}".format(round(np.std(y), 1)) + r"\:mm"+ "$"
        , ha = 'left', va = 'top', fontsize=15, bbox=dict(facecolor="white", alpha=1))
    plt.xlabel(r'$t\;\;[s]$', fontsize=20)
    plt.xlim([0, lim_x])
    plt.ylim([-lim_y, lim_y])
    plt.tick_params(axis='x', which='major', bottom=True, top=False, labelsize=15)
    plt.tick_params(axis='y', which='major', left=True, right=False, labelsize=15)
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ['$0$', '$1$', '$2$', '$3$', '$4$', '$5$', '$6$', '$7$', '$8$', '$9$', '$10$'])
    plt.yticks([-20, -16, -12, -8, -4, 0, 4, 8, 12, 16, 20],
        ['$-20$', '$-16$','$-12$', '$-8$', '$-4$', '$0$', '$4$', '$8$', '$12$', '$16$', '$20$'])
    plt.plot(t, y)
    if y[np.argmax(np.abs(y))] > 0:
        plt.plot(t[np.argmax(np.abs(y))], max(np.abs(y)), 'wo')
    else:
        plt.plot(t[np.argmax(np.abs(y))], -max(np.abs(y)), 'wo')
    plt.tight_layout()
    plt.savefig(path + '\\Saídas\\resp_tempo_' + now.strftime("%d-%m-%Y_%H-%M-%S") + '.jpg')
    plt.show()
    plt.close()


def plot_freq(X, T, titulo, path):
    # Plota a densidade espectral do sinal medido.
    
    now = datetime.now()

    f = X[0]
    x = X[1]

    N = len(x)                                     
    f_s = N/T

    lim_x = 15 # f_s
    lim_y = round(max(np.abs(x)), 2)

    plt.figure(2, figsize=(6, 5.25))
    plt.style.use('classic')
    plt.grid(True)
    # plt.title(titulo)
    plt.ylabel(r'$S\,(f)\;\;[g^2\,s]$', fontsize=22)
    plt.xlabel(r'$f\;\;[Hz]$', fontsize=22)
    plt.text(0.025 * lim_x, 1.105 * lim_y, "$S_{{max}} = {0}".format(round(x[np.argmax(np.abs(x))], 2)) +
        r"\,g^2\,s" + "$\n$f_{{max}}={0}".format(round(f[np.argmax(np.abs(x))], 2)) +
        r"\,Hz$" # + "\n" + r"$\sigma={0}".format(round(np.std(y), 1)) + r"\:mm"+ "$"
        , ha = 'left', va = 'top', fontsize=17, bbox=dict(facecolor="white", alpha=1))
    # plt.xscale('log') 
    plt.xlim([0, lim_x])
    plt.ylim([0, lim_y])
    plt.tick_params(axis='x', which='major', bottom=True, top=False, labelsize=17)
    plt.tick_params(axis='y', which='major', left=True, right=False, labelsize=17)
    plt.xticks([0, 5, 10, 15], ['$0$', '$5$', '$10$', '$15$'])
    plt.yticks([0, 10, 20, 30, 40, 50, 60, 70], ['$0$', '$10$', '$20$', '$30$', '$40$', '$50$', '$60$', '$70$'])
    plt.plot(f, x)
    plt.plot(f[np.argmax(np.abs(x))], max(np.abs(x)), 'wo')
    plt.tight_layout()
    plt.savefig(path + '\\Saídas\\resp_freq_' + now.strftime("%d-%m-%Y_%H-%M-%S") + '.jpg')
    plt.show()
    plt.close()


'''
Leitura do arquivo .CSV em uma numpy.array.
'''
path = str(os.getcwd()) + '\\Medição de viga engastada livre em vibração livre\\medida_acel\\'      # Caminho da pasta com o arquivo da medição
file_name = 'Entradas\\acel_t=10s_22.csv'                                                                      # Nome do arquivo .CSV com os dados das medições
full_path = path + file_name                                                                             # Caminho do arquivo .CSV com os dados da medição

data = ler_CSV(full_path)            # Matriz 2 x N com o registro de tempo (linha 0) e as respectivas medições (linha 1)

'''
Conversão do vetor de tempo para segundos e definição do intervalo de análise.
'''
converter_tempo(data, 0.001)    # Conversão de milissegundos para segundos
T = 10                          # Intervalo de análise em segundos

'''
Conversão da medição através da multiplicação por uma constante.
Obs.: o MPU6050 lê a aceleração em unidade g. Para converter para m/s²,
basta multiplicar pela aceleração da gravidade.
'''
# g = 9.787899                  # Aceleração da gravidade em m/s²
# data = converter(data, g)     # Converte a unidade da medição multiplicando por uma constante

'''
Interpolação dos dados para um vetor de tempo com Δt uniforme,
de modo a possibilitar a aplicação da DFT.
'''
data = interpolar(data, T)

'''
Plotagem do sinal no domínio do tempo.
'''
titulo = '$Aceleração\;vertical\;de\;viga\;engastada\;livre$\n'
plot_tempo(data, T, titulo, path)

'''
Obtenção do sinal no domínio da frequência através da transformada discreta de Fourier (DFT)
e conversão das amplitudes para densidade espectral.
Obs.: caso o sinal discreto possua comprimento igual a 2^k, k = 1, 2, 3..., o algoritmo da
transformada rápida de Fourier (FFT) pode ser aplicado.
Obs. 2: o sinal no domínio da frequência é espelhado em torno de f = 0. Logo, as amplitudes
são obtidas até N / 2 para evitar duplicidade.
'''
X = PSD(data, T)

plot_freq(X, T, titulo, path)

#endregion

# Fim do processamento
now = datetime.now()
print('')
print('Fim\n' + now.strftime("%d/%m/%Y %H:%M:%S"))
print("\nTempo de processamento: %s segundos\n" % (int(time.time() - start_time)))
