from flask import Flask, abort, redirect, url_for, request
app = Flask(__name__)

TERDAFTAR = ["Dafi", "Rehan", "Vira", "Erico", "admin", "member1"]

PRODUK = {
    1: {"nama": "Kopi Kapal Api",  "harga": 6000},
    2: {"nama": "Teh manis",  "harga": 5000},
    3: {"nama": "Indomie Goreng", "harga": 7000},
    4: {"nama": "Donat", "harga": 3000},
}

def validasi_username(username):
    """Validasi username. Mengembalikan pesan error, atau None jika valid."""
    if len(username) < 4:
        return "Username minimal 4 karakter."
    return None

# 1. ROUTE STATIS (minimal 4 halaman)
@app.route("/")
@app.route("/beranda")              
def beranda():
    link_tentang = url_for("tentang")
    link_produk  = url_for("produk")
    link_kontak  = url_for("kontak")
    link_cek     = url_for("cek_username", username="Dafi")
    link_query   = url_for("cek_query", u="Rehan")        
    return f"""
        <h1>Beranda Toko Kampus</h1>
        <p>Selamat datang! Silakan cek ketersediaan username
           pelanggan / member / admin toko.</p>
        <ul>
            <li><a href="{link_tentang}">Tentang Kami</a></li>
            <li><a href="{link_produk}">Daftar Produk</a></li>
            <li><a href="{link_kontak}">Kontak</a></li>
            <li><a href="{link_cek}">Cek username "Dafi" (dynamic route)</a></li>
            <li><a href="{link_query}">Cek username via query string</a></li>
            <li><a href="/home">URL lama /home</a> (otomatis redirect ke beranda)</li>
        </ul>
    """

@app.route("/tentang")
def tentang():
    return f"""
        <h1>Tentang Kami</h1>
        <p>Toko Kampus adalah toko milik mahasiswa yang menjual makanan
           dan minuman ringan di lingkungan kampus.</p>
        <p><a href="{url_for('beranda')}">Kembali ke beranda</a></p>
    """

@app.route("/produk")
def produk():
    # Membangun daftar link detail produk dengan url_for()
    item = "".join(
        f'<li><a href="{url_for("detail_produk", id=id)}">'
        f'{p["nama"]} — Rp{p["harga"]:,}</a></li>'
        for id, p in PRODUK.items()
    )
    return f"""
        <h1>Daftar Produk</h1>
        <ul>{item}</ul>
        <p><a href="{url_for('beranda')}">Kembali ke beranda</a></p>
    """

@app.route("/kontak")
def kontak():
    return f"""
        <h1>Kontak Kami</h1>
        <p>Email : toko@untag-sby.ac.id</p>
        <p>WA    : 0812-3456-7890</p>
        <p><a href="{url_for('beranda')}">Kembali ke beranda</a></p>
    """

# 2. DYNAMIC ROUTING + VALIDASI
# /cek/<username> — cek ketersediaan username
@app.route("/cek/<username>")
def cek_username(username):
    username = username.lower()
    error = validasi_username(username)
    if error:                                     # validasi: minimal 4 karakter
        return f"<h1>Error!</h1><p>{error}</p>", 400

    if username in TERDAFTAR:
        pesan = f"Username <b>{username}</b> <u>sudah dipakai</u>."
    else:
        pesan = f"Username <b>{username}</b> <u>tersedia</u>. Silakan daftar!"

    return f"""
        <h1>Hasil Cek Username</h1>
        <p>{pesan}</p>
        <p><a href="{url_for('beranda')}">Kembali ke beranda</a></p>
    """

@app.route("/cek")
def cek_query():
    u = request.args.get("u", "")
    if u == "":
        return f"""
            <h1>Cek Username (query string)</h1>
            <p>Contoh pemakaian: /cek?u=Dafi</p>
            <p><a href="{url_for('beranda')}">Kembali ke beranda</a></p>
        """
    # redirect + url_for: alihkan ke route /cek/<username>
    return redirect(url_for("cek_username", username=u))


# /user/<username> — profil user yang terdaftar
@app.route("/user/<username>")
def profil(username):
    username = username.lower()
    error = validasi_username(username)
    if error:
        return f"<h1>Error!</h1><p>{error}</p>", 400

    if username not in TERDAFTAR:
        abort(404)                    # user tidak terdaftar -> halaman 404 custom

    role = "Admin Toko" if username == "admin" else "Member Toko"
    return f"""
        <h1>Profil {username.title()}</h1>
        <p>Username : {username}</p>
        <p>Status   : {role} (terdaftar)</p>
        <p><a href="{url_for('beranda')}">Kembali ke beranda</a></p>
    """

#3. CONVERTER int + abort(404)
@app.route("/produk/<int:id>")
def detail_produk(id):
    p = PRODUK.get(id)                # id sudah bertipe int
    if p is None:                     # produk tidak ditemukan
        abort(404)
    return f"""
        <h2>Detail Produk #{id}</h2>
        <p>Nama  : {p['nama']}</p>
        <p>Harga : Rp{p['harga']:,}</p>
        <p><a href="{url_for('produk')}">Kembali ke daftar produk</a></p>
    """

# 4. url_for() + redirect()

@app.route("/home")
def home_lama():
    # URL lama dialihkan ke URL baru:
    # GET /home -> 302 Found -> Location: / -> 200 OK
    return redirect(url_for("beranda"))


# 5. CUSTOM HALAMAN ERROR 404
@app.errorhandler(404)
def tidak_ditemukan(e):
    return f"""
        <h1>404 — Halaman Tidak Ditemukan</h1>
        <p>Maaf, halaman atau data yang Anda cari tidak ada.</p>
        <p><a href="{url_for('beranda')}">Kembali ke beranda</a></p>
    """, 404


if __name__ == "__main__":
    app.run(debug=True)