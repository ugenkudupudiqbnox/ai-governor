class PolicyError(Exception):
    """Base class for policy errors."""


class PolicyInheritanceError(PolicyError):
    pass


class PolicyCycleError(PolicyInheritanceError):
    pass


class PolicyVersionMismatchError(PolicyInheritanceError):
    pass

