try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-mattermost').version
except Exception as e:
    VERSION = 'unknown'