app = Flask(__name__)

# ==================== DATA ====================

# Daftar username yang sudah terdaftar di toko (pelanggan/member/admin)
TERDAFTAR = ["andi", "budi", "citra", "dewi", "admin", "member1"]

# Data produk toko (dictionary) — untuk route dengan converter int
PRODUK = {
    1: {"nama": "Kopi Susu",  "harga": 18000},
    2: {"nama": "Teh Tarik",  "harga": 15000},
    3: {"nama": "Roti Bakar", "harga": 12000},
    4: {"nama": "Donat Gula", "harga": 10000},
}

# List of dict untuk {% for %} di template (beranda & daftar produk)
PRODUK_LIST = [{"id": id, **p} for id, p in PRODUK.items()]

# 1. ROUTE STATIS (minimal 4 halaman)
@app.route("/")
@app.route("/beranda")              # satu fungsi boleh punya lebih dari satu route
def beranda():
    return render_template(
        "beranda.html",
        produk=PRODUK_LIST,         # dipakai filter |length di template
        terdaftar=TERDAFTAR,
    )


@app.route("/tentang")
def tentang():
    return render_template("tentang.html")


@app.route("/produk")
def produk():
    return render_template("produk.html", produk=PRODUK_LIST)


@app.route("/kontak")
def kontak():
    return render_template("kontak.html")


# 2. DYNAMIC ROUTING + VALIDASI
# /cek/<username> — cek ketersediaan username
@app.route("/cek/<username>")
def cek_username(username):
    u = username.lower()
    valid = len(u) >= 4                       # validasi: minimal 4 karakter
    tersedia = valid and u not in TERDAFTAR   # cek di daftar terdaftar

    # template cek.html menentukan tampilan lewat {% if %} 3 kondisi:
    # tidak valid / tersedia / sudah dipakai
    status = 400 if not valid else 200
    return render_template(
        "cek.html", username=u, valid=valid, tersedia=tersedia
    ), status

@app.route("/cek")
def cek_query():
    u = request.args.get("u", "")
    if u == "":
        return redirect(url_for("beranda"))
    # redirect + url_for: alihkan ke route /cek/<username>
    return redirect(url_for("cek_username", username=u))


# /user/<username> — profil user yang terdaftar
@app.route("/user/<username>")
def profil(username):
    u = username.lower()
    if len(u) < 4:                            # validasi: minimal 4 karakter
        return render_template(
            "error.html",
            pesan="Username tidak valid — minimal 4 karakter.",
        ), 400

    if u not in TERDAFTAR:
        abort(404)                            # user tidak terdaftar -> 404 custom

    role = "Admin Toko" if u == "admin" else "Member Toko"
    return render_template(
        "profil.html", username=u, role=role, terdaftar=TERDAFTAR
    )


#3. CONVERTER int + abort(404)
@app.route("/produk/<int:id>")
def detail_produk(id):
    p = PRODUK.get(id)                # id sudah bertipe int
    if p is None:                     # produk tidak ditemukan
        abort(404)
    return render_template("detail_produk.html", p=p, id=id)

# 4. url_for() + redirect()

@app.route("/home")
def home_lama():
    # URL lama dialihkan ke URL baru:
    # GET /home -> 302 Found -> Location: / -> 200 OK
    return redirect(url_for("beranda"))


# 5. CUSTOM HALAMAN ERROR 404
@app.errorhandler(404)
def tidak_ditemukan(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)