# Ringkasan Temuan EDA

Dokumen ini memaparkan fakta dan karakteristik data yang teridentifikasi secara objektif dari kelima visualisasi *Exploratory Data Analysis* (EDA).

---

## 1. Distribusi Kelas Target (Univariate)
* **Jumlah Sampel:** Kelas `fire` berjumlah 633 data dan kelas `not fire` berjumlah 582 data[cite: 1, 2].
* **Proporsi:** Kelas `fire` mencakup 52,1% dari total data, sedangkan `not fire` mencakup 47,9%[cite: 2].
* **Karakteristik Keseimbangan:** Selisih proporsi antar kedua kelas tergolong sangat kecil (hanya berjarak sekitar 4,2%), sehingga sebaran kelas target berada dalam kondisi seimbang[cite: 2].

---

## 2. Distribusi Fitur Meteorologi & Komponen FWI (Bivariate per Kelas)
* **Temperature:** Sebaran data pada kelas `fire` bergeser ke arah kanan dengan puncak di rentang 35–38°C, sedangkan kelas `not fire` mendominasi di rentang 28–33°C[cite: 3].
* **RH (Relative Humidity):** Distribusi kelas `fire` condong berada di area nilai rendah (sekitar 20–45%), sedangkan kelas `not fire` terdistribusi dominan pada kelembapan tinggi (>60%)[cite: 3].
* **Rain:** Mengalami fenomena penumpukan nilai nol (*zero-inflation*)[cite: 3]. Sampel `fire` hampir seluruhnya berada tepat di angka 0 mm, sementara data curah hujan >0 mm hampir seluruhnya berasal dari kelas `not fire`[cite: 3].
* **Ws (Wind Speed):** Kurva sebaran antara kelas `fire` dan `not fire` saling bertumpuk (*overlapping*) secara rapat dengan puncak yang sama di sekitar 13–17 km/jam[cite: 3].
* **Komponen Indeks (FFMC, DMC, DC, ISI, BUI, FWI):** 
  * Nilai `FFMC` pada kelas `fire` terkonsentrasi sangat tinggi (>80) dengan kurva curam ke kiri (*left-skewed*)[cite: 4].
  * Fitur `Rain`, `ISI`, `DC`, dan `FWI` menunjukkan distribusi menceng kanan yang panjang (*positive/right-skewed*)[cite: 3, 4].
  * Pada fitur `FWI`, sebagian besar data `not fire` menumpuk di bawah nilai 10, sedangkan data `fire` menyebar dari nilai belasan hingga di atas 40[cite: 4].

---

## 3. Sebaran Nilai & Pencilan per Kelas (Boxplot Fitur)
* **FFMC:** Rentang antarkuartil (kotak IQR) kelas `fire` berada rapat di atas angka 90 dengan whisker pendek, terpisah cukup jauh dari kotak IQR `not fire` yang berada di kisaran 68–85[cite: 5].
* **Ws:** Nilai tengah (median) serta rentang IQR antara `fire` dan `not fire` berada pada ketinggian yang hampir setara (~15–16)[cite: 5].
* **Asimetri Outlier:**
  * Pada fitur **Rain**, titik-titik pencilan ekstrem bernilai tinggi (hingga 20 mm) terkonsentrasi pada kelas `not fire`[cite: 5].
  * Pada fitur **ISI**, titik pencilan ekstrem dengan nilai tinggi (mencapai >100) terkonsentrasi pada kelas `fire`[cite: 5].
  * Pada fitur **FWI**, pencilan di kelas `fire` memanjang hingga melewati angka 100, sedangkan rentang non-pencilan kelas `not fire` terhenti di bawah angka 20[cite: 5].

---

## 4. Korelasi Linier Antarfitur (Heatmap)
* **Korelasi Sangat Kuat / Redundan ($r \ge 0,85$):**
  * `DMC` terhadap `BUI` memiliki nilai korelasi $r = 0,98$[cite: 6].
  * `DC` terhadap `BUI` memiliki nilai korelasi $r = 0,92$[cite: 6].
  * `ISI` terhadap `FWI` memiliki nilai korelasi $r = 0,88$[cite: 6].
  * `DMC` terhadap `DC` memiliki nilai korelasi $r = 0,86$[cite: 6].
* **Korelasi Terbalik (Negatif):**
  * `Temperature` berbanding terbalik secara moderat terhadap `RH` ($r = -0,66$)[cite: 6].
  * `RH` berkorelasi negatif terhadap parameter api: `FWI` ($r = -0,69$), `ISI` ($r = -0,66$), dan `FFMC` ($r = -0,60$)[cite: 6].
* **Korelasi Linier Lemah:**
  * `Ws` terhadap mayoritas fitur lain berkorelasi rendah, kecuali terhadap `ISI` ($r = 0,61$) dan `FWI` ($r = 0,46$)[cite: 6].
  * `Rain` memiliki korelasi linier rendah terhadap sebagian besar fitur (berkisar antara $-0,01$ hingga $-0,48$)[cite: 6].

---

## 5. Hubungan Geometris & Batas Sebaran (Pairplot Fitur Kunci)
* **Pola Batas Bersiku:**
  * Sebaran data antara `FFMC` dengan fitur lainnya (seperti `Temperature`, `RH`, dan `ISI`) membentuk pola pemisahan bersudut tegak lurus (berbentuk huruf "L")[cite: 7].
  * Hampir semua titik merah (`fire`) terkumpul hanya saat nilai `FFMC` melampaui ambang batas ~80[cite: 7].
* **Hubungan Dua Variabel Linear:**
  * Sebaran scatter plot antara `ISI` dan `FWI` membentuk pola garis diagonal lurus yang rapat pada data `fire`[cite: 7].
* **Pola Tumpang Tindih:**
  * Pada kombinasi `Temperature` vs `RH`, titik hijau dan merah bercampur di area tengah (rentang suhu 30–35°C dan RH 50–70%), sehingga tidak menunjukkan batas pemisah yang bersih bila hanya melihat kedua variabel tersebut[cite: 7].