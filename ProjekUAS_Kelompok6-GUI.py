import time
import os
import tkinter as tk
from tkinter import ttk, messagebox

class NodeRiwayat:
    # Membuat data transaksi kendaraan parkir
    def __init__(self, jenis, plat_nomor, waktu_masuk):
        self.jenis = jenis
        self.plat_nomor = plat_nomor
        self.waktu_masuk = waktu_masuk
        self.waktu_keluar = "-"
        self.durasi = "-"
        self.biaya = "-"
        self.status = "Parkir"
        self.next = None

class LinkedListRiwayat:
    # Membuat linked list riwayat parkir
    def __init__(self):
        self.head = None
        self.total_pendapatan = 0
        self.total_kendaraan = 0

    # Menambahkan transaksi baru ke riwayat
    def tambah_transaksi(self, jenis, plat_nomor, waktu_masuk):
        node_baru = NodeRiwayat(jenis, plat_nomor, waktu_masuk)
        if self.head is None:
            self.head = node_baru
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node_baru

    # Mengambil seluruh data riwayat parkir
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

    # Menghitung jumlah mobil dan motor yang masih parkir
    def get_statistik(self):
        total_mobil = 0
        total_motor = 0
        current = self.head
        while current:
            if current.jenis == "Mobil": total_mobil += 1
            else: total_motor += 1
            current = current.next
        return total_mobil, total_motor
    
    # Mengunduh riwayat transaksi ke file TXT
    def unduh_riwayat(self):
        nama_file = f"Laporan_Parkir_{time.strftime('%Y-%m-%d')}.txt"
        lokasi_script = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(lokasi_script, nama_file)
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("="*90 + "\n")
                file.write("                             RIWAYAT TRANSAKSI PARKIR HARIAN\n")
                file.write("="*90 + "\n\n")
                data = self.get_semua_data()
                total_mobil = 0
                total_motor = 0
                if not data:
                    file.write("Belum ada riwayat transaksi.\n")
                else:
                    file.write(f" {'No':<2} | {'Jenis':<6} | {'Plat Nomor':<12} | {'Masuk':<8} | {'Keluar':<8} | {'Durasi':<14} | {'Biaya':<10} | {'Status':<10}\n")
                    file.write("-" * 90 + "\n")
                    for baris in data:
                        if baris[1] == "Mobil":
                            total_mobil += 1
                        else:
                            total_motor += 1
                        file.write(f" {baris[0]:<2} | {baris[1]:<6} | {baris[2]:<12} | {baris[3]:<8} | {baris[4]:<8} | {baris[5]:<14} | {baris[6]:<10} | {baris[7]:<10}\n")
                    file.write("-" * 90 + "\n")
                    file.write(f"Total Mobil Parkir : {total_mobil}\n")
                    file.write(f"Total Motor Parkir : {total_motor}\n")
                    file.write(f"Total Pendapatan : Rp{self.total_pendapatan:.2f}\n")
            return True, file_path
        except Exception as e:
            return False, str(e)

    # Memperbarui data kendaraan saat keluar parkir
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

class AntrianParkir:
    def __init__(self): # Membuat struktur antrian kendaraan
        self.data = []
    def append(self, item): self.data.append(item) # Menambahkan kendaraan ke antrian
    def popleft(self): return self.data.pop(0) if self.data else None # Mengambil kendaraan pertama dari antrian
    def __len__(self): return len(self.data) # Mengembalikan jumlah kendaraan dalam antrian
    def __getitem__(self, index): return self.data[index] # Mengakses data antrian berdasarkan indeks
    def __bool__(self): return len(self.data) > 0 # Mengecek apakah antrian masih berisi data

class SistemParkir:
    # Menginisialisasi sistem parkir
    def __init__(self, jumlah_lantai, kapasitas_per_lantai, tarif_per_jam_mb, tarif_per_jam_mt):
        self.lantai_parkir = [[] for _ in range(jumlah_lantai)]
        self.kapasitas_lantai = kapasitas_per_lantai
        self.antrian_masuk = AntrianParkir()
        self.riwayat = LinkedListRiwayat()
        self.tarif_mb = tarif_per_jam_mb
        self.tarif_mt = tarif_per_jam_mt

    # Menambahkan kendaraan ke antrian masuk
    def kendaraan_datang(self, plat_nomor, jenis):
        self.antrian_masuk.append({
            'plat': plat_nomor,
            'jenis': jenis
        })

    # Memproses kendaraan dari antrian ke slot parkir
    def proses_antrian(self):
        if not self.antrian_masuk:
            return False, "Tidak ada kendaraan di antrian."

        for i in range(len(self.lantai_parkir)):
            if len(self.lantai_parkir[i]) < self.kapasitas_lantai:
                kendaraan = self.antrian_masuk.popleft()
                kendaraan["waktu_masuk"] = time.time()

                self.lantai_parkir[i].append(kendaraan)

                jam_masuk = time.strftime(
                    "%H:%M:%S",
                    time.localtime(kendaraan["waktu_masuk"])
                )

                self.riwayat.tambah_transaksi(
                    kendaraan["jenis"],
                    kendaraan["plat"],
                    jam_masuk
                )

                return True, f"Kendaraan {kendaraan['plat']} parkir di Lantai {i + 1}."

        return False, "Seluruh lantai parkir penuh! Kendaraan tertahan di antrian."

    # Memproses kendaraan keluar dan menghitung biaya parkir
    def kendaraan_keluar(self, plat_nomor):
        for i in range(len(self.lantai_parkir)):
            lantai = self.lantai_parkir[i]
            if any(kendaraan['plat'] == plat_nomor for kendaraan in lantai):
                stack_sementara = []
                while lantai[-1]['plat'] != plat_nomor:
                    stack_sementara.append(lantai.pop())

                k_keluar = lantai.pop()
                waktu_keluar = time.time()
                durasi_detik = max(1, int(waktu_keluar - k_keluar['waktu_masuk']))
                jam = durasi_detik // 60  
                menit = durasi_detik % 60   
                durasi = f"{jam} Jam {menit} Menit"
                # durasi_menit = durasi_detik / 60

                tarif = self.tarif_mb if k_keluar['jenis'] == 'Mobil' else self.tarif_mt
                if jam < 1:
                     biaya_total = tarif
                else:
                    biaya_total = tarif * jam + ((tarif * 0.5) if menit > 30 else 0) 
                # if durasi_menit <= 1:
                #     biaya_total = tarif
                # else:
                #     biaya_total = int(durasi_menit+1) * tarif

                jam_keluar = time.strftime("%H:%M:%S", time.localtime(waktu_keluar))
                _, data_transaksi = self.riwayat.update_transaksi(plat_nomor, jam_keluar, durasi, biaya_total)
                # _, data_transaksi = self.riwayat.update_transaksi(plat_nomor, jam_keluar, f"{durasi_menit:.2f} Jam", biaya_total)

                while stack_sementara:
                    lantai.append(stack_sementara.pop())
                return True, data_transaksi

        return False, None

WARNA = {
    "bg": "#F3F4F6",
    "primary": "#0D47A1",
    "merah": "#D32F2F",
    "hijau": "#2E7D32",
    "hijau_muda": "#E8F5E9",
    "oranye": "#F57C00",
    "oranye_muda": "#FFF3E0",
    "biru_muda": "#E3F2FD",
    "ungu": "#7B1FA2",
    "ungu_muda": "#F3E5F5",
    "kosong": "#E0E0E0",
    "putih": "#FFFFFF",
    "abu_teks": "#6B7280",
    "border": "#E5E7EB",
}

FONT_JUDUL = ("Segoe UI", 18, "bold")
FONT_SUBJUDUL = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 10)
FONT_LABEL_BOLD = ("Segoe UI", 11, "bold")
FONT_ANGKA = ("Segoe UI", 22, "bold")
FONT_MENU = ("Segoe UI", 11)

# Menggambar persegi panjang dengan sudut membulat
def buat_rounded_rect(canvas, x1, y1, x2, y2, radius=18, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class RoundedCard(tk.Frame):
    # Membuat card dengan sudut membulat
    def __init__(self, parent, bg_color="white", radius=16, **kwargs):
        super().__init__(parent, bg=WARNA["bg"], **kwargs)
        self.bg_color = bg_color
        self.radius = radius
        self.canvas = tk.Canvas(self, bg=WARNA["bg"], highlightthickness=0, width=1, height=1)
        self.canvas.pack(fill="both", expand=True)
        self.inner = tk.Frame(self.canvas, bg=bg_color)
        self.canvas.bind("<Configure>", self._redraw)

    # Menggambar ulang tampilan card saat ukuran berubah
    def _redraw(self, event=None):
        self.canvas.delete("bg")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 4 or h < 4:
            return
        buat_rounded_rect(self.canvas, 1, 1, w - 1, h - 1, radius=self.radius,
                           fill=self.bg_color, outline=WARNA["border"], tags="bg")
        pad = max(self.radius // 2, 8)
        self.canvas.delete("inner_win")
        self.canvas.create_window(pad, pad, anchor="nw", window=self.inner,
                                   width=w - 2 * pad, height=h - 2 * pad, tags="inner_win")

# Membuat ikon berbentuk lingkaran
def buat_icon_bulat(parent, diameter, warna_lingkaran, warna_icon, icon_char, bg_parent="white"):
    canvas = tk.Canvas(parent, width=diameter, height=diameter, bg=bg_parent, highlightthickness=0)
    canvas.create_oval(1, 1, diameter - 1, diameter - 1, fill=warna_lingkaran, outline="")
    canvas.create_text(diameter / 2, diameter / 2, text=icon_char,
                        font=("Segoe UI Emoji", int(diameter * 0.40)), fill=warna_icon)
    return canvas


class AplikasiParkirGUI(tk.Tk):
    # Menginisialisasi aplikasi GUI parkir
    def __init__(self):
        super().__init__()
        self.title("Smart Parking System")
        self.geometry("1360x820")
        self.configure(bg=WARNA["bg"])
        try:
            self.state('zoomed')
        except tk.TclError:
            pass

        self.parkir = SistemParkir(jumlah_lantai=3, kapasitas_per_lantai=3,
                                    tarif_per_jam_mb=5000, tarif_per_jam_mt=2000)
        # self.parkir = SistemParkir(jumlah_lantai=3, kapasitas_per_lantai=3,
        #                             tarif_per_jam_mb=5000, tarif_per_jam_mt=2000)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'),
                              background=WARNA["primary"], foreground="white", relief="flat")
        self.style.map("Treeview.Heading", background=[("active", WARNA["primary"])])
        self.style.configure("Treeview", font=('Segoe UI', 10), rowheight=28,
                              background="white", fieldbackground="white", borderwidth=0)
        self.style.configure("TEntry", padding=6)

        self.setup_ui()
        self.update_waktu()
        self.refresh_dashboard()

    # Menyusun seluruh tampilan utama aplikasi
    def setup_ui(self):
        self.main_content = tk.Frame(self, bg=WARNA["bg"])
        self.main_content.pack(side="right", fill="both", expand=True)

        self.setup_header()
        self.setup_cards()
        self.setup_middle_section()
        self.setup_table_section()

    # =========================== BAGIAN ATAS ===========================
    # Membuat bagian header aplikasi
    def setup_header(self):
        header_frame = tk.Frame(self.main_content, bg=WARNA["bg"])
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        kiri = tk.Frame(header_frame, bg=WARNA["bg"])
        kiri.pack(side="left")
        tk.Label(kiri, text="Sistem Parkir Otomatis", font=FONT_JUDUL, bg=WARNA["bg"]).pack(anchor="w")
        tk.Label(kiri, text="Ringkasan informasi area parkir", font=FONT_SUBJUDUL,
                 bg=WARNA["bg"], fg=WARNA["abu_teks"]).pack(anchor="w")

        kanan = tk.Frame(header_frame, bg=WARNA["bg"])
        kanan.pack(side="right")

        jam_box = tk.Frame(kanan, bg="white", padx=12, pady=6, highlightbackground=WARNA["border"],
                            highlightthickness=1)
        jam_box.pack(side="right")
        self.lbl_waktu = tk.Label(jam_box, text="", font=("Segoe UI", 10), bg="white", justify="right")
        self.lbl_waktu.pack()

    # Membuat card informasi ringkasan di bagian atas aplikasi
    def setup_cards(self):
        self.cards_frame = tk.Frame(self.main_content, bg=WARNA["bg"])
        self.cards_frame.pack(fill="x", padx=25, pady=8)
        for i in range(4):
            self.cards_frame.columnconfigure(i, weight=1)

        self.lbl_val_mobil = self.buat_card(self.cards_frame, "Total Mobil", "0",
                                             "Kendaraan parkir", " 🚗 ", WARNA["biru_muda"],
                                             WARNA["primary"], 0)
        self.lbl_val_motor = self.buat_card(self.cards_frame, "Total Motor", "0",
                                             "Kendaraan parkir", " 🏍️ ", WARNA["hijau_muda"],
                                             WARNA["hijau"], 1)
        self.lbl_val_pendapatan = self.buat_card(self.cards_frame, "Total Pendapatan", "Rp0",
                                                  "Hari ini", " 💰 ", WARNA["oranye_muda"],
                                                  WARNA["oranye"], 2)
        self.lbl_val_slot = self.buat_card(self.cards_frame, "Slot Tersedia", "9 / 9",
                                            "Slot kosong", " 🅿️ ", WARNA["ungu_muda"],
                                            WARNA["ungu"], 3)

    # Membuat card informasi parkir
    def buat_card(self, parent, judul, nilai_awal, subjudul, icon, warna_bg_icon, warna_fg_icon, col):
        card = RoundedCard(parent, bg_color="white", radius=20, height=120)
        card.grid(row=0, column=col, sticky="ew", padx=8 if 0 < col < 3 else (0, 8) if col == 0 else (8, 0))
        card.pack_propagate(False)

        watermark = tk.Label(card.inner, text=icon, font=("Segoe UI Emoji", 46),
                              fg="#EEF1F8", bg="white")
        watermark.place(relx=1.0, x=18, rely=0.5, anchor="e")

        card.inner.grid_rowconfigure(0, weight=1)
        card.inner.grid_columnconfigure(0, weight=1)

        pembungkus = tk.Frame(card.inner, bg="white")
        pembungkus.grid(row=0, column=0, sticky="w", padx=(4, 0))

        isi = tk.Frame(pembungkus, bg="white")
        isi.pack()

        icon_bulat = buat_icon_bulat(isi, 64, warna_bg_icon, warna_fg_icon, icon, bg_parent="white")
        icon_bulat.grid(row=0, column=0, rowspan=3, sticky="w", padx=(14, 24))

        tk.Label(isi, text=judul, font=FONT_LABEL, fg=WARNA["abu_teks"], bg="white",
                 anchor="w").grid(row=0, column=1, sticky="w")
        lbl_val = tk.Label(isi, text=nilai_awal, font=FONT_ANGKA, bg="white", anchor="w")
        lbl_val.grid(row=1, column=1, sticky="w")
        tk.Label(isi, text=subjudul, font=("Segoe UI", 8), fg=WARNA["abu_teks"], bg="white",
                 anchor="w").grid(row=2, column=1, sticky="w")
        return lbl_val

    # =========================== BAGIAN TENGAH ===========================
    # Membuat bagian status parkir dan form input
    def setup_middle_section(self):
        mid_frame = tk.Frame(self.main_content, bg=WARNA["bg"])
        mid_frame.pack(fill="x", padx=25, pady=8)

        # Status Parkir
        status_card = RoundedCard(mid_frame, bg_color="white", radius=16, height=270)
        status_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        status_card.pack_propagate(False)

        header_status = tk.Frame(status_card.inner, bg="white")
        header_status.pack(fill="x", pady=(0, 10))
        tk.Label(header_status, text="Status Parkir", font=FONT_LABEL_BOLD, bg="white").pack(side="left")

        legenda = tk.Frame(header_status, bg="white")
        legenda.pack(side="right")
        for warna, teks in [(WARNA["primary"], "Mobil"), (WARNA["hijau"], "Motor"), (WARNA["kosong"], "Kosong")]:
            dot_frame = tk.Frame(legenda, bg="white")
            dot_frame.pack(side="left", padx=6)
            tk.Label(dot_frame, text="●", fg=warna, bg="white", font=("Segoe UI", 10)).pack(side="left")
            tk.Label(dot_frame, text=teks, fg=WARNA["abu_teks"], bg="white", font=("Segoe UI", 9)).pack(side="left")

        self.frame_lantai = tk.Frame(status_card.inner, bg="white")
        self.frame_lantai.pack(fill="both", expand=True)

        # Form Kendaraan Masuk
        form_masuk_card = RoundedCard(mid_frame, bg_color="white", radius=16, width=210, height=270)
        form_masuk_card.pack(side="left", fill="y", padx=8)
        form_masuk_card.pack_propagate(False)
        self.buat_header_panel(form_masuk_card.inner, "🚗", "Kendaraan Masuk", WARNA["primary"], WARNA["biru_muda"])

        tk.Label(form_masuk_card.inner, text="Jenis Kendaraan", bg="white", font=FONT_LABEL).pack(anchor="w", pady=(8, 0))
        self.var_jenis = tk.StringVar(value="Mobil")
        radio_frame = tk.Frame(form_masuk_card.inner, bg="white")
        radio_frame.pack(anchor="w")
        tk.Radiobutton(radio_frame, text="Mobil", variable=self.var_jenis, value="Mobil",
                        bg="white", font=FONT_LABEL).pack(side="left", padx=(0, 10))
        tk.Radiobutton(radio_frame, text="Motor", variable=self.var_jenis, value="Motor",
                        bg="white", font=FONT_LABEL).pack(side="left")

        tk.Label(form_masuk_card.inner, text="Plat Nomor", bg="white", font=FONT_LABEL).pack(anchor="w", pady=(10, 0))
        self.ent_masuk = ttk.Entry(form_masuk_card.inner, font=("Segoe UI", 10))
        self.ent_masuk.pack(fill="x", pady=(5, 48))

        btn_add = tk.Button(form_masuk_card.inner, text="+  Tambahkan", bg=WARNA["primary"], fg="white",
                             relief="flat", font=("Segoe UI", 10, "bold"), command=self.action_masuk, activeforeground="white", cursor="hand2")
        btn_add.pack(fill="x", pady=5, ipady=6)

        # Form Kendaraan Keluar
        form_keluar_card = RoundedCard(mid_frame, bg_color="white", radius=16, width=210, height=270)
        form_keluar_card.pack(side="left", fill="y", padx=8)
        form_keluar_card.pack_propagate(False)
        self.buat_header_panel(form_keluar_card.inner, "➡️", "Kendaraan Keluar", WARNA["merah"], "#FDECEA")

        tk.Label(form_keluar_card.inner, text="Cari Plat Nomor", bg="white", font=FONT_LABEL).pack(anchor="w", pady=(8, 0))
        self.ent_keluar = ttk.Entry(form_keluar_card.inner, font=("Segoe UI", 10))
        self.ent_keluar.pack(fill="x", pady=(5, 108))

        btn_out = tk.Button(form_keluar_card.inner, text="- Keluarkan", bg=WARNA["merah"], fg="white",
                             relief="flat", font=("Segoe UI", 10, "bold"), command=self.action_keluar,
                             activebackground="#B71C1C", activeforeground="white", cursor="hand2")
        btn_out.pack(fill="x", pady=5, ipady=6)

        # Proses Antrian
        antrian_card = RoundedCard(mid_frame, bg_color="white", radius=16, width=230, height=270)
        antrian_card.pack(side="left", fill="y", padx=(8, 0))
        antrian_card.pack_propagate(False)
        self.buat_header_panel(antrian_card.inner, "👥", "Proses Antrian", WARNA["oranye"], WARNA["oranye_muda"])

        self.list_antrian = tk.Listbox(antrian_card.inner, height=6, relief="flat", bg="#F9FAFB",
                                        font=("Segoe UI", 9), highlightthickness=0, bd=0)
        self.list_antrian.pack(fill="both", expand=True, pady=(8, 5))

        btn_proses = tk.Button(antrian_card.inner, text="→  Proses Berikutnya", bg=WARNA["oranye"], fg="white",
                                relief="flat", font=("Segoe UI", 10, "bold"), command=self.action_proses,
                                activebackground="#E65100", activeforeground="white", cursor="hand2")
        btn_proses.pack(fill="x", pady=5, ipady=6)

    # Membuat header untuk setiap panel
    def buat_header_panel(self, parent, icon, teks, warna_fg, warna_bg):
        f = tk.Frame(parent, bg="white")
        f.pack(fill="x")
        icon_lbl = tk.Label(f, text=icon, font=("Segoe UI", 11), bg=warna_bg, fg=warna_fg, width=3, height=1)
        icon_lbl.pack(side="left")
        tk.Label(f, text=f"  {teks}", font=FONT_LABEL_BOLD, fg=warna_fg, bg="white").pack(side="left")

    # Membuat tampilan slot parkir
    def buat_slot(self, parent, nomor, data, row):
        if data:
            warna_bg = WARNA["primary"] if data['jenis'] == 'Mobil' else WARNA["hijau"]
            warna_teks = "white"
            icon = "🚗" if data['jenis'] == 'Mobil' else "🏍️"
            plat = data['plat']
            jenis = data['jenis']
        else:
            warna_bg = WARNA["kosong"]
            warna_teks = "#9CA3AF"
            icon = " "
            plat = " "
            jenis = " "

        slot = tk.Frame(parent, bg=warna_bg)
        slot.grid(row=row, column=0, sticky="nsew", padx=10, pady=5)

        badge = tk.Label(slot, text=str(nomor), font=("Segoe UI", 9, "bold"), bg="white",
                          fg=warna_bg if data else "#9CA3AF", width=2, height=1)
        badge.place(x=6, y=6)

        isi = tk.Frame(slot, bg=warna_bg)
        isi.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(isi, text=icon, font=("Segoe UI", 12), bg=warna_bg, fg=warna_teks).pack(side="left", padx=(0, 6))
        teks_frame = tk.Frame(isi, bg=warna_bg)
        teks_frame.pack(side="left")
        tk.Label(teks_frame, text=plat, font=("Segoe UI", 9, "bold"), bg=warna_bg, fg=warna_teks).pack(anchor="w")
        tk.Label(teks_frame, text=jenis, font=("Segoe UI", 8), bg=warna_bg, fg=warna_teks).pack(anchor="w")

    # =========================== BAGIAN BAWAH ===========================
    # Membuat tabel riwayat transaksi
    def setup_table_section(self):
        bottom_frame = RoundedCard(self.main_content, bg_color="white", radius=16)
        bottom_frame.pack(fill="both", expand=True, padx=25, pady=(8, 20))

        header_tbl = tk.Frame(bottom_frame.inner, bg="white")
        header_tbl.pack(fill="x")
        tk.Label(header_tbl, text="Riwayat Transaksi", font=FONT_LABEL_BOLD, bg="white").pack(side="left")
        btn_unduh = tk.Button(header_tbl, text="⬇  Unduh Laporan", bg="white", fg=WARNA["primary"],
                               relief="solid", bd=1, font=("Segoe UI", 9, "bold"), cursor="hand2",
                               command=self.action_unduh, padx=10, pady=4)
        btn_unduh.pack(side="right")

        kolom = ("No", "Jenis", "Plat Nomor", "Masuk", "Keluar", "Durasi", "Biaya", "Status")
        self.tree = ttk.Treeview(bottom_frame.inner, columns=kolom, show="headings")
        lebar_kolom = [40, 80, 130, 90, 90, 110, 100, 100]
        for i, col in enumerate(kolom):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=lebar_kolom[i], anchor="center")

        self.tree.tag_configure("selesai", foreground=WARNA["hijau"])
        self.tree.tag_configure("parkir", foreground=WARNA["oranye"])
        self.tree.tag_configure("evenrow", background="#FAFAFA")
        self.tree.tag_configure("oddrow", background="white")

        scroll = ttk.Scrollbar(bottom_frame.inner, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        scroll.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, pady=10)

    # Memperbarui jam pada aplikasi setiap detik
    def update_waktu(self):
        waktu_skrg = time.strftime("%H:%M:%S\n%A, %d %b %Y")
        self.lbl_waktu.config(text=waktu_skrg)
        self.after(1000, self.update_waktu)

    # Memperbarui seluruh tampilan dashboard
    def refresh_dashboard(self):
        total_mobil, total_motor = self.parkir.riwayat.get_statistik()
        isi_total = sum(len(lantai) for lantai in self.parkir.lantai_parkir)
        kapasitas_max = self.parkir.kapasitas_lantai * len(self.parkir.lantai_parkir)

        self.lbl_val_mobil.config(text=str(total_mobil))
        self.lbl_val_motor.config(text=str(total_motor))
        self.lbl_val_pendapatan.config(text=f"Rp{self.parkir.riwayat.total_pendapatan:,.0f}")
        self.lbl_val_slot.config(text=f"{kapasitas_max - isi_total} / {kapasitas_max}")

        for widget in self.frame_lantai.winfo_children():
            widget.destroy()

        for i, lantai in enumerate(self.parkir.lantai_parkir):
            f_lantai = tk.Frame(self.frame_lantai, bg="#F9FAFB", highlightbackground=WARNA["border"],
                                 highlightthickness=1)
            f_lantai.pack(side="left", fill="both", expand=True, padx=5)
            f_lantai.grid_columnconfigure(0, weight=1)
            f_lantai.grid_rowconfigure(0, weight=0) 

            tk.Label(f_lantai, text=f"Lantai {i + 1}", font=("Segoe UI", 10, "bold"),
                     bg="#F9FAFB").grid(row=0, column=0, pady=8)

            for j in range(self.parkir.kapasitas_lantai):
                data = lantai[j] if j < len(lantai) else None
                f_lantai.grid_rowconfigure(j + 1, weight=1, uniform="slot_row", minsize=56)
                self.buat_slot(f_lantai, j + 1, data, row=j + 1)

        self.list_antrian.delete(0, tk.END)
        for i, k in enumerate(self.parkir.antrian_masuk):
            icon = "🚗" if k['jenis'] == 'Mobil' else "🏍️"
            self.list_antrian.insert(tk.END, f" {i + 1}. {icon} {k['plat']}")

        for item in self.tree.get_children():
            self.tree.delete(item)
        data = self.parkir.riwayat.get_semua_data()
        for idx, baris in enumerate(reversed(data)):
            status = baris[7]
            baris_tampil = list(baris)
            if status == "Selesai":
                baris_tampil[7] = "🟢 Selesai"
                status_tag = "selesai"
            else:
                baris_tampil[7] = "🟠 Parkir"
                status_tag = "parkir"
            row_tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=baris_tampil, tags=(status_tag, row_tag))

    # Menangani proses kendaraan masuk
    def action_masuk(self):
        plat = self.ent_masuk.get().strip().upper()
        if not plat:
            messagebox.showwarning("Peringatan", "Mohon masukkan plat nomor kendaraan yang ingin dimasukkan.")
            return
        self.parkir.kendaraan_datang(plat, self.var_jenis.get())
        self.ent_masuk.delete(0, tk.END)
        self.refresh_dashboard()

    # Menangani proses antrian kendaraan
    def action_proses(self):
        sukses, pesan = self.parkir.proses_antrian()
        if not sukses:
            messagebox.showinfo("Info", pesan)
        self.refresh_dashboard()

    # Menangani proses kendaraan keluar
    def action_keluar(self):
        plat = self.ent_keluar.get().strip().upper()
        if not plat:
            messagebox.showwarning("Peringatan", "Mohon masukkan plat nomor kendaraan yang ingin dikeluarkan.")
            return
        sukses, data = self.parkir.kendaraan_keluar(plat)
        if sukses:
            messagebox.showinfo("Berhasil", f"Kendaraan {plat} keluar.\nBiaya: Rp{data.biaya}")
        else:
            messagebox.showerror("Gagal", f"Kendaraan {plat} tidak ditemukan di area parkir.")
        self.ent_keluar.delete(0, tk.END)
        self.refresh_dashboard()

    # Menangani proses unduh laporan parkir
    def action_unduh(self):
        sukses, pesan = self.parkir.riwayat.unduh_riwayat()
        if sukses:
            messagebox.showinfo("Sukses", f"Laporan disimpan di:\n{pesan}")
        else:
            messagebox.showerror("Gagal", f"Error:\n{pesan}")

# Menjalankan aplikasi sistem parkir otomatis 
if __name__ == "__main__":
    app = AplikasiParkirGUI()
    app.mainloop()