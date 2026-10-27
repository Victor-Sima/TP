# Program principal: main.py
# Student: Victor Sima

import sys
import csv
from datetime import datetime
import webtools

def main():
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = "https://cybercor.org"

    print(f"=== Raport site: {target_url} ===")
    report = webtools.site_report(target_url)

    print(f"Cod de stare:      {report['status_code']}")
    print(f"Titlu:             {report['title']}")
    print(f"Adresă IP:         {report['ip_address']}")
    print(f"Redirecționări:    {report['redirect_chain']}")
    print(f"Scor securitate:   {report['security_score']}")
    print(f"Certificat:        {report['cert_days_left']} de zile rămase")
    print(f"Legături:          {report['internal_links']} interne, {report['external_links']} externe")
    print(f"Căi interzise:     {', '.join(report['disallowed_paths']) if report['disallowed_paths'] else 'Niciuna'}")
    print("Salvat în report.json")

    # Exercițiul 49: Salvarea rezultatului în report.csv
    paths_to_check = ["/", "/robots.txt", "/sitemap.xml"]
    checked_at = datetime.now().isoformat()
    
    with open("report.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["path", "status", "checked_at"])
        for p in paths_to_check:
            full_u = target_url.rstrip("/") + p
            st = webtools.get_status(full_u)
            writer.writerow([p, st, checked_at])
            time.sleep(1)
    print("Salvat și în report.csv")

if __name__ == "__main__":
    main()