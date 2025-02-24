# Sentry Mattermost

A Sentry plugin to send alerts to Mattermost channel.
Based on the [Sentry-Slack](https://github.com/getsentry/sentry-slack) plugin

### Installation 

#### Sentry versions >= 22.6.0
In Sentry installation folder go to the `sentry/enhance-image.sh` (if file does not exist copy `sentry/enhance-image.example.sh`)
Add next lines:
```
apt-get update && apt-get install -y git
pip install git+https://github.com/xd3coder/sentry-mattermost.git@dev#egg=sentry-mattermost
```

#### Legacy Sentry versions (<22.6.0)
Add the plugin to your `requirements.txt` (if file does not exist copy `sentry/requirements.example.txt`):
```
git+https://github.com/xd3coder/sentry-mattermost.git@dev#egg=sentry-mattermost
```

#### Configuration Steps
- Create a new webhook in Mattermost
- Go to `Organizations` -> `Projects`
- Select the project you want then go to `Legacy integrations` -> `Mattermost`
- Set your webhook URL
- Add new alert rules in `Alerts` -> `New alert rule` to trigger Mattermost plugin


### Configuration

By default the incoming messages looks like this:

![alt text](https://xd3coder.github.io/image-host/sentry-mattermost/output.jpg "Output")

You can override this configuration by defining your own template.

These are available fields:

| Field         | Description    
| ------------- |:-------------:|
| project_slug  | current project slug |
| project_name  | current project name      |  
| env | current environment  | 
|title | title of event |
| id | id of event      | 
| link | link to issue      | 
| level | level of issue     | 
| tags | collection of tags     | 
|message| error message |
| culprit | exception culprit  |

The default template is :

```
#### {project_name} - {env}
{tags}

{culprit}
[{title}]({link})
```
