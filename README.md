# Sentry Mattermost

A Sentry plugin to send alerts to a Mattermost channel.
Based on the [Sentry-Slack](https://github.com/getsentry/sentry-slack) plugin.

## Installation

### Prerequisites

- A [Sentry self-hosted](https://develop.sentry.dev/self-hosted/) instance >= 24.x
- An incoming webhook configured in Mattermost

> For older Sentry versions (< 24.x), use [version 0.0.3](https://github.com/xd3coder/sentry-mattermost/tree/v0.0.3) of the plugin.

### 1. Create a webhook in Mattermost

1. In Mattermost, go to **Integrations** > **Incoming Webhooks**
2. Click **Add Incoming Webhook**
3. Select the target channel and give it a name (e.g. "Sentry")
4. Copy the generated webhook URL (e.g. `https://mattermost.example.com/hooks/xxx-xxx-xxx`)

### 2. Install the plugin in Sentry

In your Sentry self-hosted installation folder, edit (or create) the `sentry/enhance-image.sh` file:

```bash
#!/bin/bash
apt-get update && apt-get install -y git
pip install git+https://github.com/xd3coder/sentry-mattermost.git@master#egg=sentry-mattermost
```

Then rebuild the image and restart:

```bash
./install.sh
docker compose restart web worker cron
```

### 3. Enable the plugin in Sentry

1. Go to **Settings** > **Integrations** > **Legacy Integrations** (or **All Integrations**)
2. Find **Mattermost** and click **Configure**
3. Select the relevant project
4. Paste your Mattermost webhook URL
5. Configure additional options as needed (bot name, channel, custom format, etc.)

### 4. Create an alert rule

1. Go to **Alerts** > **Create Alert Rule**
2. Configure the trigger conditions (e.g. new issue, regression, etc.)
3. In the **THEN** section, add the action **Send a notification via Mattermost**
4. Save the rule

## Configuration

### Available options

| Option | Description | Required |
|--------|-------------|----------|
| Webhook URL | Mattermost webhook URL | Yes |
| Bot Name | Display name in the channel (default: "Sentry") | No |
| Channel Name | Override to a specific channel | No |
| Formatted message | Custom template (supports markdown) | No |
| Background color match level | Color the avatar based on severity level | No |
| Include tags keys | Display tag keys alongside values | No |
| Included Tags | Comma-separated list of tags to include | No |
| Excluded Tags | Comma-separated list of tags to exclude | No |

### Message format

By default, messages look like this:

![alt text](https://xd3coder.github.io/image-host/sentry-mattermost/output.jpg "Output")

You can customize the format using these variables:

| Variable | Description |
|----------|-------------|
| `{project_slug}` | Project slug |
| `{project_name}` | Project name |
| `{env}` | Environment |
| `{title}` | Event title |
| `{id}` | Event ID |
| `{link}` | Link to the issue |
| `{level}` | Severity level |
| `{tags}` | Collection of tags |
| `{message}` | Error message |
| `{culprit}` | Exception source |
| `{release}` | Release version |

Default template:

```
#### {project_name} - {env}
{tags}

{culprit}
[{title}]({link})
```

## Changelog

### v1.0.0

- Removed dependency on deprecated `sentry-plugins` package (`CorePluginMixin`)
- Removed dependency on deprecated `sentry.tagstore` API
- Updated event attribute access for Sentry 24+ (`group.title` instead of `group.message_short`)
- Added fallbacks for environment and release fields
- Fixed `safe_execute` call to pass function reference correctly
