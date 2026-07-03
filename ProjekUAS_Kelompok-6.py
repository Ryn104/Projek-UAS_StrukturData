import time # Berfungsi untuk mengatur waktu dan tanggal, serta menghitung durasi parkir
import os # Berfungsi untuk mengatur path file dan direktori

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

# class NodeRiwayat:
#     # Membuat node untuk linked list riwayat transaksi parkir
#     def __init__(self, jenis, plat_nomor, durasi, biaya):
#         self.jenis = jenis
#         self.plat_nomor = plat_nomor
#         self.durasi = durasi
#         self.biaya = biaya
#         self.next = None

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

    # Menambahkan transaksi baru ke dalam linked list
    # def tambah_transaksi(self, jenis, plat_nomor, durasi, biaya):
    #     node_baru = NodeRiwayat(jenis, plat_nomor, durasi, biaya)
    #     if not self.head:
    #         self.head = node_baru
    #     else:
    #         current = self.head
    #         while current.next:
    #             current = current.next
    #         current.next = node_baru
    #     self.total_pendapatan += biaya
    #     self.total_kendaraan += 1

    # Menampilkan riwayat transaksi parkir dalam format tabel
    def tampilkan_riwayat(self):
        print("\n" + "═"*90)
        print("                              RIWAYAT TRANSAKSI PARKIR HARIAN")
        print("═"*90 + "\n")
        print("╒════╤═══════╤════════════╤══════════╤══════════╤════════════╤═══════════╤═══════════════╕")
        print("│ No │ Jenis │ Plat Nomor │ Masuk    │ Keluar   │ Durasi     │ Biaya     │ Status        │")

        no = 1
        current = self.head
        total_motor = 0
        total_mobil = 0

        while current:
            if current.jenis == "Mobil":
                total_mobil += 1
            else:
                total_motor += 1
            if no == 1:
                print("╞════╪═══════╪════════════╪══════════╪══════════╪════════════╪═══════════╪═══════════════╡")
            else:
                print("├────┼───────┼────────────┼──────────┼──────────┼────────────┼───────────┼───────────────┤")

            biaya = "-" if current.biaya == "-" else f"Rp{current.biaya:.0f}"
            
            print(f"│ {no:<2} │ {current.jenis:<5} │ {current.plat_nomor:<10} │ {current.waktu_masuk:<8} │ {current.waktu_keluar:<8} │ {current.durasi:<10} │ {biaya:<9} │ {current.status:<13} │")
            
            no += 1
            current = current.next

        print("╞════╧═══════╧════════════╧══════════╧══════════╧════════════╧═══════════╪═══════════════╡")
        print(f"│ Total Motor                                                            │ {total_motor:<13} │")
        print("├────────────────────────────────────────────────────────────────────────┼───────────────┤")
        print(f"│ Total Mobil                                                            │ {total_mobil:<13} │")
        print("├────────────────────────────────────────────────────────────────────────┼───────────────┤")
        print(f"│ Total Pendapatan                                                       │ Rp{self.total_pendapatan:<12.2f}│")
        print("╘════════════════════════════════════════════════════════════════════════╧═══════════════╛\n")
    
    # Mengunduh riwayat transaksi parkir ke dalam file teks
    def unduh_riwayat(self):
        nama_file = f"Laporan_Parkir_{time.strftime('%Y-%m-%d')}.txt"
        lokasi_script = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(lokasi_script, nama_file)

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("\n" + "╔" + "═"*88 + "╗" + "\n")
                file.write("                              RIWAYAT TRANSAKSI PARKIR HARIAN\n")
                file.write("╚" + "═"*88 + "╝" + "\n\n")

                if not self.head:
                    file.write("Belum ada riwayat transaksi.\n")
                else:
                    file.write("╒════╤═══════╤════════════╤══════════╤══════════╤════════════╤═══════════╤═══════════════╕\n")
                    file.write("│ No │ Jenis │ Plat Nomor │ Masuk    │ Keluar   │ Durasi     │ Biaya     │ Status        │\n")

                    no = 1
                    current = self.head
                    total_motor = 0
                    total_mobil = 0

                    while current:
                        if current.jenis == "Mobil":
                            total_mobil += 1
                        else:
                            total_motor += 1
                        if no == 1:
                            file.write("╞════╪═══════╪════════════╪══════════╪══════════╪════════════╪═══════════╪═══════════════╡\n")
                        else:
                            file.write("├────┼───────┼────────────┼──────────┼──────────┼────────────┼───────────┼───────────────┤\n")

                        biaya = "-" if current.biaya == "-" else f"Rp{current.biaya:.0f}"

                        file.write(f"│ {no:<2} │ {current.jenis:<5} │ {current.plat_nomor:<10} │ {current.waktu_masuk:<8} │ {current.waktu_keluar:<8} │ {current.durasi:<10} │ {biaya:<9} │ {current.status:<13} │\n")
                        
                        no += 1
                        current = current.next

                    file.write("╞════╧═══════╧════════════╧══════════╧══════════╧════════════╧═══════════╪═══════════════╡\n")
                    file.write(f"│ Total Motor                                                            │ {total_motor:<13} │\n")
                    file.write("├────────────────────────────────────────────────────────────────────────┼───────────────┤\n")
                    file.write(f"│ Total Mobil                                                            │ {total_mobil:<13} │\n")
                    file.write("├────────────────────────────────────────────────────────────────────────┼───────────────┤\n")
                    file.write(f"│ Total Pendapatan                                                       │ Rp{self.total_pendapatan:<12.2f}│\n")
                    file.write("╘════════════════════════════════════════════════════════════════════════╧═══════════════╛\n")

            print(f"\n[SUKSES] Riwayat berhasil disimpan.")
            print(f"[⌂] Lokasi file : {file_path}")

        except Exception as e:
            print(f"\n[GAGAL] {e}")

    # Memperbarui informasi transaksi ketika kendaraan keluar dari parkir
    def update_transaksi(self, plat_nomor, waktu_keluar, durasi, biaya):
        current = self.head

        while current:
            if current.plat_nomor == plat_nomor:
                current.waktu_keluar = waktu_keluar
                current.durasi = durasi
                current.biaya = biaya
                current.status = "Selesai"

                self.total_pendapatan += biaya
                self.total_kendaraan += 1
                return

            current = current.next

# Class untuk mengelola antrian kendaraan yang masuk ke parkir
class AntrianParkir:
    def __init__(self): # Inisialisasi antrian parkir dengan list kosong
        self.data = []
    def append(self, item): # Menambahkan item ke akhir antrian
        self.data.append(item)
    def popleft(self): # Menghapus dan mengembalikan item dari awal antrian
        return self.data.pop(0)
    def __len__(self): # Mengembalikan panjang antrian
        return len(self.data)
    def __getitem__(self, index): # Mengembalikan item pada indeks tertentu dalam antrian
        return self.data[index]
    def __bool__(self): # Mengembalikan True jika antrian tidak kosong, False jika kosong
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

    # Menambahkan kendaraan mobil ke antrian masuk
    def kendaraan_datang_mb(self, plat_nomor):
        waktu_datang = time.time()
        self.antrian_masuk.append({'plat': plat_nomor, 'jenis': 'MB', 'waktu_masuk': waktu_datang})
        jam_masuk = time.strftime("%H:%M:%S", time.localtime(waktu_datang))
        self.riwayat.tambah_transaksi("Mobil", plat_nomor, jam_masuk)
        print(f"\n[+] Mobil {plat_nomor} masuk ke antrian.")

    # Menambahkan kendaraan motor ke antrian masuk
    def kendaraan_datang_mt(self, plat_nomor):
        waktu_datang = time.time() 
        self.antrian_masuk.append({'plat': plat_nomor, 'jenis': 'MT', 'waktu_masuk': waktu_datang})
        jam_masuk = time.strftime("%H:%M:%S", time.localtime(waktu_datang))
        self.riwayat.tambah_transaksi("Motor", plat_nomor, jam_masuk)
        print(f"\n[+] Motor {plat_nomor} masuk ke antrian.")

    # Memproses antrian masuk dan menempatkan kendaraan ke lantai parkir yang tersedia
    def proses_antrian(self):
        if not self.antrian_masuk:
            print("\n[-] Tidak ada kendaraan di antrian.")
            return
        
        for i in range(len(self.lantai_parkir)):
            if len(self.lantai_parkir[i]) < self.kapasitas_lantai:
                kendaraan = self.antrian_masuk.popleft()
                self.lantai_parkir[i].append(kendaraan)
                print(f"\n[SUKSES] Kendaraan {kendaraan['plat']} dari antrian berhasil parkir di Lantai {i + 1}.")
                return
            
        print("\n[!] Seluruh lantai parkir penuh! Kendaraan tertahan di antrian.")

    # Mengeluarkan kendaraan mobil dari parkir berdasarkan plat nomor, menggunakan sistem LIFO (Last In First Out)
    def kendaraan_keluar_mb(self, plat_nomor):
        for i in range(len(self.lantai_parkir)):
            lantai = self.lantai_parkir[i]
            
            if any(mobil['plat'] == plat_nomor for mobil in lantai):
                stack_sementara = []

                print(f"\nProses pengeluaran kendaraan {plat_nomor} dari Lantai {i+1} (Sistem LIFO):")
                while lantai[-1]['plat'] != plat_nomor:
                    mobil_pindah = lantai.pop()
                    stack_sementara.append(mobil_pindah)
                    print(f"  ⟫ Memindahkan sementara mobil {mobil_pindah['plat']}...")
                
                mobil_keluar = lantai.pop()
                waktu_keluar = time.time()
                
                durasi_detik = max(1, int(waktu_keluar - mobil_keluar['waktu_masuk']))
                durasi_menit = durasi_detik / 60 # menit = jam untuk kebutuhan presentasi
                # durasi_jam = durasi_menit / 60  
                if durasi_menit <= 1:
                    biaya_total = self.tarif_mb
                else:
                    biaya_total = int(durasi_menit+1) * self.tarif_mb
                # biaya_total = durasi_menit * self.tarif
                
                print(f"  ⟫ Mobil {mobil_keluar['plat']} KELUAR.")
                print(f"    Durasi Parkir : {durasi_menit:.2f} Jam")
                print(f"    Total Biaya   : Rp{biaya_total:.2f}")

                jam_keluar = time.strftime("%H:%M:%S", time.localtime(waktu_keluar))

                self.riwayat.update_transaksi(plat_nomor, jam_keluar, f"{durasi_menit:.2f} Jam", biaya_total)
                
                while stack_sementara:
                    mobil_kembali = stack_sementara.pop()
                    lantai.append(mobil_kembali)
                    print(f"  ⟪ Mengembalikan mobil {mobil_kembali['plat']} ke posisinya.")
                return

        print(f"\n[-] Kendaraan dengan plat {plat_nomor} tidak ditemukan di area parkir.")
    
    # Mengeluarkan kendaraan motor dari parkir berdasarkan plat nomor, menggunakan sistem LIFO (Last In First Out)
    def kendaraan_keluar_mt(self, plat_nomor):
        for i in range(len(self.lantai_parkir)):
            lantai = self.lantai_parkir[i]
            
            if any(motor['plat'] == plat_nomor for motor in lantai):
                stack_sementara = []
                
                print(f"\nProses pengeluaran kendaraan {plat_nomor} dari Lantai {i+1} (Sistem LIFO):")
                while lantai[-1]['plat'] != plat_nomor:
                    motor_pindah = lantai.pop()
                    stack_sementara.append(motor_pindah)
                    print(f"  ⟫ Memindahkan sementara motor {motor_pindah['plat']}...")
                
                motor_keluar = lantai.pop()
                waktu_keluar = time.time()
                
                durasi_detik = max(1, int(waktu_keluar - motor_keluar['waktu_masuk']))
                durasi_menit = durasi_detik / 60 # menit = jam untuk kebutuhan presentasi
                # durasi_jam = durasi_menit / 60  
                if durasi_menit <= 1:
                    biaya_total = self.tarif_mt
                else:
                    biaya_total = int(durasi_menit+1)  * self.tarif_mt
                # biaya_total = durasi_menit * self.tarif
                
                print(f"  ⟫ Motor {motor_keluar['plat']} KELUAR.")
                print(f"    Durasi Parkir : {durasi_menit:.2f} Jam")
                print(f"    Total Biaya   : Rp{biaya_total:.2f}")
                
                # self.riwayat.tambah_transaksi("Motor", plat_nomor, durasi_menit, biaya_total)

                jam_keluar = time.strftime("%H:%M:%S", time.localtime(waktu_keluar))

                self.riwayat.update_transaksi(plat_nomor, jam_keluar, f"{durasi_menit:.2f} Jam", biaya_total)
                
                while stack_sementara:
                    motor_kembali = stack_sementara.pop()
                    lantai.append(motor_kembali)
                    print(f"  ⟪ Mengembalikan motor {motor_kembali['plat']} ke posisinya.")
                return

        print(f"\n[-] Kendaraan dengan plat {plat_nomor} tidak ditemukan di area parkir.")

    # Menampilkan laporan real-time kapasitas parkir dan statistik kendaraan yang sedang menunggu di antrian
    def laporan_realtime(self):
        print("\n" + "═"*64)
        print("         LAPORAN KAPASITAS PARKIR REAL-TIME & STATISTIK")
        print("═"*64)
        
        print(f"[STATUS ANTRIAN] Menunggu: [{len(self.antrian_masuk)}] kendaraan")
        if self.antrian_masuk:
            print("╔════╦════════════╦═══════╦═════════════╗")
            print("║ No ║ Plat Nomor ║ Jenis ║ Waktu Masuk ║")
            for i in range(len(self.antrian_masuk)):
                kendaraan = self.antrian_masuk[i]
                jam_masuk = time.strftime("%H:%M", time.localtime(kendaraan["waktu_masuk"]))
                if i == 0:
                    print("╠════╬════════════╬═══════╬═════════════╣")
                else:
                    print("╟────╫────────────╫───────╫─────────────╢")
                print(f"║ {i+1:<2} ║ {kendaraan['plat']:<10} ║ {'Mobil' if kendaraan['jenis']=='MB' else 'Motor'} ║ {jam_masuk:<11} ║")
            print("╚════╩════════════╩═══════╩═════════════╝")
        
        isi = len(self.lantai_parkir[0]) + len(self.lantai_parkir[1]) + len(self.lantai_parkir[2])
        kapasitas_total = self.kapasitas_lantai * len(self.lantai_parkir)
        print(f"\n[STATUS PARKIR] Terisi: [{isi}/{kapasitas_total}] kendaraan")
        print("╔═════════╦═════════════════╦═════════════════╦═════════════════╗")
        print(f"║ {'Lantai':<8}║     {'Slot 1':<11} ║     {'Slot 2':<11} ║     {'Slot 3':<11} ║")
        for i in range(len(self.lantai_parkir)):
            if i == 0:
                print("╠═════════╬═════════════════╬═════════════════╬═════════════════╣")
            else:
                print("╟─────────╫─────────────────╫─────────────────╫─────────────────╢")
            plat_list = [f"{m['plat']} [{m['jenis']}]" for m in self.lantai_parkir[i]]
            print(f"║    {i+1:<5}║ {plat_list[0] if len(plat_list) > 0 else '[Kosong]':<15} ║ {plat_list[1] if len(plat_list) > 1 else '[Kosong]':<15} ║ {plat_list[2] if len(plat_list) > 2 else '[Kosong]':<15} ║")
        print("╚═════════╩═════════════════╩═════════════════╩═════════════════╝")
        input("\n»Tekan Enter untuk kembali ke menu utama...")

    # Menampilkan laporan riwayat transaksi parkir yang telah disimpan dalam linked list
    def laporan_riwayat(self):
        self.riwayat.tampilkan_riwayat()


# Main Program Tanpa Proses Antrian
def main():
    parkir = SistemParkir(jumlah_lantai=3, kapasitas_per_lantai=3, tarif_per_jam_mb=5000, tarif_per_jam_mt=2000)
    
    # Data dummy untuk 
    parkir.kendaraan_datang_mt("D 1212 AB")
    parkir.proses_antrian()
    parkir.kendaraan_datang_mb("D 3212 DF")
    parkir.proses_antrian()
    parkir.kendaraan_keluar_mt("D 1212 AB")
    parkir.kendaraan_keluar_mb("D 3212 DF")

    # Menu utama untuk interaksi pengguna
    while True:
        print("\n" + "═"*32)
        print("          MENU PARKIR")
        print( "═"*32)
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
            print( "═"*32)
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
                parkir.kendaraan_datang_mt(plat)
            elif pilihan == '2':
                plat = input("»Masukkan Plat Nomor Motor yang akan keluar: ").upper()
                parkir.kendaraan_keluar_mt(plat)
            elif pilihan == '0':
                continue
            else:
                print("Pilihan tidak valid!")
        elif pilihan == '2':
            print("\n" + "═"*32)
            print("          MENU PARKIR")
            print( "═"*32)
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
                parkir.kendaraan_datang_mb(plat)
            elif pilihan == '2':
                plat = input("»Masukkan Plat Nomor Mobil yang akan keluar: ").upper()
                parkir.kendaraan_keluar_mb(plat)
            elif pilihan == '0':
                continue
            else:
                print("Pilihan tidak valid!")
        elif pilihan == '3':
            parkir.proses_antrian()
        elif pilihan == '4':
            parkir.laporan_realtime()
        elif pilihan == '5':
            parkir.laporan_riwayat()
            unduh = input("»Unduh Laporan Riwayat (Y/N): ").upper()
            if unduh == 'Y':
                parkir.riwayat.unduh_riwayat()
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