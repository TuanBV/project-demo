import gettext
import os

def get_translation(request):
    """
        Get translation of text according
    """
    lang = request.headers.get('Accept-Language', 'en')
    translation = gettext.translation(
        'messages', \
    localedir=os.path.join(os.getcwd(), 'locales'), languages=[lang]
    )
    translation.install()
    # Get translation
    greeting = translation.gettext("Hello")
    return greeting
