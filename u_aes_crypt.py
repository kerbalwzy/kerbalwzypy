# -*- coding:utf-8 -*-
# @Author: wzy
# @Time: 2020-12-3 11:11:30
# AES 加解密, 支持ECB和CBC两种模式

from Crypto.Cipher import AES

__all__ = ['aes_encrypt', 'aes_decrypt']


def aes_full(data):
    """
    补全明文, 16位
    :param data:
    """
    if type(data) == str:
        data = data.encode()
    length = 16 - (len(data) % 16)
    data += bytes([length]) * length
    return data


def aes_encrypt(plain_text, key: str, model: str = "ECB", iv: str = None):
    """AES加密
    :param plain_text:    明文 string or bytes
    :param model:       模式 ECB / CBC
    :param key:         密钥
    :param iv:          初始向量
    :return: bytes      密文
    """
    assert model in ["ECB", "CBC"], ValueError("model只能是'ECB'或'CBC'")
    plain_text = aes_full(plain_text)
    if model == "CBC":
        aes = AES.new(key, AES.MODE_CBC, iv)
    else:
        aes = AES.new(key, model)
    encrypt_text = aes.encrypt(plain_text)
    return encrypt_text


def aes_decrypt(cipher_text, key: str, model: str = "ECB", iv: str = None):
    """AES解密
    :param cipher_text:  密文 bytes
    :param model:       模式 ECB / CBC
    :param key:         密钥
    :param iv:          初始向量
    :return: bytes      明文
    """
    assert model in ["ECB", "CBC"], ValueError("model只能是'ECB'或'CBC'")
    if model == "CBC":
        aes = AES.new(key, AES.MODE_CBC, iv)
    else:
        aes = AES.new(key, model)
    decrypt_text = aes.decrypt(cipher_text)
    padding_bytes = decrypt_text[-1]
    decrypt_text = decrypt_text[:-1 * padding_bytes]
    return decrypt_text
