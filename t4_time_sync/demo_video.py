"""Video demo T4: radar lệch timestamp -> ghost, và bù chuyển động sửa lại.

Dùng lại mô phỏng trong benchmark.py. Mỗi frame = một mẫu radar (20 Hz), phát ở 20 fps
nên video chạy đúng thời gian thực. 4 chương: Δ = 0 / 50 / 100 ms và Δ = 100 ± 30 ms (jitter).

Chạy:  python demo_video.py      -> results/demo_time_sync.gif
"""
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

from benchmark import CFG, compensate, interp2, make_truth, simulate

RAW, COMP, LIDAR, INK, MUTED, GRID = "#eb6834", "#2a78d6", "#0b0b0b", "#0b0b0b", "#52514e", "#e5e5e2"
SPEED = 20
CHAPTERS = [
    dict(title="1 · Baseline: đồng bộ chuẩn", delta_ms=0, jitter_ms=0),
    dict(title="2 · Radar trễ 50 ms", delta_ms=50, jitter_ms=0),
    dict(title="3 · Radar trễ 100 ms", delta_ms=100, jitter_ms=0),
    dict(title="4 · Failure: trễ 100 ± 30 ms (jitter)", delta_ms=100, jitter_ms=30),
]
INTRO_FRAMES = 20          # 1 s đứng hình đầu mỗi chương để đọc tiêu đề
CAR_L, CAR_W = 4.5, 1.8


def build_chapter(ch, seed=0):
    cfg = dict(CFG, duration_s=5.0, jitter_ms=ch["jitter_ms"])
    rng = np.random.default_rng(seed)
    truth = make_truth("straight", SPEED, cfg["duration_s"])
    delta = ch["delta_ms"] / 1000
    t_l, z_l, t_r, z_r = simulate(truth, delta, rng, ch["jitter_ms"] / 1000, cfg)
    comp = compensate(t_r, z_r, t_l, z_l, delta)          # bù bằng Δ danh định
    gt = interp2(t_r, truth[0], truth[1])
    ref = interp2(t_r, t_l, z_l)                          # vị trí LiDAR tại cùng timestamp
    return dict(ch, t=t_r - t_r[0], gt=gt, ref=ref, raw=z_r, comp=comp,
                err_raw=np.linalg.norm(z_r - gt, axis=1), err_comp=np.linalg.norm(comp - gt, axis=1),
                ghost_raw=np.linalg.norm(z_r - ref, axis=1) > CFG["gate_m"],
                ghost_comp=np.linalg.norm(comp - ref, axis=1) > CFG["gate_m"])


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    chapters = [build_chapter(c) for c in CHAPTERS]
    frames = []
    for ci, c in enumerate(chapters):
        frames += [(ci, 0, True)] * INTRO_FRAMES + [(ci, k, False) for k in range(len(c["t"]))]
    frames += [(len(chapters) - 1, len(chapters[-1]["t"]) - 1, False)] * 40   # giữ frame cuối 2 s

    plt.rcParams.update({"font.size": 11, "axes.edgecolor": MUTED, "axes.labelcolor": MUTED,
                         "xtick.color": MUTED, "ytick.color": MUTED})
    fig = plt.figure(figsize=(12.8, 7.2), dpi=80, facecolor="white")
    gs = fig.add_gridspec(2, 2, width_ratios=[1.35, 1], height_ratios=[1, 1],
                          left=0.05, right=0.97, top=0.86, bottom=0.08, wspace=0.16, hspace=0.35)
    ax_map, ax_err, ax_txt = fig.add_subplot(gs[:, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, 1])
    fig.suptitle("Lệch thời gian LiDAR ↔ radar: sai số vị trí, ghost, và bù chuyển động",
                 x=0.05, ha="left", fontsize=15, color=INK)
    sub = fig.text(0.05, 0.915, "", fontsize=12, color=MUTED)

    # --- bản đồ nhìn từ trên xuống (camera bám theo xe)
    for y in (1.75, 5.25):
        for x0 in np.arange(0, 200, 6):
            ax_map.plot([x0, x0 + 3], [y, y], color="#b8b7b0", lw=2, zorder=0)
    car = Rectangle((0, 0), CAR_L, CAR_W, fc="#d9d8d2", ec=MUTED, lw=1.5, zorder=1)
    ghost_car = Rectangle((0, 0), CAR_L, CAR_W, fc="none", ec=RAW, lw=2, ls="--", zorder=1)
    ghost_car_comp = Rectangle((0, 0), CAR_L, CAR_W, fc="none", ec=COMP, lw=2, ls="--", zorder=1)
    gate = Circle((0, 0), CFG["gate_m"], fc="none", ec=LIDAR, lw=1.2, ls=":", zorder=2)
    for p in (car, ghost_car, ghost_car_comp, gate):
        ax_map.add_patch(p)
    trail_raw = ax_map.scatter([], [], s=30, color=RAW, alpha=0.35, zorder=3)
    trail_comp = ax_map.scatter([], [], s=30, color=COMP, alpha=0.35, zorder=3)
    pt_lidar, = ax_map.plot([], [], "s", ms=11, color=LIDAR, mec="white", mew=1.5, zorder=5, label="LiDAR (chuẩn)")
    pt_raw, = ax_map.plot([], [], "o", ms=13, color=RAW, mec="white", mew=2, zorder=6, label="Radar, không bù")
    pt_comp, = ax_map.plot([], [], "o", ms=13, color=COMP, mec="white", mew=2, zorder=6, label="Radar, đã bù")
    ghost_lbl = ax_map.text(0, 0, "GHOST", color=RAW, fontsize=13, weight="bold", ha="center", zorder=7)
    gate_lbl = ax_map.text(0, 0, "gate 1 m", color=MUTED, fontsize=9, ha="center", zorder=7)
    ax_map.set_aspect("equal")
    ax_map.set_xlabel("x (m) · camera bám theo xe, v = 20 m/s (72 km/h)")
    ax_map.set_ylabel("y (m)")
    ax_map.legend(loc="lower left", frameon=True, framealpha=0.9, edgecolor="none", fontsize=10, ncol=3)
    ax_map.spines[["top", "right"]].set_visible(False)

    # --- sai số theo thời gian
    ln_raw, = ax_err.plot([], [], color=RAW, lw=2, label="không bù")
    ln_comp, = ax_err.plot([], [], color=COMP, lw=2, label="đã bù")
    ax_err.axhline(CFG["gate_m"], color=MUTED, ls="--", lw=1)
    ax_err.text(0.05, CFG["gate_m"] + 0.08, "gate liên kết 1 m", color=MUTED, fontsize=9)
    ax_err.set_xlim(0, 4.2)
    ax_err.set_ylim(0, 3.6)
    ax_err.set_title("Offset error so với ground truth", loc="left", fontsize=12, color=INK)
    ax_err.set_xlabel("thời gian trong chương (s)")
    ax_err.set_ylabel("m")
    ax_err.grid(True, color=GRID)
    ax_err.legend(loc="upper right", frameon=False, fontsize=10)
    ax_err.spines[["top", "right"]].set_visible(False)

    ax_txt.axis("off")
    txt = ax_txt.text(0, 1, "", va="top", ha="left", fontsize=12.5, color=INK, family=["Consolas", "Courier New", "DejaVu Sans Mono"],
                      transform=ax_txt.transAxes, linespacing=1.6)
    banner = ax_map.text(0.5, 0.55, "", transform=ax_map.transAxes, ha="center", va="center",
                         fontsize=20, weight="bold", color=INK, zorder=10,
                         bbox=dict(boxstyle="round,pad=0.6", fc="white", ec=MUTED, lw=1.2))

    def draw(frame):
        ci, k, intro = frame
        c = chapters[ci]
        sub.set_text(f"{c['title']}   ·   Δ = {c['delta_ms']} ms"
                     + (f" ± {c['jitter_ms']} ms" if c["jitter_ms"] else ""))
        g, ref, raw, comp = c["gt"][k], c["ref"][k], c["raw"][k], c["comp"][k]
        ax_map.set_xlim(g[0] - 6, g[0] + 6)
        ax_map.set_ylim(g[1] - 3.2, g[1] + 3.2)
        car.set_xy((g[0] - CAR_L / 2, g[1] - CAR_W / 2))
        gate.center = tuple(ref)
        gate_lbl.set_position((ref[0], ref[1] + CFG["gate_m"] + 0.15))
        lo = max(0, k - 8)
        trail_raw.set_offsets(c["raw"][lo:k])
        trail_comp.set_offsets(c["comp"][lo:k])
        pt_lidar.set_data([ref[0]], [ref[1]])
        pt_raw.set_data([raw[0]], [raw[1]])
        pt_comp.set_data([comp[0]], [comp[1]])
        is_ghost = c["ghost_raw"][k] and not intro
        ghost_car.set_visible(is_ghost)
        ghost_car.set_xy((raw[0] - CAR_L / 2, raw[1] - CAR_W / 2))
        ghost_lbl.set_visible(is_ghost)
        ghost_lbl.set_position((raw[0], raw[1] + CAR_W / 2 + 0.35))
        ghost_car_comp.set_visible(c["ghost_comp"][k] and not intro)   # jitter: bù hằng số vẫn lọt ghost
        ghost_car_comp.set_xy((comp[0] - CAR_L / 2, comp[1] - CAR_W / 2))

        n = 0 if intro else k + 1
        ln_raw.set_data(c["t"][:n], c["err_raw"][:n])
        ln_comp.set_data(c["t"][:n], c["err_comp"][:n])
        banner.set_text(c["title"] if intro else "")
        banner.set_visible(intro)
        if n:
            gr, gc = c["ghost_raw"][:n].mean() * 100, c["ghost_comp"][:n].mean() * 100
            er, ec = c["err_raw"][:n].mean(), c["err_comp"][:n].mean()
            txt.set_text(
                f"Dự đoán  v × Δ        = {SPEED} × {c['delta_ms'] / 1000:.2f} = {SPEED * c['delta_ms'] / 1000:.1f} m\n"
                f"                   không bù    đã bù\n"
                f"Offset error TB   {er:6.2f} m   {ec:6.2f} m\n"
                f"Ghost rate        {gr:6.1f} %   {gc:6.1f} %\n"
                f"Số mẫu radar      {n:6d}")
        else:
            txt.set_text("")
        return []

    anim = FuncAnimation(fig, draw, frames=frames, interval=50, blit=False)
    path = os.path.join(out, "demo_time_sync.gif")
    anim.save(path, writer=PillowWriter(fps=20))
    for ci, k in [(0, 40), (2, 40), (3, 52)]:              # ảnh tĩnh cho slide
        draw((ci, k, False))
        fig.savefig(os.path.join(out, f"demo_frame_ch{ci + 1}.png"), dpi=80)
    print(f"[done] {len(frames)} frame -> {path} ({os.path.getsize(path) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
