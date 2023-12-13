from outline_vpn.outline_vpn import OutlineVPN, OutlineKey
from config import CERT_SHA256, OUTLINE_API_URL


client = OutlineVPN(api_url=OUTLINE_API_URL, cert_sha256=CERT_SHA256)


def create_user_outline(data) -> OutlineKey:
    new_key = client.create_key(data["user_name"])
    return new_key


def delete_user_outline(key_id: str):
    client.delete_key(key_id)


def block_user_outline(key_id: str):
    client.add_data_limit(key_id, 1000 * 1000 * 1)


def unblock_user_outline(key_id: str):
    client.delete_data_limit(key_id)
