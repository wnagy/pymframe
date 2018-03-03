"""
Dokumentiert ein Projekt

"""
import os
import re
files = []
data = []
oFile = None
base = r'C:\Users\nagy\data\pymframe\northwind\WEB-INF\mframe'
def getFiles(base):
   for item in os.walk(base):
      for fn in item[2]:
         fn = os.path.normcase(fn)
         fPath = item[0].replace('\\','/')
         ext = os.path.splitext(fn)[1]
         if ext in ['.py','.tpl']:
            files.append(fPath+'/'+fn)


def hadleFile(filename,base):
   lines          = []
   curClass       = '__main__'
   d              = {}
   rexClass             = re.compile(r"^\s*Class\s+(\w+)+\s*",re.I)
   rexDocstringOneline  = re.compile(r'^\s*""".*"""$')
   rexDocstringBeginn   = re.compile(r'^\s*"""')
   rexDef               = re.compile(r'^\s*def\s+(\w+)\s*')

   sFilename = filename.replace(base,'')
   print >>oFile,'<div class="filename">File: <span style="font-size:x-small">{0}</span></div>'.format(sFilename)

   f = open(filename,'r')
   lines = f.readlines()
   f.close()

   isDocstring = False
   sDocstring = ''
   for line in lines:
      mat  = rexClass.search(line)
      if mat:
         curClass = mat.group(1)
         print >>oFile,'<h1>Klasse {0}</h1>'.format(curClass)

      mat = rexDocstringOneline.search(line)
      if mat:
         value = line.replace('"""','')
         if curClass == '__main__':
            print >>oFile,'<h1 class="modul">Hintergrund</h1>'

         print >>oFile,'<p>{0}</p>\n'.format(value)
         continue

      mat = rexDocstringBeginn.search(line)
      if mat:
         if isDocstring:
            sDocstring += line
            sDocstring = sDocstring.replace('"""','')

            if filename.endswith('__init__.py'):
               print >>oFile,'<h1 class="__init__">Modulbeschreibung</h1>'
            else:
               if curClass == '__main__':
                  print >>oFile,'<h1 class="modul">Hintergrund</h1>'


            print >>oFile,"<p>\n{0}</p>\n".format(sDocstring)
            sDocstring = ''

         isDocstring = not isDocstring

      if isDocstring:
         sDocstring += line
         sDocstring = sDocstring.replace('@param','<span class="param">param</span>&nbsp;')
         sDocstring = sDocstring.replace('@return','<span class="param">return</span>&nbsp;')

      mat = rexDef.search(line)
      if mat:
         method = mat.group(1)
         if method == '__init__':
            method = 'Konstruktor'

         print>> oFile,'<h2>{0}</h2>'.format(method)
         print>> oFile,'<tt>{0}</tt>'.format(line)

oFile = open('d.html','w')
print>>oFile,'''
<html>
 <head>
  <style type="text/css">
     * {
        font-family:"Lucida Console",fixed;
        }
     h1 {
        color:navy;
        padding:0;
        margin:0;
        }
     h1.modul {
        color:black;
        padding:0;
        margin:0;
        margin-top:8px;
        text-decoration:underline;
        font-size:1.5em;
        }
     h1.__init__ {
        color:darkgreen;
        padding:0;
        margin:0;
        font-size:1.2em;
        }
     h2 {
        color:green;
        }
     p {
        font-family:"Lucida Console",fixed;
        white-space:pre;
        width:80ex
        color:darkgreen;
        }

     tt {
        font-family:Courier;
        }

     div.filename {
        border:1px solid black;
        font-size:larger;
        text-decoration:underline;
        padding-top:8px;
        padding-bottom:8px;
        }
     span.param {
        text-decoration:underline;
        }
     span.hint {
        font-weight:bold;
        }
     code {
        font-size:smaller;
        font-family:courier;
        }
  </style>
 </head>
<body>
'''
getFiles(base)

for f in files:
   hadleFile(f,base)
print>>oFile,'</body></html>'
oFile.close()