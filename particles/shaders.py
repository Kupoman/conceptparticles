import os
import inspect


from OpenGL.GL import *


_program = -1
_fragment = ("fragment.glsl", GL_FRAGMENT_SHADER)
_vertex = ("vertex.glsl", GL_VERTEX_SHADER)
_shaders = (_fragment, _vertex)


def get_program():
	global _program

	if _program != -1:
		return _program

	_program = glCreateProgram()

	file = inspect.getfile(inspect.currentframe())
	_dir = os.path.dirname(os.path.abspath(file)) + '/'
	for shader in _shaders:
		with open(_dir+shader[0]) as fin:
			source = fin.read()
			obj = glCreateShader(shader[1])
			glShaderSource(obj, source)
			glCompileShader(obj)
			log = glGetShaderInfoLog(obj).decode()
			if log:
				print(log)

			glAttachShader(_program, obj)

	glLinkProgram(_program)
	log = glGetProgramInfoLog(_program).decode()
	if log:
		print(log)

	return _program