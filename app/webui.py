import sys
sys.path.extend(['lib'])
from bottle import route, run, static_file, request
from bottle import view
from tasks import Orgapp
import doc


t = Orgapp()
@route('/')
def hello():
  return "Hello World!"


@route('/doc/<path>/edit')
@view('edit_wiki_page')
def edit_wiki_page(path):
  content = doc.render("../doc/{0}.md".format(path))
  pagename = '/doc/'+path
  return(dict(pagename=pagename, content=content))

@route('/doc/<path>/edit', method='POST')
@view('edit_wiki_page')
def save_wiki_page(path):
  content = request.forms.content
  doc.save("../doc/{0}.md".format(path), content)
  pagename = '/doc/'+path
  return(dict(pagename=pagename, content=content))

#TODO: cache pages another way, ie: cp -R doc cache + render
@route('/doc/<filename:re:[^\.]*>')
def show_wiki_page(filename):
  return static_file(filename, "../doc/cache") 
  

@route('/doc/<path:path>')
def show_wiki_resources(path):
  return static_file(path, "../doc") 

@route('/tasks')
def lsTasks():
  return(t.ls())


if __name__ == '__main__':
  run(host='localhost', port=8080, debug=True, reloader=True)