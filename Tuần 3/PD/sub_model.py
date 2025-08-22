import pandas as pd

# Đọc dataset mới
df = pd.read_csv(r'D:\Submodel\covereal.csv')

# In danh sách tên cột để kiểm tra chính tả
print(df.columns.tolist())

# Hoặc in chi tiết (có độ dài và ký tự đặc biệt)
for col in df.columns:
    print(f"'{col}' (độ dài={len(col)})")

# Nếu cần, bạn có thể đổi tên cột ngay:
df.rename(columns={
    'Calories ':'Calories', 
    'calories':'Calories',
    # … thêm nếu cần chỉnh sửa
}, inplace=True)

# 1) Thông tin chung: số dòng, cột, kiểu dữ liệu, có missing không
df.info()

# 2) Thống kê mô tả cho các cột số
df.describe()

def is_weight_loss(row) -> int:
    """
    Trả về 1 nếu row thỏa mãn tiêu chí Weight Loss, ngược lại 0.
    """
    try:
        return int(
            (row['Calories'] <= 600) and      # Nới lỏng giới hạn calories lên 500
            (row['Fat'] <= 12) and             # Nới lỏng giới hạn chất béo lên 10g
            (row['Fibre'] >= 1) and            # Hạ mức chất xơ xuống 2g
            (row['Protein'] >= 3)              # Hạ mức protein xuống 5g
        )
    except KeyError as e:
        print(f"[Warning] Thiếu cột cho Weight Loss: {e}")
        return 0


def is_bodybuilder(row) -> int:
    """
    Trả về 1 nếu row thỏa mãn tiêu chí Bodybuilder, ngược lại 0.
    """
    try:
        return int(
            (row['Protein'] >= 15) and         # Giữ nguyên mức protein (15g)
            (row['Carbs'] >= 30) and (row['Carbs'] <= 70) and  # Giữ nguyên giới hạn carbs (30-70g)
            (row['Fat'] >= 8) and (row['Fat'] <= 25)            # Giữ nguyên giới hạn chất béo (8-25g)
        )
    except KeyError as e:
        print(f"[Warning] Thiếu cột cho Bodybuilder: {e}")
        return 0

# 1) Tạo lại cột Weight_Loss (0/1) với điều kiện mới
df['Weight_Loss'] = df.apply(is_weight_loss, axis=1)

# 2) Tạo lại cột Bodybuilder (0/1) với điều kiện cũ
df['Bodybuilder'] = df.apply(is_bodybuilder, axis=1)

# Kiểm tra lại 5 dòng đầu
print("5 dòng đầu tiên trong dữ liệu sau khi phân loại:")
print(df.head(5))

# Nếu muốn đánh số từ 1 đến N
df['k'] = range(1, len(df) + 1)

# Kiểm tra lại vài dòng đầu
print("5 dòng đầu tiên với số thứ tự:")
print(df.head(5))

# 1) Xác định danh sách cột muốn giữ
cols_to_keep = ['Dish Name', 'Weight_Loss', 'Bodybuilder']

# 2) Tạo DataFrame con
df_out = df[cols_to_keep].copy()

# 3) Hiển thị vài dòng đầu để kiểm tra thứ tự & nội dung
print("5 dòng đầu tiên trong DataFrame con:")
print(df_out.head(5))

# Lưu df_out thành CSV, không lưu chỉ số index của pandas
df_out.to_csv('classified_dishes_simple_new.csv', index=False)

print("✅ Đã lưu file 'classified_dishes_simple_new.csv' thành công.")

# Hiện số lượng món ăn cho từng loại Weight_Loss và Bodybuilder
print("Số lượng món ăn theo loại Weight Loss:")
print(df['Weight_Loss'].value_counts())

print("Số lượng món ăn theo loại Bodybuilder:")
print(df['Bodybuilder'].value_counts())
