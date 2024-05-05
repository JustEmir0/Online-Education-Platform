import tkinter as tk 
from customtkinter import*
from tkinter import messagebox
from CTkListbox import * 
import sqlite3


# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('veritabani.db')
cursor = conn.cursor()

# kullanicilar tablosunu oluştur
cursor.execute('''CREATE TABLE IF NOT EXISTS kullanicilar (
                    id INTEGER PRIMARY KEY,
                    isim TEXT NOT NULL,
                    e_posta TEXT NOT NULL,
                    sifre TEXT NOT NULL
                )''')

# Değişiklikleri kaydet
conn.commit()

# Veritabanı bağlantısını kapat
conn.close()


class Kurs:
    def __init__(self,kurs_adı, eğitmen,fiyat,içerik):
        self.kurs_adı = kurs_adı
        self.eğitmen = eğitmen
        self.fiyat = fiyat
        self.içerik = içerik 

class Eğitmen:
    def __init__(self, isim, uzmanlık_alanı):
        self.isim = isim
        self.uzmanlık_alanı = uzmanlık_alanı


class Öğrenci:
    def __init__(self, isim, e_posta):
        self.isim = isim
        self.e_posta = e_posta


Kurslar = [
    Kurs("Python Programlama", "Ahmet Yılmaz", "449.99 TL", "Python programlamayı öğrenmek için kapsamlı bir kurs."),
    Kurs("Veri Bilimi", "Ayşe Demir", "499.99 TL", "Veri bilimi ve makine öğrenimi konularında derinlemesine bir kurs."),
    Kurs("Web Geliştirme", "Mehmet Kara", "599.99 TL", "HTML, CSS, JavaScript gibi web geliştirme teknolojilerini öğrenin."),
    Kurs("Yapay Zeka", "Fatma Şahin", "699.99 TL", "Yapay zeka ve derin öğrenme üzerine kapsamlı bir kurs."),
    Kurs("Mobil Uygulama Geliştirme", "Hüseyin Yıldız", "399.99 TL", "Android ve iOS için mobil uygulama geliştirme kursu."),
    Kurs("Veritabanı Yönetimi", "Elif Arslan", "599.99 TL", "SQL ve veritabanı yönetimi konularında temel bir kurs."),
    Kurs("Grafik Tasarım", "Özlem Demir", "429.99 TL", "Adobe Photoshop, Illustrator ve InDesign kursu."),
    Kurs("Blockchain ve Kripto Paralar", "Ahmet Kaplan", "399.99 TL", "Blockchain teknolojisi ve kripto para ticareti kursu."),
    Kurs("İşletme Yönetimi", "Cemal Öz", "99.99 TL", "Temel işletme yönetimi ve strateji konularında bir kurs."),
    Kurs("Yoga ve Meditasyon", "Zeynep Akgün", "199.99 TL", "Yoga ve meditasyon pratiği üzerine bir kurs.")
]




def kaydet(isim, e_posta, sifre):
    # SQLite veritabanına bağlan
    conn = sqlite3.connect('veritabani.db')
    cursor = conn.cursor()

    # E-posta adresini kontrol et
    cursor.execute("SELECT e_posta FROM kullanicilar WHERE e_posta = ?", (e_posta,))
    existing_user = cursor.fetchone()

    # Eğer kullanıcı zaten kayıtlıysa uyarı ver ve fonksiyondan çık
    if existing_user:
        messagebox.showwarning("Uyarı", "Bu e-posta adresiyle zaten bir hesap bulunmaktadır.")
        return

    # Yeni kullanıcıyı veritabanına ekle
    cursor.execute("INSERT INTO kullanicilar (isim, e_posta, sifre) VALUES (?, ?, ?)", (isim, e_posta, sifre))

    conn.commit()
    conn.close()


def kayıt_ol():
    kayit_formu = CTk()
    kayit_formu.geometry("400x300")
    kayit_formu.title("Kayıt Ol")

    label_isim = CTkLabel(master=kayit_formu, text="İsim:", font=('Arial', 14))
    label_isim.place(x=50, y=30)
    isim_entry_kayit = CTkEntry(master=kayit_formu, width=150)
    isim_entry_kayit.place(x=150, y=30)

    label_e_posta = CTkLabel(master=kayit_formu, text="E-Posta:", font=('Arial', 14))
    label_e_posta.place(x=50, y=80)
    e_posta_entry_kayit = CTkEntry(master=kayit_formu, width=150)
    e_posta_entry_kayit.place(x=150, y=80)

    label_sifre = CTkLabel(master=kayit_formu, text="Şifre:", font=('Arial', 14))
    label_sifre.place(x=50, y=130)
    sifre_entry_kayit = CTkEntry(master=kayit_formu, width=100, show="*")
    sifre_entry_kayit.place(x=150, y=130)


    def veri_kaydet():
            yeni_isim = isim_entry_kayit.get()
            yeni_e_posta = e_posta_entry_kayit.get()
            yeni_sifre = sifre_entry_kayit.get()

            # SQLite veritabanına kaydet
            kaydet(yeni_isim, yeni_e_posta, yeni_sifre)

            print("Yeni Kullanıcı Kaydedildi:")
            print("İsim:", yeni_isim)
            print("E-Posta:", yeni_e_posta)
            print("Şifre:", yeni_sifre)

            kayit_formu.destroy()

    kaydet_button = CTkButton(master=kayit_formu, text="Kaydet", font=('Arial', 14), width=150, command=veri_kaydet)
    kaydet_button.place(x=150, y=200)

    kayit_formu.mainloop()


def giris_yap():
    ad = isim_entry.get()
    e_posta = e_posta_entry.get()
    sifre = sifre_entry.get()

    if not ad or not e_posta or not sifre:
        messagebox.showwarning("Uyarı", "Lütfen adınızı , e-postanızı ve şifrenizi girin!")
        return

    root_log.destroy()
    eğitim_sistemine_giriş(ad, e_posta, sifre)
    


def eğitim_sistemine_giriş(ad, e_posta, sifre):
    
    # Kullanıcı bilgilerini almak için SQL sorgusu

    conn = sqlite3.connect('veritabani.db')
    cursor = conn.cursor()
    cursor.execute("SELECT isim, e_posta FROM kullanicilar WHERE isim = ? AND e_posta = ?AND sifre = ?", (ad, e_posta, sifre))
    user = cursor.fetchone() 
    conn.close()

    if user:
        app = CTk()
        app.geometry("1100x900")
        app.title("Online Eğitim Platformu")

        l0 = CTkLabel(master=app,text="--- RAVIL EĞİTİM PLATFORMU ---",font=("Helvetica", 22))
        l0.place(x=340,y=20)

        # Kullanıcı adını ve e-posta adresini ekle
        CTkLabel(master=app, text="Kullanıcı Adı: " + ad, font=("Helvetica", 14)).place(x=860, y=30)
        CTkLabel(master=app, text="E-Posta: " + e_posta, font=("Helvetica", 14)).place(x=860, y=60)

        l1 = CTkLabel(master=app,text="Popüler Eğitimler",font=("Helvetica", 20, "bold"))
        l1.place(x=40,y=365)

        l2 = CTkLabel(app,text="Kayıtlı Kurslarım",font=("Helvetica", 20, "bold"))
        l2.place(x=40, y=100)

        listbox = CTkListbox(app,width=1000,height=200)
        listbox.place(x=30, y=130)

        frame = CTkFrame(app)
        frame.place(x=10,y=400)

        satın_alınan_kurslar = []

        def kurs_detayları_göster(kurs):
            details_window = CTkToplevel(app)
            details_window.title(kurs.kurs_adı + " Detayları")
            CTkLabel(details_window, text="Kurs Adı:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
            CTkLabel(details_window, text=kurs.kurs_adı).grid(row=0, column=1, padx=10, pady=5)
            CTkLabel(details_window, text="Eğitmen:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
            CTkLabel(details_window, text=kurs.eğitmen).grid(row=1, column=1, padx=10, pady=5)
            CTkLabel(details_window, text="Fiyat:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
            CTkLabel(details_window, text=kurs.fiyat).grid(row=2, column=1, padx=10, pady=5)
            CTkLabel(details_window, text="Açıklama:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
            CTkLabel(details_window, text=kurs.içerik).grid(row=3, column=1, padx=10, pady=5)

        def satın_al_kurs(kurs):
            if kurs not in satın_alınan_kurslar:
                satın_alınan_kurslar.append(kurs)
                listbox.insert(tk.END, f"{kurs.kurs_adı} - Eğitmen: {kurs.eğitmen}")

        for i, course in enumerate(Kurslar):
            CTkLabel(frame, text=course.kurs_adı, font=("Helvetica", 14, "bold")).grid(row=i, column=0, padx=10, pady=10, sticky="w")
            CTkLabel(frame, text=f"Eğitmen: {course.içerik} - Fiyat: {course.fiyat}").grid(row=i, column=1, padx=10, pady=10, sticky="w")
            CTkButton(frame, text="Detayları Gör",command=lambda c=course: kurs_detayları_göster(c)).grid(row=i, column=2, padx=10, pady=5, sticky="e")
            CTkButton(frame, text="Satın Al",command=lambda c=course: satın_al_kurs(c)).grid(row=i, column=3, padx=10, pady=5, sticky="e")

        app.mainloop()
    else:
        messagebox.showerror("Hata", "Kullanıcı adı  e-posta  veya şifreniz yanlış!")



#---Logın Page---#
root_log = CTk()
root_log.geometry('450x400')
root_log.title('Logın Page')

f1 = CTkFrame(root_log,width=250,height=350)
f1.place(x=100,y=25)

l1 = CTkLabel(master=f1,text="Giriş Yap",font=("Helvetica", 20, "bold"))
l1.place(x=80, y=10)

label_isim = CTkLabel(master=f1,text="Kullanıcı Adı",font=('Arial',16))
label_isim.place(x=55, y=50)
isim_entry = CTkEntry(master=f1,width=160, height=27)
isim_entry.place(x=50, y=80)

label_e_posta = CTkLabel(master=f1,text="E-Posta",font=('Arial',16))
label_e_posta.place(x=55, y=115)
e_posta_entry = CTkEntry(master=f1,width=160, height=27)
e_posta_entry.place(x=50, y=145)

label_sifre = CTkLabel(master=f1,text="Sifre",font=('Arial',16))
label_sifre.place(x=55, y=175)
sifre_entry = CTkEntry(master=f1,width=160, height=27)
sifre_entry.place(x=50, y=200)

btn_giriş_yap_ = CTkButton(master=f1,text='Giriş Yap',font=('Arial',16),width=160, height=23,command=giris_yap)
btn_giriş_yap_.place(x=50, y=240,)

l2 = CTkLabel(master=f1,text="Hesabın Yokmu? Kayıt Ol",font=("Helvetica", 13, "bold"))
l2.place(x=50,y=280)

btn_kayıt_ol = CTkButton(master=f1,text='Kayıt Ol',font=('Arial',16),width=160, height=23,command=kayıt_ol)
btn_kayıt_ol.place(x=50, y=310,)

root_log.mainloop()