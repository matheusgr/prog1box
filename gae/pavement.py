""" Pavement build main file. Use paver (pip package) to run. """
# Based upon: https://github.com/jenisys/behave.example/blob/master/pavement.py

from paver.easy import *  # pylint: disable=W0401,W0614

options(
    setup=dict(
        name="Social Coding",
        version="0.01",
        description="Compare students submissions (Web)",
        author="Matheus Gaudencio do Rego",
        author_email="matheusgr@gmail.com",
        install_requires=[],
        # test_suite='nose.collector',
        packages=['socialcoding'],
        url="http://www.splab.ufcg.edu.br/",
    ),
    sphinx=Bunch(
        builddir="build",
        sourcedir="source"
    ),
)


@task
def init():
    docs_final = path('docs') / 'final'
    if docs_final.exists():
        docs_final.rmtree()
    path('coverage').rmtree()
    path('coverage').mkdir()
    docs_final.mkdir()


@task
def removepyc():
    """ Removed created pyc files. """
    for pyc in path.walkfiles(path('.'), '*.pyc'):
        pyc.remove()


@task
def tests():
    """ Test codecompare using tests found at tests dir. """
    sh("nosetests --with-coverage --cover-package=codecompare --cover-inclusive --cover-html --cover-html-dir=coverage")


@task
@needs(["removepyc"])
def clean():
    """ Overall clean task. """
    docs_final = path('docs') / 'final'
    if docs_final.exists():
        docs_final.rmtree()


@task
@cmdopts([("noerror", "E", "Ignore errors"), ])
def pep8(pep_options):
    """ Execute pep8 conformance test. """
    noerror = getattr(pep_options, "noerror", False)
    return sh("""find . -name "*.py" | xargs pep8 | perl -nle'\
            print; $a=1 if $_}{exit($a)'""", ignore_error=noerror)


@task
@needs(['html', "distutils.command.sdist"])
def sdist():
    """Generate docs and source distribution."""
    pass


@task
@needs(['init', 'paver.doctools.html'])
def html():
    """Build Paver's documentation and install it into paver/docs"""
    builtdocs = path('docs') / options.sphinx.builddir / "html"
    destdir = path("docs") / "final"
    builtdocs.move(destdir)


@task
@needs(["clean"])
def sync():
    """ Syncronize codecompare projects to current folder. Always run it. """
    sh("rsync -av --delete ../codecompare/codecompare/ codecompare/")
    sh("rsync -av --delete ../codecompare/codecomparejson/ codecomparejson/")
