HelloWorld
==========

Autor ... W. Nagy
Datum ... 23.07.2017


Abstrakt
--------

Demonstriert das Einbinden eines Addons in pyMFrame. 

http://pymframe.blogspot.co.at/

Installation
------------

Kopieren oder unzipen in das Verzeichnis ./addons des Frameworks.
Der Verzeichnismame muss dem Addon Name entsprechen.

Anlegen eines Controllers, welches das Plugin aufruft

Beispiel:
------- 8< -------------------------------------------------
from controller               import Controller
from helloworld.setup         import Helloworld

class HelloworldController(Controller):

   def get(self):
      helloworld = Helloworld(self)

      helloworld.get()
      return True

------- 8< -------------------------------------------------
