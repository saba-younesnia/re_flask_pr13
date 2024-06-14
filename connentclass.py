from flask import *
import sqlite3
class Connentclass:
    def connect(self):
        db=sqlite3.connect('db1.db')
        return db
