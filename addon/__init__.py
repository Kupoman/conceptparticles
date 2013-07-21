bl_info = {
    "name": "Concept Particles",
    "author": "Daniel Stokes, Mitchell Stokes",
    "version": (0, 0),
    "blender": (2, 68, 0),
    "location": "",
    "description": "BGE Particles",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Game Engine"}


import bpy
from bpy_types import NodeTree, Node, NodeSocket
import particles.generators


class ParticleTree(NodeTree):
	'''A node tree for particles'''
	bl_label = 'Particle Tree'
	bl_icon = 'PARTICLES'


class ParticleTreeNode:
	@classmethod
	def poll(cls, ntree):
		return ntree.bl_idname == 'ParticleTree'


# ------- #
# Sockets #
# ------- #


class NodeSocketParticleProperties(NodeSocket):
	'''Socket for particle properties'''
	bl_label = 'Particle Properties'

	def draw(self, context, layout, node, text):
		layout.label(text)

	def draw_color(self, context, node):
		if self.is_linked:
			return (0.0, 1.0, 0.0, 1.0)
		else:
			return (1.0, 0.0, 0.0, 1.0)


# ------------ #
# System Nodes #
# ------------ #


class SystemNode(Node, ParticleTreeNode):
	'''System node'''
	bl_label = 'System'
	bl_icon = 'NODETREE'

	def init(self, context):
		self.inputs.new('NodeSocketVectorTranslation', "Position")
		self.inputs.new('NodeSocketParticleProperties', "Particle Properties")

	def draw_buttons(self, context, layout):
		layout.label("System Properties")
		layout.label("Particle Properties")


class ParticlePropertiesNode(Node, ParticleTreeNode):
	'''Node for per particle properties'''
	bl_label = 'Particle Properties'

	def init(self, context):
		self.inputs.new('NodeSocketColor', "Color")
		self.outputs.new('NodeSocketParticleProperties', "System")


# --------------- #
# Node Categories #
# --------------- #


import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem


class ParticleNodeCategory(NodeCategory):
	@classmethod
	def poll(cls, context):
		return context.space_data.tree_type == 'ParticleTree'

node_categories = [
	ParticleNodeCategory("SYSTEM", "System Nodes", items=[
		NodeItem("SystemNode"),
		NodeItem("ParticlePropertiesNode"),
	])
]


# ------------ #
# Registration #
# ------------ #


nodes = [
	SystemNode,
	ParticlePropertiesNode,
]


def register():
	bpy.utils.register_class(ParticleTree)
	bpy.utils.register_class(NodeSocketParticleProperties)

	generated_nodes = []

	for i in [i[0] + i[1:].lower() for i in particles.generators.GENERATORS]:
		cls = getattr(particles.generators, i)
		init_str = """def init(self, context):\n"""
		for inp in cls.__slots__:
			init_str += """\tself.inputs.new('NodeSocketFloat', "%s")\n""" % inp

		init_str += """\tself.outputs.new('NodeSocketFloat', "Value")\n"""
		exec(init_str)

		d = {
			"bl_label": cls.__name__,
			"init": locals()['init'],
		}
		node = type(cls.__name__+"Node", (Node, ParticleTreeNode), d)
		nodes.append(node)
		generated_nodes.append(node)

	node_categories.append(ParticleNodeCategory("GENERATORS", "Generators",\
		items = [NodeItem(i.__name__) for i in generated_nodes]))

	for i in nodes:
		bpy.utils.register_class(i)

	try:
		nodeitems_utils.register_node_categories("PARTICLE_NODES", node_categories)
	except KeyError:
		nodeitems_utils.unregister_node_categories("PARTICLE_NODES")
		nodeitems_utils.register_node_categories("PARTICLE_NODES", node_categories)



def unregister():
	bpy.utils.unregister_class(ParticleTree)
	bpy.utils.unregister_class(NodeSocketParticleProperties)

	for i in nodes:
		bpy.utils.unregister_class(i)

	nodeitems_utils.unregister_node_categories("PARTICLE_NODES")


if __name__ == "__main__":
	register()
