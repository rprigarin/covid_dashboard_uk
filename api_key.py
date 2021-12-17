""" API key loader """

def get_api_key():
    """ API key loader (currently for newsapi only) """
    key = open("api_key.txt", "r", encoding="utf-8")

    return key.read()
