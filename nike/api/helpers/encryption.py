"""
Encryption
"""
import hashlib


def hash256(password):
  return hashlib.sha256(password.encode('utf-8')).hexdigest()
