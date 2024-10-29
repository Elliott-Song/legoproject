import bpy
import random
from mathutils import Vector
from math import radians
from math import sin, cos, pi
import os

def render_image(obj_path, output_path):
    # Clear all existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Create plane as ground
    bpy.ops.mesh.primitive_plane_add(size=500)

    # Set random noisy material for the ground
    material = bpy.data.materials.new(name="GroundMaterial")
    material.use_nodes = True

    # Create a noise texture
    texture = material.node_tree.nodes.new('ShaderNodeTexNoise')
    texture.inputs['Scale'].default_value = random.uniform(-10, 700)
    texture.inputs['Detail'].default_value = 16

    # Create a color ramp to control the color of the noise
    color_ramp = material.node_tree.nodes.new('ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].position = random.uniform(0.2, 0.8)
    color_ramp.color_ramp.elements[0].color = (random.random(), random.random(), random.random(), 1)
    color_ramp.color_ramp.elements[1].position = 1
    color_ramp.color_ramp.elements[1].color = (random.random(), random.random(), random.random(), 1)

    # Choose random image from /random_images folder
    image_path = "C:/Users/Elliott/3D Objects/Code/legoproject/random_images/" + random.choice(os.listdir("C:/Users/Elliott/3D Objects/Code/legoproject/random_images/"))
    image_texture = material.node_tree.nodes.new('ShaderNodeTexImage')
    image_texture.image = bpy.data.images.load(image_path)

    #  Create a texture coordinate node to control the texture mapping
    texture_coordinate = material.node_tree.nodes.new('ShaderNodeTexCoord')

    # Create a mapping node to control the texture mapping
    mapping = material.node_tree.nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (random.uniform(0.7, 3), random.uniform(0.7, 3), random.uniform(0.7, 3))
    mapping.inputs['Rotation'].default_value = (0, 0, radians(random.uniform(0, 360)))
    mapping.inputs['Location'].default_value = (random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(-100, 100))

    # Create a bump node to add some bumpiness to the ground
    bump = material.node_tree.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = random.uniform(0.1, 0.5)

    # Link the nodes
    material.node_tree.links.new(texture_coordinate.outputs['UV'], mapping.inputs['Vector'])
    material.node_tree.links.new(mapping.outputs['Vector'], image_texture.inputs['Vector'])
    material.node_tree.links.new(image_texture.outputs['Color'], material.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
    material.node_tree.links.new(texture.outputs['Color'], color_ramp.inputs['Fac'])
    material.node_tree.links.new(color_ramp.outputs['Color'], bump.inputs['Height'])
    material.node_tree.links.new(bump.outputs['Normal'], material.node_tree.nodes['Principled BSDF'].inputs['Normal'])
    material.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = random.uniform(0.3, 0.7)

    # Assign the material to the plane
    bpy.context.object.data.materials.append(material)


    # Import the .obj file
    bpy.ops.import_scene.obj(filepath=obj_path)

    # Get a reference to the imported object
    obj = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()

    # Randomize object position
    obj.location = (random.uniform(-3, 3), random.uniform(-3, 3), 0)
    obj.rotation_euler = (
        radians(random.uniform(85, 95)),
        radians(random.uniform(-3, 3)),
        radians(random.uniform(0, 360))
    )

    # Set random color for the object
    material = bpy.data.materials.new(name="RandomMaterial")
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (
        random.random(), random.random(), random.random(), 1
    )
    bsdf.inputs["Roughness"].default_value = random.uniform(0.2, 0.5)
    obj.data.materials.append(material)
    obj.active_material = material

    # Sun 1
    sun = bpy.data.lights.new(name="Sun", type='SUN')
    sun_obj = bpy.data.objects.new(name="Sun", object_data=sun)
    bpy.context.collection.objects.link(sun_obj)

    # Randomize world background color
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = (
        random.uniform(0.1, 0.3),
        random.uniform(0.1, 0.3),
        random.uniform(0.1, 0.3),
        1
    )
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[1].default_value = random.uniform(0.05, 0.6)

    # Randomize sun position, rotation and intensity
    sun_obj.location = (
        random.uniform(-50, 50),
        random.uniform(-50, 50),
        random.uniform(50, 100)
    )
    sun_obj.rotation_euler = (
        radians(random.uniform(-90, 90)),
        radians(random.uniform(-90, 90)),
        radians(random.uniform(0, 360))
    )
    sun_obj.data.energy = random.uniform(0.1, 3)

    # Sun 2
    sun2 = bpy.data.lights.new(name="Sun", type='SUN')
    sun_obj2 = bpy.data.objects.new(name="Sun", object_data=sun)
    bpy.context.collection.objects.link(sun_obj2)

    # Randomize sun position, rotation and intensity
    sun_obj2.location = (
        random.uniform(-50, 50),
        random.uniform(-50, 50),
        random.uniform(50, 100)
    )
    sun_obj2.rotation_euler = (
        radians(random.uniform(-90, 90)),
        radians(random.uniform(-90, 90)),
        radians(random.uniform(0, 360))
    )
    sun_obj2.data.energy = random.uniform(0, 1)

    number_of_lights = random.randint(1, 5)
    for i in range(number_of_lights):
        light_data = bpy.data.lights.new(name="RandomLight", type='POINT')
        light = bpy.data.objects.new(name="RandomLight", object_data=light_data)
        bpy.context.collection.objects.link(light)

        # Randomize light position and intensity
        light.location = (
            random.uniform(-50, 50),
            random.uniform(-50, 50),
            random.uniform(18, 100)
        )
        light.data.energy = random.uniform(100, 6000)
        light.data.color = (random.uniform(0.6, 1), random.uniform(0.6, 1), random.uniform(0.6, 1))

    # Set up the camera
    cam_data = bpy.data.cameras.new("Camera")
    cam = bpy.data.objects.new("Camera", cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam

    # Randomize camera position
    def random_camera_position():
        camera_distance = random.uniform(90, 190)
        camera_angle_theta = random.uniform(0.4, pi/2)
        camera_angle_phi = random.uniform(0, 2*pi)

        cam.location = (
            camera_distance * cos(camera_angle_phi),
            camera_distance * sin(camera_angle_phi),
            camera_distance * sin(camera_angle_theta)
        )

        # Point camera towards object
        direction = cam.location - obj.location
        rot_quat = direction.to_track_quat('Z', 'Y')
        cam.rotation_euler = rot_quat.to_euler()
        cam.rotation_euler[1] += random.uniform(-(camera_distance-90)/600, (camera_distance-90)/600)

        # Slightly shift the camera to add some randomness
        cam.location += Vector((
            random.uniform(-camera_distance/10, camera_distance/10),
            random.uniform(-camera_distance/10, camera_distance/10),
            random.uniform(-camera_distance/10, camera_distance/10)
        ))

    random_camera_position()

    # Render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.image_settings.file_format = 'PNG'

    # Output resolution
    bpy.context.scene.render.resolution_x = 244
    bpy.context.scene.render.resolution_y = 244

    # Render the image
    bpy.ops.render.render(write_still=True)

    print("Render complete. Image saved to:", output_path)

parent_dir = "C:/Users/Elliott/3D Objects/Code/legoproject/parts_obj"
obj_paths = os.listdir(parent_dir)

for obj_path in obj_paths:
    obj_path = os.path.join(parent_dir, obj_path)
    for i in range(5):
        output_path = f"C:/Users/Elliott/3D Objects/Code/legoproject/output/{os.path.splitext(os.path.basename(obj_path))[0]}/{[i]}.png"
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))
        render_image(obj_path, output_path)
        break
    break