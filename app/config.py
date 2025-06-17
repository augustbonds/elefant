"""
Application configuration and constants
"""


class Config:
    """Main configuration class with application constants"""
    
    # Pagination settings
    DEFAULT_PAGE_SIZE = 20
    
    # Search and autocomplete settings  
    MAX_AUTOCOMPLETE_SUGGESTIONS = 5
    MIN_AUTOCOMPLETE_CHARS = 1
    
    # Form validation limits
    MAX_TITLE_LENGTH = 200
    MAX_DESCRIPTION_LENGTH = 1000
    
    # Default user (TODO: move to proper authentication system)
    DEFAULT_USER = {'username': 'boonspoj'}
    
    # Search settings
    TAG_PREFIX = '#'


class DevelopmentConfig(Config):
    """Development-specific configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production-specific configuration"""
    DEBUG = False


# Default configuration
config = DevelopmentConfig()