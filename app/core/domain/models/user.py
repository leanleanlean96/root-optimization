import hashlib
import secrets
from core.domain.exceptions import DomainError


class User_name():
    def __init__(self, name: str):
        if len(name) < 3 or len(name) > 30:
            raise DomainError("Name must be between 3 and 30 characters long")
        self.name = name


class Email():
    def __init__(self, email: str):
        if "@" not in email:
            raise DomainError("Invalid email address")
        self.email = email

class Password():
    def __init__(self, password: str, hashed: bool = False):
        if not hashed and len(password) < 8:
            raise DomainError("Password must be at least 8 characters long")
        
        if hashed:
            self.password = password
        else:
            self.password = self._hash_password(password)
    
    def _hash_password(self, password: str) -> str:
        """Хэширование пароля через PBKDF2 (встроенный в Python)"""
        salt = secrets.token_hex(16)
        hash_value = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode('utf-8'), 
            salt.encode('utf-8'), 
            100000
        )
        return f"pbkdf2_sha256$100000${salt}${hash_value.hex()}"
    
    def verify(self, plain_password: str) -> bool:
        """Проверка пароля"""
        try:
            parts = self.password.split('$')
            if len(parts) != 4:
                return False
            
            algorithm = parts[0]
            iterations = int(parts[1])
            salt = parts[2]
            stored_hash = parts[3]
            
            new_hash = hashlib.pbkdf2_hmac(
                'sha256',
                plain_password.encode('utf-8'),
                salt.encode('utf-8'),
                iterations
            ).hex()
            
            return new_hash == stored_hash
        except Exception:
            return False


class User():
    def __init__(self, id, user_name: User_name, email: Email, password: Password, is_active: bool = True):
        self.id = id
        self.user_name = user_name
        self.password = password
        self.email = email
        self.is_active = is_active

    @staticmethod
    def register(user_name: str, email: str, password: str) -> "User":
        user_name_obj = User_name(user_name)    
        email_obj = Email(email)
        password_obj = Password(password, hashed=False)
        return User(id=None, user_name=user_name_obj, email=email_obj, password=password_obj)
        
    def change_email(self, new_email: str):
        self.email = Email(new_email)

    def change_name(self, new_name: str):
        self.user_name = User_name(new_name)

    def change_password(self, new_password: str):
        self.password = Password(new_password, hashed=False)
    
    def verify_password(self, password: str) -> bool:
        return self.password.verify(password)