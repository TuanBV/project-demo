"""
Common repository
"""
class CommonRepository():
    """
    Common repository
    """
    def __init__(self, session_factory, session_factory_read):
        self.session_factory = session_factory
        self.session_factory_read = session_factory_read
