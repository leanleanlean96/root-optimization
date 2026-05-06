class JWTException(Exception):
    pass

class TokenExpiredException(JWTException):
    pass


class InvalidTokenException(JWTException):
    pass


class InvalidTokenTypeException(JWTException):
    pass
