bl_info = {
    "name": "Write Arabic Text",
    "author": "ﻦﻳﺪﻟﺍ ﻲﺤﻣ ﺪﻴﺷﺭ",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3Dviewport, Text edit mode",
    "description": "ﺔﻴﺑﺮﻌﻟﺍ ﺔﻐﻠﻟﺎﺑ ﺺﻧ ﺔﺑﺎﺘﻛ",
    "warning": "",
    "wiki_url": "",
    "category": "Text",
}

import bpy
from . import ArabicTextTools as Ar


# Keyboard Handler

class __OT_ArabicTextMode(bpy.types.Operator):

    bl_idname = "view3d.arabic_text_mode"
    bl_label = "Write Arabic Text"
    
    #
    
    def modal(self, context, event):
        
        global text_buffer
        
        global current_char_index
        
        # Use this handler only when a 3DText object is selected and being edited
        
        if bpy.context.object is None or bpy.context.object.type != 'FONT' or bpy.context.object.mode != 'EDIT':
        
            return {'PASS_THROUGH'}
        
        #
        
        if event.type == 'BACK_SPACE':

            if event.value == 'PRESS':
            
                Ar.delete_previous()
            
            return {'RUNNING_MODAL'}
        
        elif event.type == 'DEL':
            
            if event.value == 'PRESS':
            
                Ar.delete_next()
            
            return {'RUNNING_MODAL'}
        
        elif event.type == 'HOME':
            
            if event.value == 'PRESS':
            
                Ar.move_line_start()
            
            return {'RUNNING_MODAL'}
        
        elif event.type == 'END':
            
            if event.value == 'PRESS':
            
                Ar.move_line_end()
            
            return {'RUNNING_MODAL'}
        
        elif event.type == 'RIGHT_ARROW':
            
            if event.value == 'PRESS':
            
                Ar.move_previous()
            
            return {'RUNNING_MODAL'}
            
        elif event.type == 'LEFT_ARROW':
            
            if event.value == 'PRESS':
            
                Ar.move_next()
            
            return {'RUNNING_MODAL'}
        
        elif event.type == 'UP_ARROW':

            if event.value == 'PRESS':
            
                Ar.move_up()
            
            return {'RUNNING_MODAL'}

        elif event.type == 'DOWN_ARROW':

            if event.value == 'PRESS':
            
                Ar.move_down()
            
            return {'RUNNING_MODAL'}

        elif event.type == 'RET':
            
            if event.value == 'PRESS':
            
                Ar.insert_text('\n')
            
            return {'RUNNING_MODAL'}
                   
        elif event.type == 'TAB':
            
            if event.value == 'RELEASE':
                
                if bpy.context.object.mode == 'EDIT':
                
                    Ar.init()
            
            return {'PASS_THROUGH'}
            
        elif event.unicode:
            
            if event.value == 'PRESS':
                
                Ar.insert_text(event.unicode)
            
            return {'RUNNING_MODAL'}
        
        return {'PASS_THROUGH'}
     
    #
        
    def invoke(self, context, event):
        
        if context.area.type == 'VIEW_3D':
            
            self.key = ""
            
            context.window_manager.modal_handler_add(self)
            
            if bpy.context.object is not None and bpy.context.object.type == 'FONT' and bpy.context.object.mode == 'EDIT':
                
                # update text data (i don't know a better way to do this)
                
                bpy.ops.object.editmode_toggle()
                bpy.ops.object.editmode_toggle()
                
                Ar.init()
            
            return {'RUNNING_MODAL'}

        else:

            return {'CANCELLED'}


keymaps = []


def register():

    bpy.utils.register_class(__OT_ArabicTextMode)
	
    wm = bpy.context.window_manager
    
    kc = wm.keyconfigs.addon
    
    if kc:
        
        km = wm.keyconfigs.addon.keymaps.new(name="Window")
        kmi = km.keymap_items.new(__OT_ArabicTextMode.bl_idname, 'F1', 'PRESS', ctrl=True)
        keymaps.append((km, kmi))
    

#

def unregister():
    
    for km, kmi in keymaps:
    
        km.keymap_items.remove(kmi)
        
    keymaps.clear()
    
    bpy.utils.unregister_class(__OT_ArabicTextMode)


# ----------------------------------------------------------------------------------------------------------------

if(__name__ == "__main__"):
    
    register()

