ZenityShell
===========

Zenity Module with more option embedded for fast integration



Example
===========

::
		import ZenityShell
		from ZenityShell import *

		class ZenitySShKeyMenu( object ):

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
			self.KeyName = List( MenuList , title=Title , boolstyle="radiolist", editable=False , data=DataMenu, **Kargs )
   
