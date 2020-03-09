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
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
        "name":        "Frames Per Beat",
        "description": "Flash an X on the timeline according to tempo and FPS",
        "author":      "Shams Kitz <dustractor@gmail.com>",
        "version":     (0,1),
        "blender":     (2,80,0),
        "tracker_url": "https://github.com/dustractor/frames_per_beat",
        "category":    "Timeline"
    }

import bpy,math

def _(c=None,r=[]):
    if c:
        r.append(c)
        return c
    return r

def is_onbeat(context):
    frames_from_beat0 = (context.scene.frame_current-context.scene.frame_start) 
    (ign,modf) =  divmod(frames_from_beat0,context.scene.frames_per_beat)
    return math.isclose(modf,0,rel_tol=modf/4)

def beat_info_display(layout,context):
    layout.box().row().label(text=" x"[is_onbeat(context)])

def timeline_drawfunc(self,context):
    beat_info_display(self.layout,context)

@_
class FPB_PT_beat_info(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FPB"
    bl_label = "Frames per Beat"

    def draw(self,context):
        layout = self.layout
        layout.prop(context.scene,"beats_per_minute")
        layout.prop(context.scene,"frames_per_beat")
        layout.prop(context.scene.render,"fps")


def calc_fpb(self):
    seconds_in_a_minute = 60
    frames_per_second = self.render.fps
    beats_per_minute = self.beats_per_minute
    return seconds_in_a_minute * frames_per_second / beats_per_minute

def register():
    list(map(bpy.utils.register_class,_()))
    bpy.types.Scene.beats_per_minute = bpy.props.FloatProperty(default=144.0)
    bpy.types.Scene.frames_per_beat = bpy.props.FloatProperty(get=calc_fpb)
    bpy.types.TIME_HT_editor_buttons.append(timeline_drawfunc)

def unregister():
    bpy.types.TIME_HT_editor_buttons.remove(timeline_drawfunc)
    del bpy.types.Scene.beats_per_minute
    del bpy.types.Scene.frames_per_beat
    list(map(bpy.utils.unregister_class,_()))



