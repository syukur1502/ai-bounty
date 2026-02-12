import google.generativeai as genai

# 1. Pastikan API KEY Anda ada di sini (Cek tanda kutipnya!)
API_KEY = " " 

print("Sedang mengetes koneksi ke Google...")

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Sapa saya dalam 1 kata")
    print(f"✅ BERHASIL! Jawaban AI: {response.text}")
except Exception as e:
    print(f"❌ GAGAL! Ini error aslinya:\n{e}")
