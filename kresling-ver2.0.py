import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 一部環境では不要だけど一応

def main():
    # 設計変数
    a = 10
    b = 25
    θ = 110
    n = 6

    # 開き角度
    r = 30 # 90より大きく180未満

    # ★ origamis 配列を用意（2層 × n点 × xyz）
    origamis = np.zeros((2, n, 3), dtype=float)

    # ======= ここから下は、あなたのアルゴリズムそのまま =======
    origamis[0, 0,0 ] = (a / 2.0) / np.tan(np.radians(180/n))
    origamis[0, 0, 1] = a / 2.0
    origamis[0, 0, 2] = 0

    for i in range(1, n):
        angle = np.radians(360/n)
        x_prev = origamis[0, i-1, 0]
        y_prev = origamis[0, i-1, 1]
        origamis[0, i, 0] = x_prev * np.cos(angle) - y_prev * np.sin(angle)
        origamis[0, i, 1] = x_prev * np.sin(angle) + y_prev * np.cos(angle)
        origamis[0, i, 2] = 0

    origamis[1, 0, 0] = origamis[0, 0, 0] - b * np.sin(np.radians(180 - θ)) * np.cos(np.radians(180 - r))
    origamis[1, 0, 1] = b * np.cos(np.radians(180-θ)) + origamis[0, 0, 1]
    origamis[1, 0, 2] = b * np.sin(np.radians(180 - θ)) * np.sin(np.radians(180 - r))

    for j in range(1, n):
        angle = np.radians(360/n)
        x_prev = origamis[1, j-1, 0]
        y_prev = origamis[1, j-1, 1]
        origamis[1, j, 0] = x_prev * np.cos(angle) - y_prev * np.sin(angle)
        origamis[1, j, 1] = x_prev * np.sin(angle) + y_prev * np.cos(angle)
        origamis[1, j, 2] = origamis[1, 0, 2]

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

    # ===== 接続リストを「変数」で自動生成 =====
    # connections: [((layer1, idx1), (layer2, idx2)), ...]
    connections = []

    # 各 layer ごとに多角形の輪郭を一周つなぐ
    for h in range(2):           # layer 0, 1
        for i in range(n):       # 頂点 i → i+1 (最後は 0 に戻る)
            connections.append(((h, i), (h, (i + 1) % n)))

    for i in range(n):
        connections.append(((0, i), (1, i)))
        connections.append(((0, i), (1, (i+1) % n)))

    for j in range(0, 2):
        for i in range(2, n-1):
            connections.append(((j, i), (j,0)))

    # ===== connections を使って線を描画 =====
    for (layer1, idx1), (layer2, idx2) in connections:
        x_vals = [origamis[layer1, idx1, 0], origamis[layer2, idx2, 0]]
        y_vals = [origamis[layer1, idx1, 1], origamis[layer2, idx2, 1]]
        z_vals = [origamis[layer1, idx1, 2], origamis[layer2, idx2, 2]]
        ax.plot(x_vals, y_vals, z_vals, color='black', linewidth=1)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    ax.set_title('Origami Points')

    # 見やすいようにスケールを揃える
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
