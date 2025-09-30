from window import Window
from shader_program import ShaderProgram
from cube import Cube
from camera import Camera
from scene import Scene
# Ventana
window = Window(800, 600, "Basic Graphic Engine") #una ventana de 800x600
# Shader
shader_program = ShaderProgram(window.ctx, '../shaders/basic.vert', '../shaders/basic.frag') #carga los shaders very y frag
# Cámara
camera = Camera((0, 0, 6), (0, 0, 0), (0, 1, 0), 45, window.width / window.height, 0.1, 100.0) 

# Objetos
cube1 = Cube((0, -2, 0), (0, 0, 0), (1, 1, 1), name="Cube1")
cube2 = Cube((-2, -2, 0), (0, 0, 0), (1, 1, 1), name="Cube2")
cube3 = Cube((0, 0, 0),    (0, 0, 0), (1, 1, 1), name="Cube3") 
cube4 = Cube((2, 2, 0),    (0, 0, 0), (1, 1, 1), name="Cube4")
cube5 = Cube((0, 2, 0), (0, 0, 0), (1, 1, 1), name="Cube5")
#creo dos cubos  en posiciones diferentes
# Escena
scene = Scene(window.ctx, camera)
#scene.add_object(cube1, shader_program)
scene.add_object(cube2, shader_program)
scene.add_object(cube3, shader_program) #añado los cubos a la escena con el shader
scene.add_object(cube4, shader_program) #añado los cubos a la escena con el shader
#scene.add_object(cube5, shader_program)
#añado los cubos a la escena con el shader
# Carga de la escena y ejecución del loop principal
window.set_scene(scene)
window.run()
