#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
# Name: ZenityShell.py
# Author:   Initial version, Brian Ramos, modified by Maxiste Deams
# Created: 09/17/2012
# Revision Information:

### Copyright (c) 2004-2012, Maxiste Deams, alis Patrick Riendeau.
### All rights reserved.
### 
### Redistribution and use in source and binary forms, with or without
### modification, are permitted provided that the following conditions are met:
###     * Redistributions of source code must retain the above copyright
###       notice, this list of conditions and the following disclaimer.
###     * Redistributions in binary form must reproduce the above copyright
###       notice, this list of conditions and the following disclaimer in the
###       documentation and/or other materials provided with the distribution.
###     * Neither the name of the <organization> nor the
###       names of its contributors may be used to endorse or promote products
###       derived from this software without specific prior written permission.
### 
### THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
### ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
### WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
### DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
### DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
### (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
### LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
### ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
### (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
### SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
################################################################################
from datetime import date
from subprocess import Popen, PIPE
from itertools import chain
from os import path

__all__ = ['GetDate', 'GetFilename', 'GetDirectory', 'GetSavename', 'GetText',
           'InfoMessage', 'Question', 'Warning', 'ErrorMessage', 
           'Notification', 'TextInfo', 'Progress','List','AddBasicParameter' ]

zen_exec = 'zenity'


### See zenity --help-all, General option, There is no way to add all theses.
##    General options
##        --title=TITLE                                  Set the dialogue title
##        --window-icon=ICONPATH                         Set the window icon
##        --width=WIDTH                                  Set the width
##        --height=HEIGHT                                Set the height
##        --timeout=TIMEOUT                              Set dialogue timeout in seconds
##        --ok-label=TEXT                                Sets the label of the Ok button
##        --cancel-label=TEXT                            Sets the label of the Cancel button

def AddBasicParameter( **kwargs ):
    for ItemParam in kwargs.keys():
        ArgValue='--{}={}'.format( ItemParam, kwargs[ItemParam] )
        print "ZenityShell: Following parameter will be added, {}".format( ArgValue )
        args.append( ArgValue )


def run_zenity(type, *args):
    return Popen([zen_exec, type] + list(args), stdin=PIPE, stdout=PIPE)


def GetDate(text=None, selected=None,**kwargs):
    """Prompt the user for a date.
    
    This will raise a Zenity Calendar Dialog for the user to pick a date.
    It will return a datetime.date object with the date or None if the 
    user hit cancel.
    
    text - Text to be displayed in the calendar dialog.
    selected - A datetime.date object that will be the pre-selected date.

    **kwargs - To add any Generic Information like height, width, other type of
    title and icons as well.
    """

    args = ['--date-format=%d/%m/%y']
    if text:
        args.append('--text=%s' % text)
    if selected:
        args.append('--day=%d' % selected.day)
        args.append('--month=%d' % selected.month)
        args.append('--year=%d' % selected.year)

    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( None, 'kwargs' ):
        AddBasicParameter( kwargs ) 

    p = run_zenity('--calendar', *args)

    if p.wait() == 0:
        retval = p.stdout.read().strip()
        day, month, year = [int(x) for x in retval.split('/')]
        return date(year, month, day)


def GetFilename(multiple=False, sep='|',**kwargs):
    """Prompt the user for a filename.
    
    This will raise a Zenity File Selection Dialog. It will return a list with 
    the selected files or None if the user hit cancel.
    
    multiple - True to allow the user to select multiple files.
    sep - Token to use as the path separator when parsing Zenity's return 
          string.

    **kwargs - To add any Generic Information like height, width, other type of
    title and icons as well.
    """

    args = []
    if multiple:
        args.append('--multiple')
    if sep != '|':
        args.append('--separator=%s' % sep)

    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( None, 'kwargs' ):
        AddBasicParameter( kwargs ) 
    
    p = run_zenity('--file-selection', *args)

    if p.wait() == 0:
        return p.stdout.read()[:-1].split('|')


def GetDirectory(multiple=False, selected=None, sep=None,**kwargs):
    """Prompt the user for a directory.
    
    This will raise a Zenity Directory Selection Dialog.  It will return a 
    list with the selected directories or None if the user hit cancel.
    
    multiple - True to allow the user to select multiple directories.
    selected - Path to the directory to be selected on startup.
    sep - Token to use as the path separator when parsing Zenity's return 
          string.

    **kwargs - To add any Generic Information like height, width, other type of
    title and icons as well.
    """

    args = ['--directory']
    if multiple:
        args.append('--multiple')
    if selected:
        if not path.lexists(selected):
            raise ValueError("File %s does not exist!" % selected)
        args.append('--filename=%s' % selected)
    if sep:
        args.append('--separator=%s' % sep)

    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( None, 'kwargs' ):
        AddBasicParameter( kwargs ) 
    
    p = run_zenity('--file-selection', *args)

    if p.wait() == 0:
        return p.stdout.read().strip().split('|')


def GetSavename(default=None,**kwargs):
    """Prompt the user for a filename to save as.
    
    This will raise a Zenity Save As Dialog.  It will return the name to save 
    a file as or None if the user hit cancel.
    
    default - The default name that should appear in the save as dialog.

    **kwargs - To add any Generic Information like height, width, other type of
    title and icons as well.

    """

    args = ['--save']
    if default:
        args.append('--filename=%s' % default)
    
    p = run_zenity('--file-selection', *args)

    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( None, 'kwargs' ):
        AddBasicParameter( kwargs ) 

    if p.wait() == 0:
        return p.stdout.read().strip().split('|')


def Notification(text=None, icon=None,**kwargs):
    """Put an icon in the notification area.
    
    This will put an icon in the notification area and return when the user
    clicks on it.
    
    text - The tooltip that will show when the user hovers over it.
    icon - The stock icon ("question", "info", "warning", "error") or path to 
           the icon to show.
    **kwargs - To add any Generic Information like height, width, other type of
    title and icons as well.
    """

    args = []
    if text:
        args.append('--text=%s' % text)
    if icon:
        args.append('--window-icon=%s' % icon)

    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( None, 'kwargs' ):
        AddBasicParameter( kwargs ) 
    
    p = run_zenity('--notification', *args)
    p.wait()


def List(column_names, title=None, boolstyle=None, editable=False, 
         select_col=None, sep='|', data=[], **kwargs ):
    """Present a list of items to select.
    
    This will raise a Zenity List Dialog populated with the colomns and rows 
    specified and return either the cell or row that was selected or None if 
    the user hit cancel.
    
    column_names - A tuple or list containing the names of the columns.
    title - The title of the dialog box.
    boolstyle - Whether the first columns should be a bool option ("checklist",
                "radiolist") or None if it should be a text field.
    editable - True if the user can edit the cells.
    select_col - The column number of the selected cell to return or "ALL" to 
                 return the entire row.
    sep - Token to use as the row separator when parsing Zenity's return. 
          Cells should not contain this token.
    data - A list or tuple of tuples that contain the cells in the row.  The 
           size of the row's tuple must be equal to the number of columns.

    **kwargs - To add any Generic Information like height, width, other type of
    title and icons as well. 
    """

    args = []
    for column in column_names:
        args.append('--column=%s' % column)
    
    if title:
        args.append('--title=%s' % title)
    if boolstyle:
        if not (boolstyle == 'checklist' or boolstyle == 'radiolist'):
            raise ValueError('"%s" is not a proper boolean column style.'
                             % boolstyle)
        args.append('--' + boolstyle)
    if editable:
        args.append('--editable')
    if select_col:
        args.append('--print-column=%s' % select_col)
    if sep != '|':
        args.append('--separator=%s' % sep)

    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( None, 'kwargs' ):
        AddBasicParameter( kwargs ) 
    
    for datum in chain(*data):
        args.append(str(datum))
    
    p = run_zenity('--list', *args)

    if p.wait() == 0:
        return p.stdout.read().strip().split(sep)


def ErrorMessage(text,**kwargs):
    """Show an error message dialog to the user.
    
    This will raise a Zenity Error Dialog with a description of the error.
    
    text - A description of the error."""

    args = [ ]
    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( 'kwargs' ):
        AddBasicParameter( kwargs ) 

    run_zenity('--error', '--text=%s' % text, *args ).wait()


def InfoMessage(text,**kwargs):
    """Show an info message dialog to the user.
    
    This will raise a Zenity Info Dialog displaying some information.
    
    text - The information to present to the user.

    **kwargs - To add any Generic Information like height, width, other type of
    title and icons as well.
    
    """
    args = []
    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( None, 'kwargs' ):
        AddBasicParameter( kwargs ) 
    run_zenity('--info', '--text=%s' % text, *args).wait()


def Question(text,**kwargs):
    """Ask the user a question.
    
    This will raise a Zenity Question Dialog that will present the user with an 
    OK/Cancel dialog box.  It returns True if the user clicked OK; False on 
    Cancel.
    
    text - The question to ask.

    **kwargs - To add any Generic Information like height, width, other type of
    title and icons as well.
    """
    args = []
    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( None, 'kwargs' ):
        AddBasicParameter( kwargs ) 

    return run_zenity('--question', '--text=%s' % text,*args).wait() == 0


def Warning(text,**kwargs):
    """Show a warning message dialog to the user.
    
    This will raise a Zenity Warning Dialog with a description of the warning.
    It returns True if the user clicked OK; False on cancel.
    
    text - A description of the warning.

    **kwargs - To add any Generic Information like height, width, other type of
    title and icons as well.
    """

    args = []
    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( None, 'kwargs' ):
        AddBasicParameter( kwargs ) 
    return run_zenity('--warning', '--text=%s' % text, *args).wait() == 0


def Progress(text='', percentage=0, auto_close=False, pulsate=False, **kwargs):
    """Show a progress dialog to the user.
    
    This will raise a Zenity Progress Dialog.  It returns a callback that 
    accepts two arguments.  The first is a numeric value of the percent 
    complete.  The second is a message about the progress.

    NOTE: This function sends the SIGHUP signal if the user hits the cancel 
          button.  You must connect to this signal if you do not want your 
          application to exit.
    
    text - The initial message about the progress.
    percentage - The initial percentage to set the progress bar to.
    auto_close - True if the dialog should close automatically if it reaches 
                 100%.
    pulsate - True is the status should pulsate instead of progress.

    **kwargs - To add any Generic Information like height, width, other type of
    title and icons as well.
    """

    args = []
    if text:
        args.append('--text=%s' % text)
    if percentage:
        args.append('--percentage=%s' % percentage)
    if auto_close:
        args.append('--auto-close=%s' % auto_close)
    if pulsate:
        args.append('--pulsate=%s' % pulsate)

    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( None, 'kwargs' ):
        AddBasicParameter( kwargs )
        
    p = Popen([zen_exec, '--progress'] + args, stdin=PIPE, stdout=PIPE)

    def update(percent, message=''):
        if type(percent) == float:
            percent = int(percent * 100)
        p.stdin.write(str(percent) + '\n')
        if message:
            p.stdin.write('# %s\n' % message)
        return p.returncode

    return update


def GetText(text='', entry_text='', password=False, **kwargs):
    """Get some text from the user.

    This will raise a Zenity Text Entry Dialog.  It returns the text the user 
    entered or None if the user hit cancel.

    text - A description of the text to enter.
    entry_text - The initial value of the text entry box.
    password - True if text entered should be hidden by stars.

    **kwargs - To add any Generic Information like height, width, other type of
    title and icons as well.
    
    """

    args = []
    if text:
        args.append('--text=%s' % text)
    if entry_text:
        args.append('--entry-text=%s' % entry_text)
    if password:
        args.append('--hide-text')

    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( None, 'kwargs' ):
        AddBasicParameter( kwargs )
        
    p = run_zenity('--entry', *args)

    if p.wait() == 0:
        return p.stdout.read()[:-1]


def TextInfo(filename=None, editable=False, **kwargs):
    """Show the text of a file to the user.

    This will raise a Zenity Text Information Dialog presenting the user with 
    the contents of a file.  It returns the contents of the text box.

    filename - The path to the file to show.
    editable - True if the text should be editable.

    **kwargs - To add any Generic Information like height, width, other type of
    title and icons as well.
    """

    args = []
    if filename:
        args.append('--filename=%s' % filename)
    if editable:
        args.append('--editable')

    ### Addin, ensure all backend like title, window-icon width height timeout ok-label cancel-label ...
    if hasattr( None, 'kwargs' ):
        AddBasicParameter( kwargs )

    p = run_zenity('--text-info', *args)

    if p.wait() == 0:
        return p.stdout.read()

