import os
import tempfile

CACHE_BACKEND = "file://" + tempfile.gettempdir()
ROOT_URLCONF = 'testsettings'
SECRET_KEY = 'mkisz0$z*2b&7m8!^#^_t&5n7ose%hqa3$m2h$9@jhy7xk#_$2'
DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'template1'
DATABASE_USER = 'jacob'

# Make sure we get a distinct test database name -- this
# settings file might be used to run multiple tests.
TEST_DATABASE_NAME = "djangotests_%s" % (os.getpid())