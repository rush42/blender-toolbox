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
    "name": "Save Incremental",
    "author": "Laurenz Rasche",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "description": "Enables incremental saving for projects",
    "warning": "",
    "wiki_url": "https://github.com/rush42",
    "category": "System",
    }
    
import bpy
from bpy.types import Operator, Menu
from bpy.utils import register_class
import os


def save_incremental( self, context ):
    file_folder = os.path.dirname( bpy.data.filepath )
    file_name = os.path.basename( bpy.data.filepath )

    print(f"old name: {file_name}")


    try:
        if( file_name[ -6: ] == ".blend" ):
            file_name = file_name[:-6]
        else:
            raise  IndexError
    except:
        print("invalid file extension")
        return -1


    num_digits = 0

    for c in file_name[::-1]:
        if( c.isdigit() ):
            num_digits += 1
        else:
            break

    if( num_digits ):
        version = int( file_name[-num_digits:] )
        file_name = file_name[:-num_digits]
        version += 1
    else:
        version = 1
        num_digits = 2

    version = str( version )
    version = "0" * ( num_digits - len( version ) ) + version


    file_name = f"{ file_name }{ version }.blend"


    file_list = [file  for file in os.listdir(file_folder) if file.count(".blend") and not file.count("blend1") ] 
    if( file_name in file_list ):
        print("file already exists")
        return -1
 

    save_path = os.path.join( file_folder, file_name )
    #bpy.ops.wm.save_as_mainfile()
    bpy.ops.wm.save_as_mainfile(filepath=save_path)  

    return 0     


class Save_Incremental (bpy.types.Operator):
    """Save the current file with increased version number"""
    bl_idname = "file.save_incremental"
    bl_label = "Save Incremental"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if( not( save_incremental(self, context) ) ):
            return {'FINISHED'}
        
        return {'CANCELLED'}
   

def menu_draw(self, context):
    self.layout.operator( "file.save_incremental" )

def register():
    register_class( Save_Incremental )
    bpy.types.TOPBAR_MT_file.prepend(menu_draw)

def unregister():
    bpy.types.TOPBAR_MT_file.remove(menu_draw)
    return


if __name__ == "__main__":
    register()
