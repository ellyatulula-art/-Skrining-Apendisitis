import csv
import io
import json
import sqlite3
from contextlib import closing
from datetime import date, datetime
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
    --ink: #54213a;
    --pink: #ec1680;
    --pink-soft: #ffe0ef;
    --paper: #fff0f7;
    --line: #f3b7d3;
    --muted: #80556b;
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
    background: linear-gradient(135deg, #f78cbd, #ffd1e5);
    color: var(--ink);
}

.hero h1 {
    margin: 0;
    padding: 0;
    color: var(--ink);
    font-size: clamp(1.9rem, 4vw, 2.9rem);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.1;
}

.hero p {
    max-width: 30rem;
    margin: 0.9rem 0 0;
    color: #6b304b;
    font-size: 1.05rem;
    line-height: 1.6;
}

.hero p.note {
    margin-top: 0.6rem;
    color: #7b4961;
    font-size: 0.9rem;
}

.hero-art {
    width: 270px;
    height: 210px;
    flex: none;
    filter: drop-shadow(0 12px 18px rgba(118, 25, 72, 0.15));
}

.hero-art .tool-card {
    fill: rgba(255, 250, 253, 0.9);
    stroke: #ee9fc2;
    stroke-width: 1.5;
}

.hero-art .tool-line {
    fill: none;
    stroke: #b81362;
    stroke-width: 4;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.hero-art .tool-fill {
    fill: #fff7fb;
    stroke: #b81362;
    stroke-width: 4;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.hero-art .accent {
    fill: #ed3b91;
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
    background: #ffd9e9;
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
    box-shadow: 0 1px 4px rgba(80, 57, 69, 0.12);
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

/* ---------- Kartu formulir ---------- */
[data-testid="stVerticalBlockBorderWrapper"]:has(.patient-card-anchor),
[data-testid="stVerticalBlockBorderWrapper"]:has(.clinical-card-anchor) {
    position: relative;
    overflow: hidden;
    border-color: #f0c4d8;
    border-radius: 18px;
    background: linear-gradient(145deg, #fff, #fff8fb);
    box-shadow: 0 8px 24px rgba(84, 33, 58, 0.07);
    transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:has(.patient-card-anchor) {
    border-top: 3px solid #ec1680;
    background: linear-gradient(145deg, #fff, #fff5fa);
}

[data-testid="stVerticalBlockBorderWrapper"]:has(.clinical-card-anchor):hover,
[data-testid="stVerticalBlockBorderWrapper"]:has(.patient-card-anchor):hover {
    border-color: #ec8ab8;
    box-shadow: 0 12px 30px rgba(129, 38, 83, 0.12);
}

[data-testid="stVerticalBlockBorderWrapper"]:has(.clinical-card-anchor):has(.keluhan-card-anchor) {
    border-left: 4px solid #ec1680;
}

[data-testid="stVerticalBlockBorderWrapper"]:has(.clinical-card-anchor):has(.fisik-card-anchor) {
    border-left: 4px solid #e39a00;
}

[data-testid="stVerticalBlockBorderWrapper"]:has(.clinical-card-anchor):has(.laboratorium-card-anchor) {
    border-left: 4px solid #6b73d9;
}

.patient-card-anchor,
.clinical-card-anchor {
    display: block;
    height: 0;
}

.grp-head {
    align-items: center;
    margin: 0.1rem 0 0.75rem;
    padding: 0.25rem 0 0.65rem;
    border-bottom: 1px solid #f5d7e5;
}

.grp-head b {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 1.08rem;
}

.grp-head b::before {
    display: inline-grid;
    width: 2rem;
    height: 2rem;
    place-items: center;
    border-radius: 10px;
    background: #ffe0ef;
    color: #b81362;
    content: "✦";
    font-size: 1rem;
}

[data-testid="stVerticalBlockBorderWrapper"]:has(.fisik-card-anchor) .grp-head b::before {
    background: #fff0cf;
    color: #986000;
    content: "＋";
}

[data-testid="stVerticalBlockBorderWrapper"]:has(.laboratorium-card-anchor) .grp-head b::before {
    background: #e9eaff;
    color: #555dbb;
    content: "◉";
}

.grp-head span {
    padding: 0.28rem 0.6rem;
    border-radius: 999px;
    background: #fff0f7;
    color: #9b426b;
    font-size: 0.76rem;
    white-space: nowrap;
}

[data-testid="stVerticalBlockBorderWrapper"]:has(.patient-card-anchor) [data-testid="stTextInput"] input,
[data-testid="stVerticalBlockBorderWrapper"]:has(.patient-card-anchor) [data-testid="stDateInput"] input {
    border-color: #efd3e0;
    border-radius: 10px;
    background: #fff;
}

[data-testid="stVerticalBlockBorderWrapper"]:has(.patient-card-anchor) [data-testid="stTextInput"] input:focus,
[data-testid="stVerticalBlockBorderWrapper"]:has(.patient-card-anchor) [data-testid="stDateInput"] input:focus {
    border-color: #ec1680;
    box-shadow: 0 0 0 3px rgba(236, 22, 128, 0.12);
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
    border-color: #f06da9;
}

[data-testid="stCheckbox"]:has(input:checked) label {
    border-color: var(--pink);
    background: var(--pink-soft);
}

[data-testid="stCheckbox"] label[data-baseweb="checkbox"]:has(input:checked) > span:first-of-type {
    border-color: var(--pink) !important;
    background-color: var(--pink) !important;
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
    background: var(--pink);
    color: #fff;
    font-weight: 700;
}

[data-testid="stBaseButton-primary"]:hover, button[kind="primary"]:hover {
    background: #c90e69;
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

    .hero-art {
        width: min(100%, 270px);
        height: auto;
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
    "birth_date": "TEXT",
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
                    patient_name, gender, birth_date, birth_month,
                    birth_year, age_years, age_months
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.now().astimezone().isoformat(timespec="seconds"),
                    score,
                    category,
                    json.dumps(answers, ensure_ascii=False),
                    pasien["nama"],
                    pasien["jenis_kelamin"],
                    pasien["tanggal_lahir"].isoformat(),
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
                   age_years, age_months, birth_date
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
def hitung_usia(tanggal_lahir, sekarang=None):
    """Usia dalam tahun dan bulan penuh, atau None bila tanggal lahir di masa depan."""
    sekarang = sekarang or datetime.now().astimezone()
    hari_ini = sekarang.date()
    if tanggal_lahir > hari_ini:
        return None
    tahun = hari_ini.year - tanggal_lahir.year
    if (hari_ini.month, hari_ini.day) < (tanggal_lahir.month, tanggal_lahir.day):
        tahun -= 1
    total_bulan = (hari_ini.year - tanggal_lahir.year) * 12 + hari_ini.month - tanggal_lahir.month
    if hari_ini.day < tanggal_lahir.day:
        total_bulan -= 1
    bulan = total_bulan - tahun * 12
    return tahun, bulan


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
<h1>Selamat datang</h1>
<p><strong>Bantu nilai risiko apendisitis sejak dini.</strong> Masukkan temuan klinis pasien untuk melihat skor Alvarado dan kategori risikonya secara langsung.</p>
<p class="note">Informasi ini mendukung penilaian awal, bukan pengganti diagnosis atau keputusan klinis tenaga medis.</p>
</div>
<svg class="hero-art" viewBox="0 0 280 220" role="img" aria-label="Ilustrasi stetoskop, termometer, lembar pemeriksaan medis, serta usus besar dan usus kecil">
<defs>
<linearGradient id="medical-glow" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#ffb5d4"/>
<stop offset="1" stop-color="#f16ca8"/>
</linearGradient>
<linearGradient id="medical-metal" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#fff"/>
<stop offset="1" stop-color="#f7dce8"/>
</linearGradient>
</defs>
<circle cx="140" cy="110" r="100" fill="url(#medical-glow)"/>
<circle cx="140" cy="110" r="87" fill="none" stroke="rgba(255,255,255,0.58)" stroke-width="1.5" stroke-dasharray="3 7"/>
<g class="tool-card">
<rect x="20" y="26" width="100" height="78" rx="24"/>
<rect x="160" y="26" width="100" height="78" rx="24"/>
<rect x="20" y="116" width="100" height="78" rx="24"/>
<rect x="160" y="116" width="100" height="78" rx="24"/>
</g>
<g class="tool-line">
<path d="M49 49v13c0 15 9 23 21 23s21-8 21-23V49"/>
<path d="M49 49v-4m42 4v-4m-21 40v5c0 8 6 12 14 12h5"/>
<path d="M51 139h39a5 5 0 0 1 5 5v36H46v-36a5 5 0 0 1 5-5Z" class="tool-fill"/>
<path d="M60 139v-7h21v7m-26 18 4 4 7-8m7 4h14m-25 10 4 4 7-8m7 4h14"/>
<path d="M186 46v34a12 12 0 1 0 17 0V46a8.5 8.5 0 0 0-17 0Z"/>
<path d="M194.5 62v21m-8-26h6m-6-9h6"/>
</g>
<path d="M188 141h5c4 0 5-5 11-5s7 5 11 5h6c5 0 8 4 8 9v13c0 5-3 8-8 8h-7c-4 0-5 6-11 6s-7-6-11-6h-4c-5 0-8-3-8-8v-14c0-5 3-8 8-8Z"
      fill="none" stroke="#b81362" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M190 149c5-5 10 5 15 0s10 5 15 0m-30 8c5-5 10 5 15 0s10 5 15 0"
      fill="none" stroke="#ed3b91" stroke-width="3.5" stroke-linecap="round"/>
<circle cx="94" cy="89" r="7" fill="#f7b1ce" stroke="#b81362" stroke-width="3"/>
<path d="M141 31c-5-9-18-4-14 6 2 4 9 10 14 13 5-3 12-9 14-13 4-10-9-15-14-6Z" class="accent"/>
<circle cx="145" cy="193" r="4" class="accent"/>
<circle cx="139" cy="198" r="2" fill="#fff"/>
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
            st.markdown('<div class="patient-card-anchor"></div>', unsafe_allow_html=True)
            nama_pasien = st.text_input("Nama pasien", key="nama_pasien")

            kol1, kol2 = st.columns(2)
            with kol1:
                jenis_kelamin = st.radio(
                    "Jenis kelamin", ["Laki-laki", "Perempuan"], horizontal=True, key="jenis_kelamin"
                )
            with kol2:
                tanggal_lahir = st.date_input(
                    "Tanggal lahir",
                    value=date(sekarang.year - 25, sekarang.month, 1),
                    min_value=date(1900, 1, 1),
                    max_value=sekarang.date(),
                    key="tanggal_lahir",
                    format="DD/MM/YYYY",
                )

            usia = hitung_usia(tanggal_lahir, sekarang)
            st.text_input("Usia (otomatis)", value=format_usia(*usia) if usia else "-", disabled=True)
            if usia is None:
                st.error("Tanggal lahir berada di masa depan. Periksa kembali data kelahiran.")

        st.header("Temuan klinis")

        pilihan = {}
        for judul, kunci_grup in GRUP:
            maks = sum(KOMPONEN[k][1] for k in kunci_grup)
            kelas_kartu = {
                "Keluhan pasien": "keluhan-card-anchor",
                "Pemeriksaan fisik": "fisik-card-anchor",
                "Laboratorium": "laboratorium-card-anchor",
            }[judul]
            with st.container(border=True):
                st.markdown(
                    f'<div class="clinical-card-anchor {kelas_kartu}"></div>',
                    unsafe_allow_html=True,
                )
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
                    st.error("Tanggal lahir tidak valid. Perbaiki data pasien dulu.")
                else:
                    pasien = {
                        "nama": nama_pasien.strip(),
                        "jenis_kelamin": jenis_kelamin,
                        "tanggal_lahir": tanggal_lahir,
                        "bulan_lahir": tanggal_lahir.month,
                        "tahun_lahir": tanggal_lahir.year,
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
        "data pasien (nama, jenis kelamin, tanggal lahir), sehingga harus dijaga kerahasiaannya."
    )
    riwayat = load_history()
    if riwayat:
        baris = []
        for (rid, waktu, skor_db, kategori_db, jawaban_json,
             nama, jk, bln, thn, usia_th, usia_bln, tgl_lahir) in riwayat:
            jawaban = json.loads(jawaban_json)
            if tgl_lahir:
                tgl = date.fromisoformat(tgl_lahir)
                lahir = f"{tgl.day} {NAMA_BULAN[tgl.month - 1]} {tgl.year}"
            else:
                lahir = f"{NAMA_BULAN[bln - 1]} {thn}" if bln and thn else "-"
            baris.append({
                "ID": rid,
                "Waktu": waktu,
                "Nama Pasien": nama or "-",
                "Jenis Kelamin": jk or "-",
                "Tanggal Lahir": lahir,
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
