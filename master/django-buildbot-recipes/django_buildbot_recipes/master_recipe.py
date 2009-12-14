# -*- coding: utf-8 -*-
"""
Buildmaster recipe.
This is copy/pasted from collective.buildbot.master_recipe; my additions are noted.
"""
import os
import shutil
import buildbot.status.web
from os.path import join
from collective.buildbot.recipe import BaseRecipe
from ConfigParser import ConfigParser
from zc.recipe.egg import Egg

class Recipe(BaseRecipe):
    """zc.buildout recipe"""

    public_html = os.path.dirname(buildbot.status.web.__file__)
    
    # JKM: use *my* recipe dir, not collective.buildbot's.
    recipe_dir = os.path.dirname(__file__)

    def install(self):
        """Installer"""
        files = []
        options = dict([(k, v) for k, v in self.options.items()])
        options.pop('recipe')

        # creates the dir
        if not os.path.exists(self.location):
            os.mkdir(self.location)

        # static files
        public_html = os.path.join(self.location, 'public_html')
        if not os.path.isdir(public_html):
            os.mkdir(public_html)

        for filename in ('index.html', 'classic.css', 'robots.txt'):
            if filename == 'classic.css':
                destination = os.path.join(public_html, 'buildbot.css')
            else:
                destination = os.path.join(public_html, filename)
            shutil.copyfile(os.path.join(self.public_html, filename),
                            destination)
            files.append(destination)

        if 'public-html' in options:
            dirname = options.pop('public-html')
            for filename in os.listdir(dirname):
                if filename.startswith('.'):
                    continue
                destination = os.path.join(public_html, filename)
                shutil.copyfile(os.path.join(dirname, filename), destination)
                if destination not in files:
                    files.append(destination)

        # virtual env
        self.create_virtualenv(self.location)

        # adds buildbot.tac
        template = open(join(self.recipe_dir, 'buildbot.tac_tmpl')).read()
        template = template % {'base_dir': self.location}
        buildbot_tac = join(self.location, 'buildbot.tac')
        open(buildbot_tac, 'w').write(str(template))
        self.log('Generated script %r.' % buildbot_tac)
        files.append(buildbot_tac)

        # Create an empty log file if necessary to avoid the error
        # message on first run.
        if not os.path.exists(os.path.join(self.location, 'twistd.log')):
            open(os.path.join(self.location, 'twistd.log'), 'w').write('')


        # generates the buildbot.cfg file
        
        # JKM: Instead of pulling slaves from the master config file, 
        # read 'em from slaves.cfg. This lets us check everything else
        # into SCM and just ignore slaves.cfg
        if os.path.exists('slaves.cfg'):
            slave_config = ConfigParser()
            slave_config.read('slaves.cfg')
            slaves = dict(slave_config.items('slaves'))
        elif 'slaves' in options:
            slaves = options.pop('slaves')
            slaves = dict([slave.split()[:2]
                           for slave in slaves.splitlines()
                           if slave.strip() != ''])
        else:
            slaves = []

        parts_directory = join(self.buildout['buildout']['parts-directory'])
        for k in ( 'projects', 'pollers'):
            options.setdefault('%s-directory' % k, join(parts_directory, k))

        for k, v in (('port', '8999'), ('wport', '9000'),
                     ('project-name', 'Buildbot'),
                     ('allow-force', 'false')):
            options.setdefault(k, v)

        for k, v in (('url', 'http://localhost:%s/'),
                     ('project-url', 'http://localhost:%s/')):
            options.setdefault(k, v % options['wport'])

        # assume trailing slash
        for k in ('url', 'project-url'):
            url = options[k]
	    if not url.endswith('/'):
                options[k] = url + '/'	

        globs = dict(buildbot=options,
                     slaves=slaves)

        files.append(self.write_config('buildbot', **globs))

        # generate script
        # JKM: use my package name instead of collective.buildbot
        options = {'eggs':'django_buildbot_recipes',
                   'entry-points': '%s=collective.buildbot.scripts:main' % self.name,
                   'arguments': 'location=%r, config_file=%r' % (
                       self.location, join(self.location, 'buildbot.cfg'))
                  }
        script = Egg(self.buildout, self.name, options)
        files.extend(list(script.install()))

        return files

    update = install