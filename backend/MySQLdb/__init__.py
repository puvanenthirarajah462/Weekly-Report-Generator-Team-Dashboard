import pymysql
from pymysql import *  # noqa: F401,F403

connect = pymysql.connect
Error = pymysql.Error
Warning = pymysql.Warning

# Common exception aliases expected by Django's MySQL backend.
DatabaseError = pymysql.DatabaseError
OperationalError = pymysql.OperationalError
IntegrityError = pymysql.IntegrityError
InternalError = pymysql.InternalError
ProgrammingError = pymysql.ProgrammingError
DataError = pymysql.DataError
NotSupportedError = pymysql.NotSupportedError

apilevel = "2.0"
threadsafety = 1
paramstyle = "pyformat"
__version__ = pymysql.__version__
