from checker import (
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check
)

print("=== PARTEA 1: Funcții ajutătoare ===")
print(build_url("example.com", "login"))
print(build_url("example.com", "/login"))
print(is_https("https://example.com"))
print(is_https("http://example.com"))

print("\n=== PARTEA 2: Trimiterea unei cereri ===")
show_response("https://example.com")

print("\n=== PARTEA 3: Un verificator reutilizabil ===")
print(check_site("https://example.com"))
print(check_site("http://this-site-does-not-exist.invalid"))

print("\n=== PARTEA 4: Verificarea mai multor site-uri ===")
scan_sites()

print("\n=== PARTEA 5: Audit de securitate ===")
print(check_headers("https://example.com"))
print(check_headers("http://this-site-does-not-exist.invalid"))

print("\n=== PARTEA 6: Încercări repetate ===")
print(retry_check("https://httpbin.org/status/200"))
print(retry_check("https://httpbin.org/status/404"))
print(retry_check("https://httpbin.org/status/500"))
print(retry_check("http://this-site-does-not-exist.invalid"))