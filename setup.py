from distutils.core import setup

setup(name='ZenityShell',
      version='0.0.1-r001a-ekcebo-ivaritt',
      description='Zenity Module with more option embedded for fast integration',
      author='Maxiste Deams, Patrick Riendeau',
      author_email='maxistedeams@gmail.com',
      maintainer='Maxiste Deams',
      maintainer_email='maxistedeams@gmail.com',
      url='http://pypi.python.org/pypi?%3Aaction=pkg_edit&name=ZenityShell',
      download_url='http://pypi.python.org/pypi?:action=files&name=ZenityShell&version=0.0.1-r001a-ekcebo-ivaritt',
      license='BSD',
      long_description="""Zenity Shell is a known UI from debian familly packages, somes already published
some work  under  reserve, they had not  all the switch  available for a more
customizable prototypying, providing some work around it offert more complete
solution.

Example
=======


This is a simple class example with property involved to create a simple File selection menu.

import ZenityShell
from ZenityShell import *

class ZenityKeyMenu( object ):

  ListColumn = list()
  MenuTitle = None
  DataMenuList=list()

  def __init__( self , **Kargs ):
    self.TitleName  = "Choose your Key to add inside AgentLoader"
    self.ColumnName = "Selection", "Key Name"
    self.DataMenu = ["FALSE","None"], ["FALSE","GitHub Key"], ["FALSE","PyPi SSH Key"]
    self.ZenityMenuKey( **Kargs )

  def getColumnName( self ):
    return self.ListColumn

  def setColumnName( self , value ):
    if len( value ) == 1 :
      self.ListColumn.append( value )
    if len( value ) > 1 :
      IterValue=iter( value ) 
      try :
        while True:
          self.ListColumn.append( IterValue.next() )
      except StopIteration:
        pass 

  def eraseColumnName( self ):
    del self.ListColumn
    self.ListColumn = list()
    return True 

  def getTitle( self ):
    return MenuTitle

  def setTitle( self, value ):
    self.MenuTitle= value

  def eraseTitle( self ):
    self.MenuTitle=None

  def getDataMenu( self ):
    return self.DataMenuList

  def setDataMeny( self , value ):
    if len( value ) == 1 :
      DefaultValue, NameValue = value 
      self.DataMenuList.append( DefaultValue, NameValue )
    if len( value ) > 1 :
      IterValue=iter( value ) 
      try :
        while True:
          self.DataMenuList.append( IterValue.next() )
      except StopIteration:
        pass     
    
  def eraseDataMenu( self ):
    del self.DataMenuList
    self.DataMenuList=list()
    
    
  ColumnName  = property( getColumnName,  setColumnName,    eraseColumnName )
  TitleName   = property( getTitle,       setTitle,         eraseTitle )
  DataMenu    = property( getDataMenu,    setDataMeny,      eraseDataMenu )
  
  def ZenityMenuKey( self , **Kargs ):
    MenuList  = self.ColumnName
    Title     = self.MenuTitle
    DataMenu  = self.DataMenu
    ### 
    self.KeyName = List( MenuList , title=Title , boolstyle="radiolist", editable=False , data=DataMenu, **Kargs )

  ### This demonstrate uses of **kwargs not present in Equal development, like PyZenity, Height and
  ### Width are not handled, also cancel-message an ok messages. 

if __name__.__eq__( '__main__' ):
  AMenu = ZenitySShKeyMenu( width=300 ,height=300 )

""", py_modules=['ZenityShell'])
