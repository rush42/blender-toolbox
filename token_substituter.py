# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Token Substituter",
    "author": "Laurenz Rasche",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "description": "Enables C4D like tokens for render/compositor paths",
    "warning": "",
    "wiki_url": "https://github.com/rush42",
    "category": "System",
    }
    

import bpy
from bpy.app.handlers import persistent


import os
import time
import platform

def replace_tokens ( string ):
    tokens = {
        "$prj": os.path.basename(bpy.data.filepath).split(".")[0],
        "$camera": bpy.context.scene.camera.name,
        "$res": str(bpy.context.scene.render.resolution_x) + "x" + str(bpy.context.scene.render.resolution_y),
        "$CVCOMPUTER": platform.uname().node,
        "$CVRENDERER": bpy.context.scene.render.engine,
        "$CVHEIGHT": str(bpy.context.scene.render.resolution_y) + "p",

        "$YYYY":  str(time.localtime().tm_year),
        "$YY":  str(time.localtime().tm_year)[2:],
        "$MM":  str(time.localtime().tm_mon),
        "$DD":  str(time.localtime().tm_mday),
        "$H":  str(time.localtime().tm_hour),
        "$M":  str(time.localtime().tm_min),
        "$S":  str(time.localtime().tm_sec),

    }
    

    substituted_string = string

    for tkn in tokens:
        substituted_string = substituted_string.replace(tkn, tokens[tkn])

    return substituted_string

@persistent
def render_init (dummy):
    global path_backups

    path_backups = { "render": bpy.context.scene.render.filepath }
    bpy.context.scene.render.filepath = replace_tokens( bpy.context.scene.render.filepath )

    if( not(bpy.context.scene.render.use_compositing) ):
        return

    for compositor_node in  bpy.context.scene.node_tree.nodes.keys():
        node = bpy.context.scene.node_tree.nodes[ compositor_node ]

        if( node.type != "OUTPUT_FILE" ):
            continue

        path_backups[ compositor_node ] = node.base_path
        node.base_path = replace_tokens( node.base_path )

        for slot in range( len( node.file_slots ) ):

            path_backups[ "_".join( [ compositor_node, str( slot ) ] ) ] = node.file_slots[ slot ].path            
            node.file_slots[ slot ].path   = replace_tokens( node.file_slots[ slot ].path )
    print("Saved paths:")
    print(path_backups)

@persistent
def render_post ( dummy ):
    bpy.context.scene.render.filepath = path_backups[ "render" ]

    if( not(bpy.context.scene.render.use_compositing) ):
        return

    for compositor_node in  bpy.context.scene.node_tree.nodes.keys():
        node = bpy.context.scene.node_tree.nodes[ compositor_node ]

        if( node.type != "OUTPUT_FILE" ):
            continue

        print(compositor_node)
        node.base_path = path_backups[ compositor_node ]

        for slot in range( len( node.file_slots ) ):
            node.file_slots[ slot ].path = path_backups[ "_".join( [ compositor_node, str( slot ) ] ) ]


def register():
    bpy.app.handlers.render_init.append( render_init )
    bpy.app.handlers.render_cancel.append( render_post ) 
    bpy.app.handlers.render_complete.append( render_post )
    print("Token Substituter: enabled")
                                   
def unregister():
    bpy.app.handlers.render_init.remove( render_init )
    bpy.app.handlers.render_cancel.remove( render_post ) 
    bpy.app.handlers.render_complete.remove( render_post )
    print("Token Substituter: disabled")


if __name__ == "__main__":
    register()
