# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright or � or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#--------------------------------------------------------------------------------

__doc__=""" Build directory configure environment. """
__license__= "Cecill-C"
__revision__="$Id: $"


import os, sys
from openalea.sconsx.config import *

class Compiler:

   def __init__( self, config ):
      self.name= 'compiler'
      self.config= config
      self._default= {}


   def default( self ):

      self._default[ 'debug' ]= False
      self._default[ 'warnings' ]= False
      self._default[ 'static' ]= False

      if isinstance( platform, Posix ):
         compilers= ['gcc']
      elif isinstance( platform, Win32 ):
         compilers= ['msvc', 'mingw']
      else:
         raise "Add a compiler support for your os !!!"

      self._default[ 'compilers' ]= compilers


   def option(  self, opts ):

      self.default()

      opts.Add( BoolOption( 'debug', 
                            'compilation in a debug mode',
                            self._default[ 'debug' ] ) )
      opts.Add( BoolOption( 'warnings',
                            'compilation with -Wall and similar',
                            self._default[ 'warnings' ] ) )
      opts.Add( BoolOption( 'static',
                            '',
                            self._default[ 'static' ] ) )

      compilers= self._default[ 'compilers' ]
      default_compiler= compilers[0]
      opts.Add( EnumOption('compiler',
                           'compiler tool used for the build',
                           default_compiler,
                           compilers ) )
                           
                           
      opts.Add( 'rpath', 'A list of paths to search for shared libraries')

      opts.Add( 'EXTRA_CXXFLAGS', 'Specific user flags for c++ compiler', '')
      opts.Add( 'EXTRA_CPPDEFINES', 'Specific c++ defines', '')
      opts.Add( 'EXTRA_LINKFLAGS', 'Specific user flags for c++ linker', '')
      opts.Add( 'EXTRA_CPPPATH', 'Specific user include path', '')
      opts.Add( 'EXTRA_LIBPATH', 'Specific user library path', '')
      opts.Add( 'EXTRA_LIBS', 'Specific user libraries', '')


   def update( self, env ):
      """ Update the environment with specific flags """

      # Set the compiler
      compiler_name= env['compiler']
      self.config.add_tool(compiler_name)
      
      if isinstance( platform, Cygwin ):
         env.AppendUnique( CPPDEFINES= 'SYSTEM_IS__CYGWIN' )
      elif isinstance( platform, Win32 ):
         env.AppendUnique( CPPDEFINES= 'WIN32' )

      env.Append( RPATH= Split( '$rpath' ) )
      env.Append( CXXFLAGS= Split( env['EXTRA_CXXFLAGS'] ) )
      env.Append( CPPDEFINES= Split( env['EXTRA_CPPDEFINES'] ) )
      env.Append( LINKFLAGS= Split( env['EXTRA_LINKFLAGS'] ) )
      env.Append( CPPPATH= Split( env['EXTRA_CPPPATH'] ) )
      env.Append( LIBPATH= Split( env['EXTRA_LIBPATH'] ) )
      env.Append( LIBS= Split( env['EXTRA_LIBS'] ) )


   def configure( self, config ):
      pass

def create( config ):
   " Create compiler tool "
   compiler= Compiler( config )

   return compiler
