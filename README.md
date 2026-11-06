# Tugas Individu 5 — Final & Demo (Routing & Template di Flask)

Aplikasi Flask sederhana **Toko Kampus** untuk pengecekan username
pelanggan / member / admin toko. Dibuat sesuai materi **Pertemuan 9 —
Routing di Flask** dan dilengkapi **Pertemuan 10 — Template di Flask
(Jinja2)** dengan template inheritance.

## Deskripsi
Ini hanya cobaan aja

## Konsep yang Digunakan (Materi Pertemuan 9 — Routing)

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

## Konsep Template yang Digunakan (Materi Pertemuan 10 — Jinja2)

- **`render_template()`** — Flask mencari file HTML di folder
  `templates/`; logika Python fokus data, tampilan fokus HTML.
- **Template inheritance** — `base.html` (template induk) berisi
  navbar, footer, dan `{% block title %}` / `{% block content %}`.
  Semua halaman anak memakai `{% extends "base.html" %}` — mengubah
  navbar cukup di satu file (prinsip DRY).
- **`super()`** — di `produk.html`, block title memanggil
  `{{ super() }}` agar isi block induk tetap tampil.
- **`{% if %}` 3 kondisi** — halaman `cek.html` menampilkan alert
  berbeda: tidak valid (warning) / tersedia (success) / sudah dipakai
  (danger).
- **`{% for %}` + variabel loop** — `produk.html` menampilkan tabel
  produk dengan `loop.index`; `{% else %}` tampil jika list kosong;
  `profil.html` menampilkan member lain dengan `loop.last`.
- **Filter Jinja2** — `{{ produk | length }}` (jumlah item),
  `{{ p.nama | title }}` (kapitalisasi), `{{ role | upper }}` (huruf
  besar), ditulis setelah tanda `|`.
- **Komentar Jinja2** — `{# ... #}` untuk catatan di template.
- **`url_for` di template** — semua link antarhalaman, link dengan
  variabel (`url_for('detail_produk', id=p.id)`,
  `url_for('profil', username=u)`) dibangun dengan `url_for()`,
  tanpa alamat manual.
- **Auto-escape** — variabel otomatis di-escape oleh Jinja2 sehingga
  aman dari XSS.

## Struktur Project

```
tugas-individu-5/
├── app.py                     # route + logika (render_template)
├── templates/                 # WAJIB bernama "templates" (dikenali Flask otomatis)
│   ├── base.html              # template INDUK: navbar + footer + block
│   ├── beranda.html           # extends base
│   ├── tentang.html           # extends base
│   ├── produk.html            # extends base — {% for %} + filter
│   ├── detail_produk.html     # extends base
│   ├── kontak.html            # extends base
│   ├── cek.html               # extends base — {% if %} 3 kondisi
│   ├── profil.html            # extends base — {% for %} member lain
│   ├── error.html             # extends base — pesan error 400
│   └── 404.html               # extends base — halaman 404 custom
├── requirements.txt           # dependensi
├── .gitignore
└── README.md
```

## Cara Menjalankan (Windows / PowerShell)

```bash
python -m pip install flask
python -m flask --version
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install flask
python app.py
```

## Cara Menjalankan di Linux

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
# Periksa versi Python
python3 --version
pip3 --version
git clone https://github.com/DafiDeo/Routing-Flask.git
cd Routing-Flask
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

Semua halaman dirender lewat template Jinja2 yang extends
`base.html`, sehingga navbar dan footer selalu sama.

## Checklist Requirement Tugas

### Bagian 1 — Routing (Pertemuan 9)

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

### Bagian 2 — Template Jinja2 (Pertemuan 10) — FINAL

1. **`base.html` sebagai template induk** → berisi navbar dan footer;
   **semua** halaman (10 template) memakai `{% extends "base.html" %}`
2. **Halaman cek username dengan `{% if %}` minimal 3 kondisi** →
   `cek.html`: tidak valid (alert warning) / tersedia (alert success) /
   sudah dipakai (alert danger)
3. **Halaman list data dengan `{% for %}` + filter Jinja2** →
   `produk.html` (tabel produk, filter `length` & `title`, `loop.index`),
   `profil.html` (daftar member, filter `length` & `title`, `loop.last`)
4. **Semua link menggunakan `url_for`** → navbar, footer, tombol, dan
   link dinamis (`url_for('detail_produk', id=p.id)`,
   `url_for('profil', username=u)`)

## Contoh Pengujian di Browser

| URL | Hasil |
|-----|-------|
| `http://127.0.0.1:5000/` | Beranda Toko Kampus (200) |
| `http://127.0.0.1:5000/cek/andi` | Username andi **sudah dipakai** — alert danger (200) |
| `http://127.0.0.1:5000/cek/zaki` | Username zaki **tersedia** — alert success (200) |
| `http://127.0.0.1:5000/cek/ab` | Error: username minimal 4 karakter — alert warning (**400**) |
| `http://127.0.0.1:5000/cek?u=budi` | Redirect ke `/cek/budi` |
| `http://127.0.0.1:5000/user/admin` | Profil Admin Toko (200) |
| `http://127.0.0.1:5000/user/ab` | Error 400 — template `error.html` |
| `http://127.0.0.1:5000/user/tidakada` | Custom 404 |
| `http://127.0.0.1:5000/produk/1` | Detail Kopi Susu Rp18,000 (200) |
| `http://127.0.0.1:5000/produk/99` | 404 (abort — data tidak ada) |
| `http://127.0.0.1:5000/produk/abc` | 404 (converter int gagal) |
| `http://127.0.0.1:5000/home` | 302 → beranda |
| `http://127.0.0.1:5000/halaman-ngawur` | Custom 404 |

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

Repo: `https://github.com/DafiDeo/Routing-Flask`

### Update setelah menambah template (Bagian 2 / Final)

```bash
git add .
git commit -m "Tugas Individu 5 - Final: template Jinja2 (Bagian 2)"
git push
git status
```

### Jika push pertama kali

```bash
git init
git add .
git commit -m "Tugas Individu 5 - Routing & Template di Flask"
git branch -M main
git remote add origin https://github.com/DafiDeo/Routing-Flask.git
git push -u origin main
```

Setelah push, kumpulkan link repo di **LMS Elitag**.
