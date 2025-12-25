# Hướng dẫn triển khai

## 1. Chuẩn bị cấu hình
1. Cài đặt Python 3.10 hoặc Docker.
2. Sao chép file `.env.example` thành `.env` rồi chỉnh các biến bắt buộc (`SECRET_KEY`, `MODEL_PATH`, `DATABASE_PATH`, ...).
3. Đảm bảo `model/my_model.h5` có trong dự án và đường dẫn trùng khớp với biến môi trường `MODEL_PATH`.
4. Nếu cần lưu trữ ảnh/audio lâu dài, chuẩn bị storage bền vững (S3, Azure Blob, mount volume, ...).

## 2. Chạy bằng Docker (khuyến nghị)
```bash
# Build image
docker build -t ocular-disease-app .

# Chạy container với file env và volume cho uploads/audio
docker run -d \
  --name ocular-disease \
  --env-file .env \
  -p 5000:5000 \
  -v $(pwd)/uploads-data:/app/static/uploads \
  -v $(pwd)/audio-data:/app/static/audio \
  ocular-disease-app
```
- `uploads-data` và `audio-data` là thư mục host để giữ file sau khi container restart.
- Có thể chỉnh số worker Gunicorn bằng biến `WEB_CONCURRENCY` riêng (ví dụ thêm `--env WEB_CONCURRENCY=4`).

## 3. Render (free tier)
1. Push repo lên GitHub, đảm bảo đã có [Dockerfile](Dockerfile), [requirements.txt](requirements.txt) và [render.yaml](render.yaml).
2. Cài `render` CLI (`npm i -g render-cli`) rồi đăng nhập `render login`.
3. Triển khai bằng blueprint: `render blueprint deploy render.yaml` (Render sẽ tạo dịch vụ web, ánh xạ đĩa và biến môi trường đúng như file cấu hình).
4. Nếu làm thủ công trên dashboard: tạo Web Service → chọn Docker → connect repo → nhập Start Command `gunicorn wsgi:app --workers 2 --bind 0.0.0.0:$PORT --timeout 120`.
5. Vào tab Environment, nhập các biến theo `.env.example`, đặc biệt `SECRET_KEY`, `DATABASE_PATH`, `UPLOAD_FOLDER`, `AUDIO_FOLDER`.
6. Ở tab Disks, tạo disk miễn phí 1GB, mount tại `/data` (hoặc vị trí bạn ghi trong `render.yaml`).

**Gợi ý biến môi trường cho Render (đồng bộ với disk `/data`):**
- `DATABASE_PATH=/data/database.db`
- `UPLOAD_FOLDER=/data/uploads`
- `AUDIO_FOLDER=/data/audio`
- `INIT_DB_ON_STARTUP=true`

Sau khi Render build xong, truy cập URL miễn phí để kiểm thử. Nếu cần scale worker, chỉnh `gunicorn` args trong Render dashboard hoặc cập nhật `render.yaml` rồi `render blueprint deploy` lại.

## 4. Azure App Service (Linux)
1. Cài Azure CLI, đăng nhập `az login`.
2. Tạo App Service Plan và Web App:
```bash
az webapp up --resource-group <rg-name> --sku B1 --location southeastasia --name <app-name> --runtime "PYTHON:3.10" --src-path .
```
3. Vào portal, thêm App Settings tương ứng `.env`.
4. Thiết lập `Startup Command`: `gunicorn wsgi:app --workers 2 --bind=0.0.0.0:$PORT --timeout 120`.
5. Dùng Azure Storage (File Share/Blob) để lưu dữ liệu người dùng, mount vào `static/uploads` và `static/audio` hoặc chuyển hướng lên dịch vụ lưu trữ khác.

## 5. Kiểm tra sau deploy
- Chạy `curl -I https://<domain>` để chắc chắn server phản hồi 200.
- Đăng nhập, kiểm thử upload ảnh và tính năng chatbot/TTS.
- Theo dõi log (Docker: `docker logs ocular-disease`, Render/Railway: tab Logs) để kiểm tra lỗi TensorFlow hoặc gTTS.
