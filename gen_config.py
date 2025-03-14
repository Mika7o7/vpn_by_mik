import os
import subprocess
from datetime import datetime

# Путь к конфигурационному файлу сервера
SERVER_CONFIG_PATH = "/etc/wireguard/wg0.conf"

# Директория для хранения конфигураций пользователей
USER_CONFIGS_DIR = "users/configs"  # Укажите путь к директории

# IP-адрес и порт сервера
SERVER_ENDPOINT = "217.18.63.138:53421"

# DNS-сервер
DNS_SERVER = "8.8.8.8"

# Диапазон IP-адресов для клиентов
CLIENT_IP_RANGE = "192.168.2.0/24"


def generate_keys():
    """Генерация приватного и публичного ключей."""
    private_key = subprocess.run(["wg", "genkey"], capture_output=True, text=True).stdout.strip()
    public_key = subprocess.run(["wg", "pubkey"], input=private_key, capture_output=True, text=True).stdout.strip()
    return private_key, public_key


def generate_client_config(private_key, client_ip, public_key_server):
    """Генерация конфигурационного файла для клиента."""
    config = f"""[Interface]
PrivateKey = {private_key}
Address = {client_ip}/24
DNS = {DNS_SERVER}

[Peer]
PublicKey = {public_key_server}
Endpoint = {SERVER_ENDPOINT}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20
"""
    return config


def add_peer_to_server_config(public_key_client, client_ip):
    """Добавление нового пира в конфигурацию сервера."""
    peer_config = f"""
[Peer]
PublicKey = {public_key_client}
AllowedIPs = {client_ip}/32
"""
    with open(SERVER_CONFIG_PATH, "a") as f:
        f.write(peer_config)


def get_next_client_ip():
    """Получение следующего доступного IP-адреса для клиента."""
    with open(SERVER_CONFIG_PATH, "r") as f:
        lines = f.readlines()

    used_ips = set()
    for line in lines:
        if "AllowedIPs" in line:
            ip = line.split("=")[1].strip().split("/")[0]
            used_ips.add(ip)

    base_ip = "192.168.2."
    for i in range(2, 255):  # Начинаем с 192.168.2.2
        ip = f"{base_ip}{i}"
        if ip not in used_ips:
            return ip
    raise ValueError("Нет доступных IP-адресов в диапазоне.")


def reload_wireguard():
    """Перезагрузка конфигурации WireGuard."""
    subprocess.run(["wg-quick", "down", "wg0"], check=True)
    subprocess.run(["wg-quick", "up", "wg0"], check=True)


def create_client_config(user_id):
    """Создание конфигурации для нового пользователя."""
    # Генерация ключей
    private_key_client, public_key_client = generate_keys()

    # Получение следующего IP-адреса
    client_ip = get_next_client_ip()

    # Чтение публичного ключа сервера
    with open(SERVER_CONFIG_PATH, "r") as f:
        for line in f:
            if "PrivateKey" in line:
                private_key_server = line.split("=")[1].strip()
                public_key_server = subprocess.run(
                    ["wg", "pubkey"], input=private_key_server, capture_output=True, text=True
                ).stdout.strip()
                break

    # Генерация конфигурационного файла для клиента
    client_config = generate_client_config(private_key_client, client_ip, public_key_server)

    # Сохранение конфигурации в файл
    os.makedirs(USER_CONFIGS_DIR, exist_ok=True)
    config_file_path = os.path.join(USER_CONFIGS_DIR, f"client_{user_id}.conf")
    with open(config_file_path, "w") as f:
        f.write(client_config)

    # Добавление нового пира в конфигурацию сервера
    add_peer_to_server_config(public_key_client, client_ip)

    # Перезагрузка WireGuard
    reload_wireguard()

    return config_file_path