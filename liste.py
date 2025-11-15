from tkinter import *
from tkinter import messagebox
import ttkbootstrap as tb

# Temayı seçiyoruz
window = tb.Window(themename="superhero")  # Farklı temalar da deneyebilirsin
window.title("To-Do List")
window.geometry("500x500")

FONT_NORMAL = ("Arial", 12, "normal")
FONT_USTU_CIZILI = ("Arial", 12, "overstrike")
task_styles = []

# -------------------- Fonksiyonlar --------------------

def gorev_ekle(event=None):
    gorev_metni = entry.get()
    if gorev_metni:
        gorev_listesi.insert(END, gorev_metni)
        task_styles.append(False)
        with open("gorevler.txt", "a", encoding="utf-8") as file:
            file.write(gorev_metni + "\n")
        entry.delete(0, END)
    else:
        messagebox.showwarning("Uyarı", "Lütfen bir görev girin!")

def gorev_sil():
    try:
        i = gorev_listesi.curselection()[0]
        silinecek_gorev = gorev_listesi.get(i)
        onay = messagebox.askyesno( "Silme Onayı", f"'{silinecek_gorev}' görevini silmek istediğinize emin misiniz?" ) 
        if not onay: 
            return
        gorev_listesi.delete(i)
        del task_styles[i]
        dosyayi_guncelle()
    except:
        messagebox.showwarning("Uyarı", "Lütfen silmek için bir görev seçin.")

def gorev_yukari_tasi():
    try:
        i = gorev_listesi.curselection()[0]
        if i == 0:
            return
        gorev = gorev_listesi.get(i)
        gorev_listesi.delete(i)
        gorev_listesi.insert(i-1, gorev)
        task_styles.insert(i-1, task_styles.pop(i))
        gorev_listesi.select_set(i-1)
        dosyayi_guncelle()
    except:
        messagebox.showwarning("Uyarı", "Taşımak için bir görev seçin.")

def gorev_asagi_tasi():
    try:
        i = gorev_listesi.curselection()[0]
        if i == gorev_listesi.size()-1:
            return
        gorev = gorev_listesi.get(i)
        gorev_listesi.delete(i)
        gorev_listesi.insert(i+1, gorev)
        task_styles.insert(i+1, task_styles.pop(i))
        gorev_listesi.select_set(i+1)
        dosyayi_guncelle()
    except:
        messagebox.showwarning("Uyarı", "Taşımak için bir görev seçin.")

def ustunu_ciz(event=None):
    try:
        i = gorev_listesi.curselection()[0]
        task_styles[i] = not task_styles[i]
        if task_styles[i]:
            gorev_listesi.itemconfig(i, font=FONT_USTU_CIZILI)
        else:
            gorev_listesi.itemconfig(i, font=FONT_NORMAL)
    except:
        pass

def dosyayi_guncelle():
    with open("gorevler.txt", "w", encoding="utf-8") as file:
        for i in range(gorev_listesi.size()):
            file.write(gorev_listesi.get(i) + "\n")

def open_file():
    try:
        with open("gorevler.txt", "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines()]
        for line in lines:
            if line:
                gorev_listesi.insert(END, line)
                task_styles.append(False)
    except FileNotFoundError:
        pass

# -------------------- Arayüz Tasarımı --------------------

# Başlık
title_label = tb.Label(window, text="📝 My To-Do List", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Giriş ve ekleme
entry_frame = tb.Frame(window)
entry_frame.pack(pady=10)

entry = tb.Entry(entry_frame, width=30, font=("Arial", 12))
entry.grid(row=0, column=0, padx=5)

add_button = tb.Button(entry_frame, text="Add", bootstyle="success-outline", command=gorev_ekle)
add_button.grid(row=0, column=1, padx=5)

# Liste ve scroll
list_frame = tb.Frame(window)
list_frame.pack(pady=10)

gorev_listesi = Listbox(list_frame, width=45, height=15, font=FONT_NORMAL)
gorev_listesi.grid(row=0, column=0)

scrollbar = tb.Scrollbar(list_frame, command=gorev_listesi.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
gorev_listesi.config(yscrollcommand=scrollbar.set)

# Butonlar
button_frame = tb.Frame(window)
button_frame.pack(pady=10)

sil_butonu = tb.Button(button_frame, text="Seçileni Sil", bootstyle="danger-outline", width=15, command=gorev_sil)
sil_butonu.grid(row=0, column=0, padx=5)

yukari_butonu = tb.Button(button_frame, text="Yukarı Taşı", bootstyle="primary-outline", width=15, command=gorev_yukari_tasi)
yukari_butonu.grid(row=0, column=1, padx=5)

asagi_butonu = tb.Button(button_frame, text="Aşağı Taşı", bootstyle="primary-outline", width=15, command=gorev_asagi_tasi)
asagi_butonu.grid(row=0, column=2, padx=5)

# Event binding
window.bind("<Return>", gorev_ekle)
gorev_listesi.bind("<Double-1>", ustunu_ciz)

open_file()
window.mainloop()
