import sys
import os
import logging
import pytest
import py


class Pdb(py.std.pdb.Pdb, object):
    def __init__(self, stdin=sys.__stdin__, stdout=sys.__stdout__, *argv, **kwargv):
        return super(Pdb, self).__init__(stdin=stdin, stdout=stdout, *argv, **kwargv)

py.std.pdb.Pdb = Pdb


def pytest_addoption(parser):
    group = parser.getgroup("gae", "google app engine plugin")
    group.addoption('--with-gae', action='store_true', dest='use_gae',
                    default=False, help='Use pytest_gae plugin')
    group.addoption('--gae-path', action='store', dest='gae_path',
                    metavar='PATH', default='./google_appengine/',
                    help="Google App Engine's root PATH")
    group.addoption('--gae-project-path', action='store', dest='gae_prj_path',
                    metavar='PATH', default='./',
                    help="Your project's source code's PATH")
    group.addoption('--use-devappserver2', action='store_true', dest='use_devappserver2',
                    default=False, help='Use devappserver2')


def pytest_configure(config):
    if not config.option.use_gae:
        return

    _add_gae_to_syspath(config)
    _add_project_to_syspath(config.option.gae_prj_path)

    _validate_gae_path(config.option.gae_path)
    _validate_project_path(config.option.gae_prj_path)


def _add_gae_to_syspath(config):
    """ Adds Google App Engine and libs that comes with GAE to sys.path

    It is hardcoded and Google may change its internal structure anytime.
    So, it is not the safetest method to do it
    """

    sys.path.insert(0, config.option.gae_path)

    if config.option.use_devappserver2:
        import devappserver2 as dev_appserver
    else:
        import dev_appserver
    dev_appserver.fix_sys_path()


def _add_project_to_syspath(path):
    sys.path.insert(0, path)


def _validate_gae_path(path):
    try:
        import google.appengine
    except ImportError:
        raise pytest.UsageError("google.appengine lib can not be imported. "
                                "Try to use --gae-path option. "
                                "Current path: <%s> " % path)


def _validate_project_path(path):
    # Google App Engine projects must contain app.yaml at their roots.
    # So, this code just checks if app.yaml exists
    if not os.path.exists(os.path.join(path, 'app.yaml')):
        raise pytest.UsageError("Your AppEngine's project can not "
                                "be found. Try to use --gae-project-path "
                                "option. Current path: <%s>" % path)
