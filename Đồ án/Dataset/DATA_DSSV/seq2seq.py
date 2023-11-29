import tensorflow as tf
import numpy as np

# Dữ liệu mẫu
sinhvien_1 = [
    {
        'courses': ['English', 'History', 'Biology'],
        'semesters': [4, 5, 6],
        'years': [2022, 2022, 2023],
        'avg_grades': [7.2, 8.8, 9.5],
        'course_difficulties': [2, 3, 3],
        'avg_semester_grades': [7.8, 8.5, 9.0],
        'accumulated_credits': [60, 75, 90],
        'next_semester_grades': [5.5,3.7,3.8]  
    },
    # Thêm dữ liệu của sinh viên khác nếu cần
]

# Xác định số lượng môn học duy nhất
unique_courses = set()
for data_point in data:
    unique_courses.update(data_point['courses'])
num_courses = len(unique_courses)

# Xây dựng mô hình LSTM
model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(input_dim=num_courses, output_dim=64),  # Lớp nhúng cho mã môn học
    tf.keras.layers.LSTM(units=64),
    tf.keras.layers.Dense(units=1, activation='linear')  # Dự đoán điểm của môn học
])

# Biên dịch mô hình
model.compile(optimizer='adam', loss='mean_squared_error')

# Chuẩn bị dữ liệu huấn luyện
X_train = np.array([np.array(data_point['courses']) for data_point in data])
y_train = np.array([np.array(data_point['next_semester_grades']) for data_point in data])

# Huấn luyện mô hình
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Dữ liệu mới cần dự đoán
new_data = [
    {
        'courses': ['English', 'History', 'Biology'],
        'semesters': [4, 5, 6],
        'years': [2022, 2022, 2023],
        'avg_grades': [7.2, 8.8, 9.5],
        'course_difficulties': [2, 3, 3],
        'avg_semester_grades': [7.8, 8.5, 9.0],
        'accumulated_credits': [60, 75, 90],
        'next_semester_grades': [0, 0, 0]  # Dự đoán sẽ được điền vào đây
    },
    # Thêm dữ liệu của sinh viên khác nếu cần
]

# Chuẩn bị dữ liệu dự đoán
X_predict = np.array([np.array(data_point['courses']) for data_point in new_data])

# Dự đoán điểm của môn học trong học kỳ tiếp theo
predictions = model.predict(X_predict)

# Lưu dự đoán vào dữ liệu
for i, data_point in enumerate(new_data):
    data_point['next_semester_grades'] = predictions[i]

# In kết quả
for data_point in new_data:
    print("Courses:", data_point['courses'])
    print("Predicted Next Semester Grades:", data_point['next_semester_grades'])
    print("--------------------")
