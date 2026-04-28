import bcrypt


class EncryptionService:
    @staticmethod
    def hash_password(pwd: str) -> str:
        return bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode()

    @staticmethod
    def check_password(pwd: str, hashed_pwd: str) -> bool:
        return bcrypt.checkpw(pwd.encode("utf-8"), hashed_pwd.encode("utf-8"))