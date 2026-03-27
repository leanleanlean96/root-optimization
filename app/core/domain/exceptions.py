class DomainError(Exception):
    """Base class for domain errors."""
    pass

class BusinessError(DomainError):
    """Ошибки бизнес-логики, которые могут возникать при выполнении операций."""
    pass
