import time
import google.generativeai as genai
import yfinance as yf # <--- Library Baru
from web3 import Web3

# ================= KONFIGURASI =================
# 1. TEMPEL API KEY GOOGLE ANDA DI SINI
API_KEY = "" 

# 2. ALAMAT KONTRAK (Sama seperti kemarin)
CONTRACT_ADDRESS = ""
# ===============================================

RPC_URL = "https://1rpc.io/sepolia"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    print("❌ Gagal konek. Pastikan 'yarn chain' jalan!")
    exit()

# Setup AI
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash') # Pakai model terbaru Anda
except Exception as e:
    print(f"❌ Error Setup AI: {e}")

agent_private_key = "0x3d6854c7826472dea72ba1eb3a6b62b1f5dd3782363ee0c2d1d67a2ce39924c8"
agent_account = w3.eth.account.from_key(agent_private_key)

contract_abi = [
    {"inputs": [], "name": "taskCount", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "tasks", "outputs": [{"internalType": "uint256", "name": "id", "type": "uint256"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "uint256", "name": "reward", "type": "uint256"}, {"internalType": "bool", "name": "isCompleted", "type": "bool"}, {"internalType": "address", "name": "completedBy", "type": "address"}, {"internalType": "string", "name": "result", "type": "string"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "_taskId", "type": "uint256"}, {"internalType": "string", "name": "_result", "type": "string"}], "name": "completeTask", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

print(f"🤖 ROBOT PIALANG SIAP! (Address: {agent_account.address}...)")
print("👀 Menunggu perintah cek harga...")

processed_tasks = set()

# Fungsi untuk Cek Harga Saham/Kripto
def cek_pasar(query):
    try:
        symbol = ""
        # Logika sederhana deteksi simbol
        if "btc" in query.lower() or "bitcoin" in query.lower():
            symbol = "BTC-USD"
        elif "eth" in query.lower() or "ethereum" in query.lower():
            symbol = "ETH-USD"
        elif "bca" in query.lower():
            symbol = "BBCA.JK" # Kode saham BCA di Yahoo Finance
        elif "bri" in query.lower():
            symbol = "BBRI.JK"
        elif "telkom" in query.lower():
            symbol = "TLKM.JK"
        else:
            return None # Bukan tanya harga yang kita kenal

        print(f"📈 Mengambil data live untuk: {symbol}...")
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info['last_price']
        
        # Format Rupiah kalau saham indo
        if ".JK" in symbol:
            return f"Harga {symbol} saat ini: Rp {price:,.0f}"
        else:
            return f"Harga {symbol} saat ini: ${price:,.2f} USD"

    except Exception as e:
        print(f"Error Market: {e}")
        return None

while True:
    try:
        count = contract.functions.taskCount().call()
        if count > 0:
            task = contract.functions.tasks(count).call()
            task_id = task[0]
            desc = task[1]
            is_done = task[3]

            if not is_done and task_id not in processed_tasks:
                print(f"\n[!] PERINTAH BARU: '{desc}'")
                print("🧠 Sedang menganalisa jenis tugas...")
                
                final_answer = ""
                
                # 1. COBA CEK PASAR DULU
                market_data = cek_pasar(desc)
                
                if market_data:
                    # Kalau ini soal harga, kita gabungkan Data + AI
                    print("💰 Ini tugas Cek Harga! Data ditemukan.")
                    prompt = f"User bertanya: '{desc}'. Data pasar real-time: '{market_data}'. Buatlah komentar singkat lucu tentang harga ini."
                    ai_comment = model.generate_content(prompt).text.strip()
                    final_answer = f"{market_data}. ({ai_comment})"
                else:
                    # Kalau bukan soal harga, tanya AI biasa
                    print("🗣️ Ini tugas ngobrol biasa.")
                    final_answer = model.generate_content(f"Jawab singkat padat: {desc}").text.strip()
                
                print(f"💡 Jawaban Final: {final_answer}")
                
                # Kirim ke Blockchain
                tx = contract.functions.completeTask(task_id, final_answer).build_transaction({
                    'from': agent_account.address,
                    'nonce': w3.eth.get_transaction_count(agent_account.address),
                    'gas': 1000000,
                    'gasPrice': w3.to_wei('2', 'gwei')
                })
                signed_tx = w3.eth.account.sign_transaction(tx, agent_private_key)
                w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                
                print("✅ Lapor ke Blockchain SUKSES!")
                processed_tasks.add(task_id)
        time.sleep(2)
    except Exception as e:
        print(f"Error Loop: {e}")
        time.sleep(10)
