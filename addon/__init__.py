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
from bpy_extras.io_utils import ExportHelper
import particles.generators
from particles.defaults import SYSTEM_PROPERTIES, PARTICLE_PROPERTIES
import json


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
		for i in SYSTEM_PROPERTIES:
			if i['type'] == 'VECTOR':
				self.inputs.new('NodeSocketVector', i['name'].title())
			elif i['type'] == 'COLOR':
				self.inputs.new('NodeSocketColor', i['name'].title())
			else:
				print("Unrecognized type for system property:", i['name'])
		self.inputs.new('NodeSocketParticleProperties', "Particle Properties")


class ParticlePropertiesNode(Node, ParticleTreeNode):
	'''Node for per particle properties'''
	bl_label = 'Particle Properties'

	def init(self, context):
		for i in PARTICLE_PROPERTIES:
			if i['type'] == 'VECTOR':
				self.inputs.new('NodeSocketVector', i['name'].title())
			elif i['type'] == 'COLOR':
				self.inputs.new('NodeSocketColor', i['name'].title())
			else:
				print("Unrecognized type for system property:", i['name'])
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


# --------- #
# Operators #
# --------- #


def write_generator(node):
	return {
		"type": node.bl_label.upper(),
	}


def write_property(node, prop):
	ns = node.inputs.get(prop.title())

	if not ns.is_linked:
		return

	return {
		"name": prop,
		"location": node.location[:],
		"generator": write_generator(ns.links[0].from_node),
	}


def write_node_tree(context, filepath):
	nt = context.space_data.node_tree

	systems = [node for node in nt.nodes if node.bl_label == 'System']

	systems_out = []

	for system in systems:
		ns = system.inputs.get("Particle Properties")
		if not ns.is_linked:
			print("Found system with no particle properties, skipping")
			continue

		sys_props = []
		for i in SYSTEM_PROPERTIES:
			prop = write_property(system, i['name'])
			if prop:
				sys_props.append(prop)

		part_props_node = ns.links[0].from_node

		part_props = []
		for i in PARTICLE_PROPERTIES:
			prop = write_property(part_props_node, i['name'])
			if prop:
				part_props.append(prop)

		sysd = {
			"particle_properties": part_props,
			"system_properties": sys_props,
		}

		systems_out.append(sysd)


	out = {
		"name": nt.name,
		"systems": systems_out,
		}

	with open(filepath, "w") as f:
		json.dump(out, f, indent=4)


class ExportNodeTree(bpy.types.Operator, ExportHelper):
	'''Save the particle node tree to a file'''
	bl_idname = "particles.export_tree"
	bl_label = "Export Particle Tree"

	filename_ext = ".fx"
	filter_glob = bpy.props.StringProperty(
			default="*.fx",
			options={'HIDDEN'},
		)

	def execute(self, context):
		write_node_tree(context, self.filepath)
		return {'FINISHED'}


# ----- #
# Panel #
# ----- #


class ParticleNodesPanel(bpy.types.Panel):
	bl_label = 'Particles'
	bl_idname = 'NODES_PT_particle_operators'
	bl_space_type = 'NODE_EDITOR'
	bl_region_type = 'UI'

	@classmethod
	def poll(cls, context):
		return context.space_data.tree_type == 'ParticleTree'

	def draw(self, context):
		layout = self.layout

		layout.operator(ExportNodeTree.bl_idname)

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

	bpy.utils.register_class(ExportNodeTree)

	bpy.utils.register_class(ParticleNodesPanel)


def unregister():
	bpy.utils.unregister_class(ParticleTree)
	bpy.utils.unregister_class(NodeSocketParticleProperties)

	for i in nodes:
		bpy.utils.unregister_class(i)

	nodeitems_utils.unregister_node_categories("PARTICLE_NODES")

	bpy.utils.unregister_class(ExportNodeTree)

	bpy.utils.unregister_class(ParticleNodesPanel)


if __name__ == "__main__":
	register()
