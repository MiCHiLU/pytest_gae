"""
TODO
"""
import sys
import os
import logging


def pytest_addoption(parser):
    group = parser.getgroup("gae", "google app engine plugin")
    group.addoption('--gae-dir', action='store', dest='gae_dir',
                    metavar='path', default=None,
                    help="Google App Engine's source dir")
    group.addoption('--gae-project-dir', action='store', dest='gae_prj_dir',
                    metavar='path', default=None,
                    help="Your app's source code's dir")


def pytest_configure(config):
    gae_path = config.option.gae_dir
    project_path = config.option.gae_prj_dir
    if not gae_path or not project_path:
        return

    sys.path.append(gae_path)
    sys.path.append(os.path.join(gae_path, 'google'))
    sys.path.append(os.path.join(gae_path, 'lib/antlr3'))
    sys.path.append(os.path.join(gae_path, 'lib/django'))
    sys.path.append(os.path.join(gae_path, 'lib/fancy_urllib'))
    sys.path.append(os.path.join(gae_path, 'lib/graphy'))
    sys.path.append(os.path.join(gae_path, 'lib/ipaddr'))
    sys.path.append(os.path.join(gae_path, 'lib/simplejson'))
    sys.path.append(os.path.join(gae_path, 'lib/webob'))
    sys.path.append(os.path.join(gae_path, 'lib/yaml/lib'))

    sys.path.append(project_path)


def pytest_runtest_setup(item):
    gae_path = item.config.option.gae_dir
    project_path = item.config.option.gae_prj_dir

    if not gae_path or not project_path:
        return

    from google.appengine.tools import dev_appserver
    from google.appengine.tools.dev_appserver_main import DEFAULT_ARGS

    config = DEFAULT_ARGS.copy()
    config.update({'template_dir': os.path.join(gae_path, 'templates'),
                   'blobstore_path': '/tmp/dev_appserver.test_blobstore',
                   'root_path': project_path,
                   'history_path': '/tmp/dev_appserver.datastore.test_history',
                   'datastore_path': '/tmp/dev_appserver.test_datastore',
                   'matcher_path': '/tmp/dev_appserver.test_matcher',
                   'clear_datastore': True})

    app_cfg, _junk = dev_appserver.LoadAppConfig(project_path, {})
    dev_appserver.SetupStubs(app_cfg.application, **config)


def pytest_runtest_teardown(item):
    # There is some problems with GAE and
    # py.test miscomunication that causes
    # closed stream handler to be flushed.
    #
    # Wich of course causes Exception and
    # some nasty errors at the end of passes tests
    for h in logging.getLogger().handlers:
        if isinstance(h, logging.StreamHandler):
            attach_save_flush(h)


def attach_save_flush(handler):
    def save_flush():
        if not handler.stream.closed:
            handler.stream.flush()

    handler.flush = save_flush
