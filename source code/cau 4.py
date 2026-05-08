import pandas as pd
import numpy as np

def analyze_and_find_best_team(input_file, output_file):
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {input_file}")
        return

    numeric_cols = ['90s', 'CrdY', 'CrdR', '2CrdY', 'Fls', 'Fld', 'Off', 'Crs', 'Int', 'TklW', 'PKwon', 'PKcon', 'OG']

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    team_stats = df.groupby('Squad')[numeric_cols].agg(['median', 'mean', 'std'])
    team_stats.columns = [f'{stat}_{metric}' for stat, metric in team_stats.columns]
    team_stats.to_csv(output_file)

    leader_counts = {}
    positive_stats = ['90s', 'Fld', 'Crs', 'Int', 'TklW', 'PKwon']

    print("--- CHI TIẾT ĐỘI DẪN ĐẦU TỪNG CHỈ SỐ ---")
    for col in numeric_cols:
        mean_col = f'{col}_mean'
        top_team = team_stats[mean_col].idxmax()
        top_value = team_stats[mean_col].max()
        print(f"{col:10}: {top_team:20} (Giá trị: {top_value:.2f})")

        if col in positive_stats:
            leader_counts[top_team] = leader_counts.get(top_team, 0) + 1

    if leader_counts:
        best_team = max(leader_counts, key=leader_counts.get)
        max_leads = leader_counts[best_team]

        print("\n" + "=" * 50)
        print(f"KẾT LUẬN PHONG ĐỘ GIẢI NGOẠI HẠNG ANH 2025-2026:")
        print(f"Đội bóng có phong độ tốt nhất là: {best_team.upper()}")
        print(f"Lý do: Đội dẫn đầu ở {max_leads} hạng mục chỉ số tích cực.")
        print("=" * 50)
    else:
        print("\n Không đủ dữ liệu để kết luận phong độ.")

if __name__ == "__main__":
    analyze_and_find_best_team('cầu thủ thi đấu trên 90ph.csv', 'thống kê median mean std của các đội bóng.csv')