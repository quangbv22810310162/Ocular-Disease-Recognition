class MedicalChatbot:
    def __init__(self):
        self.disease_info = {
            'Normal': {
                'description': 'Mắt của bạn hoàn toàn khỏe mạnh và không có dấu hiệu bệnh lý.',
                'symptoms': 'Không có triệu chứng bất thường.',
                'advice': '''
                    Tiếp tục duy trì thói quen bảo vệ mắt tốt
                    Khám mắt định kỳ 6 tháng/lần
                    Hạn chế sử dụng thiết bị điện tử quá lâu''',
                'prevention': '''
                    1. Nghỉ ngơi mắt mỗi 20 phút nhìn màn hình
                    2. Đeo kính chống tia UV khi ra nắng
                    3. Bổ sung thực phẩm giàu vitamin A
                    4. Giữ môi trường làm việc đủ ánh sáng
                    5. Tránh dụi mắt khi bẩn'''
            },
            'Diabetes': {
                'description': '''Bệnh võng mạc đái tháo đường là biến chứng nghiêm trọng của bệnh tiểu đường.
                Gây tổn thương các mạch máu nhỏ trong võng mạc, có thể dẫn đến mù lòa.''',
                'symptoms': '''
                    Nhìn mờ hoặc thị lực thay đổi
                    Thấy đốm đen hoặc vết đen trôi nổi
                    Khó nhìn vào ban đêm
                    Màu sắc trở nên nhạt nhòa
                    Mất thị lực từng vùng''',
                'advice': '''
                    1. Cần thăm khám bác sĩ chuyên khoa gấp
                    2. Kiểm soát đường huyết chặt chẽ
                    3. Có thể cần điều trị laser
                    4. Theo dõi thị lực thường xuyên
                    5. Tái khám định kỳ đều đặn''',
                'prevention': '''
                    Kiểm soát đường huyết tốt
                    Duy trì chế độ ăn lành mạnh
                    Tập thể dục đều đặn
                    Khám mắt định kỳ
                    Không hút thuốc'''
            },
            'Glaucoma': {
                'description': '''Bệnh glaucoma (tăng nhãn áp) là tình trạng tổn thương dây thần kinh thị giác, 
                thường do áp lực trong mắt tăng cao. Đây là nguyên nhân gây mù lòa phổ biến.''',
                'symptoms': '''
                    Đau nhức mắt
                    Nhìn thấy quầng sáng
                    Thị lực giảm dần
                    Mất thị trường ngoại vi
                    Buồn nôn và nôn (cấp tính)''',
                'advice': '''
                    1. Điều trị càng sớm càng tốt
                    2. Dùng thuốc nhỏ mắt đều đặn
                    3. Theo dõi nhãn áp thường xuyên
                    4. Có thể cần phẫu thuật
                    5. Tránh hoạt động gắng sức''',
                'prevention': '''
                    Khám mắt định kỳ sau 40 tuổi
                    Tập thể dục nhẹ nhàng
                    Đeo kính bảo hộ khi cần
                    Hạn chế caffeine
                    Điều trị các bệnh nền'''
            },
            'Cataract': {
                'description': '''Đục thủy tinh thể là tình trạng thủy tinh thể của mắt bị đục, 
                làm giảm thị lực và có thể dẫn đến mù lòa nếu không điều trị.''',
                'symptoms': '''
                    Nhìn mờ, không rõ
                    Nhạy cảm với ánh sáng
                    Nhìn một thành hai
                    Khó nhìn ban đêm
                    Màu sắc nhạt nhòa''',
                'advice': '''
                    1. Thăm khám bác sĩ chuyên khoa
                    2. Cân nhắc phẫu thuật thay thủy tinh thể
                    3. Đeo kính râm khi ra ngoài
                    4. Điều chỉnh ánh sáng phù hợp
                    5. Hạn chế lái xe đêm''',
                'prevention': '''
                    Bảo vệ mắt khỏi tia UV
                    Không hút thuốc
                    Ăn nhiều rau xanh
                    Kiểm tra mắt định kỳ
                    Kiểm soát bệnh nền'''
            },
            'AMD': {
                'description': '''Thoái hóa điểm vàng liên quan đến tuổi tác (AMD) là bệnh 
                gây tổn thương vùng hoàng điểm của võng mạc, ảnh hưởng đến thị lực trung tâm.''',
                'symptoms': '''
                    Nhìn không rõ ở trung tâm thị trường
                    Nhìn thấy đường thẳng bị cong
                    Khó phân biệt màu sắc
                    Cần ánh sáng mạnh hơn để đọc
                    Khó thích nghi với bóng tối''',
                'advice': '''
                    1. Thăm khám chuyên khoa gấp
                    2. Bổ sung dinh dưỡng đặc biệt
                    3. Có thể cần điều trị bằng laser
                    4. Theo dõi thị lực thường xuyên
                    5. Sử dụng công cụ hỗ trợ thị lực''',
                'prevention': '''
                    Bỏ hút thuốc
                    Ăn nhiều rau xanh và cá
                    Đeo kính chống UV
                    Kiểm tra mắt định kỳ
                    Kiểm soát huyết áp'''
            },
            'Hypertension': {
                'description': '''Bệnh võng mạc tăng huyết áp là tổn thương ở võng mạc 
                do huyết áp cao gây ra, có thể dẫn đến mất thị lực nghiêm trọng.''',
                'symptoms': '''
                    Nhìn mờ đột ngột
                    Đau đầu dữ dội
                    Giảm thị lực
                    Buồn nôn và nôn
                    Song thị (nhìn đôi)''',
                'advice': '''
                    1. Kiểm soát huyết áp gấp
                    2. Thăm khám chuyên khoa
                    3. Uống thuốc đều đặn
                    4. Theo dõi thị lực
                    5. Thay đổi lối sống''',
                'prevention': '''
                    Kiểm soát huyết áp
                    Giảm muối trong ăn uống
                    Tập thể dục đều đặn
                    Giảm stress
                    Khám định kỳ'''
            },
            'Myopia': {
                'description': '''Cận thị bệnh lý là tình trạng cận thị nặng và tiến triển, 
                có thể gây ra các biến chứng nghiêm trọng ở võng mạc.''',
                'symptoms': '''
                    Khó nhìn xa
                    Nhìn mờ
                    Đau đầu thường xuyên
                    Mỏi mắt nhanh
                    Có thể thấy đốm đen''',
                'advice': '''
                    1. Đeo kính đúng độ
                    2. Hạn chế công việc gần
                    3. Nghỉ ngơi mắt thường xuyên
                    4. Theo dõi độ cận định kỳ
                    5. Có thể cần điều trị đặc biệt''',
                'prevention': '''
                    Hạn chế dùng thiết bị điện tử
                    Đảm bảo ánh sáng đủ
                    Giữ khoảng cách khi đọc
                    Hoạt động ngoài trời
                    Khám mắt định kỳ'''
            },
            'Others': {
                'description': '''Có thể là các bệnh về mắt khác hoặc các tình trạng bất thường cần được bác sĩ chuyên khoa thăm khám chi tiết.''',
                'symptoms': '''
                    Các triệu chứng không điển hình
                    Thay đổi thị lực bất thường
                    Các dấu hiệu khác về mắt''',
                'advice': '''
                    1. Thăm khám bác sĩ chuyên khoa
                    2. Ghi chép các triệu chứng
                    3. Theo dõi thay đổi
                    4. Không tự ý điều trị
                    5. Cần chẩn đoán chính xác''',
                'prevention': '''
                    Khám mắt định kỳ
                    Bảo vệ mắt
                    Nghỉ ngơi đầy đủ
                    Dinh dưỡng cân bằng
                    Tránh các yếu tố nguy cơ'''
            }
        }

    def get_response(self, disease, query_type='description'):
        print(f"Getting response for disease: {disease}, query_type: {query_type}")  # Debug log
        
        if disease not in self.disease_info:
            return f"Xin lỗi, tôi không có thông tin về bệnh {disease}."
        
        info = self.disease_info[disease]
        if query_type in info:
            return info[query_type]
        
        return "Không tìm thấy thông tin bạn yêu cầu."