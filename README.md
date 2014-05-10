better-notification
===================

Better notifications for Nagios/Icinga


## Templates

Templates are stored in `/etc/better-notifications/templates/`. better-notifications use the Jinja2 template engine.

The following values are used for template selection

* `backend-name`. The name of the backend from `backends.cfg` (the section name, **not** the value of the type attribute).
* `alert-type`. Either 'service' or 'host'. Depends on the presence of the `SERVICEPROBLEMID` or the value of the `--alert` argument.
* `notification-type`: The lowercased value of the `NOTIFICATIONTYPE` variable

See [The Icinga documentation](http://docs.icinga.org/latest/en/macrolist.html) for a list of valid variables and their values.

Templates are resolved in the following order:

For messages:

* `<backend-name>/<alert-type>_<notification-type>.tpl`
* `<backend-name>/<notification-type>.tpl`
* `<backend-name>/<alert-type>.tpl`
* `<service|host>_<notification-type>.tpl`
* `<notification-type>.tpl`
* `<alert-type>.tpl`
* `message.tpl`

For subjects:

* `<backend-name>/<alert-type>_<notification-type>_subject.tpl`
* `<backend-name>/<notification-type>_subject.tpl`
* `<backend-name>/<alert-type>_subject.tpl`
* `<alert-type>_<notification-type>_subject.tpl`
* `<notification-type>_subject.tpl`
* `<alert-type>_subject.tpl`
* `subject.tpl`

To debug template selection run `better-notify` with `-vvvv`.


## Backends

Backends are configured in `/etc/better-notifications/backend.cfg`. 


### Email

This backends sends the notification (obviously) via email. Per default, a local SMTP server is used. 
The RECIPIENT argument should be one or more email addresses. 


### Pushover

With this backend, notification are sent via https://pushover.net/. You have to install the pushover app for iOS/Android and sign up with pushover to get an api key.
The RECIPIENT argument should be either a user or a delivery group key.