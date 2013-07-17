import random
import ctypes


from OpenGL.GL import *


from .particle import PARTICLE
from .shaders import getProgram


class System:
	def __init__(self):
		self.system_properties = {}
		self.particle_proeprties = {}
		self._particles = (PARTICLE * 1000)()
		self._x = (ctypes.c_float * (3 * 1000))()
		self._last_particle = 10
		self._buffer_id = glGenBuffers(1)
		
		glBindBuffer(GL_ARRAY_BUFFER, self._buffer_id)
		glBufferData(GL_ARRAY_BUFFER, 1000*ctypes.sizeof(PARTICLE),
						None, GL_DYNAMIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		self.update()

	def update(self):
		for i in range(self._last_particle):
			particle = self._particles[i]
			particle.x = (random.random() - 0.5) * 2 * 5
			particle.y = (random.random() - 0.5) * 2 * 5
			particle.z = (random.random() - 0.5) * 2 * 5
		
		glBindBuffer(GL_ARRAY_BUFFER, self._buffer_id)
		glBufferSubData(GL_ARRAY_BUFFER, 0,
						self._last_particle*ctypes.sizeof(PARTICLE),
						self._particles)

	def draw(self):
		glUseProgram(getProgram())
		
		glPointSize(5)
		glEnable(GL_POINT_SPRITE)
		glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		glVertexPointer(3, GL_FLOAT, ctypes.sizeof(PARTICLE), ctypes.c_void_p(0))
		glEnableClientState(GL_VERTEX_ARRAY)
		glDrawArrays(GL_POINTS, 0, self._last_particle)
		
		glUseProgram(0)
