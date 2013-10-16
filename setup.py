from distutils.core import setup
from pygments_myextra import __version__, __author__, __author_email__

setup(
    name             = "pygments_myextra",
    version          = __version__,
    author           = __author__,
    author_email     = __author_email__,
    description      = "extra pygments lexters",
    packages         = ["pygments_myextra"],
    install_requires = ["pygments"],
    entry_points     = """
[pygments.lexers]
plcon      = pygments_myextra.lexer:PerlConsoleLexer
clcon      = pygments_myextra.lexer:EmacsLispConsoleLexer
cclcon     = pygments_myextra.lexer:CommonLispConsoleLexer
cljcon     = pygments_myextra.lexer:ClojureConsoleLexer
jscon      = pygments_myextra.lexer:JavascriptConsoleLexer
coffee-con = pygments_myextra.lexer:CoffeeScriptConsoleLexer
lscon      = pygments_myextra.lexer:LiveScriptConsoleLexer
irbcon     = pygments_myextra.lexer:MyRubyConsoleLexer
scalacon   = pygments_myextra.lexer:ScalaConsoleLexer
schemecon  = pygments_myextra.lexer:SchemeConsoleLexer
haskellcon = pygments_myextra.lexer:HaskellConsoleLexer
"""
)
