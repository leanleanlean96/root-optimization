class UnauthorizedException(Exception):
    pass


class TokenExpiredException(Exception):
    pass


class InvalidTokenException(Exception):
    pass


class InvalidTokenTypeException(Exception):
    pass