import json
import os
from datetime import datetime
from typing import Dict, Any, List
from cryptography.fernet import Fernet
from app.models.schemas import AssessmentResponse

class SecurityManager:
    """
    Handles encryption/decryption of local data.
    In a real app, the key would be derived from a user password or secure keystore.
    """
    def __init__(self, key_path: str = "data/secret.key"):
        self.key_path = key_path
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)

    def _load_or_generate_key(self) -> bytes:
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(self.key_path), exist_ok=True)
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
            return key

    def encrypt_data(self, data: Dict[str, Any]) -> bytes:
        json_bytes = json.dumps(data, default=str).encode('utf-8')
        return self.cipher.encrypt(json_bytes)

    def decrypt_data(self, encrypted_data: bytes) -> Dict[str, Any]:
        decrypted_bytes = self.cipher.decrypt(encrypted_data)
        return json.loads(decrypted_bytes.decode('utf-8'))

class LocalStorage:
    """
    Persists assessments to a local file (append-only log).
    Data is fully encrypted at rest.
    """
    def __init__(self, storage_path: str = "data/assessments.enc"):
        self.storage_path = storage_path
        self.security = SecurityManager()
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def save_assessment(self, assessment: AssessmentResponse):
        encrypted_record = self.security.encrypt_data(assessment.dict())
        
        # Append to file with newline delimiter (simple log format)
        with open(self.storage_path, "ab") as f:
            f.write(encrypted_record + b"\n")

    def load_recent_assessments(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Reads the last N assessments.
        """
        if not os.path.exists(self.storage_path):
            return []
            
        results = []
        try:
            with open(self.storage_path, "rb") as f:
                lines = f.readlines()
                
            # Read from end
            for line in reversed(lines):
                if len(results) >= limit:
                    break
                if line.strip():
                    try:
                        data = self.security.decrypt_data(line.strip())
                        results.append(data)
                    except Exception:
                        continue # Skip corrupted/unreadable lines
                        
            return results
        except Exception as e:
            print(f"Error loading data: {e}")
            return []
