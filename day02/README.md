# Gün 2: Log Analiz ve Güvenlik Aracı 🛡️

Bu dizin, sistem loglarını (örneğin `/var/log/auth.log`) analiz ederek başarısız giriş denemelerini (SSH Brute-Force gibi) tespit eden bir Python aracı içerir.

## Özellikler
- **Regex Tabanlı Analiz:** `FAILED PASSWORD` gibi desenleri tespit eder.
- **Saldırgan Profilleme:** En çok saldıran IP adreslerini ve hedef alınan kullanıcı adlarını raporlar.
- **Güvenli Test:** Root yetkisi gerektirmeden `test_auth.log` dosyası ile test edilebilir.

## Kullanım

### 1. Test Verisi ile Çalıştırma
```bash
python3 log_analyzer.py --file test_auth.log
```

### 2. Gerçek Sistem Logları ile Çalıştırma (Root yetkisi gerekebilir)
```bash
sudo python3 log_analyzer.py --file /var/log/auth.log
```

## Örnek Çıktı
```text
--- Log Analizi Başlatılıyor: test_auth.log ---

[+] Toplam Başarısız Giriş Denemesi: 5

[!] En Çok Saldıran IP Adresleri (Top 5):
    10.0.0.5        : 3 deneme
    192.168.1.100   : 2 deneme

[!] Hedef Alınan Kullanıcı Adları (Top 5):
    support         : 3 deneme
    root            : 1 deneme
    admin           : 1 deneme
```
