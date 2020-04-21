# Sentry Mattermost

A Sentry plugin to send alerts to Mattermost channel.
Based on the [Sentry-Slack](https://github.com/getsentry/sentry-slack) plugin

### Installation 
Add the plugin to your `requirements.txt`
```
git+https://github.com/xd3coder/sentry-mattermost.git@dev#egg=sentry-mattermost
```
- Create a new webhook in Mattermost
- Go to `Organizations` -> `projects`
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