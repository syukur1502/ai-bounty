import google.generativeai as genai

# TEMPEL API KEY ANDA DI SINI
API_KEY = "AIzaSyCZIYYvcOniVtb_gRU9HomonAtQANYtSk8"

try:
    genai.configure(api_key=API_KEY)
    print("📋 SEDANG MENGAMBIL DAFTAR MODEL YANG TERSEDIA...")
    print("------------------------------------------------")
    
    found = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ TERSEDIA: {m.name}")
            found = True
            
    if not found:
        print("❌ Tidak ada model yang ditemukan. Cek API Key Anda.")
        
except Exception as e:
    print(f"❌ ERROR: {e}")