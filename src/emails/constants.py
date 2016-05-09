class EmailTypes(object):
    AUTH_WELCOME_EMAIL = "auth__welcome_email"
    AUTH_VERIFY_SIGNUP_EMAIL = "auth__verify_signup_email"


EMAILS = {}

EMAILS[EmailTypes.AUTH_WELCOME_EMAIL] = {
    "is_active": False,
    "html_template": "emails/action-template.html",
    "text_template": "emails/action-template.txt",
    "subject": "",
    "sender": "EMAIL SUBJECT",
    "message": u"""EMAIL MESSAGE""",
    "title": u"Title",
    "title_color": "",
    "signature": {
        "sign_off": "Best,",
        "name": "First Last Name",
        "email": "first@djangoapp.com",
        "email_subject": "",
        "tile": "",
    },
    "cta_i": {
        "button_title": "Confirm Email Address",
        "button_color": "",
        "button_link": "",
        "message": "",
    }
}


EMAILS[EmailTypes.AUTH_VERIFY_SIGNUP_EMAIL] = {
    "is_active": False,
    "html_template": "emails/action-template.html",
    "text_template": "emails/action-template.txt",
    "subject": "",
    "sender": "EMAIL SUBJECT",
    "message": u"""EMAIL MESSAGE""",
    "title": u"Title",
    "title_color": "",
    "signature": {
        "sign_off": "Best,",
        "name": "First Last Name",
        "email": "first@djangoapp.com",
        "email_subject": "",
        "tile": "",
    },
    "cta_i": {
        "button_title": "Confirm Email Address",
        "button_color": "",
        "button_link": "",
        "message": "",
    }
}
