import csv
import io
import json
import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="CDSS Skrining Apendisitis",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #0f1b33;
    --cobalt: #2a5cff;
    --cobalt-soft: #eaf0ff;
    --paper: #f3f6fb;
    --line: #dde4f0;
    --muted: #5e6b85;
}

.stApp, .stApp button, .stApp input, .stApp textarea,
.stApp [data-baseweb="select"] div {
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: var(--paper);
    color: var(--ink);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1180px;
    padding: 2rem 2rem 4rem;
}

/* ---------- Hero ---------- */
.hero {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    gap: 2rem;
    margin-bottom: 1.6rem;
    padding: 2.2rem 2.6rem;
    border-radius: 20px;
    background: var(--ink);
    color: #fff;
}

.hero h1 {
    margin: 0;
    padding: 0;
    color: #fff;
    font-size: clamp(1.9rem, 4vw, 2.9rem);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.1;
}

.hero p {
    max-width: 30rem;
    margin: 0.9rem 0 0;
    color: #b9c6e4;
    font-size: 1.05rem;
    line-height: 1.6;
}

.hero p.note {
    margin-top: 0.6rem;
    color: #7f90b6;
    font-size: 0.9rem;
}

.hero svg {
    width: 170px;
    height: 170px;
}

.pulse {
    transform-box: fill-box;
    transform-origin: center;
    animation: pulse 2.2s ease-out infinite;
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 0.7; }
    100% { transform: scale(3.2); opacity: 0; }
}

@media (prefers-reduced-motion: reduce) {
    .pulse { animation: none; opacity: 0; }
}

/* ---------- Tab ---------- */
[data-baseweb="tab-list"] {
    width: fit-content;
    gap: 0.3rem;
    padding: 0.3rem;
    border-radius: 14px;
    background: #e5ebf6;
}

[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {
    display: none;
}

[data-baseweb="tab"] {
    height: auto;
    padding: 0.55rem 1.1rem;
    border-radius: 10px;
    color: var(--muted);
    font-weight: 600;
}

[data-baseweb="tab"][aria-selected="true"] {
    background: #fff;
    color: var(--ink);
    box-shadow: 0 1px 4px rgba(15, 27, 51, 0.12);
}

/* ---------- Judul ---------- */
[data-testid="stMarkdownContainer"] h2 {
    margin-top: 1.2rem;
    color: var(--ink);
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: -0.025em;
}

.grp-head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}

.grp-head b {
    color: var(--ink);
    font-size: 1.05rem;
    font-weight: 750;
}

.grp-head span {
    color: var(--muted);
    font-size: 0.85rem;
    font-weight: 600;
}

/* ---------- Checkbox sebagai baris pilihan ---------- */
[data-testid="stCheckbox"] {
    padding: 0.15rem 0;
}

[data-testid="stCheckbox"] label {
    width: 100%;
    padding: 0.7rem 0.95rem;
    border: 1px solid var(--line);
    border-radius: 12px;
    background: #fff;
    transition: border-color 150ms ease, background 150ms ease;
}

[data-testid="stCheckbox"] label:hover {
    border-color: #9db6ff;
}

[data-testid="stCheckbox"]:has(input:checked) label {
    border-color: var(--cobalt);
    background: var(--cobalt-soft);
}

[data-testid="stCheckbox"] label[data-baseweb="checkbox"]:has(input:checked) > span:first-of-type {
    border-color: var(--cobalt) !important;
    background-color: var(--cobalt) !important;
}

[data-testid="stCheckbox"] label p {
    font-weight: 600;
}

/* ---------- Panel skor ---------- */
[data-testid="stColumn"]:has(.sticky-anchor),
[data-testid="column"]:has(.sticky-anchor) {
    position: sticky;
    top: 3.5rem;
    align-self: flex-start;
}

.panel-label {
    color: var(--muted);
    font-size: 0.9rem;
    font-weight: 700;
}

.panel-score {
    display: flex;
    align-items: baseline;
    gap: 0.3rem;
    margin: 0.1rem 0 0.8rem;
}

.panel-score .num {
    font-size: 4.6rem;
    font-weight: 800;
    letter-spacing: -0.05em;
    line-height: 1;
}

.panel-score .den {
    color: var(--muted);
    font-size: 1.4rem;
    font-weight: 700;
}

.meter {
    display: flex;
    gap: 4px;
}

.meter i {
    flex: 1;
    height: 16px;
    border-radius: 5px;
}

.zones {
    display: flex;
    gap: 4px;
    margin: 0.4rem 0 1rem;
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 600;
}

.verdict {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-size: 0.92rem;
    font-weight: 750;
}

.advice {
    margin: 0.8rem 0 0.4rem;
    color: #2b3a5c;
    font-size: 0.95rem;
    line-height: 1.6;
}

.rincian {
    margin: 0.35rem 0;
    font-size: 0.92rem;
    line-height: 1.45;
}

.rincian.off {
    color: #8a96ad;
}

/* ---------- Tombol ---------- */
[data-testid="stBaseButton-primary"], button[kind="primary"] {
    min-height: 3rem;
    border: 0;
    border-radius: 12px;
    background: var(--cobalt);
    color: #fff;
    font-weight: 700;
}

[data-testid="stBaseButton-primary"]:hover, button[kind="primary"]:hover {
    background: #1d49d6;
    color: #fff;
}

[data-testid="stBaseButton-secondary"], button[kind="secondary"] {
    border-radius: 12px;
    font-weight: 650;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

[data-testid="stMetric"] {
    padding: 0.9rem 1.1rem;
    border: 1px solid var(--line);
    border-radius: 14px;
    background: #fff;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
    line-height: 1.6;
}

@media (max-width: 800px) {
    .block-container {
        padding: 1rem 1rem 3rem;
    }

    .hero {
        grid-template-columns: 1fr;
        padding: 1.6rem 1.4rem;
    }

    .hero svg {
        width: 120px;
        height: 120px;
    }

    [data-testid="stColumn"]:has(.sticky-anchor),
    [data-testid="column"]:has(.sticky-anchor) {
        position: static;
    }
}
</style>
""", unsafe_allow_html=True)

DATABASE_PATH = Path.home() / ".cdss_apendisitis" / "skrining.db"

NAMA_BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]

KOLOM_PASIEN = {
    "patient_name": "TEXT",
    "gender": "TEXT",
    "birth_month": "INTEGER",
    "birth_year": "INTEGER",
    "age_years": "INTEGER",
    "age_months": "INTEGER",
}

# Komponen Alvarado Score: kunci -> (label, bobot)
KOMPONEN = {
    "migrasi_nyeri": ("Nyeri berpindah dari ulu hati/pusar ke perut kanan bawah", 1),
    "anoreksia": ("Anoreksia (nafsu makan menurun)", 1),
    "mual_muntah": ("Mual dan/atau muntah", 1),
    "nyeri_tekan_kanan_bawah": ("Nyeri tekan perut kanan bawah (titik McBurney)", 2),
    "nyeri_lepas": ("Nyeri lepas (rebound tenderness)", 1),
    "demam": ("Demam, suhu di atas 37,3°C", 1),
    "leukositosis": ("Leukositosis, leukosit di atas 10.000/mm³", 2),
    "shift_neutrofil": ("Neutrofil bergeser ke kiri, di atas 75%", 1),
}

GRUP = [
    ("Keluhan pasien", ["migrasi_nyeri", "anoreksia", "mual_muntah"]),
    ("Pemeriksaan fisik", ["nyeri_tekan_kanan_bawah", "nyeri_lepas", "demam"]),
    ("Laboratorium", ["leukositosis", "shift_neutrofil"]),
]

LABEL_RIWAYAT = {
    "migrasi_nyeri": "Migrasi nyeri",
    "anoreksia": "Anoreksia",
    "mual_muntah": "Mual/muntah",
    "nyeri_tekan_kanan_bawah": "Nyeri tekan kanan bawah",
    "nyeri_lepas": "Nyeri lepas",
    "demam": "Demam",
    "leukositosis": "Leukositosis",
    "shift_neutrofil": "Shift neutrofil",
}

# Warna zona risiko: (warna isi, warna teks, label, saran)
ZONA = {
    "RENDAH": (
        "#1fa67a", "#0b6e51", "Risiko rendah",
        "Apendisitis akut kecil kemungkinannya. Evaluasi ulang gejala secara berkala, "
        "dan segera periksa bila nyeri memburuk atau muncul gejala baru.",
    ),
    "SEDANG": (
        "#e39a00", "#8a5a00", "Risiko sedang (equivocal)",
        "Observasi klinis ketat 4–6 jam dan evaluasi ulang gejala. Pertimbangkan USG abdomen "
        "atau CT-scan, serta ulangi laboratorium bila gejala menetap.",
    ),
    "TINGGI": (
        "#e5484d", "#a7191f", "Risiko tinggi",
        "Segera konsultasi dengan dokter spesialis bedah. Pertimbangkan apendektomi setelah "
        "diagnosis dikonfirmasi; USG atau CT-scan dapat memperkuat diagnosis.",
    ),
}


# ======================= DATABASE =======================
def initialize_database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DATABASE_PATH, timeout=5)) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS screening_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    answers TEXT NOT NULL
                )
            """)
            ada = {row[1] for row in connection.execute("PRAGMA table_info(screening_history)")}
            for kolom, tipe in KOLOM_PASIEN.items():
                if kolom not in ada:
                    connection.execute(f"ALTER TABLE screening_history ADD COLUMN {kolom} {tipe}")


def save_screening(pasien, score, category, answers):
    with closing(sqlite3.connect(DATABASE_PATH, timeout=5)) as connection:
        with connection:
            connection.execute(
                """
                INSERT INTO screening_history (
                    created_at, score, category, answers,
                    patient_name, gender, birth_month, birth_year,
                    age_years, age_months
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.now().astimezone().isoformat(timespec="seconds"),
                    score,
                    category,
                    json.dumps(answers, ensure_ascii=False),
                    pasien["nama"],
                    pasien["jenis_kelamin"],
                    pasien["bulan_lahir"],
                    pasien["tahun_lahir"],
                    pasien["usia_tahun"],
                    pasien["usia_bulan"],
                ),
            )


def load_history():
    with closing(sqlite3.connect(DATABASE_PATH, timeout=5)) as connection:
        return connection.execute(
            """
            SELECT id, created_at, score, category, answers,
                   patient_name, gender, birth_month, birth_year,
                   age_years, age_months
            FROM screening_history
            ORDER BY id DESC
            LIMIT 100
            """
        ).fetchall()


def delete_screening(record_id):
    with closing(sqlite3.connect(DATABASE_PATH, timeout=5)) as connection:
        with connection:
            connection.execute("DELETE FROM screening_history WHERE id = ?", (record_id,))


def delete_all_screenings():
    with closing(sqlite3.connect(DATABASE_PATH, timeout=5)) as connection:
        with connection:
            connection.execute("DELETE FROM screening_history")


# ======================= LOGIKA =======================
def hitung_usia(bulan_lahir, tahun_lahir, sekarang=None):
    """Usia otomatis dari bulan & tahun lahir (perkiraan, selisih bulan kalender).
    Mengembalikan (tahun, bulan) atau None bila tanggal lahir di masa depan."""
    sekarang = sekarang or datetime.now().astimezone()
    total_bulan = (sekarang.year - tahun_lahir) * 12 + (sekarang.month - bulan_lahir)
    if total_bulan < 0:
        return None
    return total_bulan // 12, total_bulan % 12


def format_usia(tahun, bulan):
    if tahun is None:
        return "-"
    return f"{tahun} tahun {bulan} bulan"


def hitung_alvarado(pilihan):
    """
    Alvarado Score (MANTRELS) - 8 komponen, total skor maksimal 10.
    - Skor 0-4  : Risiko rendah
    - Skor 5-6  : Risiko sedang (equivocal)
    - Skor 7-10 : Risiko tinggi
    `pilihan` = dict {kunci: bool}
    """
    skor = sum(bobot for kunci, (_, bobot) in KOMPONEN.items() if pilihan[kunci])
    if skor <= 4:
        kategori = "RENDAH"
    elif skor <= 6:
        kategori = "SEDANG"
    else:
        kategori = "TINGGI"
    return skor, kategori


def zona_segmen(nomor):
    """Zona warna untuk segmen ke-nomor (1-10) pada meter skor."""
    if nomor <= 4:
        return "RENDAH"
    if nomor <= 6:
        return "SEDANG"
    return "TINGGI"


def panel_skor_html(skor, kategori):
    warna, warna_teks, label, saran = ZONA[kategori]
    segmen = ""
    for nomor in range(1, 11):
        w = ZONA[zona_segmen(nomor)][0]
        isi = w if nomor <= skor else f"{w}30"
        segmen += f'<i style="background:{isi}"></i>'
    return (
        '<div class="sticky-anchor"></div>'
        '<div class="panel-label">Skor Alvarado</div>'
        f'<div class="panel-score"><span class="num" style="color:{warna}">{skor}</span>'
        '<span class="den">/10</span></div>'
        f'<div class="meter">{segmen}</div>'
        '<div class="zones"><span style="flex:4">Rendah 0–4</span>'
        '<span style="flex:2">Sedang 5–6</span><span style="flex:4">Tinggi 7–10</span></div>'
        f'<span class="verdict" style="background:{warna}22;color:{warna_teks}">{label}</span>'
        f'<p class="advice">{saran}</p>'
    )


initialize_database()
sekarang = datetime.now().astimezone()

# ======================= HEADER =======================
st.markdown("""
<section class="hero">
<div>
<h1>Skrining dini apendisitis</h1>
<p>Centang temuan klinis pasien. Skor Alvarado dan tingkat risikonya dihitung langsung.</p>
<p class="note">Alat bantu skrining awal, bukan diagnosis.</p>
</div>
<svg viewBox="0 0 220 220" role="img" aria-label="Diagram empat kuadran perut dengan kuadran kanan bawah disorot">
<defs><clipPath id="badan"><rect x="10" y="10" width="200" height="200" rx="30"/></clipPath></defs>
<rect x="10" y="110" width="100" height="100" fill="rgba(255,255,255,0.14)" clip-path="url(#badan)"/>
<rect x="10" y="10" width="200" height="200" rx="30" fill="none" stroke="rgba(255,255,255,0.45)" stroke-width="2"/>
<line x1="110" y1="10" x2="110" y2="210" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
<line x1="10" y1="110" x2="210" y2="110" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
<circle cx="110" cy="110" r="5" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"/>
<circle class="pulse" cx="70" cy="156" r="6" fill="#ff6a5b"/>
<circle cx="70" cy="156" r="6" fill="#ff6a5b"/>
<text x="20" y="138" fill="rgba(255,255,255,0.8)" font-size="10" font-family="sans-serif">titik McBurney</text>
<text x="60" y="198" fill="rgba(255,255,255,0.6)" font-size="9" font-family="sans-serif" text-anchor="middle">kanan bawah</text>
</svg>
</section>
""", unsafe_allow_html=True)

tab_form, tab_riwayat, tab_kb = st.tabs([
    "Form skrining",
    "Riwayat & kelola data",
    "Knowledge base",
])

# ======================= TAB 1: FORM SKRINING =======================
with tab_form:
    kiri, kanan = st.columns([1.55, 1], gap="large")

    with kiri:
        st.header("Data pasien")

        with st.container(border=True):
            nama_pasien = st.text_input("Nama pasien", key="nama_pasien")

            kol1, kol2 = st.columns(2)
            with kol1:
                jenis_kelamin = st.radio(
                    "Jenis kelamin", ["Laki-laki", "Perempuan"], horizontal=True, key="jenis_kelamin"
                )
            with kol2:
                bulan_lahir_nama = st.selectbox(
                    "Bulan lahir", NAMA_BULAN, index=sekarang.month - 1, key="bulan_lahir"
                )

            kol3, kol4 = st.columns(2)
            with kol3:
                daftar_tahun = list(range(sekarang.year, 1899, -1))
                tahun_lahir = st.selectbox(
                    "Tahun lahir", daftar_tahun, index=daftar_tahun.index(sekarang.year - 25), key="tahun_lahir"
                )
            bulan_lahir = NAMA_BULAN.index(bulan_lahir_nama) + 1
            usia = hitung_usia(bulan_lahir, int(tahun_lahir), sekarang)
            with kol4:
                st.text_input("Usia (otomatis)", value=format_usia(*usia) if usia else "-", disabled=True)
            if usia is None:
                st.error("Bulan/tahun lahir berada di masa depan. Periksa kembali data kelahiran.")

        st.header("Temuan klinis")

        pilihan = {}
        for judul, kunci_grup in GRUP:
            maks = sum(KOMPONEN[k][1] for k in kunci_grup)
            with st.container(border=True):
                st.markdown(
                    f'<div class="grp-head"><b>{judul}</b><span>maksimal +{maks} poin</span></div>',
                    unsafe_allow_html=True,
                )
                for kunci in kunci_grup:
                    label, bobot = KOMPONEN[kunci]
                    pilihan[kunci] = st.checkbox(f"{label} (+{bobot})", key=f"cb_{kunci}")

        st.caption(
            "Sistem ini memakai Alvarado Score sebagai basis rule-based CDSS dan hanya membantu "
            "penilaian awal. Hasilnya bukan pengganti diagnosis atau penilaian klinis dokter."
        )

    # ----- Panel hasil (diperbarui langsung setiap checkbox diubah) -----
    skor, kategori = hitung_alvarado(pilihan)

    with kanan:
        with st.container(border=True):
            st.markdown(panel_skor_html(skor, kategori), unsafe_allow_html=True)

            with st.expander("Rincian skor"):
                for kunci, (label, bobot) in KOMPONEN.items():
                    if pilihan[kunci]:
                        st.markdown(f'<div class="rincian">✅ {label} <b>(+{bobot})</b></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="rincian off">⬜ {label}</div>', unsafe_allow_html=True)

            if st.button("Simpan hasil", type="primary", use_container_width=True):
                if not nama_pasien.strip():
                    st.error("Isi nama pasien dulu sebelum menyimpan.")
                elif usia is None:
                    st.error("Bulan/tahun lahir tidak valid. Perbaiki data pasien dulu.")
                else:
                    pasien = {
                        "nama": nama_pasien.strip(),
                        "jenis_kelamin": jenis_kelamin,
                        "bulan_lahir": bulan_lahir,
                        "tahun_lahir": int(tahun_lahir),
                        "usia_tahun": usia[0],
                        "usia_bulan": usia[1],
                    }
                    jawaban = {k: ("Ya" if pilihan[k] else "Tidak") for k in KOMPONEN}
                    save_screening(pasien, skor, kategori, jawaban)
                    st.success(f"Hasil {pasien['nama']} tersimpan di tab Riwayat & kelola data.")

# ======================= TAB 2: RIWAYAT & KELOLA DATA =======================
with tab_riwayat:
    st.header("Riwayat skrining")
    st.caption(
        "Menampilkan maksimal 100 skrining terbaru. Data tersimpan di database SQLite lokal dan memuat "
        "data pasien (nama, jenis kelamin, bulan/tahun lahir), sehingga harus dijaga kerahasiaannya."
    )
    riwayat = load_history()
    if riwayat:
        baris = []
        for (rid, waktu, skor_db, kategori_db, jawaban_json,
             nama, jk, bln, thn, usia_th, usia_bln) in riwayat:
            jawaban = json.loads(jawaban_json)
            lahir = f"{NAMA_BULAN[bln - 1]} {thn}" if bln and thn else "-"
            baris.append({
                "ID": rid,
                "Waktu": waktu,
                "Nama Pasien": nama or "-",
                "Jenis Kelamin": jk or "-",
                "Bulan/Tahun Lahir": lahir,
                "Usia": format_usia(usia_th, usia_bln),
                "Skor": f"{skor_db}/10",
                "Kategori": kategori_db,
                **{LABEL_RIWAYAT[k]: jawaban.get(k, "-") for k in KOMPONEN},
            })

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total skrining", len(baris))
        m2.metric("Risiko rendah", sum(1 for b in baris if b["Kategori"] == "RENDAH"))
        m3.metric("Risiko sedang", sum(1 for b in baris if b["Kategori"] == "SEDANG"))
        m4.metric("Risiko tinggi", sum(1 for b in baris if b["Kategori"] == "TINGGI"))

        st.write("")
        st.dataframe(baris, hide_index=True, use_container_width=True)

        buffer = io.StringIO()
        penulis = csv.DictWriter(buffer, fieldnames=list(baris[0].keys()))
        penulis.writeheader()
        penulis.writerows(baris)
        st.download_button(
            "Unduh riwayat (CSV)",
            data=buffer.getvalue().encode("utf-8-sig"),
            file_name="riwayat_skrining_apendisitis.csv",
            mime="text/csv",
        )

        st.header("Kelola data")
        opsi = {
            f"#{b['ID']} {b['Nama Pasien']}, {b['Waktu']}, skor {b['Skor']}": b["ID"]
            for b in baris
        }
        terpilih = st.selectbox("Pilih data yang akan dihapus", list(opsi.keys()))
        if st.button("Hapus data terpilih"):
            delete_screening(opsi[terpilih])
            st.rerun()

        with st.expander("Hapus semua data"):
            yakin = st.checkbox("Saya yakin ingin menghapus seluruh riwayat skrining", key="konfirmasi_hapus_semua")
            if st.button("Hapus semua riwayat", disabled=not yakin):
                delete_all_screenings()
                st.rerun()
    else:
        st.info("Belum ada hasil tersimpan. Simpan hasil dari tab Form skrining untuk mulai mengisi riwayat.")

# ======================= TAB 3: KNOWLEDGE BASE =======================
with tab_kb:
    st.header("Knowledge base")
    st.write("Komponen dan aturan yang dipakai aplikasi untuk menghitung Alvarado Score.")
    st.subheader("Komponen penilaian")
    st.dataframe(
        [{"Komponen": label, "Bobot": bobot} for label, bobot in KOMPONEN.values()],
        hide_index=True,
        use_container_width=True,
    )
    st.subheader("Interpretasi skor")
    st.markdown("""
- **0–4, risiko rendah:** evaluasi klinis tetap diperlukan.
- **5–6, risiko sedang:** pertimbangkan observasi dan pemeriksaan penunjang sesuai penilaian tenaga medis.
- **7–10, risiko tinggi:** perlu evaluasi segera oleh tenaga medis.
""")
    st.info(
        "Skor ini merupakan alat bantu skrining awal, bukan diagnosis. "
        "Keputusan pemeriksaan dan tata laksana harus ditentukan tenaga medis "
        "berdasarkan evaluasi klinis lengkap."
    )
