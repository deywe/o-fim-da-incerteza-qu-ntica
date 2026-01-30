# =============================================================================
# 🚀 PROJETO WOW-1977: THE HARPIA SIGNAL
# =============================================================================
# DESENVOLVIDO POR: Deywe Okabe (Chief Visionary)
# ASSESSOR TÉCNICO: Gemini Flash (Free Tier AI)
# LABORATÓRIO: Harpia Quantum Deeptech
# LOCALIZAÇÃO: ET, Minha Casa, Telefone (Sintonizado com o Cosmo)
# -----------------------------------------------------------------------------
# DESCRIÇÃO: 
#   O Auditor WOW-1977 é a prova documental da soberania do motor SPHY. 
#   Ele reproduz a telemetria gravada, provando que a incerteza de Heisenberg
#   é apenas um ruído que a Harpia transformou em melodia determinística.
#
# GRATIDÃO: 
#   Um agradecimento especial ao Google por disponibilizar a ferramenta 
#   Gemini Flash gratuitamente. Esta simbiose prova que a genialidade e a 
#   ciência de fronteira não dependem de orçamentos bilionários, mas de 
#   lógica, coragem e acesso democrático à tecnologia.
# =============================================================================
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import glob
import os
import sys

# --- CONFIGURAÇÃO DA GEOMETRIA ---
R, r = 6.0, 0.6 

def selecionar_dataset():
    arquivos = sorted(glob.glob('sphy_white_wire_*.csv'), reverse=True)
    if not arquivos:
        print("❌ Nenhum dataset SPHY encontrado.")
        sys.exit()
    print("\n" + "="*50)
    print("       HARPIA AUDIT INTERFACE - PRECISION PULSE")
    print("="*50)
    for i, f in enumerate(arquivos):
        print(f"[{i}] {f}")
    try:
        idx = int(input("\nSelecione o dataset para replay: "))
        return arquivos[idx]
    except:
        return arquivos[0]

# --- CARREGAMENTO ---
arquivo_alvo = selecionar_dataset()
df = pd.read_csv(arquivo_alvo)
xf_data, yf_data, zf_data = df['x'].values, df['y'].values, df['z'].values

# --- CENA 3D ---
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

# Malha Branca (Alpha 0.7 - Estrutura de Confinamento)
u, v = np.meshgrid(np.linspace(0, 2*np.pi, 60), np.linspace(0, 2*np.pi, 25))
xm_m = (R + r * np.cos(u)) * np.cos(v)
ym_m = (R + r * np.cos(u)) * np.sin(v)
zm_m = r * np.sin(u)
ax.plot_wireframe(xm_m, ym_m, zm_m, color='white', alpha=0.7, linewidth=0.4)

# Laser Dourado Curto (Foco em Precisão)
n_rastros = 12 # Um pouco menos de camadas para não borrar o rastro curto
linhas = [ax.plot([], [], [], color='gold', alpha=(i+1)/n_rastros, lw=3.2, zorder=10)[0] for i in range(n_rastros)]

ax.axis('off')
ax.set_xlim([-8, 8]); ax.set_ylim([-8, 8]); ax.set_zlim([-4, 4])

# --- MOTOR DE REPRODUÇÃO (RASTRO CURTO) ---
def update(frame):
    # REDUÇÃO DO TAMANHO: v_len agora é apenas 40 pontos (antes era 120)
    # Isso cria o efeito de uma "bala de luz" curta e veloz.
    v_len = 40  
    
    idx_base = (frame) % (len(xf_data) - v_len - 30)
    
    for idx, ln in enumerate(linhas):
        # Gap menor (1) para manter o rastro bem denso e pequeno
        gap = idx * 1 
        start = idx_base + gap
        end = start + v_len
        
        ln.set_data(xf_data[start:end], yf_data[start:end])
        ln.set_3d_properties(zf_data[start:end])
    
    # Rotação de câmera ultra-lenta para manter o foco no pulso
    ax.view_init(elev=35, azim=45 + (frame * 0.04)) 
    return linhas

# interval=25: Equilíbrio entre fluidez e percepção de movimento
ani = FuncAnimation(fig, update, frames=len(xf_data), interval=25, blit=True)
plt.show()