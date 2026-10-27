# Modulul webtools.py
# Student: Victor Sima

import requests
import time
import socket
import ssl
import hashlib
import json
import re
from datetime import datetime
import urllib.parse

DEFAULT_HEADERS = {"User-Agent": "WebLab-Victor-Sima"}
TIMEOUT = 10

def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Descărcare cerere GET cu antete personalizate și timeout."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP."""
    try:
        res = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
        return res.status_code
    except requests.RequestException:
        return 0

def get_title(html: str) -> str:
    """Extrage titlul dintr-un șir HTML."""
    start_tag = "<title>"
    end_tag = "</title>"
    start_idx = html.find(start_tag)
    if start_idx != -1:
        start_idx += len(start_tag)
        end_idx = html.find(end_tag, start_idx)
        if end_idx != -1:
            return html[start_idx:end_idx].strip()
    return "Titlu negăsit"

def security_headers(url: str) -> dict:
    """Verifică antetele de securitate."""
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    try:
        res = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
        return {h: h in res.headers for h in headers_to_check}
    except requests.RequestException:
        return {h: False for h in headers_to_check}

def score_headers(results: dict) -> str:
    """Calculează scorul de securitate sub formă de fracție."""
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    return f"{passed}/{total}"

def resolve(hostname: str) -> str:
    """Rezolvă adresa IP pentru un hostname."""
    try:
        return socket.gethostbyname(hostname)
    except socket.error:
        return "Necunoscută"

def cert_days_left(hostname: str) -> int:
    """Calculează zilele rămase până la expirarea certificatului SSL."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expiry_timestamp = ssl.cert_time_to_seconds(cert["notAfter"])
                return int((expiry_timestamp - time.time()) // 86400)
    except Exception:
        return 0

def fetch_robots_text(base: str) -> str:
    """Obține conținutul fișierului robots.txt."""
    try:
        res = requests.get(base + "/robots.txt", headers=DEFAULT_HEADERS, timeout=TIMEOUT)
        if res.status_code == 200:
            return res.text
    except requests.RequestException:
        pass
    return ""

def disallowed_paths(robots_text: str) -> list:
    """Extrage căile interzise din textul robots.txt."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        if line.strip().lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()
            if path:
                paths.append(path)
    return paths

def extract_links(html: str) -> list:
    """Extrage legăturile unice dintr-un șir HTML."""
    return list(set(re.findall(r'href="([^"]+)"', html)))

def site_report(url: str) -> dict:
    """Generează raportul complet pentru site-ul țintă."""
    parsed_base = urllib.parse.urlparse(url)
    hostname = parsed_base.netloc
    
    # Redirecționări de la http://
    history_chain = []
    final_url = url
    try:
        http_url = f"http://{hostname}"
        r_redir = requests.get(http_url, headers=DEFAULT_HEADERS, timeout=TIMEOUT, allow_redirects=True)
        history_chain = [str(hist.status_code) for hist in r_redir.history]
        final_url = r_redir.url
        main_res = r_redir
    except requests.RequestException:
        main_res = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)

    status_code = main_res.status_code
    title = get_title(main_res.text)
    ip_addr = resolve(hostname)
    sec_dict = security_headers(url)
    sec_score = score_headers(sec_dict)
    days_left = cert_days_left(hostname)
    
    links = extract_links(main_res.text)
    internal = 0
    external = 0
    for l in links:
        full = urllib.parse.urljoin(url, l)
        if urllib.parse.urlparse(full).netloc == hostname:
            internal += 1
        else:
            external += 1

    r_txt = fetch_robots_text(url)
    disallowed = disallowed_paths(r_txt)

    report_data = {
        "status_code": status_code,
        "final_url": final_url,
        "title": title,
        "ip_address": ip_addr,
        "redirect_chain": " -> ".join(history_chain + [str(status_code)]),
        "security_score": sec_score,
        "cert_days_left": days_left,
        "internal_links": internal,
        "external_links": external,
        "disallowed_paths": disallowed
    }

    # Salvare în report.json
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    return report_data

if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))