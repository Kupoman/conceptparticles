'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p, constants as _cs, arrays
from OpenGL.GL import glget
import ctypes
EXTENSION_NAME = 'GL_EXT_point_parameters'
def _f( function ):
    return _p.createFunction( function,_p.GL,'GL_EXT_point_parameters',False)
_p.unpack_constants( """GL_POINT_SIZE_MIN_EXT 0x8126
GL_POINT_SIZE_MAX_EXT 0x8127
GL_POINT_FADE_THRESHOLD_SIZE_EXT 0x8128
GL_DISTANCE_ATTENUATION_EXT 0x8129""", globals())
@_f
@_p.types(None,_cs.GLenum,_cs.GLfloat)
def glPointParameterfEXT( pname,param ):pass
@_f
@_p.types(None,_cs.GLenum,arrays.GLfloatArray)
def glPointParameterfvEXT( pname,params ):pass


def glInitPointParametersEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
