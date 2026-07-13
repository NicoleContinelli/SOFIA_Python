from model.sensor import Sensor
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from timeit import default_timer as timer


# ============================================================
# PLOT
# ============================================================
def plot_two_function(title, y1_1, y1_2, y2_1, y2_2, t,
                      color1, color2, label1, label2, label3):
    plt.figure(figsize=(15, 15))

    plt.subplot(2, 1, 1)
    plt.grid()
    plt.plot(t, y1_1, color=color1, label=label1, linestyle='dashdot', linewidth=3.5)
    plt.plot(t, y1_2, color=color2, label=label2, linewidth=1.5)
    plt.ylabel("Inclination (degrees)")
    plt.title(title)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.grid()
    plt.xlabel("Time (seconds)")
    plt.ylabel("Orientation (degrees)")
    plt.plot(t, y2_1, color=color1, label=label1, linestyle='dashdot', linewidth=3.5)
    plt.plot(t, y2_2, color=color2, label=label3, linewidth=1.5)
    plt.legend()
    plt.savefig("PINN_robot_one_pos_pt_3_13072026.png")
    plt.show()


# ============================================================
# ARQUITECTURA
# ============================================================

class AngularEncoding(nn.Module):
    """
    Entrada = [alpha_normalizado, sin(beta), cos(beta)]
    """
    def __init__(self):
        super().__init__()
        self.alpha_scale = np.deg2rad(35.0)
        self.out_dim = 3

    def forward(self, alpha, beta):
        alpha_norm = alpha / self.alpha_scale
        x = torch.stack([
            alpha_norm,
            torch.sin(beta),
            torch.cos(beta)
        ], dim=1)
        return x


class FourierEncoding(nn.Module):
    """
    Entrada = Fourier features.
    gamma(x) = [sin(2*pi*B*x), cos(2*pi*B*x)]
    x = [alpha_normalizado, beta_normalizado]
    """
    def __init__(self, num_frequencies=16, sigma=1.0):
        super().__init__()

        self.alpha_scale = np.deg2rad(35.0)
        self.beta_scale = np.pi

        B = torch.randn(num_frequencies, 2) * sigma
        self.register_buffer("B", B)

        self.out_dim = 2 * num_frequencies

    def forward(self, alpha, beta):
        alpha_norm = alpha / self.alpha_scale
        beta_norm = beta / self.beta_scale

        x = torch.stack([alpha_norm, beta_norm], dim=1)
        projection = 2.0 * np.pi * x @ self.B.T

        encoded = torch.cat([
            torch.sin(projection),
            torch.cos(projection)
        ], dim=1)

        return encoded


class CorrectionPINN(nn.Module):
    """
    Predice delta_alpha y delta_beta
    """
    def __init__(
        self,
        encoding_type="angular",
        hidden=50,
        depth=4,
        max_dalpha_deg=15.0,
        max_dbeta_deg=10.0,
    ):
        super().__init__()

        if encoding_type == "angular":
            self.encoder = AngularEncoding()
        elif encoding_type == "fourier":
            self.encoder = FourierEncoding(num_frequencies=16, sigma=1.0)
        else:
            raise ValueError("encoding_type debe ser 'angular' o 'fourier'")

        layers = []
        in_dim = self.encoder.out_dim

        for i in range(depth):
            layers.append(nn.Linear(in_dim if i == 0 else hidden, hidden))
            layers.append(nn.GELU())
            layers.append(nn.Dropout(p=0.05))

        layers.append(nn.Linear(hidden, 2))
        self.net = nn.Sequential(*layers)

        self.max_dalpha = np.deg2rad(max_dalpha_deg)
        self.max_dbeta = np.deg2rad(max_dbeta_deg)

    def forward(self, alpha, beta):
        x = self.encoder(alpha, beta)
        raw = self.net(x)

        d_alpha = self.max_dalpha * torch.tanh(raw[:, 0])
        d_beta = self.max_dbeta * torch.tanh(raw[:, 1])

        return d_alpha, d_beta


# ============================================================
# CARGAR CHECKPOINT .PT
# ============================================================
MODEL_PATH = "/home/sofia/SOFIA_Python/ml/PINN_model/pinn_neck_fourier_final.pt"   # cambia ruta
device = torch.device("cpu")

checkpoint = torch.load(MODEL_PATH, map_location=device)

model_cfg = checkpoint["model_config"]
phys_cfg = checkpoint.get("physical_params", {})

model = CorrectionPINN(
    encoding_type=model_cfg["encoding_type"],
    hidden=model_cfg["hidden"],
    depth=model_cfg["depth"],
    max_dalpha_deg=model_cfg["max_dalpha_deg"],
    max_dbeta_deg=model_cfg["max_dbeta_deg"],
).to(device)

model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

BETA_OFFSET = phys_cfg.get("BETA_OFFSET", -np.pi / 2.0)

print("Modelo cargado correctamente")
print("Encoding:", model_cfg["encoding_type"])
print("hidden:", model_cfg["hidden"])
print("depth:", model_cfg["depth"])
print("max_dalpha_deg:", model_cfg["max_dalpha_deg"])
print("max_dbeta_deg:", model_cfg["max_dbeta_deg"])
print("BETA_OFFSET:", BETA_OFFSET)


# ============================================================
# FUNCION DE CORRECCION
# ============================================================
def correct_pose_with_pinn(incli_deg, orient_deg, model, beta_offset_rad, device="cpu"):
    """
    Entrada: pose deseada en grados
    Salida:
      - pose corregida en grados
      - correcciones en grados
    """
    alpha = torch.tensor([np.deg2rad(incli_deg)], dtype=torch.float32, device=device)
    beta = torch.tensor([np.deg2rad(orient_deg)], dtype=torch.float32, device=device)

    # mismo preprocesado que en entrenamiento
    beta_model = beta + beta_offset_rad

    with torch.no_grad():
        d_alpha, d_beta = model(alpha, beta_model)

    alpha_tilde = alpha + d_alpha
    beta_tilde = beta_model + d_beta

    incli_corr_deg = np.rad2deg(alpha_tilde.item())
    orient_corr_deg = np.rad2deg(beta_tilde.item())

    d_alpha_deg = np.rad2deg(d_alpha.item())
    d_beta_deg = np.rad2deg(d_beta.item())

    return incli_corr_deg, orient_corr_deg, d_alpha_deg, d_beta_deg


# ============================================================
# HARDWARE
# ============================================================
motors = SystemMotors(3)
motors.loadMotors([1, 2, 3], "SoftNeckMotorConfig.json")
motors.startMotors()

mi_sensor = Sensor()
mi_sensor.sensorStream()


# ============================================================
# TARGET
# ============================================================
incli_target = 10
orient_target = 50

incli_corr, orient_corr, d_alpha_deg, d_beta_deg = correct_pose_with_pinn(
    incli_target,
    orient_target,
    model,
    BETA_OFFSET,
    device=device
)

print("=== Corrección PINN ===")
print(f"Target I/O: {incli_target:.2f}, {orient_target:.2f}")
print(f"d_alpha: {d_alpha_deg:.4f} deg")
print(f"d_beta : {d_beta_deg:.4f} deg")
print(f"I/O corregidas: {incli_corr:.4f}, {orient_corr:.4f}")

# IK usando la pose corregida
# Tu clase parece usar grados, por eso le pasamos grados
kine1 = InverseKinematics(incli_corr, orient_corr)
theta1, theta2, theta3 = kine1.neckInverseKinematics()

print("Theta command:")
print(theta1, theta2, theta3)

motors.setupPositionsMode(15, 15)
motors.setPositions([theta1, theta2, theta3])


# ============================================================
# LOOP PARA MEDIR UNA POSICION
# ============================================================
incli_data = []
orient_data = []
time_data = []

list_incli_target = []
list_orient_target = []

CSV_OUT = "/home/sofia/SOFIA_Python/data/Data_2026/one_pos_PINN_pt_fourier_13072026.csv"

start_time = timer()

for _ in np.arange(0, 14, 0.05):
    motors.setPositions([theta1, theta2, theta3])

    ik_incli, ik_orient = mi_sensor.readSensorNeck(mi_sensor)

    end_time = timer()
    elapsed_time = end_time - start_time

    incli_data.append(ik_incli)
    orient_data.append(ik_orient)

    list_incli_target.append(incli_target)
    list_orient_target.append(orient_target)

    time_data.append(elapsed_time)

    data = {
        "Real Incli": incli_data,
        "Real Orient": orient_data,
        "Time": time_data,
        "Target Incli": list_incli_target,
        "Target Orient": list_orient_target,
        "PINN Corrected Incli": [incli_corr] * len(incli_data),
        "PINN Corrected Orient": [orient_corr] * len(incli_data),
        "d_alpha_deg": [d_alpha_deg] * len(incli_data),
        "d_beta_deg": [d_beta_deg] * len(incli_data),
        "theta1_cmd": [theta1] * len(incli_data),
        "theta2_cmd": [theta2] * len(incli_data),
        "theta3_cmd": [theta3] * len(incli_data),
        "encoding_type": [model_cfg["encoding_type"]] * len(incli_data),
    }
    #quiero pich roll del sensor imprimir en pantalla   
    #print(f"Pitch: {mi_sensor.getPitch():.2f}, Roll: {mi_sensor.getRoll():.2f}")
    
    df = pd.DataFrame(data)
    df.to_csv(CSV_OUT, index=False)


# ============================================================
# GRAFICA
# ============================================================
plot_two_function(
    f"Control con PINN + IK ({model_cfg['encoding_type']})",
    list_incli_target,
    incli_data,
    list_orient_target,
    orient_data,
    time_data,
    "black",
    "#C70039",
    "Target",
    "Inclination - IMU",
    "Orientation - IMU"
)

motors.setPositions([0, 0, 0])

print("Final error Inclination:", round(incli_target - incli_data[-1], 2))
print("Final error Orientation:", round(orient_target - orient_data[-1], 2))