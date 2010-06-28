import bpy


FloatProperty = bpy.types.Scene.FloatProperty
IntProperty = bpy.types.Scene.IntProperty
BoolProperty = bpy.types.Scene.BoolProperty
CollectionProperty = bpy.types.Scene.CollectionProperty
EnumProperty = bpy.types.Scene.EnumProperty
FloatVectorProperty = bpy.types.Scene.FloatVectorProperty
IntVectorProperty = bpy.types.Scene.IntVectorProperty


EnumProperty(attr="bg_type",
	items = (
		("Gradient","Gradient",""),
		("Texture","Texture",""),
		("Sunsky","Sunsky",""),
		("Darktide's Sunsky","Darktide's Sunsky",""),
		("Single Color","Single Color",""),
),default="Single Color")
FloatVectorProperty(attr="bg_zenith_ground_color",description = "Color Settings", subtype = "COLOR", step = 1, precision = 2, min = 0.0, max = 1.0, soft_min = 0.0, soft_max = 1.0)
BoolProperty(attr="bg_use_IBL")
IntProperty(attr="bg_IBL_samples")
IntProperty(attr="bg_rotation")
FloatProperty(attr="bg_turbidity")
IntProperty(attr="bg_a_var")
IntProperty(attr="bg_b_var")
IntProperty(attr="bg_c_var")
IntProperty(attr="bg_d_var")
IntProperty(attr="bg_e_var")
FloatVectorProperty(attr="bg_from",description = "Point Info", subtype = "XYZ", step = 10, precision = 3)
BoolProperty(attr="bg_add_sun")
FloatProperty(attr="bg_sun_power")
BoolProperty(attr="bg_background_light")
IntProperty(attr="bg_light_samples")
IntProperty(attr="bg_dsaltitude")
BoolProperty(attr="bg_dsnight")
FloatProperty(attr="bg_dsbright")
FloatProperty(attr="bg_power")


class YAF_PT_world(bpy.types.Panel):

	bl_label = 'YafaRay Background'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'world'
	COMPAT_ENGINES =['YAFA_RENDER']


	def poll(self, context):

		engine = context.scene.render.engine

		import properties_world

		if (context.world and  (engine in self.COMPAT_ENGINES) ) :
			try :
				properties_world.unregister()
			except: 
				pass
		else:
			try:
				properties_world.register()
			except: 
				pass
		return (context.world and  (engine in self.COMPAT_ENGINES) ) 


	def draw(self, context):

		layout = self.layout
		split = layout.split()
		col = split.column()

		col.prop_menu_enum(context.scene,"bg_type", text= "Yafaray Background")

		if context.scene.bg_type == 'Gradient':
			col.prop(context.world,"horizon_color", text= "Horizon Color")
			context.world.real_sky = True
			col.prop(context.world,"ambient_color", text= "Horizon Ground Color")
			context.world.blend_sky = True
			col.prop(context.world,"zenith_color", text= "Zenith Color")
			col.prop(context.scene,"bg_zenith_ground_color", text= "Zenith Ground Color")

		if context.scene.bg_type == 'Texture':
			col.prop(context.scene,"bg_use_IBL", text= "Use IBL")
			col.prop(context.scene,"bg_IBL_samples", text= "IBL Samples")
			col.prop(context.scene,"bg_rotation", text= "Rotation")

		if context.scene.bg_type == 'Sunsky':
			col.prop(context.scene,"bg_turbidity", text= "Turbidity")
			col.prop(context.scene,"bg_a_var", text= "HorBrght")
			col.prop(context.scene,"bg_b_var", text= "HorSprd")
			col.prop(context.scene,"bg_c_var", text= "SunBrght")
			col.prop(context.scene,"bg_d_var", text= "SunSize")
			col.prop(context.scene,"bg_e_var", text= "Backlight")
			col.prop(context.scene,"bg_from", text= "From")
			col.prop(context.scene,"bg_add_sun", text= "Add Sun")
			col.prop(context.scene,"bg_sun_power", text= "Sun Power")
			col.prop(context.scene,"bg_background_light", text= "Skylight")
			col.prop(context.scene,"bg_light_samples", text= "Samples")

		if context.scene.bg_type == 'Darktide\'s Sunsky':
			col.prop(context.scene,"bg_turbidity", text= "Turbidity")
			col.prop(context.scene,"bg_a_var", text= "Brightness of horizon gradient")
			col.prop(context.scene,"bg_b_var", text= "Luminance of horizon")
			col.prop(context.scene,"bg_c_var", text= "Solar region intensity")
			col.prop(context.scene,"bg_d_var", text= "Width of circumsolar region")
			col.prop(context.scene,"bg_e_var", text= "Backscattered light")
			col.prop(context.scene,"bg_from", text= "From")
			col.prop(context.scene,"bg_dsaltitude", text= "Altitude")
			col.prop(context.scene,"bg_add_sun", text= "Add Sun")
			col.prop(context.scene,"bg_sun_power", text= "Sun Power")
			col.prop(context.scene,"bg_background_light", text= "Add Skylight")
			col.prop(context.scene,"bg_dsnight", text= "Night")
			col.prop(context.scene,"bg_dsbright", text= "Sky Brightness")
			col.prop(context.scene,"bg_light_samples", text= "Samples")

		if context.scene.bg_type == 'Single Color':
			col.prop(context.world,"horizon_color", text= "Color")

		col.prop(context.scene,"bg_power", text= "Multiplier for Background Color")


from properties_world import WORLD_PT_preview
from properties_world import WORLD_PT_context_world

classes = [
	YAF_PT_world,
]

def register():
	YAF_PT_world.prepend( WORLD_PT_preview.draw )
	YAF_PT_world.prepend( WORLD_PT_context_world.draw )
	register = bpy.types.register
	for cls in classes:
		register(cls)


def unregister():
	bpy.types.YAF_PT_world.remove( WORLD_PT_preview.draw )
	bpy.types.YAF_PT_world.remove( WORLD_PT_context_world.draw )
	unregister = bpy.types.unregister
	for cls in classes:
		unregister(cls)


if __name__ == "__main__":
	register()