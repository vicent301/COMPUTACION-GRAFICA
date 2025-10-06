from graphics import Graphics
from raytracer import RayTracer
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
            if obj.name != "Sprite":
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

    def update(self, dt):
        for obj in self.__objects:
            obj.rotation.y += 20 * dt  # Rotar 20 grados por segundo


#   Clase RayScene (para el RayTracer CPU)

class RayScene(Scene):
    def __init__(self, ctx, camera, width, height):
        super().__init__(ctx, camera)
        self.__raytracer = RayTracer(camera, width, height)

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
