from messages import english


def get_message(key):
    if key in english.messages:
        return english.messages[key]
    return 'Missing translation message ' + key + ' ! Please report this.'
