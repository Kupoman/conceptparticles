'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p
from OpenGL.GL import glget
EXTENSION_NAME = 'GL_APPLE_aux_depth_stencil'
_p.unpack_constants( """GL_AUX_DEPTH_STENCIL_APPLE 0x8A14""", globals())


def glInitAuxDepthStencilAPPLE():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
