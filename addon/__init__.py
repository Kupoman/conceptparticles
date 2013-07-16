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

class SystemNode(Node, ParticleTreeNode):
	'''System node'''
	bl_label = 'System'
	bl_icon = 'NODETREE'

	def init(self, context):
		self.inputs.new('NodeSocketVector', "Position")
		self.inputs.new('NodeSocketVector', "Color")

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

class ParticleNodeCategory(NodeCategory):
	@classmethod
	def poll(cls, context):
		return context.space_data.tree_type == 'ParticleTree'

node_categories = [
	ParticleNodeCategory("SYSTEM", "System Nodes", items=[NodeItem("SystemNode")])
]

def register():
	bpy.utils.register_class(ParticleTree)
	bpy.utils.register_class(SystemNode)
	nodeitems_utils.register_node_categories("PARTICLE_NODES", node_categories)

def unregister():
	bpy.utils.unregister_class(ParticleTree)
	bpy.utils.unregister_class(SystemNode)
	nodeitems_utils.unregister_node_categories("PARTICLE_NODES")

if __name__ == "__main__":
	register()