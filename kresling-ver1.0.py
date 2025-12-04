import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 一部環境では不要だけど一応

def main():
    # 設計変数
    a = 5
    b = 10
    θ = 100
    n = 6

    # 開き角度
    r = 150

    # ★ ここだけ追加：origamis 配列を用意（2層 × n点 × xyz）
    origamis = np.zeros((2, n, 3), dtype=float)

    # ======= ここから下は、あなたのアルゴリズムそのまま =======

    origamis[0, 0, 0] = (a / 2) / np.tan(np.radians(180/n))
    origamis[0, 0, 1] = a / 2
    origamis[0, 0, 2] = 0

    for i in range(1, n):
        origamis[0, i, 0] = origamis[0, i-1, 0] * np.cos(np.radians(360/n)) - origamis[0, i-1, 1] * np.sin(np.radians(360/n))
        origamis[0, i, 1] = origamis[0, i-1, 0] * np.sin(np.radians(360/n)) + origamis[0, i-1, 1] * np.cos(np.radians(360/n))
        origamis[0, i, 2] = 0

    origamis[1, 0, 0] = origamis[0, 0, 0] - b * np.sin(np.radians(180 - θ)) * np.cos(np.radians(180 - r))
    f1 = b**2-b**2 * np.sin(np.radians(180-θ))**2 * np.sin(np.radians(180 - r))**2-b**2 * np.sin(np.radians(180-θ))**2 * np.cos(np.radians(180 - r))**2
    origamis[1, 0, 1] = np.sqrt(f1)
    origamis[1, 0, 2] = b * np.sin(np.radians(180 - θ)) * np.sin(np.radians(180 - r))

    for j in range(1, n):
        origamis[1, j, 0] = origamis[1, j-1, 0] * np.cos(np.radians(360/n)) - origamis[1, j-1, 1] * np.sin(np.radians(360/n))
        origamis[1, j, 1] = origamis[1, j-1, 0] * np.sin(np.radians(360/n)) + origamis[1, j-1, 1] * np.cos(np.radians(360/n))
        origamis[1, j, 2] = origamis[1, j-1, 2]

    # ===== 点の座標を print =====
    print("=== layer 0 の点 ===")
    for i in range(n):
        x, y, z = origamis[0, i]
        print(f"0層, 頂点{i}: ({x:.3f}, {y:.3f}, {z:.3f})")

    print("\n=== layer 1 の点 ===")
    for i in range(n):
        x, y, z = origamis[1, i]
        print(f"1層, 頂点{i}: ({x:.3f}, {y:.3f}, {z:.3f})")

    # ===== 3D プロット =====
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(origamis[0, :, 0], origamis[0, :, 1], origamis[0, :, 2], marker='o', label='layer 0')
    ax.scatter(origamis[1, :, 0], origamis[1, :, 1], origamis[1, :, 2], marker='^', label='layer 1')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    ax.set_title('Origami Points')

    # 見やすいようにスケールを揃える（アルゴリズムには関係ない見た目調整）
    all_pts = origamis.reshape(-1, 3)
    x_min, y_min, z_min = all_pts.min(axis=0)
    x_max, y_max, z_max = all_pts.max(axis=0)
    max_range = max(x_max - x_min, y_max - y_min, z_max - z_min)
    x_mid = (x_max + x_min) / 2.0
    y_mid = (y_max + y_min) / 2.0
    z_mid = (z_max + z_min) / 2.0
    ax.set_xlim(x_mid - max_range / 2.0, x_mid + max_range / 2.0)
    ax.set_ylim(y_mid - max_range / 2.0, y_mid + max_range / 2.0)
    ax.set_zlim(z_mid - max_range / 2.0, z_mid + max_range / 2.0)

    plt.show()

if __name__ == "__main__":
    main()
