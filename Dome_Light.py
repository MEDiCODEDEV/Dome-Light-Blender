# ##### FREE ADDON - EASYHDR-BASED EXTENSION
#
# Modified by: Wanderson M Pimenta
# Credits to EasyHDRI: http://codeofart.com/easy-hdri-2-8/
#
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.props import *
from bpy.types import Panel, Operator, Menu
from bpy.utils import previews
global img_path

#CREATE NODES
def create_world_nodes():
    
    scn = bpy.context.scene
    worlds = bpy.data.worlds
    # Make sure the render engine is Cycles or Eevee
    if not scn.render.engine in ['CYCLES', 'BLENDER_EEVEE']:
        scn.render.engine = 'BLENDER_EEVEE'
    # Add a new world "EasyHDR", or reset the existing one
    if not 'World' in worlds:
        world = bpy.data.worlds.new("World")        
    else:
        world = worlds['World']
    scn.world = world       
    # Enable Use nodes
    world.use_nodes= True
    # Delete all the nodes (Start from scratch)
    world.node_tree.nodes.clear()
    
    # Adding new nodes
    tex_coord = world.node_tree.nodes.new(type="ShaderNodeTexCoord")    
    mapping = world.node_tree.nodes.new(type="ShaderNodeMapping")   
    env = world.node_tree.nodes.new(type="ShaderNodeTexEnvironment")  
    background = world.node_tree.nodes.new(type="ShaderNodeBackground")
    gamma = world.node_tree.nodes.new(type="ShaderNodeGamma")
    saturation = world.node_tree.nodes.new(type="ShaderNodeHueSaturation")
    color = world.node_tree.nodes.new(type="ShaderNodeMixRGB")
    math_multiply = world.node_tree.nodes.new(type="ShaderNodeMath")
    math_divide = world.node_tree.nodes.new(type="ShaderNodeMath")
    math_add = world.node_tree.nodes.new(type="ShaderNodeMath")    
    output = world.node_tree.nodes.new(type="ShaderNodeOutputWorld") 
       
    # Change the parameters
    env.name = 'Environment'
    background.name = 'Background'
    mapping.name = 'Mapping'
    saturation.name = 'Saturation'
    math_multiply.name = 'Math_multiply'
    math_multiply.operation = 'MULTIPLY'
    math_multiply.inputs[1].default_value = 0.0
    math_divide.name = 'Math_divide'
    math_divide.operation = 'DIVIDE'
    math_divide.inputs[1].default_value = 100.0
    math_add.name = 'Math_add'   
    math_add.operation = 'ADD'   
    math_add.inputs[1].default_value = 1.0
    color.blend_type = 'MULTIPLY'  
    color.inputs[0].default_value = 0.0
        
    world.node_tree.links.new(tex_coord.outputs['Generated'], mapping.inputs[0])
    world.node_tree.links.new(mapping.outputs[0], env.inputs[0])
    world.node_tree.links.new(env.outputs[0], gamma.inputs[0])
    world.node_tree.links.new(gamma.outputs[0], saturation.inputs[4])
    world.node_tree.links.new(saturation.outputs[0], color.inputs[1])
    world.node_tree.links.new(env.outputs[0], math_multiply.inputs[0])
    world.node_tree.links.new(math_multiply.outputs[0], math_divide.inputs[0])
    world.node_tree.links.new(math_divide.outputs[0], math_add.inputs[0])
    world.node_tree.links.new(math_add.outputs[0], background.inputs[1])
    world.node_tree.links.new(color.outputs[0], background.inputs[0])
    world.node_tree.links.new(background.outputs[0], output.inputs[0])    
    
    # Nodes location    
    tex_coord.location = (130, 252)
    mapping.location = (310, 252)
    env.location = (680, 252)
    gamma.location = (960, 350)
    saturation.location = (1120, 350)
    color.location = (1290, 350)
    math_multiply.location = (960, 100)
    math_divide.location = (1120, 100)
    math_add.location = (1290, 100)
    background.location = (1500, 252)
    output.location = (1660, 252)
    
# REMOVE UNUSED IMAGES
def remove_images():
    images = bpy.data.images
    for img in bpy.data.images:
        if not img.users or (img.users == 1 and img.use_fake_user):
            bpy.data.images.remove(img)

# Check the World's node tree
def Verify_World_Nodes():
    nodes_list = ['Texture Coordinate', 'Mapping', 'Background',
                  'World Output', 'Environment', 'Math_multiply',
                  'Math_divide', 'Math_add', 'Mix', 'Saturation',
                  'Gamma']
    all_found = True              
    scn = bpy.context.scene
    worlds = bpy.data.worlds
    if not scn.world:
        return 'Fix'        
    if not 'World' in worlds:
        return 'Create'
    else:
        world = worlds['World']
        nodes = world.node_tree.nodes
        if len(nodes) > 0:
            for n in nodes_list:
                if not n in nodes:
                    all_found = False
            if not all_found:
                return 'Fix'
        else:
            return 'Fix'
    if not scn.world.name == 'World':
        return 'Fix'      

#CLASS CREATE DOME LIGHT            
class BUTTON_PT_Create_Dome_Light(bpy.types.Operator):
    bl_idname = "view3d.domelight"
    bl_label = "FIX DOME LIGHT"
    bl_description = "Create Dome Light"
    
    def execute(self, context):
        create_world_nodes()
        return {'FINISHED'}

# REMOVE UNUSED IMAGES
class WORLD_OT_remove_unused_images(bpy.types.Operator):
    bl_idname = "world.remove_images"
    bl_label = "Remove unused images"
    bl_description = "Remove unused user images"
    
    def execute(self, context):
        remove_images()
        return {'FINISHED'}

#OPEN IMAGES
class OBJECT_OT_custompath(bpy.types.Operator):
    bl_idname = "view3d.custom_path"
    bl_label = "Select HDR file"
    bl_description = "Open Dome Light File"
    
    filename_ext = ".hdr;.exr;.png"
    filter_glob = StringProperty(default="*.hdr;*.exr;*.png", options={'HIDDEN'})    

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    files = CollectionProperty(
        name="File Path",
        type=bpy.types.OperatorFileListElement,
        )
    def execute(self, context):
              
        #change image
        bpy.data.images.load(filepath=self.properties.filepath, check_existing=True)
        print(self.properties.filepath)
        limit = 2
        index = 1
        for file in self.files:
            bpy.data.worlds["World"].node_tree.nodes["Environment"].image = bpy.data.images[file.name]
            
            index += 1
            if index == limit:
                break
            
        return {'FINISHED'}
    
    def draw(self, context):
        self.layout.operator('file.select_all_toggle') 
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'} 

#PAINEL INFO
class PAINEL_UI_Dome_Light(bpy.types.Panel) :
    bl_idname = "BUTTON_PT_Create_Dome_Light"
    bl_label = "Dome Light"
    bl_category = "Dome Light"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        col = layout.column()
        box = col.box()
        col = box.column()      
        if Verify_World_Nodes() == 'Create':
            col.operator("view3d.domelight", icon = 'WORLD_DATA')
        elif Verify_World_Nodes() == 'Fix':
            col.label(text = 'Create Dome Light:', icon = 'OUTLINER_OB_LIGHT')
            col.operator("view3d.domelight", text = 'CREATE DOME LIGHT', icon = 'WORLD_DATA') 
        else:
            col.label(text = 'Open HDRI:', icon = 'IMAGE_DATA')
            nodes = scn.world.node_tree.nodes
            box = col.box()
            box.operator('view3d.custom_path', text = "Open HDRI")
            #col.label(text = 'HDRI:', icon = 'NONE')
            box.prop(nodes['Environment'], "image", text = '')
            col.label(text = '')
            col.label(text = 'Dome Light Settings:', icon = 'WORLD_DATA')
            box = col.box()       
            if 'Math_add' in nodes:
                box.prop(nodes['Math_add'].inputs[1], "default_value", text = 'Intensity')
            if 'Math_multiply' in nodes:
                box.prop(nodes['Math_multiply'].inputs[1], "default_value", text = 'Sun Intensity')
            if 'Gamma' in nodes:
                box.prop(nodes['Gamma'].inputs[1], "default_value", text = "Gamma")
            if 'Saturation' in nodes:
                box.prop(nodes['Saturation'].inputs[1], "default_value", text = "Saturation")
            if 'Mix' in nodes:
                box.prop(nodes['Mix'].inputs[2], "default_value", text = "Tint")        
                box.prop(nodes['Mix'].inputs[0], "default_value", text = "Intensity")
            #print(OBJECT_OT_custompath.filepath)
            box.label(text = 'Projection:', icon = 'NONE')
            
            box.prop(nodes['Environment'], "projection", text = '') 
            
            box.prop(nodes["Mapping"].inputs[2], "default_value", text = "Rotation")
            
            col.label(text = '')
            box = col.box()
            box.operator("world.remove_images", text = 'REMOVE UNUSED IMAGES', icon = 'TRASH')