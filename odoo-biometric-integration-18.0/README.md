# Modul Integrasi Absensi Biometrik Profesional untuk Odoo

**Odoo Pro Biometric Integration** adalah modul komersial yang dirancang untuk menghubungkan mesin absensi (fingerprint/wajah) ZKTeco Anda secara *real-time* dengan Odoo. Dibuat dengan arsitektur yang tangguh dan antarmuka yang profesional.

---

### ✨ Fitur Utama

*   **📈 Logging & Audit Trail**: Setiap data mentah dari mesin dicatat dalam sebuah log khusus sebelum diproses. Memudahkan pelacakan dan audit.
*   **🔄 Pemrosesan Real-Time**: Data yang masuk dari mesin langsung diproses menjadi catatan absensi (`hr.attendance`) tanpa jeda.
*   **⚙️ Antarmuka Monitoring**: Dilengkapi UI untuk melihat status setiap data (Pending, Processed, Error) dengan kode warna yang informatif.
*   **🛠️ Proses Ulang Manual**: Admin dapat memproses ulang data yang gagal (error) langsung dari UI, memberikan kontrol penuh.
*   **🔗 Penanda Absensi Otomatis**: Setiap absensi yang dibuat dari mesin ditandai, membedakannya dari input manual.
*   **🌐 Konfigurasi Fleksibel**: Pengaturan penting seperti *Secret Key* dan *Timezone* mesin dapat diubah dengan mudah melalui menu Settings di Odoo.

---



### 🚀 Instalasi & Konfigurasi

1.  Unduh modul ini dalam bentuk file `.zip`.
2.  Letakkan folder modul di dalam direktori `addons` Odoo Anda.
3.  Restart server Odoo Anda.
4.  Aktifkan "Developer Mode".
5.  Navigasi ke menu **Apps**, klik **Update Apps List**, hapus filter "Apps", dan cari modul `odoo_pro_biometric_integration`.
6.  Klik tombol **Install**.
7.  Setelah instalasi selesai, navigasi ke **Attendances > Configuration > Settings**.
8.  Isi **Biometric Secret Key** dan pilih **Biometric Device Timezone** yang sesuai dengan lokasi mesin Anda. Simpan.
9.  Pastikan `Secret Key` ini sama persis dengan yang ada di script Python (`sync_to_vps2.py`) Anda.

---

### ✅ Dependensi

*   `hr_attendance` (Modul bawaan Odoo)

### ℹ️ Kompatibilitas

*   Odoo Versi 18.0

### ✉️ Kontak & Dukungan

Dibuat oleh **Dimas Aryo Novantri**. Untuk pertanyaan, kustomisasi, atau dukungan, silakan hubungi saya di: **dimasaryonovantri04@gmail.com**.



