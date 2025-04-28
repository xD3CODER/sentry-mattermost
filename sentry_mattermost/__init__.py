import importlib.metadata

try:
    VERSION = importlib.metadata.version('sentry-mattermost')
except Exception as e:
    VERSION = 'unknown'
