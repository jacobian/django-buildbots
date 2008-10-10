import tempfile

CACHE_BACKEND = "file://" + tempfile.gettempdir()
ROOT_URLCONF = 'testsettings'
SECRET_KEY = 'mkisz0$z*2b&7m8!^#^_t&5n7ose%hqa3$m2h$9@jhy7xk#_$2'
DATABASE_ENGINE = 'sqlite3'