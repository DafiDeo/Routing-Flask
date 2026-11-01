# Tugas Individu 5 (Bagian 1) — Routing di Flask

Aplikasi Flask sederhana **Toko Kampus** untuk pengecekan username
pelanggan / member / admin toko. Dibuat sesuai materi **Pertemuan 9 —
Routing di Flask**.

## Deskripsi
Ini hanya cobaan aja

## Konsep yang Digunakan (Materi Pertemuan 9)

- **Routing** — memetakan URL yang diminta pengguna ke *view function*;
  nama fungsi menjadi *endpoint* (mis. `beranda()` menangani `/beranda`).
- **Banyak route, satu fungsi** — `/` dan `/beranda` ditangani fungsi yang
  sama dengan menumpuk decorator `@app.route`.
- **Dynamic routing** — bagian URL dijadikan variabel dengan
  `<nama_variabel>` lalu diterima sebagai parameter fungsi
  (mis. `/cek/<username>`).
- **Converter tipe** — `<int:id>` memastikan variabel URL bertipe `int`;
  jika tidak sesuai, Flask otomatis mengembalikan 404
  (coba `/produk/abc`).
- **`abort(404)`** — menghentikan request dan memicu halaman 404 saat
  data tidak ditemukan di dictionary (`PRODUK.get(id)`).
- **`url_for()`** — membangun URL dari nama endpoint, bukan menulis
  alamat manual; parameter tambahan otomatis menjadi query string
  (`url_for("cek_query", u="budi")` → `/cek?u=budi`).
- **`redirect()`** — mengalihkan browser ke URL lain (302 Found),
  dikombinasikan dengan `url_for()`.
- **Query string** — `request.args.get("u")` membaca data setelah tanda
  `?` pada URL (`/cek?u=andi`).
- **Error handler** — `@app.errorhandler(404)` untuk custom halaman
  error 404.

## Struktur Project

```
tugas-individu-5/
├── app.py            # seluruh route aplikasi
├── requirements.txt  # dependensi
├── .gitignore
└── README.md
```

## Cara Menjalankan

```bash
python -m pip install flask
python -m flask --version
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install flask
python app.py
```
## Di kali Linux
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
# Periksa versi Python
python3 --version
pip3 --version
git clone https://github.com/DafiDeo/Routing-Flask.git
cd Routing Flask
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Buka browser ke `http://127.0.0.1:5000`

## Peta URL

| URL | Endpoint (fungsi) | Keterangan |
|-----|-------------------|------------|
| `/` dan `/beranda` | `beranda()` | Route statis — halaman utama toko |
| `/tentang` | `tentang()` | Route statis — tentang toko |
| `/produk` | `produk()` | Route statis — daftar produk |
| `/kontak` | `kontak()` | Route statis — kontak toko |
| `/cek/<username>` | `cek_username()` | Dynamic route — cek username (validasi min. 4 karakter → status 400) |
| `/cek?u=<username>` | `cek_query()` | Versi query string → redirect ke `/cek/<username>` |
| `/user/<username>` | `profil()` | Dynamic route — profil user terdaftar (404 jika tidak ada) |
| `/produk/<int:id>` | `detail_produk()` | Converter `int` + `abort(404)` jika produk tidak ada |
| `/home` | `home_lama()` | `redirect(url_for("beranda"))` — 302 |
| URL lain | `tidak_ditemukan()` | Custom halaman error 404 |

## Checklist Requirement Tugas

1. **Minimal 4 route statis** → `/beranda`, `/tentang`, `/produk`, `/kontak`
2. **Dynamic route dengan validasi** → `/cek/<username>` dan `/user/<username>`
   (username minimal 4 karakter, jika kurang dikembalikan status **400**)
3. **Converter int + abort(404)** → `/produk/<int:id>`, coba `/produk/1` (ada)
   dan `/produk/99` (tidak ada → 404)
4. **url_for dan redirect** → semua link dibangun dengan `url_for()`;
   `/home` dialihkan ke beranda dengan `redirect()`; `/cek?u=...` juga
   memakai `redirect(url_for(...))`
5. **Custom halaman error 404** → `@app.errorhandler(404)` dengan link
   kembali ke beranda

## Contoh Pengujian di Browser

| URL | Hasil |
|-----|-------|
| `http://127.0.0.1:5000/` | Beranda Toko Kampus (200) |
| `http://127.0.0.1:5000/cek/andi` | Username andi **sudah dipakai** (200) |
| `http://127.0.0.1:5000/cek/zaki` | Username zaki **tersedia** (200) |
| `http://127.0.0.1:5000/cek/ab` | Error: username minimal 4 karakter (**400**) |
| `http://127.0.0.1:5000/cek?u=budi` | Redirect ke `/cek/budi` |
| `http://127.0.0.1:5000/user/admin` | Profil Admin Toko (200) |
| `http://127.0.0.1:5000/user/tidakada` | Custom 404 |
| `http://127.0.0.1:5000/produk/1` | Detail Kopi Susu Rp18,000 (200) |
| `http://127.0.0.1:5000/produk/abc` | 404 (converter int gagal) |
| `http://127.0.0.1:5000/home` | 302 → beranda |

## Melihat Daftar Route

```bash
flask --app app routes
```

Hasil:

```
Endpoint       Methods  Rule                   
-------------  -------  -----------------------
beranda        GET      /beranda               
beranda        GET      /                      
cek_query      GET      /cek                   
cek_username   GET      /cek/<username>        
detail_produk  GET      /produk/<int:id>       
home_lama      GET      /home                  
kontak         GET      /kontak                
produk         GET      /produk                
profil         GET      /user/<username>       
static         GET      /static/<path:filename>
tentang        GET      /tentang               
```

## Push ke GitHub

```bash
git init
git add .
git commit -m "Tugas Individu 5 - Routing di Flask"
git branch -M main
git remote add origin https://github.com/<username-anda>/tugas-individu-5.git
git push -u origin main
git status
```
