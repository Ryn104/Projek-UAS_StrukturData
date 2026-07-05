import time
import os
import tkinter as tk
from tkinter import ttk, messagebox

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

class LinkedListRiwayat:
    def __init__(self):
        self.head = None
        self.total_pendapatan = 0
        self.total_kendaraan = 0

    def tambah_transaksi(self, jenis, plat_nomor, waktu_masuk):
        node_baru = NodeRiwayat(jenis, plat_nomor, waktu_masuk)
        if self.head is None:
            self.head = node_baru
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node_baru

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

    def get_statistik(self):
        total_mobil = 0
        total_motor = 0
        current = self.head
        while current:
            if current.status == "Parkir":
                if current.jenis == "Mobil": total_mobil += 1
                else: total_motor += 1
            current = current.next
        return total_mobil, total_motor

    def unduh_riwayat(self):
        nama_file = f"Laporan_Parkir_{time.strftime('%Y-%m-%d_%H%M%S')}.txt"
        lokasi_script = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(lokasi_script, nama_file)
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("="*88 + "\n")
                file.write("                             RIWAYAT TRANSAKSI PARKIR HARIAN\n")
                file.write("="*88 + "\n\n")
                data = self.get_semua_data()
                if not data:
                    file.write("Belum ada riwayat transaksi.\n")
                else:
                    file.write(f"{'No':<4} | {'Jenis':<6} | {'Plat Nomor':<12} | {'Masuk':<8} | {'Keluar':<8} | {'Durasi':<10} | {'Biaya':<10} | {'Status':<10}\n")
                    file.write("-" * 88 + "\n")
                    for baris in data:
                        file.write(f"{baris[0]:<4} | {baris[1]:<6} | {baris[2]:<12} | {baris[3]:<8} | {baris[4]:<8} | {baris[5]:<10} | {baris[6]:<10} | {baris[7]:<10}\n")
                    file.write("-" * 88 + "\n")
                    file.write(f"Total Pendapatan : Rp{self.total_pendapatan:.2f}\n")
            return True, file_path
        except Exception as e:
            return False, str(e)

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
    def __init__(self):
        self.data = []
    def append(self, item): self.data.append(item)
    def popleft(self): return self.data.pop(0) if self.data else None
    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.data[index]
    def __bool__(self): return len(self.data) > 0

class SistemParkir:
    def __init__(self, jumlah_lantai, kapasitas_per_lantai, tarif_per_jam_mb, tarif_per_jam_mt):
        self.lantai_parkir = [[] for _ in range(jumlah_lantai)] 
        self.kapasitas_lantai = kapasitas_per_lantai
        self.antrian_masuk = AntrianParkir() 
        self.riwayat = LinkedListRiwayat() 
        self.tarif_mb = tarif_per_jam_mb
        self.tarif_mt = tarif_per_jam_mt

    def kendaraan_datang(self, plat_nomor, jenis):
        waktu_datang = time.time()
        self.antrian_masuk.append({'plat': plat_nomor, 'jenis': jenis, 'waktu_masuk': waktu_datang})
        jam_masuk = time.strftime("%H:%M:%S", time.localtime(waktu_datang))
        self.riwayat.tambah_transaksi(jenis, plat_nomor, jam_masuk)

    def proses_antrian(self):
        if not self.antrian_masuk: return False, "Tidak ada kendaraan di antrian."
        for i in range(len(self.lantai_parkir)):
            if len(self.lantai_parkir[i]) < self.kapasitas_lantai:
                kendaraan = self.antrian_masuk.popleft()
                self.lantai_parkir[i].append(kendaraan)
                return True, f"Kendaraan {kendaraan['plat']} parkir di Lantai {i + 1}."
        return False, "Seluruh lantai parkir penuh! Kendaraan tertahan di antrian."

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
                durasi_menit = durasi_detik / 60 
                
                tarif = self.tarif_mb if k_keluar['jenis'] == 'Mobil' else self.tarif_mt
                if durasi_menit <= 1:
                    biaya_total = tarif
                else:
                    biaya_total = int(durasi_menit+1) * tarif

                jam_keluar = time.strftime("%H:%M:%S", time.localtime(waktu_keluar))
                _, data_transaksi = self.riwayat.update_transaksi(plat_nomor, jam_keluar, f"{durasi_menit:.2f} Jam", biaya_total)
                
                while stack_sementara:
                    lantai.append(stack_sementara.pop())
                return True, data_transaksi

        return False, None

# GUI
class AplikasiParkirGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Parking System")
        self.geometry("1300x768")
        self.configure(bg="#F3F4F6") 
        self.state('zoomed')

        self.parkir = SistemParkir(jumlah_lantai=3, kapasitas_per_lantai=3, tarif_per_jam_mb=5000, tarif_per_jam_mt=2000)

        # Styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), background="#0D47A1", foreground="white")
        self.style.configure("Treeview", font=('Helvetica', 10), rowheight=25)

        self.setup_ui()
        self.update_waktu()
        self.refresh_dashboard()

    def setup_ui(self):
        # --- MAIN CONTENT (Kanan) ---
        self.main_content = tk.Frame(self, bg="#F3F4F6")
        self.main_content.pack(side="right", fill="both", expand=True)

        # 1. Header Area
        header_frame = tk.Frame(self.main_content, bg="#F3F4F6")
        header_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Label(header_frame, text="Dashboard", font=("Arial", 18, "bold"), bg="#F3F4F6").pack(side="left")
        tk.Label(header_frame, text="Ringkasan informasi area parkir", font=("Arial", 10), bg="#F3F4F6", fg="gray").pack(side="left", padx=10)

        self.lbl_waktu = tk.Label(header_frame, text="", font=("Arial", 11), bg="white", padx=15, pady=5, relief="flat")
        self.lbl_waktu.pack(side="right", padx=10)

        # 2. Summary Cards Area (4 Kolom)
        self.cards_frame = tk.Frame(self.main_content, bg="#F3F4F6")
        self.cards_frame.pack(fill="x", padx=20, pady=5)
        
        self.lbl_val_mobil = self.buat_card(self.cards_frame, "Total Mobil", "0", 0)
        self.lbl_val_motor = self.buat_card(self.cards_frame, "Total Motor", "0", 1)
        self.lbl_val_pendapatan = self.buat_card(self.cards_frame, "Total Pendapatan", "Rp0", 2)
        self.lbl_val_slot = self.buat_card(self.cards_frame, "Slot Tersedia", "9 / 9", 3)

        # 3. Middle Section (Status Parkir & Panel Kontrol)
        mid_frame = tk.Frame(self.main_content, bg="#F3F4F6")
        mid_frame.pack(fill="x", padx=20, pady=10)

        # Kiri: Status Parkir
        status_frame = tk.Frame(mid_frame, bg="white", padx=10, pady=10)
        status_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(status_frame, text="Status Parkir", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=(0, 10))
        
        self.frame_lantai = tk.Frame(status_frame, bg="white")
        self.frame_lantai.pack(fill="both", expand=True)

        # Kanan 1: Form Masuk
        form_masuk = tk.Frame(mid_frame, bg="white", padx=15, pady=10, width=200)
        form_masuk.pack(side="left", fill="y", padx=(0, 10))
        tk.Label(form_masuk, text="Kendaraan Masuk", font=("Arial", 11, "bold"), fg="#0D47A1", bg="white").pack(anchor="w", pady=(0, 10))
        
        tk.Label(form_masuk, text="Jenis Kendaraan", bg="white").pack(anchor="w")
        self.var_jenis = tk.StringVar(value="Mobil")
        tk.Radiobutton(form_masuk, text="Mobil", variable=self.var_jenis, value="Mobil", bg="white").pack(anchor="w")
        tk.Radiobutton(form_masuk, text="Motor", variable=self.var_jenis, value="Motor", bg="white").pack(anchor="w")
        
        tk.Label(form_masuk, text="Plat Nomor", bg="white").pack(anchor="w", pady=(10,0))
        self.ent_masuk = ttk.Entry(form_masuk, font=("Arial", 11))
        self.ent_masuk.pack(fill="x", pady=5)
        
        btn_add = tk.Button(form_masuk, text="+ Tambahkan", bg="#0D47A1", fg="white", relief="flat", command=self.action_masuk)
        btn_add.pack(fill="x", pady=10, ipady=5)

        # Kanan 2: Form Keluar
        form_keluar = tk.Frame(mid_frame, bg="white", padx=15, pady=10, width=200)
        form_keluar.pack(side="left", fill="y", padx=(0, 10))
        tk.Label(form_keluar, text="Kendaraan Keluar", font=("Arial", 11, "bold"), fg="#D32F2F", bg="white").pack(anchor="w", pady=(0, 10))
        
        tk.Label(form_keluar, text="Cari Plat Nomor", bg="white").pack(anchor="w")
        self.ent_keluar = ttk.Entry(form_keluar, font=("Arial", 11))
        self.ent_keluar.pack(fill="x", pady=5)
        
        btn_out = tk.Button(form_keluar, text="Keluarkan", bg="#D32F2F", fg="white", relief="flat", command=self.action_keluar)
        btn_out.pack(fill="x", pady=5, ipady=5)

        # Kanan 3: Proses Antrian
        antrian_frame = tk.Frame(mid_frame, bg="white", padx=15, pady=10, width=200)
        antrian_frame.pack(side="left", fill="y")
        tk.Label(antrian_frame, text="Proses Antrian", font=("Arial", 11, "bold"), fg="#F57C00", bg="white").pack(anchor="w", pady=(0, 10))
        
        self.list_antrian = tk.Listbox(antrian_frame, height=6, relief="flat", bg="#F9FAFB", font=("Arial", 10))
        self.list_antrian.pack(fill="both", expand=True, pady=5)
        
        btn_proses = tk.Button(antrian_frame, text="→ Proses Berikutnya", bg="#F57C00", fg="white", relief="flat", command=self.action_proses)
        btn_proses.pack(fill="x", pady=5, ipady=5)

        # 4. Bottom Section (Tabel Riwayat)
        bottom_frame = tk.Frame(self.main_content, bg="white", padx=10, pady=10)
        bottom_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        header_tbl = tk.Frame(bottom_frame, bg="white")
        header_tbl.pack(fill="x")
        tk.Label(header_tbl, text="Riwayat Transaksi", font=("Arial", 12, "bold"), bg="white").pack(side="left")
        btn_unduh = tk.Button(header_tbl, text="Unduh Laporan", bg="white", fg="#0D47A1", relief="solid", bd=1, command=self.action_unduh)
        btn_unduh.pack(side="right")

        kolom = ("No", "Jenis", "Plat Nomor", "Masuk", "Keluar", "Durasi", "Biaya", "Status")
        self.tree = ttk.Treeview(bottom_frame, columns=kolom, show="headings")
        lebar_kolom = [40, 80, 150, 100, 100, 100, 100, 100]
        for i, col in enumerate(kolom):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=lebar_kolom[i], anchor="center")
        
        scroll = ttk.Scrollbar(bottom_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        scroll.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, pady=10)

    def buat_card(self, parent, judul, nilai_awal, col):
        frame = tk.Frame(parent, bg="white", padx=20, pady=15)
        frame.grid(row=0, column=col, sticky="ew", padx=(0 if col==0 else 10, 0))
        parent.columnconfigure(col, weight=1)
        
        tk.Label(frame, text=judul, font=("Arial", 10), fg="gray", bg="white").pack(anchor="w")
        lbl_val = tk.Label(frame, text=nilai_awal, font=("Arial", 20, "bold"), bg="white")
        lbl_val.pack(anchor="w", pady=5)
        return lbl_val

    def update_waktu(self):
        waktu_skrg = time.strftime("%H:%M:%S\n%A, %d %b %Y")
        self.lbl_waktu.config(text=waktu_skrg)
        self.after(1000, self.update_waktu)

    def refresh_dashboard(self):
        # Update Cards
        total_mobil, total_motor = self.parkir.riwayat.get_statistik()
        isi_total = sum(len(lantai) for lantai in self.parkir.lantai_parkir)
        kapasitas_max = self.parkir.kapasitas_lantai * len(self.parkir.lantai_parkir)
        
        self.lbl_val_mobil.config(text=str(total_mobil))
        self.lbl_val_motor.config(text=str(total_motor))
        self.lbl_val_pendapatan.config(text=f"Rp{self.parkir.riwayat.total_pendapatan:,.0f}")
        self.lbl_val_slot.config(text=f"{kapasitas_max - isi_total} / {kapasitas_max}")

        # Update Grid Status Parkir
        for widget in self.frame_lantai.winfo_children():
            widget.destroy()

        for i, lantai in enumerate(self.parkir.lantai_parkir):
            f_lantai = tk.Frame(self.frame_lantai, bg="#F9FAFB", bd=1, relief="solid")
            f_lantai.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            tk.Label(f_lantai, text=f"Lantai {i+1}", font=("Arial", 10, "bold"), bg="#F9FAFB").pack(pady=5)
            
            for j in range(self.parkir.kapasitas_lantai):
                if j < len(lantai):
                    k = lantai[j]
                    bg_color = "#1976D2" if k['jenis'] == 'Mobil' else "#388E3C"
                    teks = f"{k['plat']}\n{k['jenis']}"
                else:
                    bg_color = "#E0E0E0"
                    teks = "Kosong\n-"
                
                slot = tk.Label(f_lantai, text=teks, bg=bg_color, fg="white" if bg_color != "#E0E0E0" else "gray", 
                                font=("Arial", 9), width=15, height=3, relief="flat")
                slot.pack(pady=5, padx=10)

        # Update Antrian
        self.list_antrian.delete(0, tk.END)
        for i, k in enumerate(self.parkir.antrian_masuk):
            jam = time.strftime("%H:%M:%S", time.localtime(k["waktu_masuk"]))
            self.list_antrian.insert(tk.END, f"{i+1}. {k['plat']} ({k['jenis']}) - {jam}")

        # Update Riwayat
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = self.parkir.riwayat.get_semua_data()
        for baris in reversed(data): # Tampilkan terbaru di atas
            self.tree.insert("", tk.END, values=baris)

    def action_masuk(self):
        plat = self.ent_masuk.get().strip().upper()
        if not plat:
            messagebox.showwarning("Peringatan", "Plat nomor kosong!")
            return
        self.parkir.kendaraan_datang(plat, self.var_jenis.get())
        self.ent_masuk.delete(0, tk.END)
        self.refresh_dashboard()

    def action_proses(self):
        sukses, pesan = self.parkir.proses_antrian()
        if not sukses:
            messagebox.showinfo("Info", pesan)
        self.refresh_dashboard()

    def action_keluar(self):
        plat = self.ent_keluar.get().strip().upper()
        if not plat:
            messagebox.showwarning("Peringatan", "Plat nomor kosong!")
            return
        sukses, data = self.parkir.kendaraan_keluar(plat)
        if sukses:
            messagebox.showinfo("Berhasil", f"Kendaraan {plat} keluar.\nBiaya: Rp{data.biaya}")
        else:
            messagebox.showerror("Gagal", f"Kendaraan {plat} tidak ditemukan di area parkir.")
        self.ent_keluar.delete(0, tk.END)
        self.refresh_dashboard()

    def action_unduh(self):
        sukses, pesan = self.parkir.riwayat.unduh_riwayat()
        if sukses:
            messagebox.showinfo("Sukses", f"Laporan disimpan di:\n{pesan}")
        else:
            messagebox.showerror("Gagal", f"Error:\n{pesan}")

if __name__ == "__main__":
    app = AplikasiParkirGUI()
    app.mainloop()