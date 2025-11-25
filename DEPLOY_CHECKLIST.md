# ✅ Checklist Deploy PythonAnywhere

## 📤 Upload Files

Di tab **Files** PythonAnywhere:

- [ ] Upload `app.py`
- [ ] Upload `generator.py`  
- [ ] Upload `requirements.txt`
- [ ] Buat folder `templates/` → upload `index.html`
- [ ] Buat folder `static/` → upload `style.css` dan `script.js`

## 🔧 Install Dependencies

Di **Bash Console**:
```bash
pip3 install --user -r requirements.txt
```

## 🌐 Setup Web App

Di tab **Web**:

1. [ ] Klik "Add a new web app"
2. [ ] Pilih "Manual configuration"
3. [ ] Pilih Python 3.10

## ⚙️ Konfigurasi WSGI

1. [ ] Klik WSGI configuration file
2. [ ] Copy isi dari `wsgi_template.py`
3. [ ] **GANTI** `username` dengan username PythonAnywhere Anda
4. [ ] **GANTI** `theme-lp-editor` dengan nama folder Anda
5. [ ] Save

## 🚀 Launch!

1. [ ] Set **Source code** dan **Working directory** ke folder project
2. [ ] Klik **"Reload"**
3. [ ] Buka `http://username.pythonanywhere.com`

---

**Lihat `PYTHONANYWHERE_DEPLOY.md` untuk panduan lengkap!**
