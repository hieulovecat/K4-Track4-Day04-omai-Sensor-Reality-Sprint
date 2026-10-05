"""T4 - Time sync / motion compensation benchmark (mo phong 2D).

Bai toan: xe ADAS fuse LiDAR (10 Hz, timestamp dung) voi radar (20 Hz) bi lech
timestamp delta. Radar do vi tri o thoi diem t - delta nhung gan nhan t, nen
khi doi tuong di chuyen, diem radar bi lech ~ v * delta so voi LiDAR.

So sanh 3 phuong an:
  none        - dung timestamp radar nhu nhan duoc (khong bu)
  comp_known  - biet delta tu datasheet/calib, bu chuyen dong: z + v_est * delta
  comp_est    - tu uoc luong delta bang grid search (min residual LiDAR-radar), roi bu

Metric (cung cach tinh cho moi dieu kien):
  pos_err_m         offset error theo vi tri: |radar da xu ly - ground truth tai t_stamp| (m)
  ghost_rate        ti le diem radar nam ngoai gate lien ket voi track LiDAR (%)
                    -> fusion se tao object thu 2 ("ghost") hoac bo diem radar
  traj_residual_m   RMS khoang cach radar <-> LiDAR noi suy cung timestamp (m),
                    tinh duoc online, khong can ground truth
  offset_est_err_ms |delta_uoc_luong - delta_that| (ms), chi co o comp_est

Chay:  python benchmark.py            (ket qua vao ./results)
"""
import argparse
import datetime
import os
import platform
import sys

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CFG = dict(
    duration_s=20.0,
    lidar_hz=10.0, lidar_sigma_m=0.05,
    radar_hz=20.0, radar_sigma_m=0.15, radar_phase_s=0.013,
    gate_m=1.0,                         # nguong lien ket radar-LiDAR
    offsets_ms=[0, 25, 50, 100, 150, 200],
    speeds_mps=[5, 10, 20, 30],         # 18 / 36 / 72 / 108 km/h
    main_speed_mps=20,
    scenario_offset_ms=100,
    jitter_ms=30,                       # do lech chuan jitter cua offset (kich ban "jitter")
    search_ms=300,                      # grid search delta trong [-300, 300] ms, buoc 1 ms
    seeds=[0, 1, 2, 3, 4],
)
METHODS = ["none", "comp_known", "comp_est"]
COLORS = {"none": "#eb6834", "comp_known": "#2a78d6", "comp_est": "#1baf7a"}
LABELS = {"none": "Khong bu", "comp_known": "Bu, biet delta", "comp_est": "Bu, tu uoc luong delta"}


# ---------------------------------------------------------------- ground truth
def make_truth(scenario, speed, dur, dt=1e-3):
    """Quy dao doi tuong tren luoi min (1 ms). Tra ve t, pos (N,2), vel (N,2)."""
    t = np.arange(-1.0, dur + 1.0, dt)
    if scenario in ("straight", "jitter", "standstill"):
        v = 0.0 if scenario == "standstill" else float(speed)
        vel = np.stack([np.full_like(t, v), np.zeros_like(t)], 1)
        pos = np.stack([10.0 + v * t, np.full_like(t, 3.5)], 1)
        return t, pos, vel
    if scenario == "maneuver":
        # di thang -> phanh -3 m/s2 -> re (gia toc ngang 4 m/s2) -> tang toc +2 m/s2
        acc = np.where((t >= 5) & (t < 8), -3.0, 0.0) + np.where((t >= 12) & (t < 16), 2.0, 0.0)
        spd = np.maximum(speed + np.cumsum(acc) * dt, 1.0)
        yaw_rate = np.where((t >= 8) & (t < 12), 4.0 / spd, 0.0)
        heading = np.cumsum(yaw_rate) * dt
        vel = np.stack([spd * np.cos(heading), spd * np.sin(heading)], 1)
        pos = np.array([10.0, 3.5]) + np.cumsum(vel, 0) * dt
        return t, pos, vel
    raise ValueError(scenario)


def interp2(tq, t, xy):
    return np.stack([np.interp(tq, t, xy[:, i]) for i in range(2)], 1)


# ---------------------------------------------------------------- sensors
def simulate(truth, delta_s, rng, jitter_s=0.0, cfg=CFG):
    t, pos, _ = truth
    dur = cfg["duration_s"]
    t_l = np.arange(0.0, dur, 1 / cfg["lidar_hz"])
    z_l = interp2(t_l, t, pos) + rng.normal(0, cfg["lidar_sigma_m"], (len(t_l), 2))
    t_r = np.arange(cfg["radar_phase_s"], dur, 1 / cfg["radar_hz"])   # timestamp radar ghi ra
    d = delta_s + (rng.normal(0, jitter_s, len(t_r)) if jitter_s > 0 else 0.0)
    z_r = interp2(t_r - d, t, pos) + rng.normal(0, cfg["radar_sigma_m"], (len(t_r), 2))
    # chi danh gia cac mau ma LiDAR noi suy duoc voi moi delta trong vung search
    m = cfg["search_ms"] / 1000 + 0.1
    keep = (t_r > m) & (t_r < t_l[-1] - m)
    return t_l, z_l, t_r[keep], z_r[keep]


# ---------------------------------------------------------------- methods
def estimate_offset(t_r, z_r, t_l, z_l, search_ms):
    """Temporal calibration don gian: tim delta lam residual radar-LiDAR nho nhat."""
    grid = np.arange(-search_ms, search_ms + 1) / 1000.0
    cost = np.array([np.mean(np.sum((z_r - interp2(t_r - g, t_l, z_l)) ** 2, 1)) for g in grid])
    return grid[np.argmin(cost)], grid, cost


def compensate(t_r, z_r, t_l, z_l, delta_hat):
    """Motion compensation gia dinh van toc khong doi: day diem radar toi t_stamp."""
    v_l = np.gradient(z_l, t_l, axis=0)                    # van toc uoc luong tu track LiDAR
    v = interp2(t_r - delta_hat / 2, t_l, v_l)
    return z_r + v * delta_hat


def run_once(scenario, speed, offset_ms, seed, cfg=CFG):
    rng = np.random.default_rng(seed)
    truth = make_truth(scenario, speed, cfg["duration_s"])
    delta = offset_ms / 1000.0
    jitter = cfg["jitter_ms"] / 1000.0 if scenario == "jitter" else 0.0
    t_l, z_l, t_r, z_r = simulate(truth, delta, rng, jitter, cfg)
    gt = interp2(t_r, truth[0], truth[1])
    lidar_ref = interp2(t_r, t_l, z_l)
    delta_hat, _, _ = estimate_offset(t_r, z_r, t_l, z_l, cfg["search_ms"])

    rows = []
    for method in METHODS:
        if method == "none":
            p, d_used = z_r, np.nan
        elif method == "comp_known":
            p, d_used = compensate(t_r, z_r, t_l, z_l, delta), delta
        else:
            p, d_used = compensate(t_r, z_r, t_l, z_l, delta_hat), delta_hat
        err = np.linalg.norm(p - gt, axis=1)
        res = np.linalg.norm(p - lidar_ref, axis=1)
        rows.append(dict(
            scenario=scenario, speed_mps=speed, offset_ms=offset_ms, seed=seed, method=method,
            n_radar=len(t_r),
            pos_err_m=err.mean(), pos_err_p95_m=np.percentile(err, 95),
            ghost_rate=(res > cfg["gate_m"]).mean() * 100,
            traj_residual_m=np.sqrt(np.mean(res ** 2)),
            offset_est_err_ms=abs(d_used - delta) * 1000 if method == "comp_est" else np.nan,
            delta_hat_ms=delta_hat * 1000,
            pred_err_m=abs(speed) * delta if scenario != "standstill" else 0.0,
        ))
    return rows


# ---------------------------------------------------------------- plots
def style(ax, title, xlabel, ylabel):
    ax.set_title(title, loc="left", fontsize=11)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, color="#e5e5e2", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)


def plot_timeline(out, cfg=CFG):
    delta = 0.1
    t_l = np.arange(0, 0.6, 1 / cfg["lidar_hz"])
    t_r = np.arange(cfg["radar_phase_s"], 0.6, 1 / cfg["radar_hz"])
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.vlines(t_l, 1.8, 2.2, color="#52514e", lw=2)
    ax.vlines(t_r, 0.8, 1.2, color=COLORS["none"], lw=2)
    ax.vlines(t_r - delta, -0.2, 0.2, color=COLORS["comp_known"], lw=2)
    for tr in t_r[2:6]:
        ax.annotate("", xy=(tr - delta, 0.25), xytext=(tr, 0.75),
                    arrowprops=dict(arrowstyle="->", color="#8a8984", lw=1))
    ax.set_yticks([0, 1, 2], ["Radar: thoi diem do THAT", "Radar: timestamp ghi ra", "LiDAR (dung)"])
    ax.text(0.33, 0.5, "delta = 100 ms", color="#52514e", fontsize=9)
    style(ax, "Timeline multi-sensor: radar gan nhan muon hon thoi diem do 100 ms", "thoi gian (s)", "")
    ax.grid(False)
    ax.set_xlim(-0.12, 0.62)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "fig1_timeline.png"), dpi=150)
    plt.close(fig)


def plot_sweep(agg, out, cfg=CFG):
    d = agg[(agg.scenario == "straight") & (agg.speed_mps == cfg["main_speed_mps"])]
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for key, ax, title, ylabel in [
        ("pos_err_m", axes[0], "Offset error (vi tri)", "sai so vi tri trung binh (m)"),
        ("ghost_rate", axes[1], f"Ghost rate (gate {cfg['gate_m']} m)", "% diem radar ngoai gate"),
        ("traj_residual_m", axes[2], "Trajectory residual radar-LiDAR", "RMS residual (m)"),
    ]:
        for m in METHODS:
            s = d[d.method == m]
            ax.errorbar(s.offset_ms, s[key + "_mean"], yerr=s[key + "_std"], color=COLORS[m],
                        lw=2, marker="o", ms=6, capsize=3, label=LABELS[m],
                        ls="--" if m == "comp_est" else "-")  # comp_est trung comp_known -> net dut
        if key == "pos_err_m":
            x = np.array(cfg["offsets_ms"])
            ax.plot(x, cfg["main_speed_mps"] * x / 1000, "--", color="#8a8984", lw=1.5,
                    label="Cong thuc v x delta")
        style(ax, title, "time offset delta (ms)", ylabel)
    axes[0].legend(frameon=False, fontsize=9)
    fig.suptitle(f"Kich ban di thang, v = {cfg['main_speed_mps']} m/s, "
                 f"{len(cfg['seeds'])} seed (thanh loi = std)", x=0.01, ha="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "fig2_metrics_vs_offset.png"), dpi=150)
    plt.close(fig)


def plot_formula(agg, out):
    d = agg[(agg.scenario == "straight") & (agg.method == "none")]
    fig, ax = plt.subplots(figsize=(5.5, 5))
    ax.scatter(d.pred_err_m_mean, d.pos_err_m_mean, s=60, color=COLORS["comp_known"],
               edgecolor="white", linewidth=1.5, zorder=3)
    lim = max(d.pred_err_m_mean.max(), d.pos_err_m_mean.max()) * 1.05
    ax.plot([0, lim], [0, lim], "--", color="#8a8984", lw=1.5, label="y = x")
    ax.legend(frameon=False)
    style(ax, "Kiem tra: sai so ~ v x delta", "du doan v x delta (m)", "do duoc, khong bu (m)")
    fig.tight_layout()
    fig.savefig(os.path.join(out, "fig3_formula_check.png"), dpi=150)
    plt.close(fig)


def plot_scenarios(agg, out, cfg=CFG):
    d = agg[(agg.offset_ms == cfg["scenario_offset_ms"]) & (agg.speed_mps == cfg["main_speed_mps"])]
    scen = ["straight", "maneuver", "jitter", "standstill"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    w = 0.26
    x = np.arange(len(scen))
    for i, m in enumerate(METHODS):
        s = d[d.method == m].set_index("scenario").loc[scen]
        axes[0].bar(x + (i - 1) * w, s.pos_err_m_mean, w * 0.92, color=COLORS[m], label=LABELS[m])
        axes[1].bar(x + (i - 1) * w, s.ghost_rate_mean, w * 0.92, color=COLORS[m])
    for ax in axes:
        ax.set_xticks(x, ["di thang", "phanh + re", f"jitter {cfg['jitter_ms']} ms", "dung yen"])
    style(axes[0], f"Offset error, delta = {cfg['scenario_offset_ms']} ms", "", "m")
    style(axes[1], "Ghost rate", "", "%")
    axes[0].legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "fig4_scenarios.png"), dpi=150)
    plt.close(fig)


def plot_trajectory(out, cfg=CFG):
    rng = np.random.default_rng(0)
    delta = cfg["scenario_offset_ms"] / 1000
    truth = make_truth("maneuver", cfg["main_speed_mps"], cfg["duration_s"])
    t_l, z_l, t_r, z_r = simulate(truth, delta, rng)
    p = compensate(t_r, z_r, t_l, z_l, delta)
    gt = interp2(t_r, truth[0], truth[1])
    w = (t_r > 7.5) & (t_r < 12.5)
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.plot(gt[w, 0], gt[w, 1], color="#52514e", lw=2, label="Ground truth tai t_stamp")
    ax.scatter(z_r[w, 0], z_r[w, 1], s=18, color=COLORS["none"], label="Radar khong bu")
    ax.scatter(p[w, 0], p[w, 1], s=18, color=COLORS["comp_known"], label="Radar da bu")
    ax.set_aspect("equal")
    ax.legend(frameon=False, fontsize=9)
    style(ax, f"Doan re (t = 7.5-12.5 s), delta = {cfg['scenario_offset_ms']} ms", "x (m)", "y (m)")
    fig.tight_layout()
    fig.savefig(os.path.join(out, "fig5_trajectory_turn.png"), dpi=150)
    plt.close(fig)


def plot_cost(out, cfg=CFG):
    fig, ax = plt.subplots(figsize=(7, 4))
    for scen, color in [("straight", COLORS["comp_est"]), ("standstill", COLORS["none"])]:
        rng = np.random.default_rng(0)
        truth = make_truth(scen, cfg["main_speed_mps"], cfg["duration_s"])
        t_l, z_l, t_r, z_r = simulate(truth, cfg["scenario_offset_ms"] / 1000, rng)
        dh, grid, cost = estimate_offset(t_r, z_r, t_l, z_l, cfg["search_ms"])
        ax.plot(grid * 1000, np.sqrt(cost), color=color, lw=2,
                label=f"{'di thang 20 m/s' if scen == 'straight' else 'dung yen'} (uoc luong {dh*1000:.0f} ms)")
    ax.axvline(cfg["scenario_offset_ms"], color="#8a8984", ls="--", lw=1.5, label="delta that = 100 ms")
    ax.set_yscale("log")
    ax.legend(frameon=False, fontsize=9)
    style(ax, "Ham chi phi khi uoc luong offset", "delta thu (ms)", "RMS residual (m, log)")
    fig.tight_layout()
    fig.savefig(os.path.join(out, "fig6_offset_cost.png"), dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------- report
def md_table(df, cols, fmt):
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    return head + "".join("| " + " | ".join(fmt[c](r[c]) if c in fmt else str(r[c]) for c in cols)
                          + " |\n" for _, r in df.iterrows())


def write_summary(agg, out, cfg=CFG):
    f2 = lambda v: f"{v:.2f}"
    f1 = lambda v: f"{v:.1f}"
    fn = lambda v: "-" if pd.isna(v) else f"{v:.1f}"
    lines = [f"# Ket qua T4 (tu sinh boi benchmark.py, {datetime.datetime.now():%Y-%m-%d %H:%M})\n",
             f"Gia tri = trung binh tren {len(cfg['seeds'])} seed {cfg['seeds']}. "
             f"Gate lien ket = {cfg['gate_m']} m. Radar sigma = {cfg['radar_sigma_m']} m, "
             f"LiDAR sigma = {cfg['lidar_sigma_m']} m.\n"]

    d = agg[(agg.scenario == "straight") & (agg.speed_mps == cfg["main_speed_mps"])]
    lines.append(f"\n## Bang 1 - Di thang, v = {cfg['main_speed_mps']} m/s, quet offset\n")
    lines.append(md_table(d, ["offset_ms", "method", "pos_err_m_mean", "ghost_rate_mean",
                              "traj_residual_m_mean", "offset_est_err_ms_mean"],
                          {"pos_err_m_mean": f2, "ghost_rate_mean": f1,
                           "traj_residual_m_mean": f2, "offset_est_err_ms_mean": fn}))

    d = agg[(agg.scenario == "straight") & (agg.method == "none")].copy()
    d["ratio"] = d.pos_err_m_mean / d.pred_err_m_mean.replace(0, np.nan)
    lines.append("\n## Bang 2 - Kiem tra cong thuc sai so ~ v x delta (khong bu)\n")
    lines.append(md_table(d, ["speed_mps", "offset_ms", "pred_err_m_mean", "pos_err_m_mean",
                              "ratio", "ghost_rate_mean"],
                          {"pred_err_m_mean": f2, "pos_err_m_mean": f2, "ratio": fn,
                           "ghost_rate_mean": f1}))

    lines.append("\n## Bang 3 - Offset toi han (ly thuyet: gate / v)\n")
    lines.append("| speed (m/s) | km/h | delta toi han = gate / v (ms) |\n|---|---|---|\n")
    for v in cfg["speeds_mps"]:
        lines.append(f"| {v} | {v*3.6:.0f} | {cfg['gate_m']/v*1000:.0f} |\n")

    d = agg[(agg.offset_ms == cfg["scenario_offset_ms"]) & (agg.speed_mps == cfg["main_speed_mps"])]
    lines.append(f"\n## Bang 4 - Cac kich ban, delta = {cfg['scenario_offset_ms']} ms, "
                 f"v = {cfg['main_speed_mps']} m/s\n")
    lines.append(md_table(d, ["scenario", "method", "pos_err_m_mean", "pos_err_p95_m_mean",
                              "ghost_rate_mean", "traj_residual_m_mean", "offset_est_err_ms_mean"],
                          {"pos_err_m_mean": f2, "pos_err_p95_m_mean": f2, "ghost_rate_mean": f1,
                           "traj_residual_m_mean": f2, "offset_est_err_ms_mean": fn}))
    with open(os.path.join(out, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write("".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    print(f"[run] {datetime.datetime.now().isoformat(timespec='seconds')} python {platform.python_version()} "
          f"numpy {np.__version__} cmd: {' '.join(sys.argv)}")
    print(f"[cfg] {CFG}")
    rows = []
    for seed in CFG["seeds"]:
        for v in CFG["speeds_mps"]:
            for off in CFG["offsets_ms"]:
                rows += run_once("straight", v, off, seed)
        for scen in ["maneuver", "jitter", "standstill"]:
            rows += run_once(scen, CFG["main_speed_mps"], CFG["scenario_offset_ms"], seed)
    raw = pd.DataFrame(rows)
    raw.to_csv(os.path.join(args.out, "results_raw.csv"), index=False)

    metrics = ["pos_err_m", "pos_err_p95_m", "ghost_rate", "traj_residual_m",
               "offset_est_err_ms", "delta_hat_ms", "pred_err_m"]
    agg = raw.groupby(["scenario", "speed_mps", "offset_ms", "method"], sort=False)[metrics] \
             .agg(["mean", "std"])
    agg.columns = [f"{a}_{b}" for a, b in agg.columns]
    agg = agg.reset_index()
    agg.to_csv(os.path.join(args.out, "results_agg.csv"), index=False)

    plot_timeline(args.out)
    plot_sweep(agg, args.out)
    plot_formula(agg, args.out)
    plot_scenarios(agg, args.out)
    plot_trajectory(args.out)
    plot_cost(args.out)
    write_summary(agg, args.out)

    show = agg[(agg.speed_mps == CFG["main_speed_mps"])][
        ["scenario", "offset_ms", "method", "pos_err_m_mean", "ghost_rate_mean",
         "traj_residual_m_mean", "offset_est_err_ms_mean"]]
    print(show.to_string(index=False, float_format=lambda v: f"{v:.2f}"))
    print(f"[done] {len(raw)} dong ket qua -> {args.out}")


if __name__ == "__main__":
    main()
