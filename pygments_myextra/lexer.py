import re
from pygments.lexer  import Lexer, do_insertions
from pygments.lexers import *
from pygments.token  import Generic, Comment


line_re  = re.compile('.*?\n')

class GenericConsoleLexer(Lexer):
    name = ''
    aliases = []
    filenames = []
    mimetypes = []

    _prompt_re = re.compile('> ')
    _comment_re = re.compile('^\s*#')
    LangLexer = Lexer 

    def get_tokens_unprocessed(self, text):
        langlexer = self.LangLexer(**self.options)

        curcode = ''
        insertions = []
        for match in line_re.finditer(text):
            line = match.group()

            # prompt
            m = self._prompt_re.match(line)
            if m is not None:
                end = m.end()
                insertions.append((len(curcode),
                                   [(0, Generic.Prompt, line[:end])]))
                curcode += line[end:]
                continue
            elif curcode:
                for item in do_insertions(insertions,
                                          langlexer.get_tokens_unprocessed(curcode)):
                    yield item
                curcode = ''
                insertions = []

            # comments
            m = self._comment_re.match(line)
            if m is not None:
                yield match.start(), Comment.Single, line
                continue

            yield match.start(), Generic.Output, line

        if curcode:
            for item in do_insertions(insertions,
                                      langlexer.get_tokens_unprocessed(curcode)):
                yield item


class PerlConsoleLexer(GenericConsoleLexer):
    """
    Perl interactive console (pirl, re.pl)

    # pirl:
    >>> tokens = PerlConsoleLexer().get_tokens_unprocessed('''
    ... pirl @> @a = (1,2,3,4,5)
    ... (1, 2, 3, 4, 5)
    ... pirl @> \@a
    ... [1, 2, 3, 4, 5]
    ... ''')

    # re.pl:
    >>> tokens = PerlConsoleLexer().get_tokens_unprocessed('''
    ... $ my $a = 22
    ... 22
    ... ''')
    """
    name      = 'Perl Console Session'
    aliases   = ['pirl', 'repl', 'plcon']
    filenames = ['*.pirl']
    mimetypes = ['text/x-perl-shellsession']

    _prompt_re  = re.compile('^(?:pirl @> |\$ )')
    _comment_re = re.compile('^\s*#')

    LangLexer = PerlLexer


class EmacsLispConsoleLexer(GenericConsoleLexer):
    """
    EmacsLisp interactive console

    >>> tokens = EmacsLispConsoleLexer().get_tokens_unprocessed('''
    ... > (setq x 200)
    ... > (symbol-value 'x)
    ... 200
    ... > (fset 'x 300)
    ... 300
    ... ''')
    """
    name      = 'EmacsLisp Console Session'
    aliases   = ['clcon']
    filenames = ['*.clcon']
    mimetypes = ['text/x-emacslisp-shellsession']

    _prompt_re  = re.compile('>>> |\.\.\. ')
    _comment_re = re.compile('^\s*;')

    LangLexer = CommonLispLexer


class SchemeConsoleLexer(GenericConsoleLexer):
    """
    EmacsLisp interactive console

    >>> tokens = SchemeConsoleLexer().get_tokens_unprocessed('''
    ... gosh> (define x 200)
    ... gosh> x
    ... 200
    ... gosh:1> (string->number "9997")
    ... 9997
    ... ''')
    """
    name      = 'Scheme Console Session'
    aliases   = ['schemecon', 'scmcon', 'gosh']
    filenames = ['*.schemecon']
    mimetypes = ['text/x-scheme-shellsession']

    _prompt_re  = re.compile('gosh(?::\d+)?> |\.\.\. ')
    _comment_re = re.compile('^\s*;')

    LangLexer = SchemeLexer


class ClojureConsoleLexer(GenericConsoleLexer):
    """
    Clojure interactive console

    >>> tokens = ClojureConsoleLexer().get_tokens_unprocessed('''
    ... user=> nil
    ... nil
    ... user=> "Hello, World"
    ... "Hello, World"
    ... user=> 'x
    ... x
    ... user=> (def x 22)
    ... #'user/x
    ... user=> x
    ... 22
    ... ''')
    """
    name      = 'Clojure Console Session'
    aliases   = ['cljcon']
    filenames = ['*.cljcon']
    mimetypes = ['text/x-clojure-shellsession']

    _prompt_re  = re.compile('^(?:[a-zA-Z0-9.\-]+=?>|\.\.\. )')
    _comment_re = re.compile('^\s*;')

    LangLexer = ClojureLexer


class CommonLispConsoleLexer(GenericConsoleLexer):
    """
    Common Lisp interactive console

    >>> tokens = CommonLispConsoleLexer().get_tokens_unprocessed('''
    ... ? (defun foo (&key x (y 123) (z 456 z-supplied-p))
    ... .   (pprint (list x y z z-supplied-p)))
    ... FOO
    ... ? (foo)
    ... (NIL 123 456 NIL)
    ... ''')
    """
    name      = 'Common Lisp Console Session'
    aliases   = ['cclcon']
    filenames = ['*.cclcon']
    mimetypes = ['text/x-common-lisp-shellsession']

    _prompt_re  = re.compile('^(\?|\.) ')
    _comment_re = re.compile('^\s*;')

    LangLexer = CommonLispLexer


class JavascriptConsoleLexer(GenericConsoleLexer):
    """
    Javascript interactive console

    >>> tokens = JavascriptConsoleLexer().get_tokens_unprocessed('''
    ... > o = {  a: 2, b: [1,2,3] }
    ... [object Object]
    ... > o['a']
    ... 2
    ... ''')

    >>> tokens = JavascriptConsoleLexer().get_tokens_unprocessed('''
    ... >>> o.a
    ... 2
    ... >>> (function() print("hello world"))()
    ... hello world
    ... ''')
    """
    name      = 'Javascript Console Session'
    aliases   = ['jscon', 'mongo']
    filenames = ['*.jscon']
    mimetypes = ['text/x-javascript-shellsession']

    _prompt_re  = re.compile('^(>|js>|>>>) ')
    _comment_re = re.compile('^\s*//')

    LangLexer = JavascriptLexer


class ScalaConsoleLexer(GenericConsoleLexer):
    """
    Scala interactive console

    >>> tokens = ScalaConsoleLexer().get_tokens_unprocessed('''
    ... scala> var aList = List(1,2,3,4,5)
    ... aList: List[Int] = List(1, 2, 3, 4, 5)
    ... scala> aList ::: List("yama")
    ... res16: List[Any] = List(1, 2, 3, 4, 5, yama)
    ... scala> "ddd" :: aList
    ... res17: List[Any] = List(ddd, 1, 2, 3, 4, 5)
    ... ''')
    """
    name      = 'Scala Console Session'
    aliases   = ['scalacon']
    filenames = ['*.scalacon']
    mimetypes = ['text/x-scala-shellsession']

    _prompt_re  = re.compile('scala> |\s*\|')
    _comment_re = re.compile('^\s*//')

    LangLexer = ScalaLexer


class HaskellConsoleLexer(GenericConsoleLexer):
    """
    Haskell (ghci) interactive console

    >>> tokens = HaskellConsoleLexer().get_tokens_unprocessed('''
    ... Prelude List> any (\\\\x -> x `mod` 7 == 0) [1..10]
    ... True
    ... Prelude List> [2,4..10]
    ... [2,4,6,8,10]
    ... ''')
    """
    name      = 'Haskell Console Session'
    aliases   = ['haskellcon', 'ghci', 'hugs']
    filenames = ['*.haskellcon']
    mimetypes = ['text/x-haskell-shellsession']

    _prompt_re  = re.compile('^[0-9a-zA-Z .*]+>')
    _comment_re = re.compile('^\s*--')

    LangLexer = HaskellLexer


class OcamlConsoleLexer(GenericConsoleLexer):
    """
    Ocaml interactive console

    >>> tokens = OcamlConsoleLexer().get_tokens_unprocessed('''
    ... # sqrt (-1.);;
    ... - : float = nan
    ... # infinity +. neg_infinity;;
    ... - : float = nan
    ... ''')
    """
    name = 'OCaml Console Session'
    aliases = ['ocamlcon']
    filenames = ['*.ocamlcon']
    mimetypes = ['text/x-ocaml-shellsession']

    _prompt_re = re.compile('^# ')
    _comment_re = re.compile('^\s*\(\*.*\*\)')

    LangLexer = OcamlLexer


class CoffeeScriptConsoleLexer(GenericConsoleLexer):
    """
    CoffeeScript interactive console

    >>> tokens = CoffeeScriptConsoleLexer().get_tokens_unprocessed('''
    ... coffee> hash = null
    ... null
    ... coffee> hash or= {}
    ... {}
    ... coffee> hash = 0
    ... 0
    ... coffee> hash or= {}
    ... {}
    ... ''')
    """
    name = 'CoffeeScript Console Session'
    aliases = ['coffee-con']
    filenames = ['*.coffeecon']
    mimetypes = ['text/x-coffeescript-shellsession']

    _prompt_re  = re.compile('^(?:coffee> |------> |\.\.\.\.\.\.\. )')
    _comment_re = re.compile('^\s*#')

    LangLexer = CoffeeScriptLexer


class LiveScriptConsoleLexer(GenericConsoleLexer):
    """
    LiveScript interactive console

    >>> tokens = LiveScriptConsoleLexer().get_tokens_unprocessed('''
    ... # $ lsc
    ... ls> hash = null
    ... null
    ... ls> hash or= {}
    ... {}
    ... ls> f = (a, b, c) --> a + b + c
    ... [Function]
    ... ls> f 2 3 4
    ... 9
    ... ''')
    """
    name      = 'LiveScript Console Session'
    aliases   = ['lscon']
    filenames = ['*.lscon']
    mimetypes = ['text/x-livescript-shellsession']

    _prompt_re  = re.compile('^(?:ls> |\.\.\. )')
    _comment_re = re.compile('^\s*#')

    LangLexer = LiveScriptLexer


class MyRubyConsoleLexer(Lexer):
    """
    Ruby interactive console

    >>> tokens = MyRubyConsoleLexer().get_tokens_unprocessed('''
    ... irb(main):001:0> a = 1
    ... => 1
    ... irb(main):002:0> puts a
    ... 1
    ... => nil
    ... ''')

    >>> tokens = MyRubyConsoleLexer().get_tokens_unprocessed('''
    ... [2] pry 1.9.3-p392 (main)> a = 1
    ... 1
    ... [3] pry 1.9.3-p392 (main)> puts a
    ... 1
    ... [4] pry 1.9.3-p392 (main)> cd x
    ... [4] pry 1.9.3-p392 ("hello"):1> upcase
    ... "HELLO"
    ... pry 1.9.3-p392 (main)> a
    ... 1
    ... pry 1.9.3-p392> a
    ... 1
    ... ''')
    """
    name      = 'Ruby irb, pry session'
    aliases   = ['myirb', 'pry']
    mimetypes = ['text/x-ruby-shellsession']

    _prompt_re = re.compile('irb\([a-zA-Z_][a-zA-Z0-9_]*\):\d{3}:\d+[>*"\'] '
                            '|(?:\[\d+\] )?pry [0-9.]+-p\d+(?: \([^)]+\))?(?::\d+)?[>*]'
                            '|irb> |pry> '
                            '|>> |\?> ')

    def get_tokens_unprocessed(self, text):
        rblexer = RubyLexer(**self.options)

        curcode = ''
        insertions = []
        for match in line_re.finditer(text):
            line = match.group()
            m = self._prompt_re.match(line)
            if m is not None:
                end = m.end()
                insertions.append((len(curcode),
                                   [(0, Generic.Prompt, line[:end])]))
                curcode += line[end:]
            else:
                if curcode:
                    for item in do_insertions(insertions,
                                    rblexer.get_tokens_unprocessed(curcode)):
                        yield item
                    curcode = ''
                    insertions = []
                yield match.start(), Generic.Output, line
        if curcode:
            for item in do_insertions(insertions,
                                      rblexer.get_tokens_unprocessed(curcode)):
                yield item


if __name__ == '__main__':
    from pygments import highlight
    from pygments.formatters import HtmlFormatter

    lexers = {
        'perlcon' : {
            'code'  :  "pirl @> print 'hello world';\n$ my $a = 22;\n# comment\n",
            'lexer' : PerlConsoleLexer,
        },
        'clcon' : {
            'code'  : ">>> (symbol-value 'x)\n200\n>>> (fset 'x 300)\n300\n; comment\n",
            'lexer' : EmacsLispConsoleLexer,
        },
        'cljcon' : {
            'code'  : "user=> (def x 22)\n#'user/x\nuser=> ; aa",
            'lexer' : ClojureConsoleLexer,
        },
        'schemecon' : {
            'code'  : "gosh> (define x\n.. 22) ;comment",
            'lexer' : SchemeConsoleLexer,
        },
        'jscon' : {
            'code'  : "js> o = {  a: 2, b: [1,2,3] }\n[object Object]\njs> o['a']\n// comment\n",
            'lexer' : JavascriptConsoleLexer,
        },
        'scalacon' : {
            'code'  : "scala> var aList = List(1,2,3)\naList: List[Int] = List(1,2,3)\nscala> (x:Int) => x + 1\n// comment\n",
            'lexer' : ScalaConsoleLexer,
        },
        'haskellcon' : {
            'code' : "Prelude List> any (\\x -> x `mod` 7 == 0) [1..10]\nTrue\n-- comment\nPrelude List> [2,4..10]\n[2,4,6,8,10]",
            'lexer' : HaskellConsoleLexer,
        },
        'ocamlcon' : {
            'code' : "# sqrt (-1.);;\n- : float = nan\n# infinity +. neg_infinity;;\n- : float = nan",
            'lexer' : OcamlConsoleLexer,
        },
        'coffee-con' : {
            'code' : "coffee> hash = null\nnull\n# coffee> comment\ncoffee> hash = 0\n",
            'lexer' : CoffeeScriptConsoleLexer,
        },
        'lscon' : {
            'code' : "ls> f  =  (a, b, c) -->\n...   a + b + c\n[Function]\nls> f 2 3 4\n9",
            'lexer' : LiveScriptConsoleLexer,
        },
        'myruby-con' : { 
            'code' : """irb(main):002:0> puts a\n1\n=> nil\n[2] pry 1.9.3-p392 (main)> a = 1\n1\n[2] pry 1.9.3-p392 ("hello"):1> upcase\n""",
            'lexer' : MyRubyConsoleLexer,
        },
    }

    for k in lexers:
        lexer = lexers[k]['lexer']
        code  = lexers[k]['code']

        print "[%s]" % k 
        print "\t-- check proccessing"
        for l in lexer().get_tokens_unprocessed(code):
            print "\t", l
        print

        print "\t-- check html format"
        print "\t", highlight(code, lexer(), HtmlFormatter())

    import doctest
    doctest.testmod()
