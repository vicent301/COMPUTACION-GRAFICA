from window import Window
from texture import Texture
from material import Material
from shader_program import ShaderProgram
from cube import Cube
from quad import Quad
from camera import Camera
from scene import Scene, RayScene
import numpy as np
import moderngl 
# --- Loop principal ---
WIDTH, HEIGHT = 800, 600

# Ventana
window = Window(WIDTH, HEIGHT, "Basic Graphic Engine") #una ventana de 800x600

# Cámara
camera = Camera((0, 0, 6), (0, 0, 0), (0, 1, 0), 45, window.width / window.height, 0.1, 100.0) 

# Shader
shader_program = ShaderProgram(window.ctx, '../shaders/basic.vert', '../shaders/basic.frag') #carga los shaders very y frag
shader_program_skybox = ShaderProgram(window.ctx, '../shaders/sprite.vert', '../shaders/sprite.frag') #carga los shaders very y frag

#textura
skybox_texture = Texture(width=WIDTH, height=HEIGHT, channels_amount=3, color=(0, 0, 0)) #crea una textura del color del cielo

material = Material(shader_program)
material_sprite = Material(shader_program_skybox, textures_data = [skybox_texture])


#Quad 

# Objetos
cube1 = Cube((-2, 0, 2), (0, 45, 0), (1, 1, 1), name="Cube1")
cube2 = Cube((2, 0, 2), (0, 45, 0), (1, 0.5, 1), name="Cube2")

quad = Quad((0,0,0), (0,0,0), (6,5,1), name="Sprite", hittable = False) #un quad grande que hace de fondo (skybox)

window.ctx.enable(moderngl.DEPTH_TEST)


# Escena
scene = RayScene(window.ctx, camera, WIDTH, HEIGHT) #crea una escena con la camara y el contexto de la ventana
scene.add_object(quad, material_sprite) #añado el quad a la escena con el shader
scene.add_object(cube1, material)
scene.add_object(cube2, material)

# Carga de la escena y ejecución del loop principal
window.set_scene(scene)
window.run()
