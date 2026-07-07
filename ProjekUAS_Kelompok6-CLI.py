import time  # Berfungsi untuk mengatur waktu dan tanggal, serta menghitung durasi parkir
import os    # Berfungsi untuk mengatur path file dan direktori

# Class untuk membuat node dalam linked list riwayat transaksi parkir
class NodeRiwayat:
    def __init__(self, jenis, plat_nomor, waktu_masuk):
        self.jenis = jenis
        self.plat_nomor = plat_nomor
        self.waktu_masuk = waktu_masuk
        self.waktu_keluar = "-"
        self.durasi = "-"
        self.biaya = "-"
        self.status = "Parkir"
        self.next = None


# Class untuk mengelola linked list riwayat transaksi parkir
class LinkedListRiwayat:
    # Inisialisasi linked list untuk menyimpan riwayat transaksi parkir
    def __init__(self):
        self.head = None
        self.total_pendapatan = 0
        self.total_kendaraan = 0

    # Menambahkan transaksi baru ke dalam linked list
    def tambah_transaksi(self, jenis, plat_nomor, waktu_masuk):
        node_baru = NodeRiwayat(jenis, plat_nomor, waktu_masuk)

        if self.head is None:
            self.head = node_baru
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node_baru

    # Mengambil seluruh data riwayat parkir dalam bentuk list of tuple.
    # Dipakai bersama oleh tampilan menu dan proses unduh laporan,
    # supaya kedua fitur selalu menampilkan data yang sama persis (sinkron dengan versi GUI).
    def get_semua_data(self):
        data = []
        current = self.head
        no = 1
        while current:
            biaya = "-" if current.biaya == "-" else f"Rp{current.biaya:.0f}"
            data.append((no, current.jenis, current.plat_nomor, current.waktu_masuk,
                         current.waktu_keluar, current.durasi, biaya, current.status))
            no += 1
            current = current.next
        return data

    # Menghitung jumlah mobil dan motor yang tercatat dalam riwayat
    def get_statistik(self):
        total_mobil = 0
        total_motor = 0
        current = self.head
        while current:
            if current.jenis == "Mobil":
                total_mobil += 1
            else:
                total_motor += 1
            current = current.next
        return total_mobil, total_motor

    # Menampilkan riwayat transaksi parkir dalam format tabel
    def tampilkan_riwayat(self):
        data = self.get_semua_data()
        total_mobil, total_motor = self.get_statistik()

        print("\n" + "═"*90)
        print("                              RIWAYAT TRANSAKSI PARKIR HARIAN")
        print("═"*90 + "\n")

        if not data:
            print("Belum ada riwayat transaksi.\n")
            return

        print("╒════╤═══════╤════════════╤══════════╤══════════╤════════════╤═══════════╤═══════════════╕")
        print("│ No │ Jenis │ Plat Nomor │ Masuk    │ Keluar   │ Durasi     │ Biaya     │ Status        │")

        for i, baris in enumerate(data):
            no, jenis, plat, masuk, keluar, durasi, biaya, status = baris
            if i == 0:
                print("╞════╪═══════╪════════════╪══════════╪══════════╪════════════╪═══════════╪═══════════════╡")
            else:
                print("├────┼───────┼────────────┼──────────┼──────────┼────────────┼───────────┼───────────────┤")

            print(f"│ {no:<2} │ {jenis:<5} │ {plat:<10} │ {masuk:<8} │ {keluar:<8} │ {durasi:<10} │ {biaya:<9} │ {status:<13} │")

        print("╞════╧═══════╧════════════╧══════════╧══════════╧════════════╧═══════════╪═══════════════╡")
        print(f"│ Total Motor                                                            │ {total_motor:<13} │")
        print("├────────────────────────────────────────────────────────────────────────┼───────────────┤")
        print(f"│ Total Mobil                                                            │ {total_mobil:<13} │")
        print("├────────────────────────────────────────────────────────────────────────┼───────────────┤")
        print(f"│ Total Pendapatan                                                       │ Rp{self.total_pendapatan:<12.2f}│")
        print("╘════════════════════════════════════════════════════════════════════════╧═══════════════╛\n")

    # Mengunduh riwayat transaksi parkir ke dalam file teks.
    # Mengembalikan (True, file_path) jika berhasil atau (False, pesan_error) jika gagal,
    # sama seperti pola return di versi GUI.
    def unduh_riwayat(self):
        nama_file = f"Laporan_Parkir_{time.strftime('%Y-%m-%d')}.txt"
        lokasi_script = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(lokasi_script, nama_file)

        try:
            data = self.get_semua_data()
            total_mobil, total_motor = self.get_statistik()

            with open(file_path, "w", encoding="utf-8") as file:
                file.write("\n" + "╔" + "═"*88 + "╗" + "\n")
                file.write("                              RIWAYAT TRANSAKSI PARKIR HARIAN\n")
                file.write("╚" + "═"*88 + "╝" + "\n\n")

                if not data:
                    file.write("Belum ada riwayat transaksi.\n")
                else:
                    file.write("╒════╤═══════╤════════════╤══════════╤══════════╤════════════╤═══════════╤═══════════════╕\n")
                    file.write("│ No │ Jenis │ Plat Nomor │ Masuk    │ Keluar   │ Durasi     │ Biaya     │ Status        │\n")

                    for i, baris in enumerate(data):
                        no, jenis, plat, masuk, keluar, durasi, biaya, status = baris
                        if i == 0:
                            file.write("╞════╪═══════╪════════════╪══════════╪══════════╪════════════╪═══════════╪═══════════════╡\n")
                        else:
                            file.write("├────┼───────┼────────────┼──────────┼──────────┼────────────┼───────────┼───────────────┤\n")

                        file.write(f"│ {no:<2} │ {jenis:<5} │ {plat:<10} │ {masuk:<8} │ {keluar:<8} │ {durasi:<10} │ {biaya:<9} │ {status:<13} │\n")

                    file.write("╞════╧═══════╧════════════╧══════════╧══════════╧════════════╧═══════════╪═══════════════╡\n")
                    file.write(f"│ Total Motor                                                            │ {total_motor:<13} │\n")
                    file.write("├────────────────────────────────────────────────────────────────────────┼───────────────┤\n")
                    file.write(f"│ Total Mobil                                                            │ {total_mobil:<13} │\n")
                    file.write("├────────────────────────────────────────────────────────────────────────┼───────────────┤\n")
                    file.write(f"│ Total Pendapatan                                                       │ Rp{self.total_pendapatan:<12.2f}│\n")
                    file.write("╘════════════════════════════════════════════════════════════════════════╧═══════════════╛\n")

            return True, file_path

        except Exception as e:
            return False, str(e)

    # Memperbarui informasi transaksi ketika kendaraan keluar dari parkir.
    # Hanya memperbarui transaksi yang statusnya masih "Parkir", supaya kalau ada plat nomor
    # yang sama pernah parkir sebelumnya (sudah "Selesai"), transaksi lama itu tidak ikut
    # tertimpa secara keliru (perbaikan bug yang sudah diterapkan di versi GUI).
    def update_transaksi(self, plat_nomor, waktu_keluar, durasi, biaya):
        current = self.head

        while current:
            if current.plat_nomor == plat_nomor and current.status == "Parkir":
                current.waktu_keluar = waktu_keluar
                current.durasi = durasi
                current.biaya = biaya
                current.status = "Selesai"

                self.total_pendapatan += biaya
                self.total_kendaraan += 1
                return True, current

            current = current.next

        return False, None


# Class untuk mengelola antrian kendaraan yang masuk ke parkir
class AntrianParkir:
    def __init__(self):  # Inisialisasi antrian parkir dengan list kosong
        self.data = []

    def append(self, item):  # Menambahkan item ke akhir antrian
        self.data.append(item)

    def popleft(self):  # Menghapus dan mengembalikan item dari awal antrian
        return self.data.pop(0) if self.data else None

    def __len__(self):  # Mengembalikan panjang antrian
        return len(self.data)

    def __getitem__(self, index):  # Mengembalikan item pada indeks tertentu dalam antrian
        return self.data[index]

    def __bool__(self):  # Mengembalikan True jika antrian tidak kosong, False jika kosong
        return len(self.data) > 0


# Class untuk mengelola sistem parkir, termasuk antrian masuk, lantai parkir, dan riwayat transaksi
class SistemParkir:
    # Inisialisasi sistem parkir dengan jumlah lantai, kapasitas per lantai, dan tarif per jam untuk mobil dan motor
    def __init__(self, jumlah_lantai, kapasitas_per_lantai, tarif_per_jam_mb, tarif_per_jam_mt):
        self.lantai_parkir = [[] for _ in range(jumlah_lantai)]
        self.kapasitas_lantai = kapasitas_per_lantai
        self.antrian_masuk = AntrianParkir()
        self.riwayat = LinkedListRiwayat()
        self.tarif_mb = tarif_per_jam_mb
        self.tarif_mt = tarif_per_jam_mt

    # Menambahkan kendaraan (Mobil/Motor) ke antrian masuk.
    # Disatukan menjadi satu fungsi dengan parameter jenis, mengikuti pola di versi GUI
    # (dulu ada kendaraan_datang_mb & kendaraan_datang_mt yang terpisah).
    # Catatan: sesuai versi GUI, waktu masuk BELUM dicatat di sini — baru dicatat saat
    # kendaraan benar-benar diproses masuk ke lantai parkir (lihat proses_antrian).
    def kendaraan_datang(self, plat_nomor, jenis):
        self.antrian_masuk.append({'plat': plat_nomor, 'jenis': jenis})
        print(f"\n[+] {jenis} {plat_nomor} masuk ke antrian.")

    # Memproses antrian masuk dan menempatkan kendaraan ke lantai parkir yang tersedia.
    # Waktu masuk (untuk perhitungan durasi & biaya) dicatat di sini, tepat saat kendaraan
    # benar-benar mendapat slot parkir — bukan saat masih di antrian. Ini membuat perhitungan
    # durasi lebih akurat dan konsisten dengan versi GUI.
    def proses_antrian(self):
        if not self.antrian_masuk:
            return False, "Tidak ada kendaraan di antrian."

        for i in range(len(self.lantai_parkir)):
            if len(self.lantai_parkir[i]) < self.kapasitas_lantai:
                kendaraan = self.antrian_masuk.popleft()
                kendaraan["waktu_masuk"] = time.time()
                self.lantai_parkir[i].append(kendaraan)

                jam_masuk = time.strftime("%H:%M:%S", time.localtime(kendaraan["waktu_masuk"]))
                self.riwayat.tambah_transaksi(kendaraan["jenis"], kendaraan["plat"], jam_masuk)

                return True, f"Kendaraan {kendaraan['plat']} berhasil parkir di Lantai {i + 1}."

        return False, "Seluruh lantai parkir penuh! Kendaraan tertahan di antrian."

    # Mengeluarkan kendaraan (Mobil/Motor) dari parkir berdasarkan plat nomor,
    # menggunakan sistem LIFO (Last In First Out). Disatukan menjadi satu fungsi,
    # tarif otomatis mengikuti jenis kendaraan yang tersimpan (mengikuti pola versi GUI;
    # dulu ada kendaraan_keluar_mb & kendaraan_keluar_mt yang terpisah).
    def kendaraan_keluar(self, plat_nomor):
        for i in range(len(self.lantai_parkir)):
            lantai = self.lantai_parkir[i]

            if any(k['plat'] == plat_nomor for k in lantai):
                stack_sementara = []

                print(f"\nProses pengeluaran kendaraan {plat_nomor} dari Lantai {i+1} (Sistem LIFO):")
                while lantai[-1]['plat'] != plat_nomor:
                    k_pindah = lantai.pop()
                    stack_sementara.append(k_pindah)
                    print(f"  ⟫ Memindahkan sementara {k_pindah['jenis'].lower()} {k_pindah['plat']}...")

                k_keluar = lantai.pop()
                waktu_keluar = time.time()

                durasi_detik = max(1, int(waktu_keluar - k_keluar['waktu_masuk']))
                durasi_menit = durasi_detik / 60  # menit = jam untuk kebutuhan presentasi

                tarif = self.tarif_mb if k_keluar['jenis'] == 'Mobil' else self.tarif_mt
                if durasi_menit <= 1:
                    biaya_total = tarif
                else:
                    biaya_total = int(durasi_menit + 1) * tarif

                print(f"  ⟫ {k_keluar['jenis']} {k_keluar['plat']} KELUAR.")
                print(f"    Durasi Parkir : {durasi_menit:.2f} Jam")
                print(f"    Total Biaya   : Rp{biaya_total:.2f}")

                jam_keluar = time.strftime("%H:%M:%S", time.localtime(waktu_keluar))
                sukses, data_transaksi = self.riwayat.update_transaksi(
                    plat_nomor, jam_keluar, f"{durasi_menit:.2f} Jam", biaya_total
                )

                while stack_sementara:
                    k_kembali = stack_sementara.pop()
                    lantai.append(k_kembali)
                    print(f"  ⟪ Mengembalikan {k_kembali['jenis'].lower()} {k_kembali['plat']} ke posisinya.")

                return sukses, data_transaksi

        print(f"\n[-] Kendaraan dengan plat {plat_nomor} tidak ditemukan di area parkir.")
        return False, None

    # Menampilkan laporan real-time kapasitas parkir dan statistik kendaraan yang sedang menunggu di antrian.
    # Catatan: sesuai versi GUI, data antrian sekarang hanya menyimpan plat & jenis
    # (waktu masuk belum ada selama masih di antrian), sehingga kolom "Waktu Masuk"
    # pada tabel antrian dihapus supaya sesuai dengan struktur data yang sebenarnya.
    def laporan_realtime(self):
        print("\n" + "═"*40)
        print("  LAPORAN KAPASITAS PARKIR REAL-TIME")
        print("═"*40)

        print(f"[STATUS ANTRIAN] Menunggu: [{len(self.antrian_masuk)}] kendaraan")
        if self.antrian_masuk:
            print("╔════╦════════════╦═══════╗")
            print("║ No ║ Plat Nomor ║ Jenis ║")
            for i in range(len(self.antrian_masuk)):
                kendaraan = self.antrian_masuk[i]
                if i == 0:
                    print("╠════╬════════════╬═══════╣")
                else:   
                    print("╟────╫────────────╫───────╢")
                print(f"║ {i+1:<2} ║ {kendaraan['plat']:<10} ║ {kendaraan['jenis']:<5} ║")
            print("╚════╩════════════╩═══════╝")

        isi = sum(len(lantai) for lantai in self.lantai_parkir)
        kapasitas_total = self.kapasitas_lantai * len(self.lantai_parkir)
        print(f"\n[STATUS PARKIR] Terisi: [{isi}/{kapasitas_total}] kendaraan")
        print("╔═════════╦═════════════════╦═════════════════╦═════════════════╗")
        print(f"║ {'Lantai':<8}║     {'Slot 1':<11} ║     {'Slot 2':<11} ║     {'Slot 3':<11} ║")
        for i in range(len(self.lantai_parkir)):
            if i == 0:
                print("╠═════════╬═════════════════╬═════════════════╬═════════════════╣")
            else:
                print("╟─────────╫─────────────────╫─────────────────╫─────────────────╢")
            # plat_list = [f"{m['plat']} [{m['jenis']}]" for m in self.lantai_parkir[i]]
            plat_list = []

            for kendaraan in self.lantai_parkir[i]:
                if kendaraan["jenis"] == "Motor":
                    kode = "Mtr"
                elif kendaraan["jenis"] == "Mobil":
                    kode = "Mbl"
                else:
                    kode = "-"

                plat_list.append(f"{kendaraan['plat']} [{kode}]")

            print(
                f"║    {i+1:<5}║ "
                f"{plat_list[0] if len(plat_list) > 0 else '[Kosong]':<15} ║ "
                f"{plat_list[1] if len(plat_list) > 1 else '[Kosong]':<15} ║ "
                f"{plat_list[2] if len(plat_list) > 2 else '[Kosong]':<15} ║"
            )
        print("╚═════════╩═════════════════╩═════════════════╩═════════════════╝")
        input("\n»Tekan Enter untuk kembali ke menu utama...")

    # Menampilkan laporan riwayat transaksi parkir yang telah disimpan dalam linked list
    def laporan_riwayat(self):
        self.riwayat.tampilkan_riwayat()


# Main Program
def main():
    parkir = SistemParkir(jumlah_lantai=3, kapasitas_per_lantai=3, tarif_per_jam_mb=5000, tarif_per_jam_mt=2000)

    # Data dummy untuk demonstrasi
    parkir.kendaraan_datang("D 1212 AB", "Motor")
    parkir.proses_antrian()
    parkir.kendaraan_datang("D 3212 DF", "Mobil")
    parkir.proses_antrian()
    parkir.kendaraan_keluar("D 1212 AB")
    parkir.kendaraan_keluar("D 3212 DF")

    # Menu utama untuk interaksi pengguna
    while True:
        print("\n" + "═"*32)
        print("          MENU PARKIR")
        print("═"*32)
        print("\n╒══════════════════════════════╕")
        print("│===[ MENU PARKIR OTOMATIS ]===│")
        print("╞═══╤══════════════════════════╡")
        print("│ 1 │ Motor                    │")
        print("├───┼──────────────────────────┤")
        print("│ 2 │ Mobil                    │")
        print("├───┼──────────────────────────┤")
        print("│ 3 │ Proses Antrian           │")
        print("├───┼──────────────────────────┤")
        print("│ 4 │ Lihat Laporan Real-Time  │")
        print("├───┼──────────────────────────┤")
        print("│ 5 │ Lihat Riwayat            │")
        print("├───┼──────────────────────────┤")
        print("│ 0 │ Keluar Program           │")
        print("╘═══╧══════════════════════════╛\n")

        pilihan = input("»Pilih menu (0-5): ")

        if pilihan == '1':
            print("\n" + "═"*32)
            print("          MENU PARKIR")
            print("═"*32)
            print("\n ╒═══════════════════════════╕")
            print(" │===[ MENU PARKIR MOTOR ]===│")
            print(" ╞═══╤═══════════════════════╡")
            print(" │ 1 │ Motor Datang          │")
            print(" ├───┼───────────────────────┤")
            print(" │ 2 │ Motor Keluar          │")
            print(" ├───┼───────────────────────┤")
            print(" │ 0 │ Kembali               │")
            print(" ╘═══╧═══════════════════════╛\n")
            pilihan = input("»Pilih (0-2): ")
            if pilihan == '1':
                plat = input("»Masukkan Plat Nomor Motor: ").upper()
                parkir.kendaraan_datang(plat, "Motor")
            elif pilihan == '2':
                plat = input("»Masukkan Plat Nomor Motor yang akan keluar: ").upper()
                parkir.kendaraan_keluar(plat)
            elif pilihan == '0':
                continue
            else:
                print("Pilihan tidak valid!")
        elif pilihan == '2':
            print("\n" + "═"*32)
            print("          MENU PARKIR")
            print("═"*32)
            print("\n ╒═══════════════════════════╕")
            print(" │===[ MENU PARKIR MOBIL ]===│")
            print(" ╞═══╤═══════════════════════╡")
            print(" │ 1 │ Mobil Datang          │")
            print(" ├───┼───────────────────────┤")
            print(" │ 2 │ Mobil Keluar          │")
            print(" ├───┼───────────────────────┤")
            print(" │ 0 │ Kembali               │")
            print(" ╘═══╧═══════════════════════╛\n")
            pilihan = input("»Pilih (0-2): ")
            if pilihan == '1':
                plat = input("»Masukkan Plat Nomor Mobil: ").upper()
                parkir.kendaraan_datang(plat, "Mobil")
            elif pilihan == '2':
                plat = input("»Masukkan Plat Nomor Mobil yang akan keluar: ").upper()
                parkir.kendaraan_keluar(plat)
            elif pilihan == '0':
                continue
            else:
                print("Pilihan tidak valid!")
        elif pilihan == '3':
            sukses, pesan = parkir.proses_antrian()
            print(f"\n{'[SUKSES]' if sukses else '[!]'} {pesan}")
        elif pilihan == '4':
            parkir.laporan_realtime()
        elif pilihan == '5':
            parkir.laporan_riwayat()
            unduh = input("»Unduh Laporan Riwayat (Y/N): ").upper()
            if unduh == 'Y':
                sukses, hasil = parkir.riwayat.unduh_riwayat()
                if sukses:
                    print(f"\n[SUKSES] Riwayat berhasil disimpan.")
                    print(f"[⌂] Lokasi file : {hasil}")
                else:
                    print(f"\n[GAGAL] {hasil}")
            elif unduh == 'N':
                print("Laporan riwayat tidak diunduh.")
            else:
                print("Pilihan tidak valid!")
        elif pilihan == '0':
            print("Terima kasih telah menggunakan sistem simulasi parkir.")
            break
        else:
            print("Pilihan tidak valid!")


main()