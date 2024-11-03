import json
from web3 import Web3

# Load konfigurasi
with open('config.json') as config_file:
    config = json.load(config_file)

# Menampilkan semua jaringan yang tersedia
print("=======================================")
print("           Pilih Jaringan")
print("=======================================")
network_options = config['networks']
for index, (network_name, details) in enumerate(network_options.items(), start=1):
    print(f"{index}. {network_name}")

# Meminta pengguna untuk memilih jaringan
network_choice = input("Silakan pilih jaringan (masukkan nomor): ")
network_choice_index = int(network_choice) - 1

if 0 <= network_choice_index < len(network_options):
    selected_network = list(network_options.keys())[network_choice_index]
    selected_details = network_options[selected_network]
    rpc_url = selected_details['rpc_url']
    token_contract = selected_details['token_contract']
    chain_id = selected_details['chain_id']

    # Koneksi ke jaringan yang dipilih
    web3 = Web3(Web3.HTTPProvider(rpc_url))

    # Cek koneksi
    if not web3.isConnected():
        print("Tidak terhubung ke jaringan")
        exit()

    # Load private key
    with open('private_key.txt') as pk_file:
        private_key = pk_file.read().strip()

    # Alamat pengirim
    sender_address = web3.eth.account.from_key(private_key).address

    # Load alamat penerima
    with open('addresses.txt') as address_file:
        recipient_addresses = [line.strip() for line in address_file if line.strip()]

    # Alamat kontrak token dan ABI-nya
    token_address = token_contract
    token_abi = [
        # Masukkan ABI kontrak token di sini
    ]

    # Inisialisasi kontrak token
    token_contract_instance = web3.eth.contract(address=token_address, abi=token_abi)

    # Menampilkan jumlah alamat penerima
    print("=======================================")
    print("          Transfer Token")
    print("=======================================")
    print(f"Jumlah alamat penerima: {len(recipient_addresses)}")
    print("Alamat penerima:")
    for index, address in enumerate(recipient_addresses, start=1):
        print(f"{index}. {address}")

    # Mengambil saldo ETH di wallet pengirim
    balance = web3.eth.getBalance(sender_address)
    eth_balance = web3.fromWei(balance, 'ether')
    print(f"\nSaldo ETH di wallet pengirim: {eth_balance} ETH")

    # Menanyakan pilihan pengiriman
    choice = input("\nApakah Anda ingin mengirim ke seluruh penerima (ketik 'semua') atau memilih penerima tertentu (ketik 'pilih')? (ketik 'keluar' untuk membatalkan) ").strip().lower()

    if choice == 'keluar':
        print("Pengiriman dibatalkan.")
        exit()
    elif choice == 'pilih':
        selected_indices = input("Anda memilih untuk mengirim ke penerima tertentu. Silakan pilih nomor penerima (pisahkan dengan koma jika lebih dari satu): ")
        selected_indices = [int(i.strip()) - 1 for i in selected_indices.split(',')]
        selected_addresses = [recipient_addresses[i] for i in selected_indices]
        print(f"Alamat penerima yang dipilih: {selected_addresses}")
        # Lanjutkan ke proses pengiriman menggunakan selected_addresses
    elif choice == 'semua':
        print("Anda memilih untuk mengirim ke semua penerima.")
        # Lanjutkan ke proses pengiriman menggunakan recipient_addresses
    else:
        print("Pilihan tidak dikenali, silakan coba lagi.")
else:
    print("Pilihan jaringan tidak valid.")
