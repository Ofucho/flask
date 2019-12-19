import os

class Development():
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:1234@127.0.0.1:5432/postgres'
    SECRET_KEY = 'Jaye7eus'
    DEBUG = True

class Production():
    SQLALCHEMY_DATABASE_URI='postgres://uznkseklvbnfef:55299305ede78a0573470bc71af221eff6eefc12543e84aef8655543eb550d57@ec2-46-137-91-216.eu-west-1.compute.amazonaws.com:5432/d17mv44gh3t9bl'
    SECRET_KEY = 'Jaye7eus'
    DEBUG = False


