'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p
from OpenGL.GL import glget
EXTENSION_NAME = 'GL_MESAX_texture_stack'
_p.unpack_constants( """GL_TEXTURE_1D_STACK_MESAX 0x8759
GL_TEXTURE_2D_STACK_MESAX 0x875A
GL_PROXY_TEXTURE_1D_STACK_MESAX 0x875B
GL_PROXY_TEXTURE_2D_STACK_MESAX 0x875C
GL_TEXTURE_1D_STACK_BINDING_MESAX 0x875D
GL_TEXTURE_2D_STACK_BINDING_MESAX 0x875E""", globals())


def glInitTextureStackMESAX():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )