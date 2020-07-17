REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        # 'rest_framework.filters.OrderingFilter',
    ],
    'SEARCH_PARAM':'search',
    # 'ORDERING_PARAM':'ordering',
}

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read' : 'Read scope',
        'write' : 'Write scope',
        'groups' : 'Access to your groups'
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
)