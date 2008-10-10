Django's buildbots
==================

Utilities for configuring and running Django's buildbot and build slaves. This
is based around `zc.buildout`_ and the `collective.buildbot`_ recipe.

These aren't actually running on http://buildbot.djangoproject.com/ yet, but
they will soon.

The master config is here mostly for others to look at for example. The useful
bit is in the slave.

.. _zc.buildout: http://pypi.python.org/pypi/zc.buildout
.. _collective.buildbot: http://pypi.python.org/pypi/zc.buildout

Setting up a build slave
------------------------

1. Bootstrap ``zc.buildout``::

        easy_install zc.buildout
        cd slave/
        buildout init
    
2. Edit ``slave/buildout.cfg`` for your environment. The version
   here has configs for a couple of slaves (one that tests against
   sqlite, and one against PostgreSQL); it's probably easier to
   start with just a single slave.
   
   See the documentation for `the build slave recipe`_ for more
   info on the build slave options.
   
3. Give the slave a good, unique name that'll tell what it is and what it does
   (i.e. ``osx-10.5-python2.5-sqlite``, ``ubuntu-hardy-python2.6-mysql-5.0``,
   etc.)

4. Make up a slave password.
   
5. Make sure the slave environment has ``DJANGO_SETTINGS_MODULE`` and
   ``PYTHONPATH`` set correctly, and make sure that ``DJANGO_SETTINGS_MODULE``
   exists and is configured correctly.
   
   Note that the same slave may test multiple branches, so you'll need to make
   sure that nothing's shared between the slaves. See
   ``testsettings/postgres.py`` for one of the things you'll need to do: set
   ``TEST_DATABASE_NAME`` to something that'll be different for each slave.


6. Create the buildbot by running ``./bin/buildout`` from the slave directory.

7. Start the slave: ``./bin/<my-slave-name> start``

8. Send the buildbot name and password to XXX FIXME.

.. _the build slave recipe: http://pypi.python.org/pypi/collective.buildbot/0.3.3#the-build-slave-recipe
