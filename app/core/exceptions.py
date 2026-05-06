class JWTException(Exception):
    pass

class UnauthorizedException(JWTException):
    pass


class TokenExpiredException(JWTException):
    pass


class InvalidTokenException(JWTException):
    pass


class InvalidTokenTypeException(JWTException):
    pass
