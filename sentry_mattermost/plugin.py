from __future__ import absolute_import

from sentry import tagstore
from sentry.plugins.bases import notify
from sentry_plugins.base import CorePluginMixin
from sentry.http import safe_urlopen, is_valid_url
from sentry.utils.safe import safe_execute

try:
    from sentry.integrations import FeatureDescription, IntegrationFeatures
except ImportError:
    from sentry.integrations.base import FeatureDescription, IntegrationFeatures

import sentry_mattermost


def get_tags(event):
    tag_list = event.tags
    if not tag_list:
        return ()

    return (
        (tagstore.get_tag_key_label(k), tagstore.get_tag_value_label(k, v)) for k, v in tag_list
    )


class Mattermost(CorePluginMixin, notify.NotificationPlugin):
    title = 'Mattermost'
    slug = 'mattermost'
    description = 'Sends alerts to Mattermost channel based on Sentry alerts rules'
    version = sentry_mattermost.VERSION
    timeout = 3
    author = 'Nathan KREMER'
    author_url = 'https://github.com/xd3coder/sentry-mattermost'
    user_agent = 'sentry-webhooks/%s' % version
    feature_descriptions = [
        FeatureDescription(
            """
            Send notifications to Mattermost channel based on Sentry alerts rules
            """,
            IntegrationFeatures.ALERT_RULE,
        )
    ]

    def get_tag_list(self, name, project):
        option = self.get_option(name, project)
        if option:
            return set(tag.strip().lower() for tag in option.split(","))
        return None

    def is_configured(self, project):
        return bool(self.get_option("webhook", project))

    def render_notification(self, data, customFormat):
        if customFormat:
            template = customFormat
        else:
            template = "#### {project_name} - {env}\n{tags}\n\n{culprit}\n[{title}]({link})"
        return template.format(**data)


    def create_payload(self, event):
        group = event.group
        project = group.project

        tags = []
        included_tags = set(self.get_tag_list("included_tag_keys", project) or [])
        excluded_tags = set(self.get_tag_list("excluded_tag_keys", project) or [])
        for tag_key, tag_value in get_tags(event):
            key = tag_key.lower()
            std_key = tagstore.get_standardized_key(key)
            if included_tags and key not in included_tags and std_key not in included_tags:
                continue
            if excluded_tags and (key in excluded_tags or std_key in excluded_tags):
                continue
            if self.get_option("include_keys_with_tags", project) :
                tags.append("`{}: {}` ".format(tag_key, tag_value))
            else:
                tags.append("`{}` ".format(tag_value))

        data = {
            "title": group.message_short,
            "link": group.get_absolute_url(),
            "id": event.event_id,
            "culprit": group.culprit,
            "env": event.get_environment().name,
            "project_slug": group.project.slug,
            "project_name": group.project.name,
            "tags": " ".join(tags),
            "level": event.get_tag("level"),
            "message": event.message,
            "release": event.release,
        }

        icon_url = "https://xd3coder.github.io/image-host/sentry-mattermost/64/warning.jpg"
        if self.get_option("logo_match_level", project):
            icon_url = "https://xd3coder.github.io/image-host/sentry-mattermost/64/" + event.get_tag("level") + ".jpg"
        payload = {
            "username": self.get_option("username", project) or "Sentry",
            "icon_url": icon_url,
            "text": self.render_notification(data, self.get_option("custom_format", project))
        }
        return payload

    def get_config(self, project, **kwargs):
        return [
            {
                "name": "webhook",
                "label": "Webhook URL",
                "type": "url",
                "required": True,
                "help": "Your custom Mattermost webhook URL.",
            },
            {
                "name": "username",
                "label": "Bot Name",
                "type": "string",
                "placeholder": "e.g. Sentry",
                "default": "Sentry",
                "required": False,
                "help": "The name used in channel when publishing notifications.",
            },
            {
                "name": "custom_format",
                "label": "Formatted message",
                "type": "textarea",
                "placeholder": "",
                "required": False,
                "help": "Customize notification message, you can use markdown. More informations here https://github.com/xd3coder/sentry-mattermost",
            },
            {
                "name": "logo_match_level",
                "label": "Background color match notification level",
                "type": "bool",
                "required": False,
                "help": "Avatar in channel will use a color according to Sentry logging level.",
            },
            {
                "name": "include_keys_with_tags",
                "label": "Include tags keys in messages",
                "type": "bool",
                "required": False,
                "help": "Write keys before tags in rendered messages.",
            },
            {
                "name": "included_tag_keys",
                "label": "Included Tags",
                "type": "string",
                "required": False,
                "help":  "Only include these tags (comma separated list). Leave empty to include all."
            },
            {
                "name": "excluded_tag_keys",
                "label": "Excluded Tags",
                "type": "string",
                "required": False,
                "help": "Exclude these tags (comma separated list).",
            }
        ]

    def send_webhook(self, url, data):
        return safe_urlopen(
            url=url,
            json=data,
            timeout=self.timeout,
            user_agent=self.user_agent
        )

    def notify(self, notification, raise_exception=False):
        event = notification.event
        group = event.group
        project = group.project
        if not self.is_configured(project):
            return
        webhook = self.get_option("webhook", project).strip()
        payload = self.create_payload(event)
        return safe_execute(self.send_webhook(webhook, payload))
