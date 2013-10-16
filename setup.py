from distutils.core import setup
import pygments_myextra 

setup(
    name             = "pygments_myextra",
    version          = pygments_myextra.__version__,
    author           = pygments_myextra.__author__,
    author_email     = pygments_myextra.__author_email__,
    description      = "extra pygments lexters",
    long_description = pygments_myextra.__doc__
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
