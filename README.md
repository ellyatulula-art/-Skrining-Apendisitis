# CDSS Skrining Apendisitis

Aplikasi web sederhana untuk skrining awal apendisitis akut menggunakan **Alvarado Score (MANTRELS)**. Aplikasi dibuat dengan Streamlit dan menyimpan rekap skrining secara lokal menggunakan SQLite.

Form pasien menerima tanggal lahir lengkap dan menghitung usia secara otomatis. Tampilan aplikasi menggunakan tema pink lembut.

> **Catatan:** Hasil aplikasi merupakan alat bantu skrining awal, bukan diagnosis. Keputusan klinis tetap harus dilakukan oleh tenaga medis profesional.

## Persyaratan

- Python terpasang
- Koneksi internet saat memasang dependensi

## Instalasi dan Menjalankan  

Buka PowerShell atau terminal pada folder proyek, lalu jalankan:
```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit akan menampilkan alamat aplikasi di terminal, biasanya `http://localhost:8501`. Buka alamat tersebut di browser.

## Cara Menggunakan

1. Buka menu **Form Skrining**.
2. Isi data pasien dan tanggal pemeriksaan. Nama pasien dan No. RM wajib diisi sebelum data dapat disimpan.
3. Centang indikator yang ditemukan, lalu pilih **Jalankan Skrining Dini**.
4. Periksa skor, kategori risiko, dan rekomendasi yang ditampilkan.
5. Pilih **Simpan ke Database** untuk menyimpan hasil skrining.
6. Buka **Database Rekap** untuk melihat data tersimpan, memfilter kategori risiko, mengunduh CSV, atau menghapus data.
7. Buka **Kamus Skor** untuk melihat indikator dan bobot Alvarado Score.

Tanggal pemeriksaan dibatasi mulai 1 Januari dari lima tahun sebelum tahun berjalan hingga tanggal hari ini.

## Penyimpanan Data

Database `cdss_apendisitis.db` dibuat otomatis di folder proyek saat aplikasi dijalankan. File tersebut berisi data pasien dan hasil skrining; file CSV yang diunduh hanya berisi rekap yang sedang ditampilkan.

Database lokal ini tidak menyediakan autentikasi atau enkripsi. Simpan dan bagikan file database maupun CSV dengan hati-hati, terutama jika berisi informasi pasien.

## Struktur Proyek

- `app.py` - kode aplikasi Streamlit dan logika Alvarado Score
- `requirements.txt` - dependensi Python
- `cdss_apendisitis.db` - database SQLite yang dibuat otomatis saat aplikasi berjalan

