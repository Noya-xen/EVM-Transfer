import json
import time
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
    if not web3.is_connected():
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
    balance = web3.eth.get_balance(sender_address)
    eth_balance = web3.from_wei(balance, 'ether')
    print(f"\nSaldo ETH di wallet pengirim: {eth_balance} ETH")

    # Menanyakan pilihan pengiriman
    print("\n=======================================")
    print("          Pilih Opsi Pengiriman")
    print("=======================================")
    print("1. Kirim ke semua penerima")
    print("2. Kirim ke alamat tertentu")
    print("3. Keluar")

    choice = input("Silakan pilih opsi (masukkan nomor): ").strip()

    if choice == '3':
        print("Pengiriman dibatalkan.")
        exit()
    elif choice == '2':
        selected_indices = input("Anda memilih untuk mengirim ke penerima tertentu. Silakan pilih nomor penerima (pisahkan dengan koma jika lebih dari satu): ")
        selected_indices = [int(i.strip()) - 1 for i in selected_indices.split(',')]
        selected_addresses = [recipient_addresses[i] for i in selected_indices]
        print(f"Alamat penerima yang dipilih: {selected_addresses}")

        amount = input("Masukkan jumlah token yang akan dikirim ke setiap penerima: ")
        amount = web3.to_wei(float(amount), 'ether')  # Mengonversi jumlah ke Wei

        for recipient in selected_addresses:
            # Dapatkan nonce terbaru sebelum mengirim
            nonce = web3.eth.get_transaction_count(sender_address)

            transaction = {
                'to': recipient,
                'value': amount,
                'gas': 2000000,  # Tentukan gas limit sesuai kebutuhan
                'gasPrice': web3.eth.gas_price,  # Gunakan harga gas saat ini
                'nonce': nonce,
                'chainId': chain_id
            }

            # Tanda tangani transaksi
            signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

            # Kirim transaksi
            while True:  # Ulangi hingga transaksi berhasil
                try:
                    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                    print(f'Transaksi berhasil dikirim ke {recipient}. Hash: {txn_hash.hex()}')
                    time.sleep(5)  # Tunggu selama 5 detik sebelum mengirim transaksi berikutnya
                    break  # Keluar dari loop jika transaksi berhasil
                except ValueError as e:
                    if 'replacement transaction underpriced' in str(e):
                        # Naikkan harga gas jika ada kesalahan
                        transaction['gasPrice'] = int(transaction['gasPrice'] * 1.1)  # Naikkan 10%
                        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)  # Tanda tangani ulang transaksi
                    elif 'nonce too low' in str(e):
                        # Jika nonce terlalu rendah, ambil nonce terbaru
                        nonce = web3.eth.get_transaction_count(sender_address)
                        transaction['nonce'] = nonce
                        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)  # Tanda tangani ulang transaksi
                    else:
                        print(f'Error mengirim transaksi ke {recipient}: {e}')
                        break

    elif choice == '1':
        print("Anda memilih untuk mengirim ke semua penerima.")
        amount = input("Masukkan jumlah token yang akan dikirim ke setiap penerima: ")
        amount = web3.to_wei(float(amount), 'ether')  # Mengonversi jumlah ke Wei

        for recipient in recipient_addresses:
            # Dapatkan nonce terbaru sebelum mengirim
            nonce = web3.eth.get_transaction_count(sender_address)

            transaction = {
                'to': recipient,
                'value': amount,
                'gas': 2000000,  # Tentukan gas limit sesuai kebutuhan
                'gasPrice': web3.eth.gas_price,  # Gunakan harga gas saat ini
                'nonce': nonce,
                'chainId': chain_id
            }

            # Tanda tangani transaksi
            signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

            # Kirim transaksi
            while True:  # Ulangi hingga transaksi berhasil
                try:
                    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                    print(f'Transaksi berhasil dikirim ke {recipient}. Hash: {txn_hash.hex()}')
                    time.sleep(5)  # Tunggu selama 5 detik sebelum mengirim transaksi berikutnya
                    break  # Keluar dari loop jika transaksi berhasil
                except ValueError as e:
                    if 'replacement transaction underpriced' in str(e):
                        # Naikkan harga gas jika ada kesalahan
                        transaction['gasPrice'] = int(transaction['gasPrice'] * 1.1)  # Naikkan 10%
                        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)  # Tanda tangani ulang transaksi
                    elif 'nonce too low' in str(e):
                        # Jika nonce terlalu rendah, ambil nonce terbaru
                        nonce = web3.eth.get_transaction_count(sender_address)
                        transaction['nonce'] = nonce
                        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)  # Tanda tangani ulang transaksi
                    else:
                        print(f'Error mengirim transaksi ke {recipient}: {e}')
                        break
    else:
        print("Pilihan tidak dikenali, silakan coba lagi.")
else:
    print("Pilihan jaringan tidak valid.")
