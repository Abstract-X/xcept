

class XceptWarning(UserWarning):
    """Base class for xcept warnings."""
    pass


class MissingTemplateWarning(XceptWarning):
    """Class for warnings about a missing message template."""


class MissingFieldWarning(XceptWarning):
    """Class for warnings about missing replacement fields in
    a message template.
    """


class UnknownFieldWarning(XceptWarning):
    """Class for warnings about unknown replacement fields
    in a message template.
    """
