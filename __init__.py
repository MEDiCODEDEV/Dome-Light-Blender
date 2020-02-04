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

import bpy, os
from . Dome_Light import *
from bpy.props import *
from bpy.types import Panel, Operator, Menu
from bpy.utils import previews
global img_path

# Add-on info
bl_info = {
    "name": "Dome Light",
    "author": "Wanderson M Pimenta",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Properties > Dome Light",
    "description": "Create a Dome Light", 
    "wiki_url": "",
    "tracker_url": "",      
    "category": "3D View"}
    
classes = (Buttom_Create_PT_Dome_Light, Painel_UI_Dome_Light, OBJECT_OT_custompath, WORLD_OT_remove_unused_images)

def register():
    
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
def unregister():
    
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()