# -*- coding: iso-8859-15 -*-
"""Basisklasse fuer Elementen zur Bildschirmdarstellung im Browser"""
import datetime
from pagination               import Pagination
from conf.config              import Config
import ConfigParser

class TaglibBase():
   input_text_container             = '<input type="text" name="%(name)s" value="%(value)s" %(more)s/>'
   input_textmail_container         = '<input type="email" name="%(name)s" value="%(value)s" %(more)s/>'
   input_hidden_container           = '<input type="hidden" name="%(name)s" value="%(value)s" />'
   input_displayandhidden_container = '<input type="hidden" name="%(name)s" value="%(value)s" /><div class="displayandhidden">%(value)s</div>'
   input_select_container           = '<select name="%(name)s" %(more)s >\n %(options)s</select>\n'
   input_textarea_container         = '<textarea name="%(name)s" %(more)s>%(value)s</textarea>'
   input_label_container            = '<label class="mask" for="%(for)s" %(more)s>%(value)s</label>'
   input_label_grid_container       = '<label class="mask-grid-col" for="%(for)s" %(more)s>%(value)s</label>'

   deletebuttonIcon  = "../images/skin/normal/database_delete.png"
   editbuttonIcon    = "../images/skin/normal/database_edit.png"
   addbuttonIcon     = "../images/skin/normal/database_add.png"
   savebuttonIcon    = '../images/skin/normal/database_save.png'

   # ### Verhalten von HTML Tabellen
   #     in promptinput
   #
   TABLE_USE_NONE    = 0b00000000    # Keine <tr> und <td>
   TABLE_USE_TD      = 0b00000001    # Benutze <td>
   TABLE_USE_TR      = 0b00000010    # Benutze <tr>
   TABLE_USE_TRTD    = 0b00000011    # Benutze <tr> und <td>
   NOTABLE           = 0b11111111    # Keine <table>

   # Standardverhalten <tr> und <td>
   tableRowMode= TABLE_USE_TR | TABLE_USE_TD

   httpMethod = 'post'

   # Readonly Kennzeichen
   isReadonly = False

   cntTabLn=0                          # Zeilenzaehler fuer Tabelle
   default_input_ccs_class = None

   config = Config()

   formId      = 0
   fieldId     = 0
   lastFormId  = ''

   MONTHNAME = ('J&auml;nner',
                'Februar',
                'M&auml;z',
                'April',
                'Mai',
                'Juni',
                'Juli',
                'August',
                'September',
                'Oktober',
                'November',
                'Dezember')
                  
   def __init__(self,isReadonly=None,config=None):
      self.isReadonly = self.isReadonly or False
      formId      = 0
      fieldId     = 0
      
      if config is not None:
         self.config = config
      
   def getClass(self,theClass):
      """Liefert ein HTML class Attribute wenn nicht None"""
      if theClass is not None:
         return ' class="%(class)s" ' % {'class':theClass}
      else:
         if self.default_input_ccs_class is not None:
            return ' class="%(class)s" ' % {'class':self.default_input_ccs_class}
         else:
            return ''

   def getStyle(self,theStyle):
      """Liefert ein HTML style Attribute wenn nicht None"""
      if theStyle is not None:
         return ' style="%(style)s" ' % {'style':theStyle}
      else:
         return ''

   def isnull(value,nvl):
      """Wandelt den None in uebergebenen Wert aus nvl um"""
      if value is None:
         return nvl
      else:
         return value

   def _getYear(self,year):
      """ Liefert einen Jahreseintrag
          @param item      Jahr
                           als Integer: wird zurueckgeliefert
                           als Kennung:
                              'now'        aktuelles Jahr
                              'next'       aktuelles Jahr + 1
                              'last'       aktuelles Jahr - 1
          """
      # Abfangen ev. None
      if year is None: return None

      now = datetime.datetime.now()
      if year == 'now':
         year = now.year
      elif year == 'last':
         year = now.year
         year -= 1
      elif year == 'next':
         year = now.year
         year += 1
      else:
         year = int(year)
      return year


   def promptinput(
      self,
      prompt='',                                   # Promptstring
      id = None,                                   # ID-Tag im HTML
      name=None,                                   # Name fuer den HTML Tag
      value=None,                                  # Wert (value) des Tags, bei Type=Select der vorselektierte Wert
      maxlength=None,                              # Maxlength Attribut des Inputtags
      size=None,                                   # Size Attribut des Inputtags
      css_class=None,                              # CSS Klassenname
      datasource=None,                             # Datasource fuer Select Tag
      tableRowMode=TABLE_USE_TD + TABLE_USE_TR,    # Das Widget wird in HTML Tabellenzeile eingefuegt
      style=None,                                  # Style Attribut des Tags
      buttonIcon=None,                             # [True|False]  ist diese Option True wird das entsprechende Icon vor value gesetzt
      type='text',                                 # Type text, select, displayandhidden, submit
                                                   # HTML5 Spezial: @html5-type:[date,number, ...]
      nvl=None,                                    # Vorgabewert wenn value None ist
      fromyear=None,                               # Fuer Jahreswaehler von Jahr
      toyear=None,                                 # Fuer Jahreswaehler bis Jahr
      more = None,                                 # Weiter Parameter fuer das Widget
      addempty=None,                               # Fuer Jahreswaehler, wenn Angegeben wird der Inhalt in die  selectbox gestellt und als Jahr "0" erstellt
      text=None,                                   # Fuer Buttons, wird kein Text angegeben, wird value verwendet
      isReadonly=None,                             # Lokales setzen des Readonly Flags
      labelFor=None,                               # Foroption in Label
      jsOnBlur=None,                               # Javascript Event
      jsOnFocus=None,                              # Javascript Event
      jsOnClick=None,                              # Javascript Event
      jsOnDblClick=None,                           # Javascript Event
      jsOnChange=None,                             # Javascript Event
      jsOnKeyDown=None,                            # Javascript Event
      jsOnKeyPress=None,                           # Javascript Event   
      jsOnKeyUp=None,                              # Javascript Event
      jsOnOnMouseOver=None,                        # Javascript Event
      jsOnOnMouseOut=None,                         # Javascript Event
      jsOnOnMouseUp=None,                          # Javascript Event
      jsOnOnReset=None,                            # Javascript Event
      jsOnOnSelect=None,                           # Javascript Event
      highlightPrompt=None,
      highlightGridCol=None,
      ):
      """Liefert ein Input Widget"""

      # Steuerun des Readonly-Flags
      # wird dieses mit dem Aufruf uebergeben werden alle anderen
      # Einstellungen uebersteuert. Als zweites wird die Objekteinstellung verwendet.
      # der Vorgabewert ist False
      readonly = False
      auxid = ''

      if self.isReadonly:
         readonly = self.isReadonly

      if isReadonly is not None:
         readonly = isReadonly
            
         
      if readonly:
         type = 'display'
         value = value or ''

      if more is None: more = []
      
      auxName = name

      if id is not None:  
         auxid = id
         more.append('id="{0}"'.format(id))
         
      else:
         if type in ('label','grid-label'):
            if id is None:
               auxid = 'label-'+labelFor
               idid = 'id="{0}"'.format(auxid)
            else:
               auxid = id
               idid = 'id="{0}"'.format(id)

         else:
            if name is None:
               auxid = '{0}-{1}'.format(self.lastFormId,self.fieldId)
               idid = 'id="{0}"'.format(auxid)
               auxName = idid
            else:
               auxid = '{0}-{1}'.format(self.lastFormId,name)
               idid = 'id="{0}"'.format(auxid)
               auxName = name

         more.append(idid)
         self.fieldId += 1

      if maxlength         is not None:  more.append('maxlength="%(val)s"' % {'val':maxlength})
      if size              is not None:  more.append('size="%(val)s"' % {'val':size})

      if highlightPrompt:
         more.append('''onfocus="document.getElementById('label-grid-edit-'+this.getAttribute('name')).className='mask-active'" ''')
         more.append('''onblur="document.getElementById('label-grid-edit-'+this.getAttribute('name')).className='mask'" ''')

      if highlightGridCol:
         more.append('''onfocus="document.getElementById('label-grid-edit-'+this.getAttribute('name')).className='grid-col-active'" ''')
         more.append('''onblur="document.getElementById('label-grid-edit-'+this.getAttribute('name')).className='grid-col'" ''')

      #  JS Events ============================================================
      if jsOnBlur          is not None:  more.append('onblur="{0}"'.format(jsOnBlur))
      if jsOnFocus         is not None:  more.append('onfocus="{0}"'.format(jsOnFocus))
      if jsOnClick         is not None:  more.append('onclick="{0}"'.format(jsOnClick))
      if jsOnDblClick      is not None:  more.append('ondblclick="{0}"'.format(jsOnDblClick))
      if jsOnChange        is not None:  more.append('onchange="{0}"'.format(jsOnChange))
      if jsOnKeyDown       is not None:  more.append('onkeydown="{0}"'.format(jsOnKeyDown))
      if jsOnKeyPress      is not None:  more.append('onkeypress="{0}"'.format(jsOnKeyPress))
      if jsOnKeyUp         is not None:  more.append('onkeyup="{0}"'.format(jsOnKeyUp))
      if jsOnOnMouseOver   is not None:  more.append('ononmouseover="{0}"'.format(jsOnOnMouseOver))
      if jsOnOnMouseOut    is not None:  more.append('ononmouseout="{0}"'.format(jsOnOnMouseOut))
      if jsOnOnMouseUp     is not None:  more.append('ononmouseup="{0}"'.format(jsOnOnMouseUp))
      if jsOnOnReset       is not None:  more.append('ononreset="{0}"'.format(jsOnOnReset))
      if jsOnOnSelect      is not None:  more.append('ononselect="{0}"'.format(jsOnOnSelect))
      # END of JS Events ======================================================

      myClass = self.getClass(css_class)
      if myClass != '':
         more.append(myClass)

      myStyle = self.getStyle(style)
      if style is not None:
         myStyle = ' style="%(style)s" ' % {'style':style}
         more.append(myStyle)

      # Wenn value None ist wird der
      # angegebene Wert als Vorgabe eingesetzt
      if nvl is not None and value is None:
         value = nvl

      if type.startswith('@html5-type:'):
         widget = self.input_text_container % {
            'name':name,
            'value':value,
            'more':' '.join(more)
            }
         t = type[12:]
         widget = widget.replace('type="text"','type="{0}"'.format(t))

      elif type == 'text':
         widget = self.input_text_container % {
            'name':name,
            'value':value,
            'more':' '.join(more)
            }

      elif type == 'text-email':
         widget = self.input_textmail_container % {
            'name':name,
            'value':value,
            'more':' '.join(more)
            }

      elif type == 'textarea':
         widget = self.input_textarea_container % {
            'name':name,
            'value':value,
            'more':' '.join(more)
            }

      elif type == 'displayandhidden':
         widget = self.input_displayandhidden_container % {
            'name':name,
            'value':value
            }

      elif type == 'display':
         if nvl is not None:
            if value is None: value = nvl

         widget = value


      elif type == 'hidden':
         widget = self.input_hidden_container % {
            'name':name,
            'value':value
            }
      
      elif type == 'label':
         widget = self.input_label_container % {
            'for':labelFor,
            'more':' '.join(more),
            'value':value
            }
      
      elif type == 'grid-label':
         
         widget = self.input_label_grid_container % {
            'for':labelFor,
            'more':' '.join(more),
            'value':value
            }

      elif type == 'select' :

         if datasource is None:
            raise Exception('Methode promptinput mit Type select benoetigt den Parameter datasource')
         aOptions = []

         for option in datasource:                        
            if isinstance(option,list):
               
               selected = ''
               if (len(option) < 3):
                  if str(option[0]) == str(value): selected = ' selected '
               else:
                  if option[2] is not None:
                     selected = ' selected ' if option[2] else ''

               aOptions.append(' <option value="%(val)s"%(selected)s>%(text)s</option>\n' % {
                  'val':option[0],
                  'text':option[1],
                  'selected':selected
                  })

            elif isinstance(option,dict):
               selected = ''
               title = ''

               if 'value' in option:
                  val = option['value']
               else:
                  raise Exception("Bei select '{0}' fehlt in einer Option das value Attribut".format(name))

               if 'text' in option:
                  text = option['text']
               else:
                  raise Exception("Bei select '{0}' fehlt in einer Option das text Attribut".format(name))

               if 'selected' in option:
                  selected = ' selected ' if option['selected'] else ''
               else:
                  selected = ' selected ' if option['value'] == str(value) else ''
                                 
               if 'title' in option and option['title'] is not None:
                  title = ' title="{0}" '.format(option['title'])

               aOptions.append(' <option value="%(val)s"%(selected)s%(title)s>%(text)s</option>\n' % {
                  'val':val,
                  'text':text,
                  'selected':selected,
                  'title':title
                  })
            else:
               raise Exception(repr(option))
               
               raise Exception('Bei select Name: "{0}" als Parameter nur List oder Dictionary erlaubt.'.format(name))
               

         widget = self.input_select_container % {
            'name':name,
            'value':value,
            'more':' '.join(more),
            'options':' '.join(aOptions)
            }


      elif type=="chooseyear":
         now = datetime.datetime.now()

         nameatt = ''
         if name is not None:
            nameatt = ' name="%(name)s" ' %{'name':name}
         else:
            nameatt = ' name="%(name)s" ' %{'name':'year'}

         widget = '<select %(nameatt)s>\n' % {'nameatt':nameatt}

         fromyear = self._getYear(fromyear)
         toyear = self._getYear(toyear)
         curyear = self._getYear(value)

         lstOptions = []

         if addempty is not None:
            lstOptions.append(' <option value="0" >%(addempty)s</option>' % {'addempty':addempty})

         while fromyear <= toyear:
            selected = ''
            if curyear is not None and fromyear == curyear:
               selected = ' selected '
            else:
               selected = ''

            lstOptions.append(' <option value="%(fromyear)d" %(selected)s>%(fromyear)d</option>' % {
               'fromyear':fromyear,
               'selected':selected
               })
            fromyear+=1

         widget += '\n'.join(lstOptions)+'\n</select>'


      elif type=='submit':
         nameatt = ''
         if name is not None:
            nameatt = ' name="%(name)s" ' %{'name':name}
         if css_class is not None:
            css_class=' class="{0}" '.format(css_class)

         widget='<input type="submit" value="%(value)s" %(nameatt)s %(css_class)s/>' % {'value':value,'nameatt':nameatt,'css_class':css_class}

      # Liefert eine Schaltflaeche 'entfernen'
      elif type=='deletebutton':
         nameatt = ''
         if name is not None:
            nameatt = ' name="%(name)s" ' %{'name':name}
         widget='<button value="delete"  %(nameatt)s>%(value)s</button>' % {'value':value,'nameatt':nameatt}
      
      # ### Die Buttens sind fuer die Verwendung
      #     in Viewhandlern (Grind und List/Edit Layouts) optimiert
      #
      elif type=='addbutton':
         nameatt = ''
         if name is not None:
            nameatt = ' name="%(name)s" ' %{'name':name}
         
         prompt = '' if prompt is None else prompt

         if buttonIcon is None: buttonIcon = True
         if value is None: value = 'save'
         if name is None: name = 'action'
         if tableRowMode & self.TABLE_USE_TRTD: tableRowMode = self.TABLE_USE_TD

         if buttonIcon:
            # IE8-error: widget = '<button type="submit" name="{2}" value="{1}" title="{1}" class="grid-layout-button"><img src="{0}" />{3}</button>'.format(self.addbuttonIcon,value,name,prompt)
            widget = '<input type="image" title="{1}" class="grid-layout-button" src="{0}" /><input type="hidden" name="{2}" value="{1}"/>'.format(self.addbuttonIcon,value,name)
         else:
            widget='<button value="edit"  %(nameatt)s>%(value)s</button>' % {'value':value,'nameatt':nameatt}

      # Liefert eine Schaltflaeche zum Rueckspeichern (Haeckchen)
      elif type=='savebutton':
         if buttonIcon is None: buttonIcon = True
         if value is None: value = 'save'
         if name is None: name = 'action'
         if tableRowMode & self.TABLE_USE_TRTD: tableRowMode = self.TABLE_USE_TD
         if text is None: text = value


         if buttonIcon:
            #ie8 error: widget = '<button type="submit" name="{2}" value="{1}" title="{1}" class="grid-layout-button"><img src="{0}" /></button>'.format(self.savebuttonIcon,value,name)
            widget = '<input type="image" title="speichern" class="grid-layout-button" src="{0}" /><input type="hidden" name="{2}" value="{1}"/>'.format(self.savebuttonIcon,value,name)
         else:
            widget = '<button type="submit" name="{1}" title="speichern" value="{0}">{2}</button>'.format(value,name,text)

      elif type=='savebutton-save':
         if buttonIcon is None: buttonIcon = False
         if value is None: value = 'save'
         if name is None: name = 'action'
         if tableRowMode & self.TABLE_USE_TRTD: tableRowMode = self.TABLE_USE_NONE
         if text is None: text = value


         if buttonIcon:
            widget = '<button type="submit" name="{2}" value="{1}" title="{1}" class="grid-layout-button"><img src="{0}" /></button>'.format(self.savebuttonIcon,value,name)
         else:
            widget = '<button type="submit" name="{1}" title="{1}" value="{0}">{2}</button>'.format(value,name,text)

      elif type=='savebutton-delete':
         if buttonIcon is None: buttonIcon = False
         if value is None: value = 'delete'
         if name is None: name = 'action'
         if tableRowMode & self.TABLE_USE_TRTD: tableRowMode = self.TABLE_USE_NONE
         if text is None: text = value


         if buttonIcon:
            widget = '<button type="submit" name="{2}" value="{1}" title="{1}" class="grid-layout-button"><img src="{0}" /></button>'.format(self.savebuttonIcon,value,name)
         else:
            widget = '<button type="submit" name="{1}" title="{1}" value="{0}">{2}</button>'.format(value,name,text)
      else:
         raise Exception('ein bislang unbekannte type "{0}" stellt sich vor.'.format(type))
         
      # ### HTML-Table Bearbeiturng
      #     Abhaengig der Einstellungen in tableRowMode
      #     wir das Widget in unterschiedlech Formate eingebettet.
      #
      retval = ''

      # In <td> einbetten
      if tableRowMode & self.TABLE_USE_TD:
         if prompt != '':
            prompt = '' if prompt == '' else '<label class="mask" for="{0}" id="label-{2}">{1}</label>'.format(auxid,prompt,auxid)
            retval = '<td class="mask">{0}</td><td>{1}</td>'.format(prompt,widget)
         else:
            retval = '<td>{0}</td>'.format(widget)
      else:
         retval = widget

      # in <tr> einbetten
      if tableRowMode & self.TABLE_USE_TR:
         retval = '<tr>{0}</tr>'.format(retval)

         
      # Keine Einbettung
      if tableRowMode & self.TABLE_USE_NONE:            
         prompt = '' if prompt == '' else '<label class="mask" for="{0}" id="label-{2}">{1}</label>'.format(auxid,prompt,auxid)
         retval = '%(0)s%(1)s'.format(prompt,widget)
            
      return retval



   def form(self,name=None,style='display:inline;',css_class=None,method=None):
      """
      Liefert einen Form-Tag
      @param   name        Name der Form. Default: 'edit'
      @param   style       Styleattribut. Default: 'display:inline'
      @param   css_class   Classattribute. Default: Kein class
      @param   method      HTTP Form method (Vorgabewert 'post')
      """

      method = self.httpMethod if method is None else method

      self.formId += 1
      
      if name==None: name='edit-{0}'.format(self.formId)
      self.lastFormId = name

      myStyle = self.getStyle(style)

      return '\n<!-- BEGINN-FORM -->\n<form name="%(name)s" %(style)s method="%(method)s">' % {'name':name,'style':myStyle,'method':method}


   def endform(self):
      """Liefert einen End-Form Tag"""
      return '</form>\n<!-- END-FORM -->'


   def table(self,name=None,style=None,colgroup=None):
      """Liefert eine Table-Tag
         @param name          Name der Table
         @param style         Style Atritbute. Default nichts
         @param colgroup      Liefert nach dem Table-Tag ein Colgroup Tag
                              mit der Anzahl der Cols mit Breite 1%, Abschliessend
                              wird ein weitere Col Attribute mit dem Wert 99% eingefuegt
         """

      # Tabellen Zeilenzaehler auf Null stellen
      self.cntTabLn=0

      myName = ''
      if name is not None:
        myName = ' name="%(name)s" ' % {'name':name }
      myStyle = self.getStyle(style)
      aColgroup = []

      if colgroup is not None:
         aColgroup.append('\n<colgroup>')
         for cg in range(1,int(colgroup)):
            aColgroup.append('<col style="width:1%" />')
         aColgroup.append('<col style="width:99%"/>\n</colgroup>')
         colgroup = '\n '.join(aColgroup)
      else:
        colgroup = ''

      retval = '<table%(name)s%(style)s>%(colgroup)s' %{'name':myName,'style':myStyle,'colgroup':colgroup }
      return retval


   def tablehead(self,heads,css_class=None,style=None):
      """ Liefert eine Tabellenzeile
          @param heads        ist eine Liste von Tabellenkoepfe
          @param css_class    CSS Klasse fuer TH Element
          @param style        Style Attribut fuer TH Element
          """
      if heads is None:
         raise Exception("tablehead muss den parameter heads haben")

      ths = []
      ths.append('<thead><tr>')
      myClass = self.getClass(css_class)
      myStyle = self.getStyle(style)
      for head in heads:
         if isinstance(head,dict):            
            myClass = self.getClass(css_class) if not 'class' in head else self.getClass(head['class'])            
            myStyle = self.getStyle(style)     if not 'style' in head else self.getStyle(head['style'])

            text = head['text']
            if 'popup' in head:
               popup = '<span class="popup" title="" popup="{0}"><img src="../images/skin/normal/help.png" style="display:inline"/></span>'.format(head['popup'])
               ths.append('<th {1} {2}>{0}&nbsp;{3}</th>'.format(text, myClass, myStyle, popup))
            else:
               ths.append('<th {1}&nbsp;{2}>{0}</th>'.format(text, myClass, myStyle))
         else:
            ths.append('<th%(class)s%(style)s>%(text)s</th>' % {'class':myClass,'text':head,'style':myStyle})

      ths.append('</tr></thead>')
      return ''.join(ths)

   def tablerow(self,values='',usezebra=True):
      """Liefert eine Tabellenzeile"""

      retval = ''
      # Bei 1. Zeile
      if self.cntTabLn == 0: retval = '<tbody>'

      theClass=''

      if usezebra:
         self.cntTabLn+=1
         if self.cntTabLn % 2 != 0:
            thClass=' class="line-1" '
         else :
            thClass=' class="line-2" '

      vals=[]

      for value in values:
         vals.append('\n  <td class="list">%(value)s</td>' % {'value':value})

      retval += '\n <tr {0}>'.format(thClass)+'\n'.join(vals)+'\n </tr>'
      return  retval

   def endtable(self):
      """Liefert ein End-Table HTML Tag"""
      return '</tbody></table>'

   def hidden(self,name=None, value=None):
      """Liefert eine Hidden Inputtag"""
      if name==None:  raise Exception('hidden muss den Parameter name haben')
      if value==None:  raise Exception("hidden '{0}' muss den Parameter value haben".format(name))
      return '<input type="hidden" name="%(name)s" value="%(value)s" />' % {'name':name,'value':value}

   def gridButtons(self,id=None,addhidden=[],deletebutton=True,editbutton=True,isReadonly=None):
      """ Liefert einen Satz von Schaltflaechen in einer Form
         
         HINT:
            Ist in der CONFIG eine Variable confirmdelete definiert,
            wir der dort notierte Text in einer Javascript Confirmbox angezeigt.
         
         @param  id             Datensatzkennung
         @param  idname         Name der Datensatzkennung
                                 ist None dann wird 'id' angenommen.
         @param  addhidden      Zusaetzliche hidden Felder in der Form als Liste von Strings
         @param  deletebutton   True: Schaltflaeche zum Loeschen anzeigen
                                 action=edit
         @param  editbutton     True: Schaltflaeche zum Bearbeiten anzeigen
                                 action=delete
         @param  isReadonly     Lokale Uebersteueren der globalen isReadonly einstellung


          """
      
      if isReadonly is not None:
         readonly = isReadonly
      else:
         readonly = self.isReadonly
      
      if readonly: return '&nbsp;'

      retval = []
      sIdName = 'id'
      sValue = ''
      if isinstance(id,dict):
         sIdName  = id['name']
         sValue   = id['value']
      else:
         sValue = id

      if editbutton:
         retval.append(self.form(name='griededit',style='display:inline;'))
         retval.append(self.hidden(name='action',value='edit'))
         retval.append(self.hidden(name=sIdName,value=sValue))

         for hidden in addhidden:
            retval.append(self.hidden(name=hidden[0],value=hidden[1]))

         retval.append('<input type="image" src="{0}" class="mask" alt="bearbeiten" title="bearbeiten"/>'.format(self.editbuttonIcon))
         retval.append(self.endform())

      if deletebutton:
         onclick = ''         
         try:
            if self.config.confirmondelete:
               onclick = ''' onclick="return {0}" '''.format(self.config.confirmondelete)
         except: pass

         retval.append(self.form(name='griededit',style='display:inline;'))
         retval.append(self.hidden(name='action',value='delete'))
         retval.append(self.hidden(name=sIdName,value=sValue))
         for hidden in addhidden:
            retval.append(self.hidden(name=hidden[0],value=hidden[1]))
         retval.append('''<input type="image" src="{0}" {1} class="mask" alt="l&ouml;schen" title="l&ouml;schen" />'''.format(self.deletebuttonIcon,onclick))
         retval.append(self.endform())

      return '\n'.join(retval)

   def editButton(self,id=None,addhidden=[],idname=None):
      """ Liefert eine Edit Schaltflaeche in einer Form
          @param  id             Datensatzkennung
          @param  idname         Name des ID Feldes (Default 'id')
          @param  addhidden      Zusaetzliche hidden Felder in der Form als Liste von Strings
          """

      retval = []
      retval.append(self.form())
      retval.append(self.hidden(name='action',value='edit'))
      thisIdName = 'id'

      if idname is not None: thisIdName = idname

      retval.append(self.hidden(name=idname,value=id))
      for hidden in addhidden:
         retval.append(self.hidden(name=hidden[0],value=hidden[1]))
      retval.append('<input type="image" src="{0}" border="0" alt="bearbeiten" title="bearbeiten"/>'.format(self.editbuttonIcon))
      retval.append(self.endform())
      return '\n'.join(retval)

   def truncate(self,value=None,size=16,nvl=''):
      retval = ''
      title = value
      if value is None:
         value = nvl

      if len(value) > size :
         value = value[:size]
         while ord(value[-1]) > 127: value = value[:-1]
         value += '&hellip;'

      retval = '<span title="{1}">{0}</span>'.format(value,title)
      return retval

   def normalizeFilter(_filter):
      """
      Bearbeiten des Filters
      ''          -->   %
      None        -->   %
      *           -->   %
      ?           -->   _
      """
      _filter = '' if _filter is None else _filter

      _filter = _filter.rstrip(' ')
      _filter = '%' if _filter == '' else _filter
      _filter = _filter.replace('*','%')
      _filter = _filter.replace('?','_')

      return _filter
   normalizeFilter = staticmethod(normalizeFilter)

   def addhiddentolink (self,addhidden):
      retval = []
      for hd in addhidden:
         retval.append('{0}={1}'.format(hd[0],hd[1]))
      return '&'.join(retval)


   def paginationWidget (self,pagination,addhidden=[]):
      """
      Liefert die Ausgabe fuer Pagination

      @param   pagination        Paginierung Objekt

      """
      retval   = []
      aTpl = '<a href="start.py?_page={0}&{1}" class="{2}">{3}</a>'

      retval.append('<div class="pagination">')
      pages = 0
      pgnList = pagination.getPageList(pagination.curpage)
      for pg in pgnList:
         pages+=1
         cssClass = 'pagination'

         if pg == pagination.curpage:
            cssClass = 'pagination-current-page'
         retval.append(aTpl.format(pg,self.addhiddentolink(addhidden),cssClass,pg+1))

      # Wurden Seiten Gefunden
      if len(pgnList) != 0:
         # Beginnt die Liste mit der 1. Seite
         if pgnList[0] != 0:
            retval.insert(1,aTpl.format('0',self.addhiddentolink(addhidden),'pagination','|&lt;'))
         if pgnList[-1] != pagination.pages-1:
            retval.append(aTpl.format(pagination.pages-1,self.addhiddentolink(addhidden),'pagination','|&gt;'))


      retval.append('Pg: {0}/{1}'.format(pagination.curpage+1,pagination.pages))
      retval.append('</div>')
      return '\n'.join(retval)


   def tabbing (self,tabs=[],curtab=None):
      if curtab is None:
         raise Exception('die Option curpath nicht ueberegeben.')


      retval = []
      retval.append('<div class="tabbing">')
      retval.append('<ul class="tabbing">')
      for tab in tabs:
         if 'path' not in tab:
            raise Exception('In Tab "{0}" fehlt Path'.format(tab['text']))

         params = ''
         if 'param' in tab:
            params = '&'+'&'.join(tab['param'])

         link = '<a href="{0}?path={1}&_curtab={2}{3}" class="tabbing">{4}</a>'.format(self.config.homeurl,tab['path'],tab['name'],params,tab['text'])

         if tab['name'] == curtab:
            retval.append(' <li class="tabbing-active">{0}</li>'.format(link))
         else:
            retval.append(' <li class="tabbing">{0}</li>'.format(link))
      retval.append('</ul>')
      retval.append('</div>')
      return '\n'.join(retval)


