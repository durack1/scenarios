#!/usr/bin/env python3
"""
makeFig.py
CO2 emissions trajectories across CMIP scenario generations.
Message: "futures avoided, opportunities lost"

Usage:
    micromamba run -n xcd0112 python3 makeFig.py
"""

import csv
import urllib.request
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import PchipInterpolator

# ─── constants ────────────────────────────────────────────────────────────────

C_TO_CO2 = 44.0 / 12.0  # PgC or GtC → Gt CO₂
T_FINE = np.arange(1985, 2101, 1.0)
OUT_DIR = Path(__file__).parent

GEN_COLORS = {
    "SA90":  "#8B4513",
    "IS92":  "#808080",
    "SRES":  "#FF8C00",
    "RCP":   "#1E90FF",
    "SSP":   "#2E8B57",
    "CMIP7": "#9400D3",
}

# ─── interpolation ────────────────────────────────────────────────────────────

def interp(t_orig, values):
    """PchipInterpolate to T_FINE; NaN outside native range."""
    vals = np.array([np.nan if v is None else float(v) for v in values])
    t = np.asarray(t_orig, dtype=float)
    mask = ~np.isnan(vals)
    t_v, v_v = t[mask], vals[mask]
    if len(t_v) < 2:
        return np.full_like(T_FINE, np.nan)
    return PchipInterpolator(t_v, v_v, extrapolate=False)(T_FINE)

# ─── SA90 ─────────────────────────────────────────────────────────────────────

SA90_TIME = [1985, 2000, 2025, 2050, 2075, 2100]
SA90 = {
    "SA90: 2030 High Emissions":        [6.0, 7.7, 11.5, 15.2, 18.7, 22.4],
    "SA90: 2060 Low Emissions":         [5.9, 5.5,  6.4,  7.5,  8.8, 10.3],
    "SA90: Control Policies":           [5.9, 5.6,  6.3,  7.1,  5.1,  3.5],
    "SA90: Accelerated Policies":       [6.0, 5.6,  5.1,  2.9,  3.0,  2.7],
    "SA90: Alt. Accelerated Policies":  [6.0, 4.6,  3.8,  3.7,  3.5,  2.6],
}
SA90_MARKERS = {"SA90: 2030 High Emissions", "SA90: Accelerated Policies"}

# ─── IS92 ─────────────────────────────────────────────────────────────────────

IS92_TIME = [1990, 2000, 2025, 2050, 2100]
IS92 = {
    "IS92a (updated)": [7.4, 8.4, 12.2, 14.5, 20.3],
    "IS92a":           [6.0, 7.0, 10.7, 13.2, 19.8],
    "IS92b":           [6.0, 6.8, 10.3, 12.5, 18.6],
    "IS92c":           [6.0, 6.0,  7.4,  6.5,  4.6],
    "IS92d":           [6.0, 6.4,  8.6,  8.4,  9.9],
    "IS92e":           [6.0, 7.6, 13.5, 18.6, 34.9],
    "IS92f":           [6.0, 7.3, 12.6, 15.8, 25.9],
}
IS92_MARKERS = {"IS92a", "IS92e", "IS92c"}

# ─── SRES ─────────────────────────────────────────────────────────────────────

SRES_TIME = [1990, 2000, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]
SRES = {
    "A1B-AIM":      [7.10, 7.97, 10.88, 12.64, 14.48, 15.35, 16.38, 16.00, 15.73, 15.18, 14.30, 13.49],
    "A1B-ASF":      [7.10, 7.97, 11.13, 15.91, 20.62, 23.59, 26.56, 24.72, 22.87, 21.15, 19.53, 17.92],
    "A1B-IMAGE":    [7.10, 7.97,  9.27, 12.11, 15.00, 17.61, 18.71, 18.45, 18.02, 16.96, 15.07, 13.39],
    "A1B-MARIA":    [7.10, 7.97,  8.80,  9.61, 10.44, 11.51, 13.01, 12.87, 13.50, 14.07, 15.86, 16.44],  # fixed 12,87→12.87
    "A1B-MESSAGE":  [7.10, 7.97,  9.36, 10.81, 13.33, 15.56, 16.45, 17.81, 18.70, 17.83, 15.44, 13.83],
    "A1B-MiniCAM":  [7.10, 7.97,  9.60, 12.33, 15.13, 17.35, 19.19, 19.64, 20.24, 20.98, 18.43, 15.96],
    "A1C-AIM":      [7.10, 7.97, 11.79, 16.12, 20.06, 22.88, 26.91, 28.51, 30.26, 32.23, 34.41, 36.75],
    "A1C-MESSAGE":  [7.10, 7.97,  9.65, 11.23, 14.17, 17.16, 20.62, 24.47, 27.33, 29.03, 30.78, 32.07],
    "A1C-MiniCAM":  [7.10, 7.97,  9.66, 12.54, 16.14, 20.48, 25.37, 26.27, 26.64, 26.46, 26.09, 25.89],
    "A1G-AIM":      [7.10, 7.97, 11.11, 14.87, 18.01, 21.44, 25.62, 27.08, 28.67, 29.76, 30.26, 30.79],
    "A1G-MESSAGE":  [7.10, 7.97,  9.54, 10.91, 14.12, 17.61, 21.42, 26.08, 29.04, 30.55, 31.13, 30.31],
    "A1FI-MiniCAM": [7.10, 7.97,  9.73, 12.73, 16.19, 19.97, 23.90, 25.69, 27.28, 28.68, 28.42, 28.24],
    "A1T-AIM":      [7.10, 7.97,  9.81, 11.52, 12.15, 11.67, 11.28, 10.49,  9.63,  9.29,  8.97,  8.66],
    "A1T-MESSAGE":  [7.10, 7.97,  9.38, 10.26, 12.38, 12.65, 12.26, 11.38,  9.87,  8.02,  6.26,  4.32],
    "A1T-MARIA":    [7.10, 7.97,  8.70,  9.39,  9.82, 10.58, 11.26, 10.43,  9.85,  9.18,  8.94,  9.10],
    "A1v1-MiniCAM": [7.10, 7.97,  9.16, 11.35, 13.29, 14.97, 16.53, 17.14, 17.53, 17.70, 16.83, 15.98],
    "A1v2-MiniCAM": [7.10, 7.97,  9.23, 11.42, 13.34, 14.78, 16.10, 16.49, 16.80, 17.04, 16.47, 15.93],
    "A2-AIM":       [7.10, 7.97, 10.22, 11.36, 13.72, 15.31, 17.23, 19.47, 22.07, 25.38, 29.56, 34.47],
    "A2-ASF":       [7.10, 7.97,  9.58, 12.25, 14.72, 16.07, 17.43, 19.16, 20.89, 23.22, 26.15, 29.09],
    "A2G-IMAGE":    [7.10, 7.97, 10.02, 12.08, 14.39, 16.70, 19.01, 19.12, 19.23, 19.34, 19.45, 19.56],
    "A2-MESSAGE":   [7.10, 7.97,  9.45, 11.46, 13.33, 14.62, 15.91, 17.05, 18.76, 21.32, 25.00, 28.19],
    "A2-MiniCAM":   [7.10, 7.97,  9.12, 10.83, 12.19, 13.96, 16.15, 18.44, 20.83, 23.32, 26.19, 29.30],
    "A2-A1-MiniCAM":[7.10, 7.97,  8.39,  8.51,  8.50,  9.24, 11.05, 12.52, 14.87, 18.08, 20.38, 22.89],
    "B1-AIM":       [7.10, 7.97,  9.39, 10.28, 11.22, 11.69, 12.35, 10.84,  9.67,  8.20,  7.06,  6.15],
    "B1-ASF":       [7.10, 7.97, 10.76, 14.46, 16.85, 17.59, 18.33, 15.29, 12.24,  9.86,  8.13,  6.41],
    "B1-IMAGE":     [7.10, 7.97,  9.28, 10.63, 11.11, 11.72, 11.29,  9.74,  8.18,  6.70,  5.32,  4.23],
    "B1-MARIA":     [7.10, 7.97,  8.25,  8.71,  9.31,  9.85,  9.64,  8.80,  8.05,  7.88,  7.90,  8.19],
    "B1-MESSAGE":   [7.10, 7.97,  9.05,  9.16,  9.27,  9.25,  8.57,  7.74,  6.75,  5.79,  4.63,  4.04],
    "B1-MiniCAM":   [7.10, 7.97,  8.38,  9.53, 10.13,  9.94,  9.45,  8.94,  8.08,  6.87,  6.07,  5.28],
    "B1T-MESSAGE":  [7.10, 7.97,  9.05,  9.08,  9.11,  8.95,  7.81,  6.63,  5.35,  4.35,  3.35,  2.68],
    "B1High-MESSAGE":[7.10, 7.97,  8.69,  8.96,  9.32,  9.61,  9.44,  8.94,  8.03,  7.06,  6.38,  5.68],
    "B1High-MiniCAM":[7.10, 7.97,  8.82, 10.48, 11.70, 12.09, 12.18, 12.35, 12.21, 11.74, 11.08, 10.43],
    "B2-AIM":       [7.10, 7.97,  9.43, 10.47, 11.90, 13.36, 15.20, 15.07, 15.01, 14.76, 14.41, 14.04],
    "B2-ASF":       [7.10, 7.97,  9.97, 12.73, 14.75, 15.51, 16.27, 16.52, 16.78, 17.35, 18.24, 19.13],
    "B2-IMAGE":     [7.10, 7.97,  9.19, 10.40, 11.06, 11.71, 12.36, 12.04, 11.72, 11.40, 11.07, 10.75],
    "B2-MARIA":     [7.10, 7.97,  8.84,  9.93, 11.05, 12.70, 13.70, 14.55, 14.96, 15.16, 15.20, 15.15],
    "B2-MESSAGE":   [7.10, 7.97,  8.78,  9.05,  9.90, 10.69, 11.01, 11.49, 11.62, 12.15, 12.79, 13.32],
    "B2-MiniCAM":   [7.10, 7.97,  8.88, 10.48, 11.51, 12.27, 13.18, 13.85, 14.34, 14.67, 14.73, 14.82],
    "B2C-MARIA":    [7.10, 7.97,  9.12, 10.67, 12.85, 14.76, 15.51, 16.81, 17.74, 18.57, 19.16, 19.71],
    "B2High-MiniCAM":[7.10, 7.97,  9.23, 11.30, 13.06, 14.86, 17.02, 18.65, 19.80, 20.47, 21.09, 21.78],
}
SRES_MARKERS = {"A1B-AIM", "A1C-AIM", "B1T-MESSAGE"}

# ─── RCP ──────────────────────────────────────────────────────────────────────

RCP_TIME = [1990, 2000, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]
RCP = {
    "RCP3-PD (2.6) - IMAGE":  [ 7.884,  9.167,  9.878, 10.260,  7.946,  5.024,  3.387,  2.035,  0.654,  0.117, -0.268, -0.420],
    "RCP 4.5 - MiniCAM":      [ 7.884,  9.167,  9.518, 10.212, 11.170, 11.537, 11.280,  9.585,  7.222,  4.190,  4.220,  4.249],
    "RCP 6.0 - AIM":          [ 7.884,  9.167,  9.389,  9.357,  9.438, 10.840, 12.580, 14.566, 16.477, 17.525, 14.556, 13.935],
    "RCP 8.5 - MESSAGE":      [ 7.884,  9.167,  9.969, 12.444, 14.554, 17.432, 20.781, 24.097, 26.374, 27.715, 28.531, 28.817],
}
RCP_MARKERS = {"RCP 8.5 - MESSAGE", "RCP3-PD (2.6) - IMAGE"}

# ─── SSP ──────────────────────────────────────────────────────────────────────

SSP_TIME = [2005, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]
SSP = {
    # SSP1-19
    "SSP1-19 - AIM/CGE":          [34.3739, 35.7826, 37.2339, 19.0575,  8.2293,  1.7946, -2.1812, -3.7571, -4.3382, -4.3905, -4.4749],
    "SSP1-19 - GCAM4":            [None,    35.7754, 37.6844, 19.3081, 10.5799,  3.2627, -0.6336, -4.3354, -8.4210,-12.9638,-17.6742],
    "SSP1-19 - IMAGE":            [33.1661, 35.4888, 33.2088, 17.9680,  6.4139,  0.9680, -1.6500, -4.1369, -7.3702,-10.5677,-14.3404],
    "SSP1-19 - MESSAGE-GLOBIOM":  [37.7208, 40.2656, 38.0939, 23.4042, 14.9339,  3.6300, -4.0297, -8.1185,-11.9321,-14.3159,-15.4871],
    "SSP1-19 - REMIND-MAGPIE":    [35.2500, 36.2500, 35.2000, 26.3100, 16.4100,  3.7610, -6.3150, -9.5580,-11.3900,-12.7700,-13.3700],
    "SSP1-19 - WITCH-GLOBIOM":    [31.9220, 35.3034, 37.3123, 10.5600,  7.4359,  3.0999, -0.6957, -3.7652, -7.2216, -9.2466, -9.6483],
    # SSP1-26
    "SSP1-26 - AIM/CGE":          [34.3739, 35.7818, 37.1813, 29.7905, 19.4314, 13.6790,  8.6772,  4.1001,  2.0832,  0.6270,  0.0177],
    "SSP1-26 - GCAM4":            [None,    35.7754, 35.5266, 28.0269, 23.5731, 17.7668, 11.3240,  4.9210, -0.5556, -5.8802,-10.9639],
    "SSP1-26 - IMAGE":            [33.1661, 35.4888, 38.3898, 33.9309, 25.9047, 17.7329, 10.5658,  4.7852, -2.9218, -8.0983, -8.3474],
    "SSP1-26 - MESSAGE-GLOBIOM":  [37.7204, 40.2677, 38.4204, 32.7693, 28.1346, 19.7942,  9.6692,  1.6915, -4.1995, -9.0668,-12.2154],
    "SSP1-26 - REMIND-MAGPIE":    [35.7798, 35.9142, 35.0616, 32.0562, 28.0504, 21.3754, 12.1056,  3.0790, -2.7938, -6.7056, -8.5880],
    "SSP1-26 - WITCH-GLOBIOM":    [31.9220, 35.3034, 39.6159, 17.3084, 15.0936, 12.7871, 10.4918,  7.2188,  4.3399,  0.3642, -4.9390],
    # SSP1-34
    "SSP1-34 - AIM/CGE":          [34.3739, 35.7818, 37.1813, 35.2018, 31.2749, 26.4760, 21.5056, 16.6316, 13.4870, 10.8822,  9.0378],
    "SSP1-34 - GCAM4":            [None,    35.7754, 35.5266, 34.6401, 33.5372, 30.0823, 27.3479, 20.8789, 11.0185,  4.1001, -1.3456],
    "SSP1-34 - IMAGE":            [33.1661, 35.4888, 39.6388, 39.3514, 37.4431, 32.9473, 27.9556, 19.8133,  9.1234, -2.2754, -6.6155],
    "SSP1-34 - MESSAGE-GLOBIOM":  [37.7205, 40.2677, 39.8620, 38.4487, 35.7083, 32.9907, 27.0370, 17.2956,  7.6326, -0.1029, -6.1741],
    "SSP1-34 - REMIND-MAGPIE":    [35.7798, 35.9142, 34.9482, 37.1577, 37.4380, 34.1812, 28.0783, 19.2030,  9.8699,  2.4769, -2.8272],
    "SSP1-34 - WITCH-GLOBIOM":    [31.9220, 35.3034, 39.9652, 33.2526, 28.4091, 24.3865, 21.0793, 16.4961, 12.0979,  6.6008, -0.2423],
    # SSP1-45
    "SSP1-45 - AIM/CGE":          [34.3739, 35.7818, 36.5886, 39.4589, 38.4481, 35.0301, 31.9299, 28.4270, 24.7902, 21.5447, 18.7381],
    "SSP1-45 - GCAM4":            [None,    35.7754, 35.5266, 37.8637, 39.2495, 37.2480, 35.7798, 32.4987, 24.5445, 17.4022, 15.3691],
    "SSP1-45 - IMAGE":            [33.1661, 35.4888, 39.8601, 40.9581, 41.4986, 40.0210, 37.7347, 32.3230, 24.4556, 17.3077, 11.0790],
    "SSP1-45 - MESSAGE-GLOBIOM":  [37.7205, 40.2678, 40.5438, 41.9594, 41.4559, 41.2462, 40.1594, 35.7068, 28.3964, 18.6463,  8.9047],
    "SSP1-45 - REMIND-MAGPIE":    [35.7798, 35.9142, 34.9693, 38.9416, 42.3109, 40.9010, 36.4236, 30.2545, 23.3356, 16.5421, 12.1158],
    "SSP1-45 - WITCH-GLOBIOM":    [31.9220, 35.3034, 39.5882, 41.2656, 39.1855, 37.3502, 33.7811, 29.6420, 25.7285, 18.1402,  9.6865],
    # SSP1-60
    "SSP1-60 - WITCH-GLOBIOM":    [31.9220, 35.3034, 39.4591, 42.8967, 43.9289, 45.5231, 44.3028, 42.3248, 40.1720, 37.6757, 31.6750],
    # SSP1-Baseline
    "SSP1-Baseline - AIM/CGE":    [34.3739, 35.8887, 39.1303, 41.8712, 42.1128, 40.1919, 38.8316, 35.9351, 33.4663, 31.6029, 29.8798],
    "SSP1-Baseline - GCAM4":      [None,    35.7754, 36.8388, 41.7402, 46.5879, 48.0428, 49.1563, 48.0765, 44.0571, 39.6679, 34.8398],
    "SSP1-Baseline - IMAGE":      [33.1661, 35.4888, 40.0690, 42.6532, 43.7785, 42.4548, 41.6019, 39.2175, 33.3923, 28.6184, 24.6129],
    "SSP1-Baseline - MESSAGE-GLOBIOM": [37.7182, 40.2672, 41.2087, 43.5139, 45.6372, 47.2822, 49.5684, 50.0562, 49.2543, 49.5868, 49.2707],
    "SSP1-Baseline - REMIND-MAGPIE":   [35.2499, 36.2509, 38.2048, 40.6691, 44.5641, 46.3531, 43.1878, 39.0578, 33.0532, 26.6236, 21.7717],
    "SSP1-Baseline - WITCH-GLOBIOM":   [31.9220, 35.3034, 41.3191, 44.2131, 48.1516, 47.2839, 46.6030, 45.3935, 42.9200, 39.3101, 31.2779],
    # SSP2-19
    "SSP2-19 - AIM/CGE":          [34.3739, 38.2054, 43.3381, 20.1386,  8.2232,  0.3992, -4.8961, -7.0386, -7.9892, -8.4073, -8.9869],
    "SSP2-19 - GCAM4":            [None,    35.7754, 41.3377, 36.0020,  9.5357, -7.4522,-13.1871,-14.1276,-18.1780,-23.5224,-31.6837],
    "SSP2-19 - MESSAGE-GLOBIOM":  [37.7672, 40.3135, 40.9313, 23.6331, 11.5241,  3.7789, -1.5107, -6.5404,-10.6089,-12.4109,-13.0489],
    "SSP2-19 - REMIND-MAGPIE":    [35.0900, 37.0100, 42.3100, 31.1100,  8.6230, -7.2500,-10.4800,-12.6200,-13.6400,-13.2400,-14.1800],
    # SSP2-26
    "SSP2-26 - AIM/CGE":          [34.3739, 38.2519, 43.2312, 30.4271, 18.7647, 10.5879,  6.5209,  1.0069, -1.5818, -3.6535, -4.8416],
    "SSP2-26 - GCAM4":            [None,    35.7754, 39.8926, 46.3374, 24.6618,  4.0134, -4.4409, -6.5519,-11.1757,-17.0790,-24.0182],
    "SSP2-26 - IMAGE":            [33.1827, 35.6126, 39.7871, 28.6978, 18.5500, 10.8425,  2.8712, -0.4699, -2.9248, -3.9852, -5.2415],
    "SSP2-26 - MESSAGE-GLOBIOM":  [37.7708, 40.2943, 40.6570, 34.5416, 26.3056, 16.3306,  9.2479,  2.0103, -4.0458, -6.4958, -8.3573],
    "SSP2-26 - REMIND-MAGPIE":    [35.0755, 35.5959, 43.2856, 35.9917, 27.6483, 19.3515,  7.5494, -1.4445, -6.8490,-10.4949,-12.0717],
    "SSP2-26 - WITCH-GLOBIOM":    [31.9220, 35.3034, 37.4229, 17.1300, 15.2224, 13.3312, 10.1107,  6.9524,  3.1773,  0.6133, -3.7286],
    # SSP2-34
    "SSP2-34 - AIM/CGE":          [34.3739, 38.2519, 43.2312, 38.7326, 31.2436, 23.7069, 17.4882, 12.7307,  9.4446,  6.6960,  4.2354],
    "SSP2-34 - GCAM4":            [None,    35.7754, 39.8926, 46.3374, 39.8314, 25.4204, 13.7471,  7.4187,  2.7189, -3.4274,-10.4349],
    "SSP2-34 - IMAGE":            [33.1827, 35.6145, 41.2109, 39.0743, 34.0681, 25.9235, 16.1120, 13.3713,  7.1378,  2.8810,  0.3072],
    "SSP2-34 - MESSAGE-GLOBIOM":  [37.7708, 40.2943, 41.6859, 42.0316, 38.2197, 32.6119, 24.3027, 15.4234,  7.9744,  1.8600, -1.4181],
    "SSP2-34 - REMIND-MAGPIE":    [35.0755, 35.5959, 43.2691, 40.8878, 34.3304, 29.4215, 24.0969, 17.2968,  9.2118,  0.3554, -5.2282],
    "SSP2-34 - WITCH-GLOBIOM":    [31.9220, 35.3034, 39.7593, 29.6830, 25.9122, 22.8045, 19.7284, 16.6409, 13.3991,  7.7080,  2.4612],
    # SSP2-45
    "SSP2-45 - AIM/CGE":          [34.3739, 38.2519, 43.2312, 45.3260, 46.2846, 40.6484, 34.0910, 26.8606, 20.2881, 15.2502, 11.6656],
    "SSP2-45 - GCAM4":            [None,    35.7754, 39.8926, 46.3374, 42.7904, 32.3017, 20.9787, 12.6946,  9.4622,  8.8659,  6.1285],
    "SSP2-45 - IMAGE":            [33.1827, 35.6126, 42.6448, 46.7843, 45.4248, 42.1623, 36.3746, 31.4626, 23.5006, 16.0121, 14.9788],
    "SSP2-45 - MESSAGE-GLOBIOM":  [37.7708, 40.2943, 42.2849, 44.3857, 44.4916, 42.8322, 39.0424, 34.1932, 25.8238, 15.4685,  9.1150],
    "SSP2-45 - REMIND-MAGPIE":    [35.0755, 35.5959, 43.2660, 42.8401, 40.7524, 36.9163, 33.0420, 29.4438, 26.2527, 22.4943, 21.9697],
    "SSP2-45 - WITCH-GLOBIOM":    [31.9220, 35.3034, 40.7819, 39.7420, 39.4024, 34.5172, 30.9843, 27.9721, 24.9147, 20.7535, 13.7370],
    # SSP2-60
    "SSP2-60 - AIM/CGE":          [34.3739, 38.2519, 43.2312, 46.6386, 49.2098, 48.5556, 47.5999, 46.5671, 45.9422, 45.5001, 44.9382],
    "SSP2-60 - GCAM4":            [None,    35.7754, 39.8926, 46.3374, 50.6053, 51.9722, 51.8293, 50.2295, 45.5255, 38.5298, 28.7234],
    "SSP2-60 - IMAGE":            [33.1827, 35.6126, 43.0631, 49.0232, 51.8339, 53.8201, 53.6763, 53.7241, 51.0194, 47.0254, 46.0603],
    "SSP2-60 - MESSAGE-GLOBIOM":  [37.7708, 40.2943, 42.3922, 46.1252, 49.5448, 52.5857, 54.6635, 55.5372, 55.9741, 56.2188, 55.4263],
    "SSP2-60 - REMIND-MAGPIE":    [35.0755, 35.5959, 43.2597, 44.9714, 49.0029, 51.8075, 51.9716, 51.1867, 49.3382, 44.7598, 41.9362],
    "SSP2-60 - WITCH-GLOBIOM":    [31.9220, 35.3034, 40.9937, 46.4843, 50.8120, 50.8068, 50.5173, 50.1152, 47.4155, 44.1585, 36.8897],
    # SSP2-Baseline
    "SSP2-Baseline - AIM/CGE":    [34.3739, 38.3755, 45.7930, 51.7113, 56.6881, 59.8065, 61.8338, 63.6788, 65.6396, 68.3136, 70.7118],
    "SSP2-Baseline - GCAM4":      [None,    35.7754, 41.4685, 49.5212, 56.8670, 61.9235, 67.5110, 71.2133, 72.6043, 73.7888, 75.3574],
    "SSP2-Baseline - IMAGE":      [33.1827, 35.6126, 43.4780, 49.4744, 52.9137, 55.9911, 57.6216, 60.8667, 64.4431, 67.8371, 72.4926],
    "SSP2-Baseline - MESSAGE-GLOBIOM": [37.7690, 40.2946, 42.2624, 46.7276, 51.6065, 56.6516, 61.4023, 65.9970, 74.1336, 81.0284, 85.6842],
    "SSP2-Baseline - REMIND-MAGPIE":   [35.0905, 37.0096, 43.2700, 48.6399, 56.5394, 60.4799, 67.4407, 70.4504, 72.5400, 69.4599, 64.3597],
    "SSP2-Baseline - WITCH-GLOBIOM":   [31.9220, 35.3034, 43.9520, 51.8725, 57.9626, 62.5435, 66.6327, 71.3462, 75.3250, 77.9304, 73.3703],
    # SSP3-34
    "SSP3-34 - AIM/CGE":          [34.3739, 39.3986, 46.6377, 48.2922, 32.5528, 22.9309, 16.7540,  9.4947,  3.9252, -0.7134, -3.8619],
    "SSP3-34 - IMAGE":            [33.1779, 35.7104, 44.7148, 41.8120, 29.4204, 19.4304,  8.2742,  4.2035,  3.3002,  3.1802,  2.8201],
    "SSP3-34 - MESSAGE-GLOBIOM":  [37.7204, 40.3451, 47.8801, 47.0385, 31.2601, 21.8035, 12.8588,  6.1047,  2.2271, -0.1828, -0.7153],
    "SSP3-34 - WITCH-GLOBIOM":    [31.9220, 35.3034, 39.4283, 26.3234, 22.9757, 20.4554, 16.4079, 13.5896, 10.9920,  5.9176,  1.7376],
    # SSP3-45
    "SSP3-45 - AIM/CGE":          [34.3739, 39.3986, 46.6377, 50.5891, 43.0262, 36.5619, 25.4704, 19.7139, 15.9589, 11.4000,  6.4018],
    "SSP3-45 - IMAGE":            [33.1779, 35.7104, 45.7028, 48.8320, 43.6970, 38.3183, 28.9404, 20.3699, 13.9083, 10.1226,  8.2186],
    "SSP3-45 - MESSAGE-GLOBIOM":  [37.7168, 40.3744, 48.2529, 52.2746, 45.2494, 36.9094, 27.5329, 18.2116, 11.7530,  7.2209,  4.7921],
    "SSP3-45 - WITCH-GLOBIOM":    [31.9220, 35.3034, 43.9966, 42.4446, 39.9711, 33.8283, 28.0426, 24.5205, 21.0812, 15.9874, 10.4060],
    # SSP3-60
    "SSP3-60 - AIM/CGE":          [34.3739, 39.3986, 46.6377, 50.8053, 48.0745, 46.8881, 48.0484, 43.5267, 37.5542, 33.7122, 31.2482],
    "SSP3-60 - IMAGE":            [33.1779, 35.7104, 46.5032, 53.1322, 54.2868, 56.0912, 52.6234, 46.0200, 37.7846, 31.3229, 27.4345],
    "SSP3-60 - MESSAGE-GLOBIOM":  [37.7205, 40.3727, 49.1496, 57.9140, 60.3150, 59.9811, 54.7114, 44.4708, 35.3239, 29.3898, 25.5462],
    "SSP3-60 - WITCH-GLOBIOM":    [31.9220, 35.3034, 45.4161, 52.2676, 55.1196, 52.5772, 47.6706, 44.3303, 39.0177, 31.9923, 26.9228],
    # SSP3-Baseline
    "SSP3-Baseline - AIM/CGE":    [34.3739, 39.5608, 48.5027, 55.0009, 59.8773, 64.0014, 67.9623, 71.7927, 75.5715, 80.1372, 85.2150],
    "SSP3-Baseline - GCAM4":      [None,    35.7758, 44.6183, 53.6253, 60.2101, 64.8293, 70.1155, 74.7981, 78.2723, 80.9670, 86.1140],
    "SSP3-Baseline - IMAGE":      [33.1779, 35.7104, 46.6496, 53.6693, 56.3442, 61.1271, 61.3071, 63.8387, 66.9267, 70.9804, 76.4771],
    "SSP3-Baseline - MESSAGE-GLOBIOM": [37.8062, 40.3811, 52.0613, 62.4478, 70.6995, 77.0191, 84.1347, 91.3238,102.8427,115.6809,129.7206],
    "SSP3-Baseline - WITCH-GLOBIOM":   [31.9220, 35.3034, 48.2870, 58.2936, 63.5330, 66.7181, 68.3092, 72.4773, 75.9627, 80.3705, 84.1363],
    # SSP4-19
    "SSP4-19 - WITCH-GLOBIOM":    [31.9220, 35.3034, 39.2530, 12.7402,  9.2860,  4.1926, -0.1842, -3.5386, -7.2457, -9.3590,-10.8016],
    # SSP4-26
    "SSP4-26 - AIM/CGE":          [34.3739, 38.1982, 44.8181, 34.9675, 22.4191, 15.2162,  9.0045,  3.2987,  0.6722, -1.5518, -2.7853],
    "SSP4-26 - GCAM4":            [None,    35.7758, 40.0488, 23.8218, 16.3242, 11.8814,  6.6660, -0.1231,-10.6230,-19.0914,-27.5445],
    "SSP4-26 - IMAGE":            [33.1115, 35.6758, 37.4709, 27.0762, 16.5133,  6.0174,  1.7844, -0.0901, -1.0350, -1.4936, -0.9609],
    "SSP4-26 - WITCH-GLOBIOM":    [31.9220, 35.3034, 41.9903, 22.1593, 17.7386, 13.8643,  9.2958,  6.6592,  3.8444, -0.4650, -4.7809],
    # SSP4-34
    "SSP4-34 - AIM/CGE":          [34.3739, 38.1982, 44.8181, 41.4356, 35.7335, 29.2190, 22.7722, 16.6672, 12.5219,  9.0330,  6.3274],
    "SSP4-34 - GCAM4":            [None,    35.7758, 40.0488, 35.0211, 28.0994, 19.9397, 14.7987, 10.2469,  2.7735, -7.1320,-15.9621],
    "SSP4-34 - IMAGE":            [33.1115, 35.6757, 41.0767, 39.3308, 34.6741, 24.8456, 15.3210, 10.4495,  6.7794,  2.7016,  0.6638],
    "SSP4-34 - WITCH-GLOBIOM":    [31.9220, 35.3034, 41.9912, 36.8613, 30.6032, 24.3539, 20.4937, 16.2186, 11.8727,  5.5980,  0.3949],
    # SSP4-45
    "SSP4-45 - AIM/CGE":          [34.3739, 38.1982, 44.8181, 46.2551, 46.0072, 40.8497, 35.4630, 30.2517, 25.2502, 20.7386, 16.7182],
    "SSP4-45 - GCAM4":            [None,    35.7758, 40.0488, 39.4511, 36.5661, 29.0346, 21.4804, 15.7154, 10.9315,  9.7826,  7.6940],
    "SSP4-45 - IMAGE":            [33.1923, 35.5837, 42.0861, 46.4136, 48.7907, 42.4438, 33.5338, 27.6916, 21.1188, 12.7455,  9.7988],
    "SSP4-45 - WITCH-GLOBIOM":    [31.9220, 35.3034, 41.6166, 43.8136, 41.1921, 36.8143, 32.8945, 29.6309, 23.9316, 19.3534, 11.5852],
    # SSP4-60
    "SSP4-60 - GCAM4":            [None,    35.7758, 40.0488, 46.1208, 48.9949, 49.0547, 47.6125, 44.5910, 36.8058, 28.5648, 20.5693],
    "SSP4-60 - IMAGE":            [33.1923, 35.5837, 42.1051, 46.7052, 49.7615, 49.2201, 47.7756, 47.5549, 47.0321, 42.7186, 41.1561],
    "SSP4-60 - WITCH-GLOBIOM":    [31.9220, 35.3034, 41.3390, 45.9710, 46.6743, 47.8875, 47.4644, 46.9065, 44.2359, 41.0056, 32.8489],
    # SSP4-Baseline
    "SSP4-Baseline - AIM/CGE":    [34.3739, 38.2566, 45.1252, 49.7726, 50.5498, 47.2948, 43.7342, 40.5643, 38.9131, 37.8999, 36.7635],
    "SSP4-Baseline - GCAM4":      [None,    35.7758, 41.6360, 49.0696, 53.8469, 55.6644, 56.9540, 55.8982, 51.1729, 47.5327, 44.7847],
    "SSP4-Baseline - IMAGE":      [33.1818, 35.5945, 42.4640, 48.2878, 50.8252, 50.3889, 48.4022, 47.7029, 47.0377, 44.7352, 44.3589],
    "SSP4-Baseline - WITCH-GLOBIOM":   [31.9220, 35.3034, 43.0450, 47.2814, 50.5272, 49.7304, 48.9851, 48.9186, 47.2698, 42.4343, 33.6540],
    # SSP5-19
    "SSP5-19 - GCAM4":            [None,    35.7754, 41.9760, 35.6754,  4.9079, -8.9962, -9.6578, -9.4891,-12.1645,-18.1806,-26.3951],
    "SSP5-19 - REMIND-MAGPIE":    [35.2800, 36.3700, 39.7000, 37.7700, 22.1400,  1.2540,-12.8400,-16.2500,-17.9300,-19.5500,-21.3100],
    # SSP5-26
    "SSP5-26 - AIM/CGE":          [34.3739, 37.2297, 41.8081, 28.0629, 21.7403, 11.0077,  4.2979, -1.8447, -4.4437, -6.4810, -7.6392],
    "SSP5-26 - GCAM4":            [None,    35.7754, 39.4785, 51.1094, 23.6863,  0.1864, -3.1119, -3.7129, -6.7789,-12.7737,-21.6660],
    "SSP5-26 - REMIND-MAGPIE":    [35.2299, 36.3350, 39.5613, 43.1646, 38.0200, 24.9853,  7.4833, -3.9883,-11.3497,-16.4938,-18.9766],
    # SSP5-34
    "SSP5-34 - AIM/CGE":          [34.3739, 37.2297, 41.8081, 37.3896, 35.4775, 27.4798, 17.2479, 11.1832,  7.0819,  3.9777,  1.6142],
    "SSP5-34 - GCAM4":            [None,    35.7754, 39.4785, 51.1094, 38.9118, 17.6772, 10.0899,  7.1783,  3.7726, -1.2527, -9.4378],
    "SSP5-34 - IMAGE":            [33.1674, 35.9993, 44.0374, 45.2118, 40.0689, 29.5708, 16.8092,  9.4625,  6.5513,  2.4587,  0.7014],
    "SSP5-34 - REMIND-MAGPIE":    [35.2299, 36.3350, 39.5499, 44.4740, 43.5223, 37.4209, 28.4542, 15.5094,  2.7482, -8.5353,-13.6001],
    "SSP5-34 - WITCH-GLOBIOM":    [31.9220, 35.3034, 37.8139, 18.9242, 19.5757, 18.5962, 18.1806, 17.8306, 17.6273, 15.5800,  5.3557],
    # SSP5-45
    "SSP5-45 - AIM/CGE":          [34.3739, 37.2297, 41.8081, 43.3378, 44.6982, 36.6339, 27.3095, 22.0941, 20.1424, 15.4761, 11.8037],
    "SSP5-45 - GCAM4":            [None,    35.7754, 39.4785, 51.1094, 48.4267, 32.7242, 21.9739, 15.8026, 11.4441, 13.6515, 14.2051],
    "SSP5-45 - IMAGE":            [33.1674, 35.9993, 45.1235, 52.2617, 53.2681, 47.2155, 34.9504, 27.7631, 20.2589, 12.8879,  7.6007],
    "SSP5-45 - REMIND-MAGPIE":    [35.2299, 36.3350, 39.5425, 44.9341, 46.0024, 43.2244, 37.1714, 29.4774, 23.6499, 17.1663, 15.8607],
    "SSP5-45 - WITCH-GLOBIOM":    [31.9220, 35.3034, 39.8794, 32.1821, 32.6526, 32.2219, 31.3125, 29.7799, 27.3652, 24.8722, 14.4960],
    # SSP5-60
    "SSP5-60 - AIM/CGE":          [34.3739, 37.2297, 41.8081, 44.7397, 48.3713, 45.7505, 41.9519, 40.1417, 39.2958, 38.4108, 37.2012],
    "SSP5-60 - GCAM4":            [None,    35.7754, 39.4785, 51.1094, 59.1264, 58.7816, 57.4864, 52.7798, 40.9079, 30.9422, 21.7658],
    "SSP5-60 - IMAGE":            [33.1682, 35.9825, 45.9513, 57.9475, 66.2722, 69.5887, 62.6355, 53.6939, 41.2712, 32.3227, 23.9956],
    "SSP5-60 - REMIND-MAGPIE":    [35.2299, 36.3350, 39.5604, 47.8360, 54.5127, 58.1730, 58.9398, 55.2990, 50.5401, 44.1863, 40.9689],
    "SSP5-60 - WITCH-GLOBIOM":    [31.9220, 35.3034, 40.9541, 45.0476, 51.4851, 50.2298, 45.1993, 45.8068, 46.1934, 44.5405, 38.6313],
    # SSP5-Baseline
    "SSP5-Baseline - AIM/CGE":    [34.3739, 37.4032, 44.2750, 54.2289, 64.9723, 73.6589, 82.2667, 90.2872, 97.7439,105.9660,114.4410],
    "SSP5-Baseline - GCAM4":      [None,    35.7754, 41.2035, 55.1423, 71.3284, 83.2515, 93.7571,101.1123,104.2832,105.3475,104.1186],
    "SSP5-Baseline - IMAGE":      [33.1682, 35.9825, 46.6306, 60.2897, 72.7072, 86.4405, 94.7489,105.5553,110.4329,112.4234,111.9100],
    "SSP5-Baseline - REMIND-MAGPIE":   [35.2796, 36.3711, 44.6104, 56.7265, 69.8616, 84.4365,101.3016,117.4998,129.4993,130.3975,126.0977],
    "SSP5-Baseline - WITCH-GLOBIOM":   [31.9220, 35.3034, 44.3215, 56.6257, 72.8812, 88.3262,100.0683,109.3883,116.2267,118.5059,114.6223],
}
SSP_MARKERS = {
    "SSP5-Baseline - REMIND-MAGPIE",
    "SSP1-19 - IMAGE",
    "SSP2-45 - MESSAGE-GLOBIOM",
}

# ─── CMIP7 fetch ──────────────────────────────────────────────────────────────

CMIP7_URL = (
    "https://raw.githubusercontent.com/chrisroadmap/cmip7-scenariomip/"
    "1.0/data/emissions/extensions_1750-2500.csv"
)
CMIP7_TIME = [2005, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]
CMIP7_INDICES = [260, 265, 275, 285, 295, 305, 315, 325, 335, 345, 355]


def fetch_cmip7():
    print(f"Fetching CMIP7 data from {CMIP7_URL} ...")
    rows = []
    with urllib.request.urlopen(CMIP7_URL, timeout=60) as resp:
        lines = resp.read().decode("utf-8").splitlines()
    reader = csv.reader(lines)
    for row in reader:
        rows.append(row)
    scenarios = {}
    for row in rows:
        if len(row) < max(CMIP7_INDICES) + 1:
            continue
        scen = row[0]
        var = row[2] if len(row) > 2 else ""
        if var == "CO2 FFI":
            try:
                vals = [float(row[i]) for i in CMIP7_INDICES]
                scenarios[scen] = vals
            except (ValueError, IndexError):
                pass
    print(f"  Loaded {len(scenarios)} CMIP7 CO2 FFI scenarios")
    return scenarios


def cmip7_markers(scenarios):
    """Return set of scenario names for high-extension and verylow extremes."""
    markers = set()
    for name in scenarios:
        nl = name.lower()
        if "high-extension" in nl or "high_extension" in nl:
            markers.add(name)
        elif ("verylow" in nl or "very_low" in nl or "very-low" in nl) and (
            "overshoot" not in nl
        ):
            markers.add(name)
    return markers

# ─── historical emissions ─────────────────────────────────────────────────────

OWID_URL = (
    "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
)
_HIST_FALLBACK = {  # GtCO2/yr, GCP 2024 estimates
    1950: 6.0, 1960: 9.4, 1970: 14.7, 1975: 17.2, 1980: 19.5,
    1985: 19.9, 1990: 22.6, 1995: 23.6, 2000: 25.3, 2005: 30.1,
    2010: 33.1, 2015: 35.7, 2019: 37.1, 2020: 34.8, 2021: 36.6,
    2022: 37.2, 2023: 37.4,
}


def fetch_historical():
    """Return (years_array, gt_co2_array) for World fossil+industrial CO2."""
    print(f"Fetching historical CO2 from OWID ...")
    try:
        with urllib.request.urlopen(OWID_URL, timeout=60) as resp:
            lines = resp.read().decode("utf-8").splitlines()
        reader = csv.DictReader(lines)
        years, vals = [], []
        for row in reader:
            if row.get("country") != "World":
                continue
            yr = int(row["year"])
            co2_str = row.get("co2", "").strip()
            if not co2_str:
                continue
            years.append(yr)
            vals.append(float(co2_str) / 1000.0)  # MtCO2 → GtCO2
        years = np.array(years, dtype=float)
        vals = np.array(vals, dtype=float)
        mask = (years >= 1950) & (years <= 2024)
        print(f"  Loaded {mask.sum()} years of historical data")
        return years[mask], vals[mask]
    except Exception as exc:
        print(f"  OWID fetch failed ({exc}), using fallback")
        yrs = np.array(sorted(_HIST_FALLBACK), dtype=float)
        vals = np.array([_HIST_FALLBACK[int(y)] for y in yrs])
        return yrs, vals

# ─── CMIP-used scenario selection ────────────────────────────────────────────

CMIP_USED = {
    "SA90":  [],  # CMIP1: no specific scenarios prescribed
    "IS92":  ["IS92a"],
    "SRES":  ["A1B-AIM", "A2-ASF", "B1-IMAGE"],
    "RCP":   ["RCP3-PD (2.6) - IMAGE", "RCP 4.5 - MiniCAM",
               "RCP 6.0 - AIM", "RCP 8.5 - MESSAGE"],
    "SSP":   [
        "SSP1-19 - IMAGE",            # ssp119
        "SSP1-26 - IMAGE",            # ssp126
        "SSP2-45 - MESSAGE-GLOBIOM",  # ssp245
        "SSP3-Baseline - AIM/CGE",    # ssp370
        "SSP4-34 - GCAM4",            # ssp434
        "SSP4-60 - GCAM4",            # ssp460
        "SSP5-34 - REMIND-MAGPIE",    # ssp534-over
        "SSP5-Baseline - REMIND-MAGPIE",  # ssp585
    ],
}

CMIP_SHORT = {
    "IS92a":                           "IS92a",
    "A1B-AIM":                         "A1B",
    "A2-ASF":                          "A2",
    "B1-IMAGE":                        "B1",
    "RCP3-PD (2.6) - IMAGE":           "RCP2.6",
    "RCP 4.5 - MiniCAM":               "RCP4.5",
    "RCP 6.0 - AIM":                   "RCP6.0",
    "RCP 8.5 - MESSAGE":               "RCP8.5",
    "SSP1-19 - IMAGE":                 "SSP1-1.9",
    "SSP1-26 - IMAGE":                 "SSP1-2.6",
    "SSP2-45 - MESSAGE-GLOBIOM":       "SSP2-4.5",
    "SSP3-Baseline - AIM/CGE":         "SSP3-7.0",
    "SSP4-34 - GCAM4":                 "SSP4-3.4",
    "SSP4-60 - GCAM4":                 "SSP4-6.0",
    "SSP5-34 - REMIND-MAGPIE":         "SSP5-3.4os",
    "SSP5-Baseline - REMIND-MAGPIE":   "SSP5-8.5",
    "high-extension":                  "high",
    "high-overshoot":                  "hi-os",
    "low":                             "low",
    "medium-extension":                "med",
    "medium-overshoot":                "med-os",
    "verylow":                         "vlow",
    "verylow-overshoot":               "vlow-os",
}

# y-offsets (GtCO2) for end-of-line labels that would otherwise overlap
_LABEL_Y_OFFSET = {
    "IS92a":  +2.5,   # sits just above CMIP7 "high"
    "high":   -2.5,   # sits just below IS92a
    "A2":     +2.5,   # sits just above RCP8.5
    "RCP8.5": -2.5,   # sits just below A2
}

# ─── figure ───────────────────────────────────────────────────────────────────

def make_figure(cmip7_scenarios, hist_years, hist_vals):
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.axhline(0, color="black", lw=0.5, ls="--", alpha=0.3, zorder=1)

    # ── shaded p10–p90 bands per generation (drawn first, lowest z-order) ────
    shade_families = [
        ("SA90",  SA90_TIME,  SA90,  C_TO_CO2),
        ("IS92",  IS92_TIME,  IS92,  C_TO_CO2),
        ("SRES",  SRES_TIME,  SRES,  C_TO_CO2),
        ("RCP",   RCP_TIME,   RCP,   C_TO_CO2),
        ("SSP",   SSP_TIME,   SSP,   1.0),
        ("CMIP7", CMIP7_TIME, cmip7_scenarios, 1.0),
    ]
    for gen, t, dct, conv in shade_families:
        if not dct:
            continue
        _, p10, p90 = family_stats(t, dct, conv=conv)
        ax.fill_between(T_FINE, p10, p90,
                        color=GEN_COLORS[gen], alpha=0.10, zorder=0,
                        linewidth=0)
        c = GEN_COLORS[gen]
        ax.plot(T_FINE, p10, color=c, lw=0.8, alpha=0.6, zorder=1, solid_capstyle="round")
        ax.plot(T_FINE, p90, color=c, lw=0.8, alpha=0.6, zorder=1, solid_capstyle="round")

    # ── CMIP-used scenario lines ─────────────────────────────────────────────
    cmip_families = [
        ("SA90",  SA90_TIME,  SA90,  C_TO_CO2, CMIP_USED["SA90"]),
        ("IS92",  IS92_TIME,  IS92,  C_TO_CO2, CMIP_USED["IS92"]),
        ("SRES",  SRES_TIME,  SRES,  C_TO_CO2, CMIP_USED["SRES"]),
        ("RCP",   RCP_TIME,   RCP,   C_TO_CO2, CMIP_USED["RCP"]),
        ("SSP",   SSP_TIME,   SSP,   1.0,       CMIP_USED["SSP"]),
        ("CMIP7", CMIP7_TIME, cmip7_scenarios, 1.0,
         list(cmip7_scenarios.keys())),
    ]
    idx_2100 = np.argmin(np.abs(T_FINE - 2100))
    for gen, t, dct, conv, selected in cmip_families:
        c = GEN_COLORS[gen]
        # interpolate all selected curves first so we can rank by 2100 value
        curves = {}
        for name in selected:
            if name not in dct:
                print(f"  WARNING: {name!r} not found in {gen} data")
                continue
            curves[name] = interp(t, dct[name]) * conv
        if not curves:
            continue
        # identify extreme (highest/lowest at 2100) vs intermediate scenarios
        end_vals = {n: (y[idx_2100] if not np.isnan(y[idx_2100]) else np.nanmax(y))
                    for n, y in curves.items()}
        sorted_names = sorted(end_vals, key=end_vals.get)
        extremes = {sorted_names[0], sorted_names[-1]}
        for name, y in curves.items():
            bold = name in extremes or len(curves) == 1
            if not bold:
                continue
            ax.plot(T_FINE, y, color=c, lw=2.0, alpha=0.92,
                    zorder=4, solid_capstyle="round")
            valid = np.where(~np.isnan(y))[0]
            if not len(valid):
                continue
            xi = valid[-1]
            label = CMIP_SHORT.get(name, name)
            y_off = _LABEL_Y_OFFSET.get(label, 0.0)
            ax.text(T_FINE[xi] + 1.0, y[xi] + y_off, label,
                    fontsize=7, va="center", color=c, fontweight="bold")

    # historical
    ax.plot(
        hist_years, hist_vals,
        color="black", lw=2.5, ls="-", zorder=10,
        solid_capstyle="round",
        label="Historical (GCP/OWID)",
    )

    # ── right-side 2100 summary bars ─────────────────────────────────────────
    ax.axvline(2102.5, color="0.75", lw=0.8, ls=":", zorder=1)
    bar_x = {"SA90": 2104.5, "IS92": 2106, "SRES": 2107.5,
              "RCP": 2109, "SSP": 2110.5, "CMIP7": 2112}
    tick_hw = 0.55
    for gen, t, dct, conv in shade_families:
        if not dct:
            continue
        matrix = np.array([interp(t, vals) * conv for vals in dct.values()])
        col = matrix[:, idx_2100]
        col = col[~np.isnan(col)]
        if not len(col):
            continue
        lo   = col.min()
        hi   = col.max()
        p10  = np.percentile(col, 10)
        p50  = np.percentile(col, 50)
        p90  = np.percentile(col, 90)
        mean = np.mean(col)
        c = GEN_COLORS[gen]
        bx = bar_x[gen]
        ax.plot([bx, bx], [lo, hi], color=c, lw=1.5, zorder=5,
                solid_capstyle="round")
        ax.plot([bx - tick_hw, bx + tick_hw], [lo, lo], color=c, lw=1.5, zorder=5)
        ax.plot([bx - tick_hw, bx + tick_hw], [hi, hi], color=c, lw=1.5, zorder=5)
        ax.plot([bx - tick_hw * 0.6, bx + tick_hw * 0.6], [p90, p90],
                color=c, lw=1.5, zorder=5, alpha=0.5)
        ax.plot([bx - tick_hw * 0.6, bx + tick_hw * 0.6], [p50, p50],
                color=c, lw=1.5, zorder=5)
        ax.plot([bx - tick_hw * 0.6, bx + tick_hw * 0.6], [mean, mean],
                color=c, lw=1.5, ls="--", zorder=5)
        ax.plot([bx - tick_hw * 0.6, bx + tick_hw * 0.6], [p10, p10],
                color=c, lw=1.5, zorder=5, alpha=0.5)
        ax.text(bx, hi + 2.5, f"n={len(col)}", fontsize=6.5,
                color=c, ha="center", va="bottom", fontweight="bold")

    # ── summary bar legend ────────────────────────────────────────────────────
    lx = 2113.5  # label x, just right of the rightmost bar
    ax.text(2108, 140, "at 2100", fontsize=7, color="0.4",
            ha="center", va="bottom", style="italic")
    p90_label_y = p90 - 3.0 if abs(p90 - hi) < 3 else p90
    p10_label_y = p10 + 3.0 if abs(p10 - lo) < 3 else p10
    ax.text(lx, hi,          "max",    fontsize=6.5, color="0.45", va="center")
    ax.text(lx, p90_label_y, "p90",    fontsize=6.5, color="0.45", va="center", alpha=0.7)
    ax.text(lx, p50,         "median", fontsize=6.5, color="0.45", va="center")
    ax.text(lx, mean,        "mean --",fontsize=6.5, color="0.45", va="center")
    ax.text(lx, p10_label_y, "p10",    fontsize=6.5, color="0.45", va="center", alpha=0.7)
    ax.text(lx, lo,          "min",    fontsize=6.5, color="0.45", va="center")

    # ── "futures avoided / opportunities lost" annotations ───────────────────
    ax.annotate(
        "Futures\navoided",
        xy=(2090, 110),
        xytext=(2063, 128),
        fontsize=9, ha="center", color="0.3", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="0.4", lw=1.2),
    )
    ax.annotate(
        "Opportunities\nlost",
        xy=(2026, 20),
        xytext=(2010, 5),
        fontsize=9, ha="center", color="0.3", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="0.4", lw=1.2),
    )

    # ── generation legend ────────────────────────────────────────────────────
    gen_labels = {
        "SA90":  "SA90 (IPCC FAR, 1990) — range only",
        "IS92":  "IS92 (IPCC SAR, 1992)",
        "SRES":  "SRES (IPCC AR4 / CMIP3, 2000)",
        "RCP":   "RCP (IPCC AR5 / CMIP5, 2009)",
        "SSP":   "SSP (IPCC AR6 / CMIP6, 2016)",
        "CMIP7": "ScenarioMIP (IPCC AR7 / CMIP7, 2026)",
    }
    patches = [
        mpatches.Patch(color=GEN_COLORS[k], label=v)
        for k, v in gen_labels.items()
    ]
    patches.append(
        plt.Line2D([0], [0], color="black", lw=2.5, label="Historical (GCP/OWID)")
    )
    ax.legend(
        handles=patches,
        loc="upper left",
        fontsize=8,
        framealpha=0.85,
        edgecolor="0.7",
    )

    # ── axes decoration ──────────────────────────────────────────────────────
    ax.set_xlim(1983, 2115)
    ax.set_ylim(-35, 145)
    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("CO₂ emissions (Gt CO₂ yr⁻¹)", fontsize=11)
    ax.set_title(
        "CO₂ emissions trajectories across IPCC and CMIP scenario generations\n"
        "\"Futures avoided, opportunities lost\"",
        fontsize=12,
        pad=10,
    )
    ax.tick_params(labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


# ─── per-generation statistics ───────────────────────────────────────────────

def family_stats(time, data_dict, conv=1.0):
    """Return (mean, min, max) arrays on T_FINE across all scenarios."""
    matrix = np.array([
        interp(time, vals) * conv for vals in data_dict.values()
    ])
    mean = np.nanmean(matrix, axis=0)
    lo   = np.nanmin(matrix, axis=0)
    hi   = np.nanmax(matrix, axis=0)
    return mean, lo, hi


# ─── average-per-generation sanity-check figure ───────────────────────────────

def make_figure_avg(cmip7_scenarios, hist_years, hist_vals):
    """Single mean line per generation — sanity check for downward trend."""
    families = [
        ("SA90",  SA90_TIME,  SA90,  C_TO_CO2),
        ("IS92",  IS92_TIME,  IS92,  C_TO_CO2),
        ("SRES",  SRES_TIME,  SRES,  C_TO_CO2),
        ("RCP",   RCP_TIME,   RCP,   C_TO_CO2),
        ("SSP",   SSP_TIME,   SSP,   1.0),
        ("CMIP7", CMIP7_TIME, cmip7_scenarios, 1.0),
    ]

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axhline(0, color="black", lw=0.5, ls="--", alpha=0.3)

    gen_labels = {
        "SA90":  "SA90 (IPCC FAR, 1990)",
        "IS92":  "IS92 (IPCC SAR, 1992)",
        "SRES":  "SRES (IPCC AR4 / CMIP3, 2000)",
        "RCP":   "RCP (IPCC AR5 / CMIP5, 2009)",
        "SSP":   "SSP (IPCC AR6 / CMIP6, 2016)",
        "CMIP7": "ScenarioMIP (IPCC AR7 / CMIP7, 2026)",
    }

    for gen, t, dct, conv in families:
        if not dct:
            continue
        mean, p10, p90 = family_stats(t, dct, conv=conv)
        c = GEN_COLORS[gen]
        n = len(dct)
        ax.fill_between(T_FINE, p10, p90, color=c, alpha=0.15)
        ax.plot(T_FINE, mean, color=c, lw=2.5, label=f"{gen_labels[gen]} (n={n})")
        # annotate the 2100 end-point with n-count
        idx_2100 = np.argmin(np.abs(T_FINE - 2100))
        yval = mean[idx_2100]
        if not np.isnan(yval):
            ax.text(2101, yval, f"{yval:.0f}", fontsize=7.5,
                    va="center", color=c, fontweight="bold")

    # historical
    ax.plot(hist_years, hist_vals, color="black", lw=2.5, ls="-",
            label="Historical (GCP/OWID)", zorder=10)

    ax.set_xlim(1983, 2115)
    ax.set_ylim(-30, 100)
    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("CO₂ emissions (Gt CO₂ yr⁻¹)", fontsize=11)
    ax.set_title(
        "Mean CO₂ emissions trajectory per CMIP scenario generation\n"
        "(shading = full scenario range across all scenarios in each family)",
        fontsize=11, pad=10,
    )
    ax.legend(loc="upper left", fontsize=8.5, framealpha=0.85, edgecolor="0.7")
    ax.tick_params(labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    cmip7 = fetch_cmip7()
    hist_years, hist_vals = fetch_historical()

    prefix = date.today().strftime("%y%m%d")

    fig1 = make_figure(cmip7, hist_years, hist_vals)
    for ext in ("pdf", "svg", "png"):
        for stem in (f"{prefix}_scenariosThroughTime", "scenariosThroughTime"):
            out = OUT_DIR / f"{stem}.{ext}"
            fig1.savefig(out, dpi=300, bbox_inches="tight")
            print(f"Saved {out}")
    plt.close(fig1)

    fig2 = make_figure_avg(cmip7, hist_years, hist_vals)
    for ext in ("pdf", "svg", "png"):
        for stem in (f"{prefix}_scenariosThroughTime_avg", "scenariosThroughTime_avg"):
            out = OUT_DIR / f"{stem}.{ext}"
            fig2.savefig(out, dpi=300, bbox_inches="tight")
        print(f"Saved {out}")
    plt.close(fig2)

    print("Done.")


if __name__ == "__main__":
    main()
