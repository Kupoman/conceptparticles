import bpy
from bpy_types import NodeTree, Node, NodeSocket


class ParticleTree(NodeTree):
	'''A node tree for particles'''
	bl_label = 'Particle Tree'
	bl_icon = 'NODETREE'


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
# Generator Nodes #
# --------------- #

class RandomScalarGeneratorNode(Node, ParticleTreeNode):
	'''Generates random scalar values'''
	bl_label = 'Random Scalar Generator'

	def init(self, context):
		self.outputs.new('NodeSocketFloat', "Value")

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
	]),

	ParticleNodeCategory("SCALAR_GENERATORS", "Scalar Generators", items=[
		NodeItem("RandomScalarGeneratorNode"),
	]),
]


# ------------ #
# Registration #
# ------------ #


nodes = [
	SystemNode,
	ParticlePropertiesNode,
	RandomScalarGeneratorNode,
]


def register():
	bpy.utils.register_class(ParticleTree)
	bpy.utils.register_class(NodeSocketParticleProperties)

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
