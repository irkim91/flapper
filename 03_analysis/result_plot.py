import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import detrend

# --- 1. Configuration & Data Load ---
# 데이터가 실제로 위치한 절대 경로 설정 [cite: 7]
processed_data_path = r'F:\flapper\06_data\02_processed'
file_name = '0206t100.csv'  # 분석하고자 하는 파일명으로 수정하세요.
file_path = os.path.join(processed_data_path, file_name)

# 결과 저장 폴더 설정 (03_analysis 폴더 하위에 생성) 
figure_root = r'F:\flapper\03_analysis\Figure_Results'
if not os.path.exists(figure_root):
    os.makedirs(figure_root)

# 데이터 로드
try:
    # bin2csv.py에서 저장할 때 헤더를 포함했으므로 header=0으로 읽어옵니다.
    df = pd.read_csv(file_path)
    data = df.values
    columns = df.columns.tolist()
    print(f"데이터 로드 성공: {file_path}")
except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {file_path}")
    exit()

# --- 2. Data Extraction (MATLAB 로직 이식) ---
# Python은 0-index이므로 MATLAB 인덱스에서 -1을 적용합니다.
dt = 1/500
Fs = 500

# Time (ms -> sec)
# CSV의 첫 번째 열이 timestamp라고 가정 (MATLAB: data(:,1))
time        = (data[:, 0] - data[0, 0]) * 0.001
pm          = data[:, 1:3]   # Power Management (V, A, W)
motor       = data[:, 4:7]   # Motor PWMs
cmd         = data[:, 8:11]  # Control Commands (T, A, E, R)
ref_eul     = data[:, 12:14] # Reference (Euler, Rates)
ref_rate    = data[:, 15:17] # Reference (Euler, Rates)
thrust      = data[:, 18]    # Thrust
pos         = data[:, 19:21] # Position (X, Y, Z)
vel         = data[:, 22:24] # Velocity (X, Y, Z)
eul         = data[:, 25:27] # Euler Angles (Roll, Pitch, Yaw)
ref_pos     = data[:, 28] # Position Reference
ref_vel     = data[:, 29:31] # Position Reference
gyro        = data[:, 32:34] # Gyro Rates (p, q, r)
acc         = data[:, 35:37] # Accelerometer (ax, ay, az)

# --- 3. Plotting Functions ---
def apply_custom_style(ax, title_y="", is_ref=False):
    ax.grid(True, linestyle='-', linewidth=0.5, alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylabel(title_y, fontsize=10)
    if is_ref:
        lines = ax.get_lines()
        if len(lines) >= 2:
            lines[0].set(color='#C43302', linewidth=1.5, label='ref')   # Deep Red
            lines[1].set(color='#0F4C81', linewidth=1.0, label='state') # Dark Navy
            ax.legend(loc='upper right', frameon=False, ncol=2, fontsize=8)

# --- 4. Visualizations ---
plt.rcParams['font.family'] = 'sans-serif'
figsize_cm = (16.93 / 2.54, 11 / 2.54)

# 1. Euler Angles Plot (Roll, Pitch, Yaw)
fig, axs = plt.subplots(3, 1, figsize=figsize_cm, sharex=True)
labels = [r'$\phi$ [deg]', r'$\theta$ [deg]', r'$\psi$ [deg]']
for i in range(3):
    # MATLAB: plot(TT, ref(:,7+i), TT, eul(:,i))
    axs[i].plot(time, ref_eul[:, i], time, eul[:, i])
    apply_custom_style(axs[i], labels[i], True)
plt.xlabel('time [sec]')
plt.tight_layout()
plt.savefig(os.path.join(figure_root, f'euler_angles_{file_name[:-4]}.png'), dpi=300)

# 2. Velocity Plot
fig, axs = plt.subplots(3, 1, figsize=figsize_cm, sharex=True)
vel_labels = ['Vel. X [m/s]', 'Vel. Y [m/s]', 'Vel. Z [m/s]']
for i in range(3):
    axs[i].plot(time, ref_vel[:, i], time, vel[:, i])
    apply_custom_style(axs[i], vel_labels[i], True)
plt.xlabel('time [sec]')
plt.tight_layout()
plt.savefig(os.path.join(figure_root, f'velocity_{file_name[:-4]}.png'), dpi=300)

print(f"분석 완료! 그래프가 다음 폴더에 저장되었습니다: {figure_root}")
plt.show()