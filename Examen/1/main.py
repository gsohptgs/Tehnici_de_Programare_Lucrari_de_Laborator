from checker import (
    build_url, 
    is_https, 
    show_response, 
    check_site, 
    scan_sites, 
    check_headers, 
    retry_check
)

print("--- Partea 1: Funcții ---")
print("build_url ('login'):", build_url("example.com", "login"))
print("build_url ('/login'):", build_url("example.com", "/login"))
print("is_https (HTTPS):", is_https("https://example.com"))
print("is_https (HTTP):", is_https("http://example.com"))
print()

print("--- Partea 2: Trimiterea unei cereri ---")
show_response("https://example.com")
show_response("http://this-site-does-not-exist.invalid")
print()

print("--- Partea 3: Un verificator reutilizabil ---")
print("Site ok:", check_site("https://example.com"))
print("Site picat:", check_site("http://this-site-does-not-exist.invalid"))
print()

print("--- Partea 4: Verificarea mai multor site-uri ---")
scan_sites()
print()

print("--- Partea 5: Audit de securitate ---")
print("Are 2 anteturi:", check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print("Nu are anteturi:", check_headers("https://example.com"))
print("Site picat:", check_headers("http://this-site-does-not-exist.invalid"))
print()

print("--- Partea 6: Încercări repetate ---")
print("Status 200 (se oprește instant):", retry_check("https://httpbin.org/status/200"))
print("Status 404 (se oprește instant):", retry_check("https://httpbin.org/status/404"))
print("Status 500 (încearcă de 3 ori):", retry_check("https://httpbin.org/status/500"))
print("Status 500 (încearcă de 2 ori, limitat):", retry_check("https://httpbin.org/status/500", attempts=2))
print("Conexiune picată (încearcă de 3 ori):", retry_check("http://this-site-does-not-exist.invalid"))
