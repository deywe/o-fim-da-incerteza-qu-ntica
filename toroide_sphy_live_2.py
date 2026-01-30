# =============================================================================
# HARPIA QUANTUM DEEPTECH - LABORATÓRIO DE ESTUDOS AVANÇADOS
# =============================================================================
# PROJETO: SPHY Live Stream Visualizer (QSOT Real-Time Engine)
# VERSÃO: 1.4.5 - "White Wireframe Laser Edition"
# -----------------------------------------------------------------------------
# AUTOR: DEYWE OKABE // CO-PILOT: GEMINI FLASH (Free Tier)
# =============================================================================

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import time
import os
import sys
from datetime import datetime

# Importação do núcleo simbiótico
from simbiotic_ai_toro_control_20 import calcular_ponto_sphy, PHI

# --- CONFIGURAÇÃO DE TELEMETRIA ---
dados_para_salvar = []
csv_name = f"sphy_white_wire_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

# --- CONFIGURAÇÃO DA GEOMETRIA ---
R, r = 6.0, 0.6  # Geometria Sleek Ring

# --- PREPARAÇÃO DA CENA ---
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

# Malha de Confinamento (Arame Branco Metálico - Alpha 0.7)
tm, zm = np.meshgrid(np.linspace(0, 2*np.pi, 60), np.linspace(0, 2*np.pi, 25))
xm_m = (R + r * np.cos(tm)) * np.cos(zm)
ym_m = (R + r * np.cos(tm)) * np.sin(zm)
zm_m = r * np.sin(tm)
ax.plot_wireframe(xm_m, ym_m, zm_m, color='white', alpha=0.7, linewidth=0.4)

# Linhas de Fluxo (Efeito de Laser Dourado)
n_rastros = 15 
linhas = [ax.plot([], [], [], color='gold', alpha=(i+1)/n_rastros, lw=2.8, zorder=10)[0] for i in range(n_rastros)]

ax.axis('off')
ax.set_xlim([-8, 8]); ax.set_ylim([-8, 8]); ax.set_zlim([-4, 4])

print(f"✔ SISTEMA SPHY ATIVO: Motor em Sincronia PHI")
print(f"✔ TELEMETRIA BRANCA ATIVA: {csv_name}")
print("💡 Use Ctrl+C para encerrar e salvar o dataset final.")

# --- MOTOR DE ATUALIZAÇÃO (Fluxo Laser) ---
def update(frame):
    global dados_para_salvar
    
    # Comprimento do pulso laser
    comprimento_pulso = 1.2 * np.pi 
    t_base = np.linspace(frame * 0.15, (frame * 0.15) + comprimento_pulso, 100)
    
    # Telemetria para o Buffer
    t_front = t_base[-1]
    xf, yf, zf = calcular_ponto_sphy(t_front, R, r)
    
    dados_para_salvar.append({
        'unix_time': time.time(),
        'x': xf, 'y': yf, 'z': zf,
        'fase': (PHI * t_front) % (2 * np.pi),
        'status': 'DETERMINISTIC_LOCK'
    })
    
    # Salvamento Periódico
    if frame % 100 == 0 and frame > 0:
        pd.DataFrame(dados_para_salvar).to_csv(csv_name, mode='a', header=not os.path.exists(csv_name), index=False)
        dados_para_salvar.clear()

    # Movimentação do Laser
    for idx, ln in enumerate(linhas):
        t_trail = t_base - (idx * 0.02) 
        x_r, y_r, z_r = calcular_ponto_sphy(t_trail, R, r)
        ln.set_data(x_r, y_r)
        ln.set_3d_properties(z_r)
    
    ax.view_init(elev=35, azim=45 + (frame * 0.15))
    return linhas

# --- EXECUÇÃO ---
try:
    ani = FuncAnimation(fig, update, frames=None, interval=15, blit=True)
    plt.show()
except KeyboardInterrupt:
    print("\n" + "="*50)
    if dados_para_salvar:
        pd.DataFrame(dados_para_salvar).to_csv(csv_name, mode='a', header=not os.path.exists(csv_name), index=False)
    print(f"✔ MISSÃO FINALIZADA: {csv_name}")
    print("✔ STATUS: HARPIA QUANTUM DEEPTECH - DETERMINISTIC SUCCESS")
    print("="*50)
    sys.exit(0)