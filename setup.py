#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setup.py for installing ZenityShell

Usage:
   python setup.py install

Copyright 2011-2012 Maxiste Deams all rights reserved,
Maxiste Deams <maxistedeams@gmail.com>
Permission to use, modify, and distribute this software is given under the
terms of the New BSD license :
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided when fullfiling requirement in
    License.txt, take time to read. 

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 0.0.1-r001a-ekcebo-ivaritt $
$Date: Mon Sep 10 22:01:31 EDT 2012 $
Maxiste Deams
"""
import os, sys, re, numpy
from distutils.core import setup
import UnderscoreX
from UnderscoreX import * 



ActualModuleInformation = dir( )

PackageHandler = open( 'PKG-INFO', 'r+' )
FileLicenseH = open( 'LICENCE.TXT', 'r+' )

TagSplit=re.compile( r'(?i):' )
TagReg=re.compile( r'(?i)^[a-z0-9\-]*:' )
ExceptionTag=[ 'metadata_version', 'license' ]
InListForTag=[ 'keywords','classifiers','requires','platforms']


for Item in PackageHandler.readlines( ):
    if TagReg.search( Item):
        TagInfo=TagSplit.split( Item, 1  )
        TagTransform=TagInfo[0].replace( '-', '_' ).lower()
        TagContent=TagInfo[1].replace( '\n', '' ) 
        if TagTransform not in ExceptionTag:
            if TagTransform in InListForTag:
                nameListVar='List{}'.format( TagTransform )
                if not hasattr( __builtins__, nameListVar ):
                    print "No List present for Item {}".format( nameListVar )
                    setattr( __builtins__, nameListVar, list() )
                else:
                    print "Append {} to Var {}".format( TagContent, nameListVar )
                    getattr( getattr( __builtins__, nameListVar ), 'append' )( TagContent )
            else:
                nameUniqueVar='Unique{}'.format( TagTransform , TagContent)
                print "Var {} will hold: [ {} ] ".format( nameUniqueVar, TagContent)
                setattr( __builtins__, 'Unique{}'.format( TagTransform ), TagContent )

for ListTagVar in InListForTag:
    nameListVar='List{}'.format( ListTagVar )
    if not hasattr( __builtins__, nameListVar ):
        setattr( __builtins__, nameListVar, list() )

UseNumpyDistutilsConfiguration = False


def configuration( PackageName ):
    Pconfig = Configuration( PackageName, 
                             top_path=None,
                             parent_package='')
    return Pconfig
    
if __name__ == "__main__":
    ListAttr=[ 'make_svn_version_py', 'make_config_py' ]

    if UseNumpyDistutilsConfiguration:
        config = configuration( __package__ )
        config.add_data_dir('UnderscoreX')
        config.add_subpackage('UnderscoreX')
        config = config.todict()

    
    if 'config' in dir():
        for AddAttr in ListAttr:
            if hasattr( config, AddAttr ):
                if callable( getattr( config, AddAttr ) ) :
                    getattr( getattr( config, AddAttr )( ) )
    
        if sys.version[:3] >= '2.6':
            config['download_url'] = "http://github.com/priendeau/UnderscoreX"
            config['author']= "Maxiste Deams"
            config['author_email']= __author_email__
            config['classifiers'] = ClassifierField
    
    setup( name=Uniquename,
           version=Uniqueversion,
           url=Uniqueurl,
           description=Uniquedescription,
           license=FileLicenseH.read(),
           long_description=Uniquelong_description,
           keywords = Listkeywords,
           classifiers=Listclassifiers ,
           author_email = Uniqueauthor_email,
           download_url = Uniquedownload_url,
           author = Uniqueauthor,
           maintainer = Uniquemaintainer,
           maintainer_email = Uniquemaintainer_email,
           requires = Listrequires, 
           platforms = Listplatforms )
