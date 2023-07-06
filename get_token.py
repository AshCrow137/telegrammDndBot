import os


def getToken():
  my_secret = os.environ['TOKEN']
  return my_secret
