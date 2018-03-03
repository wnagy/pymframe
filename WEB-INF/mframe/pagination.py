from math import ceil


class Pagination(object):
   records     = 0
   pagesize    = 0
   curpage     = 0
   radius      = 0
   pages       = 0
   leftPages   = 0
   rightPages  = 0

   def __init__ (self,curpage=0,records=0,pagesize=16,radius=4):
      self.curpage   = curpage
      self.records   = records
      self.pagesize  = pagesize
      self.radius    = radius
      if self.pagesize != 0:
         self.pages     = int(ceil(self.records / float(self.pagesize)))



   def getPageList (self,curpage = None):
      retval = []
      
      if curpage is None:
         raise Exception('Aktuelle Seite fehlt')
      self.curpage = curpage
      if self.curpage > self.pages: self.curpage = self.pages

      # Berechne linke Seite
      self.leftPages = self.curpage - self.radius
      # berechne rechte Seite
      self.rightPages = self.curpage + self.radius

      # Adjustiere Seitenraender
      if self.rightPages > self.pages:
         self.leftPages -= abs(self.pages-self.rightPages)

      if self.leftPages < 0:
         self.rightPages = (self.radius*2)
         self.leftPages = 0
      if self.rightPages > self.pages: self.rightPages = self.pages

      for p in range(self.leftPages,self.rightPages):
         retval.append(p)

      return retval
