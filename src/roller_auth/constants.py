# disabling ugettext_lazy as it causes serialization problems if used with The
# rest framework serializer. The errors can be avoided if the string is wrapped
# by str(AuthErrorMessages.CONSTANT_NAME). Decided not to go with it becuase
# langs is a low priority.
# from django.utils.translation import ugettext_lazy as _

SUPPORTED_PROFILE_PICTURE_FORMATS = ('jpg', 'jpeg', 'png')

class AuthErrorMessages(object):
    FORM_REQUIRED_EMAIL = u'Email is required.'
    FORM_REQUIRED_PASSWORD = u'Email is required.'
    LOGIN_INVALID_CREDENTIALS = u'Invalid email or password. Please try again.'
    EMAIL_IN_USE = u'This email address is already in use.'
    INVALID_NUMBER_OF_PROFILE_PICTURES_UPLOADED = u'Only one file can be uploaded for your profile picture'
    UNSUPPORTED_PROFILE_PICTURE_FORMAT = u'Profile pictures must be in either JPEG or PNG formats'


INITIALS_AVATAR_COLORS = [
    "#5A8770",
    "#B2B7BB",
    "#6FA9AB",
    "#F5AF29",
    "#0088B9",
    "#F18636",
    "#D93A37",
    "#A6B12E",
    "#5C9BBC",
    "#F5888D",
    "#9A89B5",
    "#407887",
    "#9A89B5",
    "#5A8770",
    "#D33F33",
    "#A2B01F",
    "#F0B126",
    "#0087BF",
    "#F18636",
    "#0087BF",
    "#B2B7BB",
    "#72ACAE",
    "#9C8AB4",
    "#5A8770",
    "#EEB424",
    "#407887",
]
