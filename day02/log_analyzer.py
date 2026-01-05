import re
import argparse
from collections import Counter

def analyze_log(log_file):
    """
    Belirtilen log dosyasını okur ve başarısız giriş denemelerini analiz eder.
    """
    valid_users = Counter()
    invalid_users = Counter()
    ip_addresses = Counter()
    
    # Regex pattern: "Failed password for (invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)"
    failed_pwd_pattern = re.compile(r"Failed password for (invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)")

    print(f"--- Log Analizi Başlatılıyor: {log_file} ---")
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                if "Failed password" in line:
                    match = failed_pwd_pattern.search(line)
                    if match:
                        # match.group(1) -> "invalid user " veya None
                        # match.group(2) -> kullanıcı adı
                        # match.group(3) -> IP adresi
                        
                        is_invalid_user = bool(match.group(1))
                        user = match.group(2)
                        ip = match.group(3)
                        
                        ip_addresses[ip] += 1
                        
                        if is_invalid_user:
                            invalid_users[user] += 1
                        else:
                            valid_users[user] += 1
                            
        # Raporlama
        total_failed = sum(ip_addresses.values())
        print(f"\n[+] Toplam Başarısız Giriş Denemesi: {total_failed}")
        
        print("\n[!] En Çok Saldıran IP Adresleri (Top 5):")
        if not ip_addresses:
            print("    Heriangibir kayıt bulunamadı.")
        for ip, count in ip_addresses.most_common(5):
            print(f"    {ip:<15} : {count} deneme")
            
        print("\n[!] Hedef Alınan Kullanıcı Adları (Top 5):")
        all_users = valid_users + invalid_users
        if not all_users:
             print("    Herhangi bir kayıt bulunamadı.")
        for user, count in all_users.most_common(5):
             print(f"    {user:<15} : {count} deneme")

    except FileNotFoundError:
        print(f"Hata: '{log_file}' dosyası bulunamadı.")
    except PermissionError:
        print(f"Hata: '{log_file}' dosyasını okuma izniniz yok (sudo gerekiyor olabilir).")
    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gün 2: SSH Log Analiz Aracı v1.0")
    parser.add_argument("--file", help="Analiz edilecek log dosyasının yolu (örn: /var/log/auth.log)", required=True)
    args = parser.parse_args()
    
    analyze_log(args.file)
