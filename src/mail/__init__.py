from . import googlemail


def send(content, attachment=None):
    googlemail.send_with_attachment(content, attachment)
