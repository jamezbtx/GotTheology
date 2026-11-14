import http.server, os, sys
ROOT='/workspace/gt-creeds-mock/public'
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=ROOT,**k)
    def translate_path(s,path):
        p=super().translate_path(path)
        if not os.path.exists(p) and os.path.exists(p+'.html'): return p+'.html'
        return p
    def log_message(s,*a): pass
http.server.ThreadingHTTPServer(('127.0.0.1',4199),H).serve_forever()
