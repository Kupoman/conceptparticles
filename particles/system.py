import random
import ctypes


from OpenGL.GL import *
import PIL.Image as pil


from .particle import PARTICLE
from .shaders import getProgram


class System:
	def __init__(self):
		self.system_properties = {}
		self.particle_proeprties = {}
		self._texture_path = "sprites/stars_4.png"
		self._particles = (PARTICLE * 1000)()
		self._x = (ctypes.c_float * (3 * 1000))()
		self._last_particle = 10
		self._buffer_id = glGenBuffers(1)
		self._texture_id = glGenTextures(1)
		self._uniform_loc = {}
		
		glBindBuffer(GL_ARRAY_BUFFER, self._buffer_id)
		glBufferData(GL_ARRAY_BUFFER, 1000*ctypes.sizeof(PARTICLE),
						None, GL_DYNAMIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		self.update()
		
		im = pil.open(self._texture_path)
		try:
			imdata = im.tostring("raw", "RGBA", 0, -1)
		except (SystemError):
			imdata = im.tostring("raw", "RGBX", 0, -1)
		
		glBindTexture(GL_TEXTURE_2D, self._texture_id)
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, im.size[0], im.size[1],
						0, GL_RGBA, GL_UNSIGNED_BYTE, imdata)
		glBindTexture(GL_TEXTURE_2D, 0)
		
		self._uniform_loc['texture'] = glGetUniformLocation(getProgram(), b"texture")

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
		glEnable(GL_TEXTURE_2D)
		glEnable(GL_POINT_SPRITE)
		glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self._texture_id)
		glUniform1i(self._uniform_loc['texture'], 0)
		
		glVertexPointer(3, GL_FLOAT, ctypes.sizeof(PARTICLE), ctypes.c_void_p(0))
		glEnableClientState(GL_VERTEX_ARRAY)
		glDrawArrays(GL_POINTS, 0, self._last_particle)
		
		glUseProgram(0)
		glBindTexture(GL_TEXTURE_2D, 0)
