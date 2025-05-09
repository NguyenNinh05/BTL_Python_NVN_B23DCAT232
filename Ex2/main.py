import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import defaultdict

if not os.path.exists('../results'):
    os.makedirs('../results')

def load_data():
    try:
        df = pd.read_csv('../results/result.csv')
        print(f"Đã đọc được {len(df)} dòng dữ liệu")
        return df
    except Exception as e:
        print(f"Lỗi khi đọc file CSV: {e}")
        return None

def find_top_and_bottom_players(df):
    if 'name' in df.columns and 'Player' not in df.columns:
        df['Player'] = df['name']
    if 'team' in df.columns and 'Team' not in df.columns:
        df['Team'] = df['team']
    
    # Danh sách các chỉ số cần phân tích
    stats_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    results = []
    
    for col in stats_columns:
        valid_data = df[~df[col].isna()]
        
        if len(valid_data) == 0:
            continue
        
        top_3 = valid_data.nlargest(3, col)[['Player', 'Team', col]]
        
        bottom_3 = valid_data.nsmallest(3, col)[['Player', 'Team', col]]
        
        results.append({
            'stat': col,
            'top_3': top_3,
            'bottom_3': bottom_3
        })
    
    return results

# Lưu kết quả top 3 ra file text
def save_top_players_to_txt(top_results):
    with open('../results/top_3.txt', 'w', encoding='utf-8') as f:
        for result in top_results:
            stat = result['stat']
            f.write(f"\n{'='*50}\n")
            f.write(f"Statistic: {stat}\n")
            f.write(f"{'='*50}\n\n")
            
            f.write("Top 3 Highest Players:\n")
            f.write(f"{'-'*50}\n")
            for i, (_, row) in enumerate(result['top_3'].iterrows(), 1):
                f.write(f"{i}. {row['Player']} ({row['Team']}): {row[stat]:.2f}\n")
            
            f.write(f"\nTop 3 Lowest Players:\n")
            f.write(f"{'-'*50}\n")
            for i, (_, row) in enumerate(result['bottom_3'].iterrows(), 1):
                f.write(f"{i}. {row['Player']} ({row['Team']}): {row[stat]:.2f}\n")
            
            f.write(f"\n{'='*50}\n")
    
    print(f"Đã lưu thông tin top 3 vào file ../results/top_3.txt")

def calculate_statistics(df):
    if 'team' in df.columns and 'Team' not in df.columns:
        df['Team'] = df['team']
    
    stats_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    teams = df['Team'].unique()
    result_df = pd.DataFrame(index=range(len(teams) + 1))
    
    result_df.at[0, 'Team'] = 'All'
    for i, team in enumerate(teams, 1):
        result_df.at[i, 'Team'] = team
    
    for col in stats_columns:
        valid_data = df[~df[col].isna()]
        
        if len(valid_data) == 0:
            continue
        
        median_all = valid_data[col].median()
        mean_all = valid_data[col].mean()
        std_all = valid_data[col].std()
        
        result_df.at[0, f'Median of {col}'] = median_all
        result_df.at[0, f'Mean of {col}'] = mean_all
        result_df.at[0, f'Std of {col}'] = std_all
        
        for i, team in enumerate(teams, 1):
            team_data = valid_data[valid_data['Team'] == team]
            
            if len(team_data) > 0:
                median_team = team_data[col].median()
                mean_team = team_data[col].mean()
                std_team = team_data[col].std()
                
                result_df.at[i, f'Median of {col}'] = median_team
                result_df.at[i, f'Mean of {col}'] = mean_team
                result_df.at[i, f'Std of {col}'] = std_team
            else:
                result_df.at[i, f'Median of {col}'] = np.nan
                result_df.at[i, f'Mean of {col}'] = np.nan
                result_df.at[i, f'Std of {col}'] = np.nan
    
    return result_df

# Vẽ histogram cho phân phối các chỉ số
def plot_histograms(df):
    if 'team' in df.columns and 'Team' not in df.columns:
        df['Team'] = df['team']
    
    if not os.path.exists('../results/histograms'):
        os.makedirs('../results/histograms')
    
    stats_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    teams = df['Team'].unique()
    
    for col in stats_columns:
        plt.figure(figsize=(12, 6))
        
        valid_data = df[~df[col].isna()]
        
        if len(valid_data) < 5:  # Không đủ dữ liệu để vẽ histogram có ý nghĩa
            continue
        
        plt.hist(valid_data[col], bins=20, color='skyblue', edgecolor='black')
        plt.title(f'Distribution of {col} - All Players')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        
        safe_col_name = col.replace('/', '_per_').replace('\\', '_').replace(':', '_').replace('?', '_').replace('*', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
        plt.savefig(f'../results/histograms/{safe_col_name}_all_players.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    for col in stats_columns:
        n_teams = len(teams)
        n_cols = 5
        n_rows = (n_teams + n_cols - 1) // n_cols
        
        plt.figure(figsize=(20, 4*n_rows))
        
        for idx, team in enumerate(teams, 1):
            plt.subplot(n_rows, n_cols, idx)
            
            team_data = df[df['Team'] == team]
            valid_team_data = team_data[~team_data[col].isna()]
            
            if len(valid_team_data) < 5:
                continue
            
            plt.hist(valid_team_data[col], bins=10, color='skyblue', edgecolor='black')
            plt.title(f'{team}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
        
        plt.suptitle(f'Distribution of {col} across all teams', y=1.02, fontsize=16)
        plt.tight_layout()
        
        safe_col_name = col.replace('/', '_per_').replace('\\', '_').replace(':', '_').replace('?', '_').replace('*', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
        plt.savefig(f'../results/histograms/{safe_col_name}_all_teams.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    print(f"Đã lưu các biểu đồ histogram vào thư mục ../results/histograms")

# Xác định đội có điểm cao nhất cho mỗi chỉ số
def identify_best_teams(stats_df):
    """Xác định đội có điểm tốt nhất cho mỗi chỉ số và đánh giá đội tốt nhất.
    Lưu ý: Với một số chỉ số như thẻ vàng, thẻ đỏ, phạm lỗi, v.v., giá trị thấp hơn là tốt hơn."""
    team_stats = stats_df[stats_df['Team'] != 'All'].copy()
    
    best_teams = defaultdict(int)
    best_stats = {}
    
    mean_columns = [col for col in team_stats.columns if col.startswith('Mean of')]
    
    for col in mean_columns:
        stat_name = col.replace('Mean of ', '')
        lower_is_better = any(keyword in col.lower() for keyword in [
            'fls', 'off', 'lost', 'mis', 'dis', 
            'yellow_cards', 'red_cards', 'card', 
            'foul', 'challenge', 'aerial_lost', 'og',
            'tkld', 'failed', 'unsuccessful', 'carries_mis', 'carries_dis'
        ])
        
        if not lower_is_better:
            best_team = team_stats.loc[team_stats[col].idxmax()]
        else:
            best_team = team_stats.loc[team_stats[col].idxmin()]
        
        best_teams[best_team['Team']] += 1
        best_stats[stat_name] = best_team['Team']
    
    sorted_teams = sorted(best_teams.items(), key=lambda x: x[1], reverse=True)
    
    with open('../results/best_teams.txt', 'w', encoding='utf-8') as f:
        f.write("Đội có chỉ số tốt nhất cho mỗi thống kê:\n")
        f.write(f"{'='*50}\n")
        f.write("(Lưu ý: Với các chỉ số như thẻ vàng, thẻ đỏ, phạm lỗi, mất bóng,... thì giá trị thấp nhất là tốt nhất)\n\n")
        
        for stat, team in best_stats.items():
            is_negative_stat = any(keyword in stat.lower() for keyword in [
                'fls', 'off', 'lost', 'mis', 'dis', 
                'yellow_cards', 'red_cards', 'card', 
                'foul', 'challenge', 'aerial_lost', 'og',
                'tkld', 'failed', 'unsuccessful', 'carries_mis', 'carries_dis'
            ])
            
            if is_negative_stat:
                f.write(f"{stat}: {team} (thấp nhất)\n")
            else:
                f.write(f"{stat}: {team} (cao nhất)\n")
        
        f.write(f"\n{'='*50}\n")
        f.write("Xếp hạng đội theo số chỉ số tốt nhất:\n")
        f.write(f"{'='*50}\n")
        
        for i, (team, count) in enumerate(sorted_teams, 1):
            f.write(f"{i}. {team}: {count} chỉ số\n")
        
        f.write(f"\n{'='*50}\n")
        f.write(f"Theo phân tích, đội {sorted_teams[0][0]} đang có phong độ tốt nhất trong mùa giải Premier League 2024-2025,")
        f.write(f" dẫn đầu với {sorted_teams[0][1]} chỉ số tốt nhất.\n")
    
    print(f"Đã lưu thông tin đội tốt nhất vào file ../results/best_teams.txt")
    
    return sorted_teams[0][0]  # Trả về tên đội tốt nhất

def main():
    # Đọc dữ liệu
    df = load_data()
    if df is None:
        print("Không thể đọc dữ liệu, hãy kiểm tra lại file CSV")
        return
    
    # Hiển thị một số cột đầu tiên để kiểm tra
    print("\nCác cột trong dữ liệu:")
    print(df.columns.tolist())
    
    # Chuyển đổi các cột dữ liệu sang số (nếu có thể)
    for col in df.columns:
        if col not in ['name', 'nation', 'team', 'position', 'Player', 'Team']:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                pass
    
    # 1. Tìm top và bottom 3 cầu thủ cho mỗi chỉ số
    print("Đang tìm top 3 cầu thủ cao nhất và thấp nhất cho mỗi chỉ số...")
    top_results = find_top_and_bottom_players(df)
    save_top_players_to_txt(top_results)
    
    # 2. Tính trung vị, trung bình và độ lệch chuẩn
    print("Đang tính toán các chỉ số thống kê...")
    stats_df = calculate_statistics(df)
    stats_df.to_csv('../results/results2.csv', index=False)
    print("Đã lưu kết quả thống kê vào file ../results/results2.csv")
    
    # 3. Vẽ histogram
    print("Đang vẽ biểu đồ histogram...")
    plot_histograms(df)
    
    # 4. Xác định đội có phong độ tốt nhất
    print("Đang xác định đội có phong độ tốt nhất...")
    best_team = identify_best_teams(stats_df)
    print(f"Đội có phong độ tốt nhất trong mùa giải Premier League 2024-2025: {best_team}")
    
    print("Đã hoàn thành tất cả các phân tích!")

if __name__ == "__main__":
    main()