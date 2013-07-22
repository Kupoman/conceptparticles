import random
import ctypes


from OpenGL.GL import *
import PIL.Image as pil


from .particle import GPUPARTICLE, CPUPARTICLE
from .shaders import get_program
from .property import Property
from .generators import get_generator


def _struct_copy(dst, src):
	for field in src._fields_:
		fname = field[0]
		setattr(dst, fname, getattr(src, fname))


class System:
	def __init__(self):
		self._system_properties = {}
		self._particle_properties = {}
		self._texture_path = "sprites/stars_4.png"
		self._capacity = 0
		self._particles = []
		self._particle_data = []
		self._size = 0
		self._buffer_id = glGenBuffers(1)
		self._texture_id = glGenTextures(1)
		self._uniform_loc = {}
		self._attrib_loc = {}

		self._expand(1000)

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
		
		self._uniform_loc['texture'] = \
			glGetUniformLocation(get_program(), b"texture")
		self._uniform_loc['model_view_mat'] = \
			glGetUniformLocation(get_program(), b"model_view_mat")
		self._uniform_loc['projection_mat'] = \
			glGetUniformLocation(get_program(), b"projection_mat")
		self._attrib_loc['position'] = \
			glGetAttribLocation(get_program(), b"position_in")
		self._attrib_loc['color'] = \
			glGetAttribLocation(get_program(), b"color_in")

		self._init_props()

	def _init_props(self):
		self._particle_properties["position"] = \
			Property("position", "VECTOR", (0, 0, 0))
		self._particle_properties["position"].generator = \
			get_generator("MIX3", {"n3":"LINEAR"})
		self._particle_properties["color"] = \
			Property("color", "COLOR", (1.0, 1.0, 1.0, 1.0))

	def _add_particle(self):
		if self._size >= self._capacity:
			self._expand(self._capacity*2)

		self._size += 1

		particle = self._particles[self._size-1]
		data = self._particle_data[self._size-1]

		data.life = 60
		data.time = 0

	def _remove_particle(self, index):
		self._size -= 1

		tmp_part = GPUPARTICLE()
		tmp_data = CPUPARTICLE()

		_struct_copy(tmp_part, self._particles[self._size])
		_struct_copy(tmp_data, self._particle_data[self._size])

		_struct_copy(self._particles[self._size], self._particles[index])
		_struct_copy(self._particle_data[self._size], self._particle_data[index])

		_struct_copy(self._particles[index], tmp_part)
		_struct_copy(self._particle_data[index], tmp_data)
		
	def _expand(self, new_capacity):
		new_parts = (GPUPARTICLE * new_capacity)()
		new_data = (CPUPARTICLE * new_capacity)()

		for i in range(self._size):
			_struct_copy(new_parts[i], self._particles[i])
			_struct_copy(new_data[i], self._particle_data[i])

		self._capacity = new_capacity

		self._particles = new_parts
		self._particle_data = new_data

		glBindBuffer(GL_ARRAY_BUFFER, self._buffer_id)
		glBufferData(GL_ARRAY_BUFFER, self._capacity*ctypes.sizeof(GPUPARTICLE),
						None, GL_DYNAMIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, 0)

	def update(self):
		self._add_particle()
		rem_list = []
		for i in range(self._size):
			particle = self._particles[i]
			data = self._particle_data[i]
			data.time += 1

			if data.time >= data.life:
				rem_list.append(i)

			value = self._particle_properties['position'].get_value(data.time)
			particle.x = value[0]
			particle.y = value[1]
			particle.z = value[2]

			value = self._particle_properties['color'].get_value(0)
			particle.r = value[0]
			particle.g = value[1]
			particle.b = value[2]
			particle.a = value[3]
		
		for index in rem_list:
			self._remove_particle(index)

		glBindBuffer(GL_ARRAY_BUFFER, self._buffer_id)
		glBufferSubData(GL_ARRAY_BUFFER, 0,
						self._size*ctypes.sizeof(GPUPARTICLE),
						self._particles)

	def draw(self, model_view, projection):
		self.update()

		glUseProgram(get_program())

		glEnable(GL_TEXTURE_2D)
		glEnable(GL_POINT_SPRITE)
		glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self._texture_id)
		glUniform1i(self._uniform_loc['texture'], 0)

		glUniformMatrix4fv(self._uniform_loc['model_view_mat'], 1, GL_FALSE,
							model_view)
		glUniformMatrix4fv(self._uniform_loc['projection_mat'], 1, GL_FALSE,
							projection)

		glEnableVertexAttribArray(0)
		glVertexAttribPointer(self._attrib_loc['position'],
								3, GL_FLOAT, GL_FALSE, 
								ctypes.sizeof(GPUPARTICLE), ctypes.c_void_p(0))
		glEnableVertexAttribArray(1)
		glVertexAttribPointer(self._attrib_loc['color'],
								4, GL_FLOAT, GL_TRUE, 
								ctypes.sizeof(GPUPARTICLE), 
								ctypes.c_void_p(GPUPARTICLE.r.offset))

		glDrawArrays(GL_POINTS, 0, self._size)

		glUseProgram(0)
		glBindTexture(GL_TEXTURE_2D, 0)
