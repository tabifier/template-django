from notifications.channels import SLACK, DB, EMAIL


notification_events = {
    'api.roller_auth.user.signup': {'channels': [SLACK, EMAIL, DB]},
    'api.roller_auth.user.login': {'channels': [SLACK, DB]},
    'api.roller_auth.user.logout': {'channels': [DB]},
    'api.roller_auth.email.signup_verification:request': {'channels': [DB, EMAIL]},
    'api.roller_auth.email.verification:request': {'channels': [DB, EMAIL]},
    'api.roller_auth.email.verification:sent': {'channels': [DB]},
    'api.roller_auth.email.verification:verified': {'channels': [DB]},
    'api.roller_auth.profile.picture_raw:uploaded': {'channels': [DB]},
    'api.roller_auth.profile.picture_raw:deleted': {'channels': [DB]},
    'api.roller_auth.profile.generated_pictures:uploaded': {'channels': [DB]},
    'api.roller_auth.profile.generated_pictures:deleted': {'channels': [DB]},
    'api.notifications.slack.ping': {'channels': [SLACK]},
}
