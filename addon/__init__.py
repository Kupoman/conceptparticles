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
from particles.defaults import PROPERTIES
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


class NodeSocketGeneratorScalar(NodeSocket):
	'''Node socket type for scalar generators'''
	bl_label = 'Scalar Generator'

	def draw(self, context, layout, node, text):
		layout.label(text)

	def draw_color(self, context, node):
		return (1.0, 0.4, 0.216, 1.0)


class NodeSocketGeneratorVector(NodeSocket):
	'''Node socket type for vector generators'''
	bl_label = 'Vector Generator'

	def draw(self, context, layout, node, text):
		layout.label(text)

	def draw_color(self, context, node):
		return (0.4, 1.0, 0.216, 1.0)


class NodeSocketGeneratorColor(NodeSocket):
	'''Node socket type for color generators'''
	bl_label = 'Color Generator'

	def draw(self, context, layout, node, text):
		layout.label(text)

	def draw_color(self, context, node):
		return (0.4, 0.216, 1.0, 1.0)


# ------------ #
# System Nodes #
# ------------ #


class SystemNode(Node, ParticleTreeNode):
	'''System node'''
	bl_label = 'System'
	bl_icon = 'NODETREE'

	def init(self, context):
		types = {
			'SCALAR': 'NodeSocketGeneratorScalar',
			'VECTOR': 'NodeSocketGeneratorVector',
			'COLOR': 'NodeSocketGeneratorColor',
		}

		for k,v in PROPERTIES.items():
			socket = types.get(v.type)
			if socket:
				self.inputs.new(socket, k)
			else:
				print("Unrecognized type for system property:", k)


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
		NodeItem("SystemNode")
	])
]


# --------- #
# Operators #
# --------- #


def write_generator(node):
	d = {"type": node.bl_label.upper()}

	for prop in node.props:
		d[prop] = getattr(node, prop)

	for inp_sock in [i for i in node.inputs if i.is_linked]:
		d[inp_sock.name.lower().replace(" ", "_")] = write_generator(inp_sock.links[0].from_node)

	return d


def write_property(node, prop):
	ns = node.inputs.get(prop)

	if not ns.is_linked:
		return

	return {
		"name": prop,
		"location": node.location[:],
		"generator": write_generator(ns.links[0].from_node),
	}


def write_node_tree(context, filepath, use_pretty_print):
	nt = context.space_data.node_tree

	systems = [node for node in nt.nodes if node.bl_label == 'System']

	systems_out = []

	for system in systems:
		props = []
		for i in PROPERTIES:
			prop = write_property(system, i)
			if prop:
				props.append(prop)

		sysd = {
			"properties": props,
		}

		systems_out.append(sysd)


	out = {
		"name": nt.name,
		"systems": systems_out,
		}

	with open(filepath, "w") as f:
		json.dump(out, f, indent=4 if use_pretty_print else None)


class ExportNodeTree(bpy.types.Operator, ExportHelper):
	'''Save the particle node tree to a file'''
	bl_idname = "particles.export_tree"
	bl_label = "Export Particle Tree"

	filename_ext = ".fx"
	filter_glob = bpy.props.StringProperty(
			default="*.fx",
			options={'HIDDEN'},
		)

	use_pretty_print = bpy.props.BoolProperty(
			name="Use Pretty Print",
			description="Add nice formatting to the output file",
			default=True,
		)

	def execute(self, context):
		write_node_tree(context, self.filepath, self.use_pretty_print)
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
	SystemNode
]


sockets = [
	NodeSocketGeneratorScalar,
	NodeSocketGeneratorVector,
	NodeSocketGeneratorColor,
]


def register():
	bpy.utils.register_class(ParticleTree)

	generated_nodes = []

	socket_types = {
		'GENERATOR_SCALAR': 'NodeSocketGeneratorScalar',
		'GENERATOR_VECTOR': 'NodeSocketGeneratorVector',
		'GENERATOR_COLOR': 'NodeSocketGeneratorColor',
		}

	property_types = {
		'SCALAR': (bpy.props.FloatProperty, {}),
		'VECTOR': (bpy.props.FloatVectorProperty, {'subtype':'XYZ', 'size':3}),
		'COLOR':  (bpy.props.FloatVectorProperty, {'subtype':'COLOR', 'size':4}),
		}

	for i in [i[0] + i[1:].lower() for i in particles.generators.GENERATORS]:
		cls = getattr(particles.generators, i)
		d = {"bl_label": cls.__name__}
		props = []

		# Create init method
		init_str = """def init(self, context):\n"""
		for k,v in cls.type_map.items():
			if v.startswith('GENERATOR'):
				init_str += """\tself.inputs.new('%s', "%s")\n""" % (socket_types[v], k.title().replace('_', ' '))
			else:
				d[k] = property_types[v][0](name=k.title().replace('_', ' '), **property_types[v][1])
				props.append(k)

		init_str += """\tself.outputs.new('%s', "Value")\n""" % socket_types['GENERATOR_' + cls.out_type]
		exec(init_str)

		d["init"] = locals()['init']

		# Create draw_buttons method
		if props:
			db_str = """def draw_buttons(self, context, layout):\n"""
			for prop in props:
				db_str += """\tlayout.prop(self, "%s")\n""" % prop

			exec(db_str)
			d["draw_buttons"] = locals()['draw_buttons']
		d["props"] = props
		
		node = type(cls.__name__+"Node", (Node, ParticleTreeNode), d)
		nodes.append(node)
		generated_nodes.append(node)

	node_categories.append(ParticleNodeCategory("GENERATORS", "Generators",\
		items = [NodeItem(i.__name__) for i in generated_nodes]))

	for i in nodes+sockets:
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

	for i in nodes+sockets:
		bpy.utils.unregister_class(i)

	nodeitems_utils.unregister_node_categories("PARTICLE_NODES")

	bpy.utils.unregister_class(ExportNodeTree)

	bpy.utils.unregister_class(ParticleNodesPanel)


if __name__ == "__main__":
	register()
