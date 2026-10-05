# Ket qua T4 (tu sinh boi benchmark.py, 2026-10-05 16:54)
Gia tri = trung binh tren 5 seed [0, 1, 2, 3, 4]. Gate lien ket = 1.0 m. Radar sigma = 0.15 m, LiDAR sigma = 0.05 m.

## Bang 1 - Di thang, v = 20 m/s, quet offset
| offset_ms | method | pos_err_m_mean | ghost_rate_mean | traj_residual_m_mean | offset_est_err_ms_mean |
|---|---|---|---|---|---|
| 0 | none | 0.19 | 0.0 | 0.22 | - |
| 0 | comp_known | 0.19 | 0.0 | 0.22 | - |
| 0 | comp_est | 0.19 | 0.0 | 0.22 | 0.2 |
| 25 | none | 0.53 | 0.3 | 0.55 | - |
| 25 | comp_known | 0.19 | 0.0 | 0.22 | - |
| 25 | comp_est | 0.19 | 0.0 | 0.22 | 0.2 |
| 50 | none | 1.02 | 54.6 | 1.03 | - |
| 50 | comp_known | 0.19 | 0.0 | 0.22 | - |
| 50 | comp_est | 0.19 | 0.0 | 0.22 | 0.2 |
| 100 | none | 2.01 | 100.0 | 2.02 | - |
| 100 | comp_known | 0.19 | 0.0 | 0.22 | - |
| 100 | comp_est | 0.19 | 0.0 | 0.22 | 0.2 |
| 150 | none | 3.01 | 100.0 | 3.01 | - |
| 150 | comp_known | 0.20 | 0.0 | 0.22 | - |
| 150 | comp_est | 0.20 | 0.0 | 0.22 | 0.2 |
| 200 | none | 4.01 | 100.0 | 4.01 | - |
| 200 | comp_known | 0.20 | 0.0 | 0.22 | - |
| 200 | comp_est | 0.20 | 0.0 | 0.22 | 0.2 |

## Bang 2 - Kiem tra cong thuc sai so ~ v x delta (khong bu)
| speed_mps | offset_ms | pred_err_m_mean | pos_err_m_mean | ratio | ghost_rate_mean |
|---|---|---|---|---|---|
| 5 | 0 | 0.00 | 0.19 | - | 0.0 |
| 5 | 25 | 0.12 | 0.22 | 1.8 | 0.0 |
| 5 | 50 | 0.25 | 0.30 | 1.2 | 0.0 |
| 5 | 100 | 0.50 | 0.53 | 1.1 | 0.3 |
| 5 | 150 | 0.75 | 0.77 | 1.0 | 6.3 |
| 5 | 200 | 1.00 | 1.02 | 1.0 | 54.6 |
| 10 | 0 | 0.00 | 0.19 | - | 0.0 |
| 10 | 25 | 0.25 | 0.30 | 1.2 | 0.0 |
| 10 | 50 | 0.50 | 0.53 | 1.1 | 0.3 |
| 10 | 100 | 1.00 | 1.02 | 1.0 | 54.6 |
| 10 | 150 | 1.50 | 1.51 | 1.0 | 99.9 |
| 10 | 200 | 2.00 | 2.01 | 1.0 | 100.0 |
| 20 | 0 | 0.00 | 0.19 | - | 0.0 |
| 20 | 25 | 0.50 | 0.53 | 1.1 | 0.3 |
| 20 | 50 | 1.00 | 1.02 | 1.0 | 54.6 |
| 20 | 100 | 2.00 | 2.01 | 1.0 | 100.0 |
| 20 | 150 | 3.00 | 3.01 | 1.0 | 100.0 |
| 20 | 200 | 4.00 | 4.01 | 1.0 | 100.0 |
| 30 | 0 | 0.00 | 0.19 | - | 0.0 |
| 30 | 25 | 0.75 | 0.77 | 1.0 | 6.3 |
| 30 | 50 | 1.50 | 1.51 | 1.0 | 99.9 |
| 30 | 100 | 3.00 | 3.01 | 1.0 | 100.0 |
| 30 | 150 | 4.50 | 4.51 | 1.0 | 100.0 |
| 30 | 200 | 6.00 | 6.01 | 1.0 | 100.0 |

## Bang 3 - Offset toi han (ly thuyet: gate / v)
| speed (m/s) | km/h | delta toi han = gate / v (ms) |
|---|---|---|
| 5 | 18 | 200 |
| 10 | 36 | 100 |
| 20 | 72 | 50 |
| 30 | 108 | 33 |

## Bang 4 - Cac kich ban, delta = 100 ms, v = 20 m/s
| scenario | method | pos_err_m_mean | pos_err_p95_m_mean | ghost_rate_mean | traj_residual_m_mean | offset_est_err_ms_mean |
|---|---|---|---|---|---|---|
| straight | none | 2.01 | 2.25 | 100.0 | 2.02 | - |
| straight | comp_known | 0.19 | 0.37 | 0.0 | 0.22 | - |
| straight | comp_est | 0.19 | 0.37 | 0.0 | 0.22 | 0.2 |
| maneuver | none | 1.63 | 2.17 | 94.4 | 1.68 | - |
| maneuver | comp_known | 0.19 | 0.37 | 0.0 | 0.22 | - |
| maneuver | comp_est | 0.19 | 0.37 | 0.0 | 0.22 | 0.2 |
| jitter | none | 1.99 | 3.03 | 94.3 | 2.09 | - |
| jitter | comp_known | 0.54 | 1.21 | 11.7 | 0.65 | - |
| jitter | comp_est | 0.54 | 1.21 | 11.6 | 0.65 | 1.0 |
| standstill | none | 0.19 | 0.37 | 0.0 | 0.22 | - |
| standstill | comp_known | 0.19 | 0.37 | 0.0 | 0.22 | - |
| standstill | comp_est | 0.19 | 0.38 | 0.0 | 0.22 | 123.0 |
