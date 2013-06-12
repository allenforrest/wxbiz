#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-16
Description: ���ܽ����㷨
Others:
Key Class&Method List:
    1. Cipher.encrypt: ����
    2. Cipher.decrypt: ����
History:
1. Date:
   Author:
   Modification:
"""
import base64
import hashlib
import random

class Cipher:
    """
    Class: Cipher
    Description: ���ܽ���
    Others:
    """
    CRYPT_KEY = 'acp_cipher'
    RAND_KEY_LENGTH = 8

    def __init__(self, crypt_key = CRYPT_KEY, rand_key_length = RAND_KEY_LENGTH):
        """
        Method: __init__
        Description: ��Կ��ʼ��
        Parameters:
            crypt_key: ��Կ
            rand_key_length: ���������
        """
        self.crypt_key = crypt_key
        if rand_key_length <= 0:
            raise ValueError('rand_key_length should be larger than 0')
        self.rand_key_length = rand_key_length

    def _generate_key(self, text, key, is_decrypt = False):
        """
        Method: _generate_key
        Description: ���ɼ�����Կ
        Parameters:
            text: ƽ��
            key: �û��ṩ����Կ
            is_decrypt: �Ƿ����
        """
        md5key = hashlib.md5(key).hexdigest()
        keya = md5key[0:16]
        keyb = md5key[16:32]
        if is_decrypt is True:
            keyc = text[0:self.rand_key_length]
        else:
            keyc = ''
            (quotient, remainder) = divmod(self.rand_key_length, 32)
            for i in range(quotient):
                rand = "%f" % random.random()
                keyc = keyc + hashlib.md5(rand).hexdigest()
            if remainder > 0:
                rand = "%f" % random.random()
                keyc = keyc + hashlib.md5(rand).hexdigest()[0:remainder]
            keyc = keyc.upper()
        crypted_key = keya + hashlib.md5(keyb + keyc).hexdigest()
        return (crypted_key, keyc)

    def _generate_password_box(self, crypted_key):
        """
        Method: _generate_password_box
        Description: �������뱾
        Parameters:
            crypted_key: ������Կ
        """
        key_length = len(crypted_key)
        rndkeys = []
        for i in range(0, 256):
            j = divmod(i, key_length)[1]
            rndkeys.append(crypted_key[j])
        j = 0
        for i in range(0, 256):
            j = divmod(j + ord(rndkeys[i]) + i, 256)[1]
            temp = rndkeys[i]
            rndkeys[i] = rndkeys[j]
            rndkeys[j] = temp
        return rndkeys

    def encrypt(self, plain, key = None):
        """
        Method: encrypt
        Description: ����
        Parameters:
            plain: ƽ��
            key: ��Կ
        Others: keyû�����õĳ��ϲ���ȱʡֵ
        """
        if key is None:
            key = self.crypt_key
        (crypted_key, keyc) = self._generate_key(plain, key)
        rndkeys = self._generate_password_box(crypted_key)
        i = 0
        j = 0
        encrypted_text = ''
        while i < len(plain):
            j = divmod(ord(rndkeys[i]) + j, 256)[1]
            encrypted_text = encrypted_text + "%c" % (ord(plain[i]) ^ ord(rndkeys[j]))
            i = i + 1
        return keyc + base64.encodestring(encrypted_text)

    def decrypt(self, encrypted_text, key = None):
        """
        Method: encrypt
        Description: ����
        Parameters:
            plain: ����
            key: ��Կ
        Others: keyû�����õĳ��ϲ���ȱʡֵ
        """
        if key is None:
            key = self.crypt_key
        (crypted_key, keyc) = self._generate_key(encrypted_text, key, True)
        rndkeys = self._generate_password_box(crypted_key)
        encrypted_text = base64.decodestring(encrypted_text[self.rand_key_length:])

        i = 0
        j = 0
        decrypted_text = ''
        while i < len(encrypted_text):
            j = divmod(ord(rndkeys[i]) + j, 256)[1]
            decrypted_text = decrypted_text + "%c" % (ord(encrypted_text[i]) ^ ord(rndkeys[j]))
            i = i + 1
        return decrypted_text

if __name__ == '__main__':
    cipher = Cipher()
    enc = cipher.encrypt("Oracle-1")
    print(enc)
    print(cipher.decrypt(enc))
