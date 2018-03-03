# -*- coding: iso-8859-15 -*-
"""
   Routie zum Maskenhandling.

   Es werden zwei Layouts angeboten
   List/Edit:
      Es wird eine Liste angeboten, welche eine Editierbutton enthaelt.
      Wird dieser betaetigt, so wird eine Editiermaske mit dem gewaehlten
      Datensatz angezeigt.
      Dieser kann Veraendert oder geloescht werden.
   """
from utility      import Utility
from pagination   import Pagination

import copy,sys

class Viewhandler() :

   controller        = None
   domain            = None
   listparam         = {}

   listView          = 'list.tpl'
   editView          = 'edit.tpl'
   gridView          = 'grid.tpl'

   LOADFROMCGI       = 'cgi'
   LOADFROMDOMAIN    = 'domain'
   LOADEMTPY         = None

   SAVE              = 'save'
   EDIT              = 'edit'
   DELETE            = 'delete'
   NEW_EDIT          = 'new-edit'
   LIST              = 'list'

   GRID_LAYOUT       = 'grid'
   LISTEDIT_LAYOUT   = 'listedit'
   LIST_LAYOUT       = 'list'

   textNew           = 'neu'

   layout            = GRID_LAYOUT

   lastDomain     = None
   gridlist          = None
   where             = None
   orderby           = None
   filter            = None
   action            = None

   limit             = None

   pagination        = None

   lastPk            = None
   show              = True

   # LIST_LAYOUT: die Anwendung bleibt nach
   # Save in der Editiermaske
   keepEdit          = True    
                             

   # ### nextDomain Mode
   #
   NONE               = 0b00000000
   NEVERNEWEDIT       = 0b00000001
   NEWEDIT            = 0b00000010
   action             = None

   def __init__(self,
                controller = None,
                db         = None,
                domain     = None,
                listparam  = None,
                layout     = None,
                gridlist   = None,
                where      = None,
                orderby    = None,
                limit      = None,
                filter     = None,
                pagination = None,
                curpage    = None,
                action     = None,
                keepedit   = True
                ):
      if controller is None: raise Exception('Bei Viewhandler fehlt Parameter "controller"')

      self.controller   = controller
      self.domain       = domain
      if listparam is not None:
         self.listparam=listparam
      self.listparam['path'] = self.controller.cgiparam(name='path',nvl='')

      if layout is not None: self.layout = layout
      self.gridlist = gridlist
      self.where=where
      self.orderby=orderby
      self.limit = limit
      self.keepEdit = keepedit
      self.filter = filter
      
      if pagination is not None:
         if isinstance(pagination,int):
            self.paginationFactory(pagination)
         elif isinstance(pagination,dict):
            self.paginationFactory(pagination['curpage'])
         else:
            raise Exception('viewhandler: die Option pagination muss ein Dictionary sein.')
      self.action = self.action or self.controller.cgiparam(name='action',nvl='')
      
      self.isReadonly = controller.isReadonly
      self.action = action or controller.cgiparam('action')
      

   def paginationFactory (self,curpage):
      """
      Erzeugen eines Paginations Objekts

      @param   curpage        aktuelle Seite
      """
      countrec = self.countRecords()
      pagination = Pagination(records=countrec,curpage=curpage)

      # in Viewhandler Limit eintragen = ([von Datensatz],[max. Anzahl der auszugebenden Datensaetze])
      self.limit = (curpage * pagination.pagesize,pagination.pagesize)

      # Erzeugen und Uebergeben einer Paginationsliste
      self.listparam['pagination'] = pagination

      #
      # ### Ende Pagination



   def getCurrentDomain(self,domain=None):
      """ Gibt die aktuelle domain zurueck.

          @param  domain         Domainobjekt

          Ist domain deklariert, wird diese geliefert.
          Ist domain None, wird versucht die Klassendomain
          zu liefer. Ist diese auch nicht deklariert wird eine
          Ausnahme geworfen
          """
      if domain is not None:
         return domain

      if self.domain is None:
         raise Exception('Es wurde weder der Parameter domain noch self.doamin delklariert')

      return self.domain

   def loadDomain(self,domain=None,key=None):
      """ Laedt die Domain aus der Datenbank

          @param  domain      Domain Objekt
                              ist dieser None wird das aktuelle Domainobjekt
                              des Objekts verwendet.

          @param  key         Wert ueber welchen aus der
                              Datenbak gelesen werde soll.
                              Ist dieser nicht deklariert,
                              wird der Wert aus dem CGI ermittelt.

          """


      curDomain = self.getCurrentDomain(domain)

      if key is None:
         pk = curDomain.getPK()
         key = self.controller.cgiparam(name=pk,nvl='')

      curDomain.get(key)


   def showEditMask(self,loadfrom='cgi',domain=None):
      """ Anzeigen einer Editiermaske.

          @param  loadfrom       gibt an, von wo die
                                 Felder befuellt werden sollen
                                 'cgi'    Daten aus dem CGI
                                 'domain' Daten aus der Domain
                                 None     Leere Maske wird angezeigt.

          Als Viewerfile wird edit.tpl angenommen (wenn nicht anders in der
          Klassenvariable deklariert.
          """

      # Automatischer Zurueck-Button  ausshalten
      # und auf List Anzeige anpassen.
      returnText = self.controller.menu.returnText
      self.controller.menu.returnText = None

      self.controller.addEntry(
         path='@current',
         text=returnText,
         addparam=['action=list']
         )

      utility = Utility()
      curDomain = self.getCurrentDomain(domain)

      if loadfrom == self.LOADFROMCGI:
         curDomain.fromCgi(self.controller.cgiparam,typecheckStrict=False)

      elif loadfrom == self.LOADFROMDOMAIN:
         self.loadDomain(curDomain)

      elif loadfrom == self.LOADEMTPY:
         curDomain.clear()
      else:
         raise Exception("Eine ungueltige Option von loadfrom '{0} stellt sich vor.".format(loadfrom))

      fields = utility.fieldsObjectFactory(curDomain)
      
      self.controller.view(self.editView,{
         'fields':fields,
         'path':self.controller.cgiparam(name='path',nvl=''),
         'controller':self.controller
         })


   def showList(self,listparam=None,action=None):
      """
      Behandelt bei List/Edit layout die Liste

      @param   listparam         Ein Dictionary, welches die
                                 Parameter fuer List-Viewer enhaelt.
      """

      curListparam = self.listparam
      if listparam is not None:
         curListparam = listparam      
      curListparam['controller'] = self.controller
      
      self.controller.view (self.listView,curListparam)
         

   def save(self,key=None, domain=None,action=None):
      # Wenn eine Fehler aufgetreten ist
      # Daten aus dem CGI einlesen
      self.lastDomain = None

      curDomain = None

      # Wurde domain uebergeben
      # diese verwenden
      if domain is None:
         curDomain = self.domain

      # Versuche die Domain aus Klasse zu bekommen
      if curDomain is None:
         curDomain = self.domain

      if key is None:
         key = curDomain.getPK()

      if action is None:
         action= self.controller.cgiparam(name='action', nvl=self.SAVE)

      isOk = curDomain.writedb(
         cgiparam=self.controller.cgiparam,
         flash=self.controller.flash,
         action=action,
         id=key
         )

      # Fehlerfall behandeln
      # Wenn nicht OK wird die aktuelle Domain gestellt
      # sonst enthaelt das Attribut None
      #
      if not isOk:
         self.controller.flash('<br />'.join(curDomain.errors))
         self.lastDomain = copy.copy(curDomain)
      else:
         # ist keepEdit Flag gesetzt,
         # wird nicht die Liste aufgerufen sonder das Programm
         # verbleibt in der Maske.
         if self.keepEdit:
            self.lastDomain = copy.copy(curDomain)
            if curDomain.mode == curDomain.INSERT:
               pkFld = curDomain.getPK()
               pkValue = curDomain.lastAutoincrement
               curDomain.set(pkFld,pkValue)
            return False
         else:
            self.lastDomain = None

         if curDomain.mode == curDomain.INSERT:
            self.lastPk = curDomain.lastAutoincrement
         else:
            self.lastPk = None
         

      return isOk

   def nextDomain(self,domain=None,where=None,orderby=None,onRead=None,filter=None,mode=NONE):
      """
      Liefert fuer jeden gefunden Datensatz ein Tupple zurueck.

      1 die Domain
      2 ein Boolean das angibt, ob eine Daten oder Eingabemaske
        erzeugt werden soll.

      @param      domain         Domain Objekt
      @param      where          SQL Where Klausel
      @param      orderby        SQL Order By Klausel
      @param      onRead         Handler wird nach jedem Aufruf
                                 einer Domain aufgerufen. Der Routine
                                 wird mit der Domain und dem Kennzeichen
                                 isEditMask befuellt  und liefert
                                 die Domain zurueck.
      @param      filter         Filter Optione fuer eachDomain
      @param      nevernewedit   [True|False] Wenn True wird keine
                                 leere Editiermaske am Ende der Liste angezeigt.
      """
      newedit = True
      isDelete = False
      pk = domain.getPK()
            
      for curDomain in domain.eachDomain(where=where,orderby=orderby,limit=self.limit,filter=self.filter):

         isEditMask = self.isEditMask(pk,curDomain.getValue(pk))

         # Behandlung wenn Fehler beim schreiben in die Datenbank
         # aufgetreten ist.
         if self.lastDomain is not None and self.lastDomain.getValue(pk) == curDomain.getValue(pk):

            if curDomain.mode == curDomain.DELETE:
               isDelete = True
               isEditMask = False
            else:
               curDomain = self.lastDomain
               isEditMask = True

         if isEditMask: newedit = False
         if curDomain.mode == curDomain.DELETE:
            newedit = True

         if onRead is not None:
            curDomain = onRead(curDomain,isEditMask)

         yield (curDomain,isEditMask)

      if mode != self.NEVERNEWEDIT and newedit:
         # HINT: domain sicherheitshalber leeren.
         if not isDelete and self.lastDomain is not None:
            domain = self.lastDomain
         else:
            domain.clear()

         if onRead is not None:
            curDomain = onRead(curDomain,True)
         yield (domain,True)

   def datarow(self,row=[],nvl='',params=[]):
      """
      Liefert eine Liste von Eintraegen.
      Ist eine Element der Liste leer, so wird
      der Wert aus nvl ausgegeben.

      @param 1          Nono Wert
      @param 2..        offene Liste von Werten
      """
      for value in params:
         if value is None: value = nvl
         row.append(value)



   def gridrow(self,editmask=None,listrow=None,list=None,taglib=None,addhidden=[]):
      """ Erzeugen einer Grid Row

          @param  editmask       Routine welche die Editiermaske beschreibt
          @param  listrow        Routine welche eine Liste mit Datenzeileneintragen erzeugt
          @param  list           Routine welche durch die Datenzeilen itteriert.
                                 Diese liefert zwei Werte
                                   1) Eine Domain mit den Dateninhalten
                                   2) ein Flag welches angeibt ob die Domain als
                                      Datenliste oder als Editiermaske angezeigt werden soll
          @param  taglib         das aktuelle Taglib Objekt

          @return Ein HTML Fragment, welches die gerenderte Datentabelle liefert.

          """

      rows = []
      path = self.controller.path
      for (domain,isEditMask) in list():
         # Wenn Editiermaske, diese Ausgeben

         if isEditMask:
            newedit=False  # Keine Neueingabemaske
            rows.append('<!-- EDITIERMASKE -->')
            rows.append(taglib.form(name='grid-edit'))
            rows.append(taglib.hidden(name='path',value=path))
            for hidden in addhidden:
               rows.append(taglib.hidden(name=hidden[0],value=hidden[1]))
            rows.append('\n'.join(editmask(domain)))
            rows.append(taglib.endform())
            rows.append('<!-- ENDE EDITIERMASKE -->')
         else:
            rows.append(taglib.tablerow(listrow(domain)))

      return '\n'.join(rows)

   def countRecords (self):
      """
      Liefert die Anzahl der Datensaetze,
      welche basierend auf filter und where gefunden werden.
      """
      retval = self.domain.count(self.where,self.filter)
      return retval



   def callViewer(self):
      if self.show:
         self.controller.view(self.gridView,self.listparam)

   def handleListEdit(self):
      """ Shot and forget Funktion fuer Behandlung
          eines List-Edit Layouts
          """
      #action = self.controller.cgiparam(name='action',nvl='')
      action = self.action
      
      # Neu Anzeigen?
      if action in [self.LIST,self.SAVE,self.DELETE,'']:
         self.controller.addEntry(
            path='@current',
            text=self.textNew,
            addparam=['action='+self.NEW_EDIT]
            )
            
      # Liste Anzeigen
      if action in [self.LIST,'']:
         self.showList()

      # Eingaben aus Maske speichern
      elif action in [self.SAVE,self.DELETE]:
         isOk = self.save()
         if isOk:
            self.showList()
         else:
            self.showEditMask(loadfrom='cgi')

      # Editiermaske anzeigen
      elif action == self.EDIT:
         self.showEditMask(loadfrom='domain')

      elif action == self.NEW_EDIT:
         self.showEditMask(loadfrom=None)

      elif action == self.DELETE:
         self.showEditMask(loadfrom=None)

      # Sonst Fehler
      else:
         raise ValueError("Eine bislang unbekannte Action '{0}' stellt sich vor".format(action))

   def isEditMask(self,idfieldname,domainvalue):
      """ Prueft ob ein Eingabemaske angezeigt werden soll
          @param  idfieldname       Name des ID Fields
          """

      if self.isReadonly: return False
      
      action = self.action

      idfieldvalue = self.controller.cgiparam(idfieldname)
      retval = action not in ['save','delete'] and str(idfieldvalue) == str(domainvalue)
      return retval

   def handleGrid(self):
      """
      Shot and forget Funktionen fuer Behandlung
      eines Grid Layouts.
      """

      if self.action in ['save','delete']:
         isOk = self.save(action=self.action)
         if not isOk:
            self.listparam['isOk']=False

      if 'controller' not in self.listparam.keys():
         self.listparam['controller'] = self.controller

      if self.gridlist is None:

         def viewHelper():
            mode = self.NEVERNEWEDIT if self.isReadonly else self.NONE
            
            nxtRecord = self.nextDomain(domain=self.domain,where=self.where,orderby=self.orderby,mode=mode)            
            for (curDomain,isEditMask) in nxtRecord:
               yield (curDomain,isEditMask)

         self.listparam['list'] = viewHelper 
         self.callViewer()
      else:
         if 'list' not in self.listparam.keys():
            if self.gridlist is not None:
               self.listparam['list'] = self.gridlist
            else:
               raise Exception('Viewhandler::handleGrind: Es wurde kein list Methode deklariert')

         self.controller.view (self.gridView,self.listparam)

   def handleList (self):
      """
      Kobination aus GRID Anzeige der Datenzeilen mit Editmasek
      """
      self.listparam['controller'] = self.controller
      def viewHelper():
         yield (self.domain,True)
      
      def viewHelperFull():

         # nevernewedit schalte die zusaetzliche Eingabezeile aus
         #
         for (curDomain,False) in self.nextDomain(domain=self.domain,where=self.where,orderby=self.orderby,mode=Viewhandler.NEVERNEWEDIT):
            yield (curDomain,False)
      
      if self.action in [self.SAVE,self.DELETE]:
         isOk = self.save(action=self.action)         
         if not isOk:
            self.listparam['isOk']=False
            if self.action == 'delete':
               self.listparam['list'] = viewHelperFull
            else:
               self.listparam['list'] = viewHelper
            self.callViewer()
            if self.action == self.DELETE:
               self.controller.addEntry(
                  path='@current',
                  text=self.textNew,
                  addparam=['action='+self.NEW_EDIT]
                  )
            return

      elif self.action == self.NEW_EDIT:
         self.domain.clear()
         self.loadDomain(self.domain)
         self.listparam['list'] = viewHelper
         self.callViewer()
         return

      elif self.action == self.EDIT:
         self.loadDomain(self.domain)
         self.listparam['list'] = viewHelper
         self.callViewer()
         return

      if self.gridlist is None:

         # Neu Anzeigen?
         if self.action in [self.LIST,self.DELETE,''] and not self.isReadonly:
            self.controller.addEntry(
               path='@current',
               text=self.textNew,
               addparam=['action='+self.NEW_EDIT]
               )
         def viewHelper():
            # nevernewedit schalte die zusaetzliche Eingabezeile aus
            #
            for (curDomain,False) in self.nextDomain(domain=self.domain,where=self.where,orderby=self.orderby,mode=Viewhandler.NEVERNEWEDIT):
               yield (curDomain,False)
         
         if 'list' not in self.listparam:
            self.listparam['list'] = viewHelper
         
         self.callViewer()

   def run(self,layout=None,show=True):
      """ Allgemeiner Aufruf des Viewhandlers.
          In der Opton layout wird festgelegt ob
          Grid oder List/Edit angewendet werden soll.
          """
      if layout is None:
         layout = self.layout

      self.show = show
     
      if self.controller is None:
         raise Exception('Viewhandler.:run kann keine Referenz auf controller finden.')

      
      if layout == self.GRID_LAYOUT:
         self.keepEdit=False
         self.handleGrid()
      elif layout == self.LISTEDIT_LAYOUT:
         self.handleListEdit()
      elif layout == self.LIST_LAYOUT:
         self.handleList()
      else:
         raise Exception('Es wurde weder LIST/EDIT nocht GRIND Layout deklariert' )
      
   @staticmethod
   def inList(action):
      return action in [Viewhandler.LIST,Viewhandler.DELETE,Viewhandler.SAVE,'']
