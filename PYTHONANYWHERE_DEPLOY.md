# 🚀 Deploy Flask App ke PythonAnywhere

## Langkah 1: Upload File ke PythonAnywhere

### Via Web Interface (Paling Mudah):

1. **Buka tab "Files"** di dashboard PythonAnywhere
2. **Klik "Upload a file"**
3. **Upload file-file ini satu per satu:**
   - `app.py`
   - `generator.py`
   - `requirements.txt`
   - `.env.example`
   
4. **Buat folder `templates`:**
   - Klik "New directory" → ketik `templates`
   - Masuk ke folder `templates`
   - Upload file `index.html`

5. **Buat folder `static`:**
   - Kembali ke home directory
   - Klik "New directory" → ketik `static`
   - Masuk ke folder `static`
   - Upload `style.css` dan `script.js`

### Via Git (Alternatif):

```bash
# Di PythonAnywhere Bash Console
git clone https://github.com/username/your-repo.git
cd your-repo
```

## Langkah 2: Install Dependencies

1. **Buka "Consoles"** → Klik **"Bash"**
2. **Jalankan:**
   ```bash
   pip3 install --user -r requirements.txt
   ```

## Langkah 3: Setup Web App

1. **Buka tab "Web"**
2. **Klik "Add a new web app"**
3. **Pilih "Manual configuration"**
4. **Pilih Python version:** Python 3.10 (atau yang tersedia)
5. **Klik "Next"**

## Langkah 4: Konfigurasi WSGI

1. **Di halaman Web, scroll ke "Code" section**
2. **Klik link WSGI configuration file** (contoh: `/var/www/username_pythonanywhere_com_wsgi.py`)
3. **Hapus semua isi file, ganti dengan:**

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/username/theme-lp-editor'  # Ganti 'username' dengan username Anda
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable (optional)
os.environ['GEMINI_API_KEY'] = 'AIzaSy...'  # Opsional: masukkan API key

# Import flask app
from app import app as application
```

4. **Klik "Save"**

## Langkah 5: Set Working Directory

1. **Kembali ke tab "Web"**
2. **Di section "Code":**
   - **Source code:** `/home/username/theme-lp-editor`
   - **Working directory:** `/home/username/theme-lp-editor`

## Langkah 6: Reload & Test

1. **Scroll ke atas**
2. **Klik tombol hijau "Reload username.pythonanywhere.com"**
3. **Klik link** `http://username.pythonanywhere.com`

## ✅ Selesai!

Aplikasi Anda sekarang live di: `http://username.pythonanywhere.com`

## 🔧 Troubleshooting

### Error 500?
- Cek **Error log** di tab Web
- Pastikan semua file sudah ter-upload
- Pastikan path di WSGI file benar

### Module not found?
```bash
# Di Bash console
pip3 install --user nama-module
```
Lalu reload web app.

### Update Code?
1. Upload file baru via Files tab
2. Klik "Reload" di tab Web

## 📝 Catatan Penting

- **Free tier**: 1 web app, always-on
- **Custom domain**: Perlu upgrade (tapi subdomain gratis)
- **Reload manual**: Setiap update code, harus klik "Reload"
- **API Key**: Bisa set di WSGI file atau user input di app
