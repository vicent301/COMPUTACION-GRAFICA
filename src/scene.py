from graphics import Graphics
from raytracer import RayTracer
from raytracer import RayTracerGPU
from graphics import ComputeGraphics
import numpy as np
import glm
import math

class Scene:
    def __init__(self, ctx, camera):
        self.__ctx = ctx
        self.__camera = camera
        self.__objects = []
        self.__graphics = {}

        self.__model = glm.mat4(1)
        self.__view = self.__camera.get_view_matrix()
        self.__projection = self.__camera.get_perspective_matrix()
        self.__time = 0.0

    def add_object(self, obj, material):
        self.__objects.append(obj)
        self.__graphics[obj.name] = Graphics(self.__ctx, obj, material)

    def start(self):
        print("$Start Scene$")

    def render(self):
        self.__time += 0.01
        for obj in self.__objects:
            if (obj.animated):
                # Rotaciones y pequeñas traslaciones animadas
                obj.rotation += glm.vec3(0.8, 0.6, 0.4)
                obj.position.x += math.sin(self.__time) * 0.01

            model = obj.get_model_matrix()
            mvp = self.__projection * self.__view * model
            self.__graphics[obj.name].render({"Mvp": mvp})

    def on_mouse_click(self, u, v):
        ray = self.__camera.raycast(u, v)
        for obj in self.__objects:
            if obj.check_hit(ray.origin, ray.direction):
                print(f"$$ GOLPEASTE AL OBJETO: {obj.name} !!")
                return

    def on_resize(self, width, height):
        self.__ctx.viewport = (0, 0, width, height)
        self.__camera.projection = glm.perspective(glm.radians(45), width / height, 0.1, 100.0)

    #def update(self, dt):
     #   for obj in self.__objects:
      #      obj.rotation.y += 20 * dt  # Rotar 20 grados por segundo


#   Clase RayScene (para el RayTracer CPU)

class RayScene(Scene):
    def __init__(self, ctx, camera, width, height):
        super().__init__(ctx, camera)
        self.__raytracer = RayTracer(camera, width, height)
##ojo aca con los __raytracer...
    def start(self):
        self.__raytracer.render_frame(self._Scene__objects)
        if "Sprite" in self._Scene__graphics:
            self._Scene__graphics["Sprite"].update_texture(
                "u_texture", self.__raytracer.get_texture()
            )

    def render(self):
        super().render()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.__raytracer = RayTracer(self._Scene__camera, width, height)
        self.start()


class RaySceneGPU(Scene):
    def __init__(self, ctx, camera, width, height, output_model, output_material):
        self.ctx = ctx
        self.camera = camera
        self.width = width
        self.height = height
        self.raytracer = None
        self.objects = [] #agregue estas 2 lineas sin saber porque pero anda.
        self.graphics = {} #agregue estas 2 lineas sin saber porque pero anda.
        self.time = 0.0
        
        self.output_graphics = Graphics(ctx, output_model, output_material)
        self.raytracer = RayTracerGPU(self.ctx, self.camera, self.width, self.height, self.output_graphics)
        super().__init__(self.ctx, self.camera)
        
    def add_object(self, model, material):
        self.objects.append(model)
        self.graphics[model.name] = ComputeGraphics(self.ctx, model, material)
    
    def start(self):
        print("Start Raytracing GPU!!!!!!!")
        self.primitives = []
        n = len(self.objects)
        self.models_f = np.zeros((n, 16), dtype='f4')
        self.inv_f = np.zeros((n, 16), dtype='f4')
        self.mats_f = np.zeros((n, 4), dtype='f4')
        
        self._update_matrix()
        self._matrix_to_ssbo()
        
    def render(self):
        self.time += 0.01
        for obj in self.objects:
            if obj.animated:
                obj.rotation += glm.vec3(0.8, 0.6, 0.4)
                obj.position.x += math.sin(self.time) * 0.01
        
        if(self.raytracer is not None):
            self._update_matrix()
            self._matrix_to_ssbo()
            self.raytracer.run()
                
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.width = width
        self.height = height
        self.camera.aspect = width / height

    
    def _update_matrix(self):
        self.primitives = []
            
        for i,(name,graphics) in enumerate(self.graphics.items()):
            graphics.create_primitive(self.primitives)
            graphics.create_transformation_matrix(self.models_f, i)
            graphics.create_inverse_transformation_matrix(self.inv_f, i)
            graphics.create_material_matrix(self.mats_f, i)
                
    def _matrix_to_ssbo(self):
        self.raytracer.matrix_to_ssbo(self.models_f,0)
        self.raytracer.matrix_to_ssbo(self.inv_f,1)
        self.raytracer.matrix_to_ssbo(self.mats_f,2)
        self.raytracer.primitives_to_ssbo(self.primitives,3)
        
        