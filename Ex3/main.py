import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.impute import KNNImputer

warnings.filterwarnings('ignore')

# Đọc dữ liệu
df = pd.read_csv(r'../results/result.csv', header=0)

# Kiểm tra giá trị thiếu
print("Tỷ lệ giá trị thiếu (%):")
print(df.isna().sum() / len(df) * 100)

# Lựa chọn đặc trưng
selected_features = [
    'goals', 'xG', 'assists', 'SCA', 'Att_Pen', 'SoT%', 
    'Pass_Cmp%', 'PrgP', 'KP', 'Recov', 'Take_Succ%', 'Mid_3rd', 
    'Tkl', 'Blocks', 'Blocks_Int', 'Challenges_Att', 'Def_3rd', 
    'GA90', 'Save%', 'CS%', 'PK_Save%', 'Def_Pen' 
]

# Kiểm tra cột tồn tại
missing_features = [feat for feat in selected_features if feat not in df.columns]
if missing_features:
    print(f"Các đặc trưng không có trong dữ liệu: {missing_features}")
    selected_features = [feat for feat in selected_features if feat in df.columns]

numerical_data = df[selected_features].copy()

# In dữ liệu ban đầu để kiểm tra
print("\nDữ liệu ban đầu (5 hàng đầu):")
print(numerical_data.head())

# Chuyển giá trị 'N/a' thành NaN và ép kiểu dữ liệu thành số
for col in numerical_data.columns:
    # Đảm bảo mọi giá trị 'N/a' đều được chuyển thành NaN
    numerical_data[col] = numerical_data[col].astype(str).replace('N/a', np.nan)
    numerical_data[col] = pd.to_numeric(numerical_data[col], errors='coerce')

# Kiểm tra lại tỷ lệ giá trị thiếu sau khi thay thế 'N/a'
print("\nTỷ lệ giá trị thiếu sau khi thay thế 'N/a' (%):")
print(numerical_data.isna().sum() / len(numerical_data) * 100)

# Xử lý giá trị thiếu bằng KNNImputer
imputer = KNNImputer(n_neighbors=5)
numerical_data_imputed = imputer.fit_transform(numerical_data)
numerical_data = pd.DataFrame(numerical_data_imputed, columns=selected_features)

# Kiểm tra kiểu dữ liệu sau khi impute
print("\nKiểu dữ liệu sau khi impute:")
print(numerical_data.dtypes)

# Kiểm tra xem còn giá trị không phải số không
for col in numerical_data.columns:
    if pd.to_numeric(numerical_data[col], errors='coerce').isna().any():
        print(f"Cột {col} vẫn còn giá trị không phải số")
        # In các giá trị không hợp lệ để kiểm tra
        invalid_values = numerical_data.loc[pd.to_numeric(numerical_data[col], errors='coerce').isna(), col]
        print(f"Các giá trị không hợp lệ: {invalid_values.unique()}")
        # Xử lý các giá trị không hợp lệ bằng cách thay thế bằng giá trị trung bình
        mean_val = pd.to_numeric(numerical_data[col], errors='coerce').mean()
        numerical_data[col] = pd.to_numeric(numerical_data[col], errors='coerce').fillna(mean_val)

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X = scaler.fit_transform(numerical_data)

# Giảm chiều bằng PCA trước khi phân cụm
pca = PCA(n_components=0.9)  # Giữ 90% phương sai
X_reduced = pca.fit_transform(X)
print(f'Explained variance ratio (PCA trước khi phân cụm): {pca.explained_variance_ratio_.sum():.3f}')

# Tìm số lượng cụm tối ưu (trực quan hóa)
sse = []
silhouette_scores = []
for k in range(2, 10):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_reduced)
    sse.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_reduced, kmeans.labels_))

# Vẽ đồ thị Elbow và Silhouette Score
plt.figure(figsize=(15, 5))

# Phương pháp Elbow
plt.subplot(1, 2, 1)
plt.plot(range(2, 10), sse, marker='o')
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
plt.title("Elbow Method")

# Đánh giá Silhouette Score
plt.subplot(1, 2, 2)
plt.plot(range(2, 10), silhouette_scores, marker='o')
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Score")
plt.title("Silhouette Score")
plt.savefig('../results/cluster_analysis.png')
plt.close()

# Phân cụm với K-means (4 cụm tối ưu)
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
cluster_labels = kmeans.fit_predict(X_reduced)
df['Cluster'] = cluster_labels

# Đánh giá Silhouette Score
silhouette_avg = silhouette_score(X_reduced, df['Cluster'])
print(f"Silhouette Score với k={optimal_k}: {silhouette_avg:.3f}")

# Trực quan hóa bằng PCA
pca_2d = PCA(n_components=2)
X_pca = pca_2d.fit_transform(X_reduced)
print(f'Explained variance ratio (PCA 2D): {pca_2d.explained_variance_ratio_.sum():.3f}')
plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['Cluster'], cmap='viridis', s=100, alpha=0.7)
plt.title('Phân cụm cầu thủ thành 4 nhóm sử dụng PCA và K-means')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(scatter, label='Cluster')
plt.savefig('../results/cluster_visualization_4_groups.png')
plt.close()

# Phân tích kết quả phân cụm
print("\nKết quả phân cụm:")
print("1. Số lượng cầu thủ trong mỗi cụm:")
print(df['Cluster'].value_counts())

print("\n2. Đặc điểm của từng cụm:")
for cluster in range(optimal_k):
    # Lấy chỉ số của các dòng thuộc cụm hiện tại
    cluster_indices = df[df['Cluster'] == cluster].index
    
    # Lấy dữ liệu của cụm từ bảng numerical_data (đã được làm sạch)
    cluster_data = numerical_data.loc[cluster_indices]
    
    print(f"\nCụm {cluster} (Số lượng: {len(cluster_data)}):")
    for stat in selected_features:
        # Đảm bảo dữ liệu được chuyển đổi thành số trước khi tính trung bình
        mean_value = cluster_data[stat].astype(float).mean()
        print(f"- {stat}: {mean_value:.2f}")

print("\n3. Nhận xét về phân cụm:")
print("- Cụm 0: Nhiều khả năng là tiền đạo — nổi bật ở các chỉ số tấn công như goals, xG, assists, SCA, SoT%")
print("- Cụm 1: Có thể là tiền vệ — mạnh ở chuyền bóng và kiểm soát: Pass_Cmp%, PrgP, KP, Recov, Mid_3rd")
print("- Cụm 2: Có thể là hậu vệ — nổi bật ở phòng ngự như Tkl, Blocks, Blocks_Int, Challenges_Att, Def_3rd")
print("- Cụm 3: Nhiều khả năng là thủ môn — đặc trưng bởi GA90, Save%, CS%, PK_Save%, Def_Pen")
print("- Nếu các cụm không rõ ràng trên biểu đồ PCA, có thể thử thuật toán khác như DBSCAN hoặc GMM để cải thiện phân tách.")

# Lưu kết quả
df[['name', 'nation', 'team', 'position', 'Cluster']].to_csv('../results/cluster_results_4_groups.csv', index=False)
print("\nĐã lưu kết quả vào cluster_results_4_groups.csv")