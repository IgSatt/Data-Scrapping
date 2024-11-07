from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# Konfigurasi opsi dan driver
opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=opsi)

# Ubah URL ke halaman pencarian Nike
nike_link = "https://www.nike.com/id/w/mens-shoes-nik1zy7ok"
driver.set_window_size(1300,800)
driver.get(nike_link)

# Gulir halaman untuk memuat lebih banyak produk
rentang = 500
for i in range(1,7):
    akhir = rentang * i 
    perintah = "window.scrollTo(0,"+str(akhir)+")"
    driver.execute_script(perintah)
    print("Loading ke-"+str(i))
    time.sleep(1)

time.sleep(5)
driver.save_screenshot("nike_home.png")
content = driver.page_source
driver.quit()

# Parse konten halaman menggunakan BeautifulSoup
data = BeautifulSoup(content, 'html.parser')

# Variabel untuk menyimpan data produk
list_nama, list_gambar, list_harga, list_link = [], [], [], []
base_url = "https://www.nike.com"

# Cari elemen produk berdasarkan class yang sesuai di situs Nike
for area in data.find_all('div', class_="product-card__body"):  # class ini perlu disesuaikan
    nama = area.find('a', class_="product-card__link-overlay").get_text(strip=True)
    gambar = area.find('img')['src']
    harga = area.find('div', class_="product-price").get_text(strip=True)
    link = base_url + area.find('a', class_="product-card__link-overlay")['href']
    
    list_nama.append(nama)
    list_gambar.append(gambar)
    list_harga.append(harga)
    list_link.append(link)
    print("Produk:", nama, "| Harga:", harga)

# Simpan ke Excel
df = pd.DataFrame({
    'Nama': list_nama,
    'Gambar': list_gambar,
    'Harga': list_harga,
    'Link': list_link
})

with pd.ExcelWriter('nike_products.xlsx') as writer:
    df.to_excel(writer, 'Sheet1', index=False)
print("Data produk Nike berhasil disimpan ke nike_products.xlsx")

