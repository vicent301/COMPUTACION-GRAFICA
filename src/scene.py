from graphics import Graphics
import glm

class Scene:
    def __init__(self, ctx, camera):
        self.ctx = ctx
        self.objects = []
        self.graphics = {}
        self.camera = camera
        self.model = glm.mat4(1)
        self.view = camera.get_view_matrix()
        self.projection = camera.get_perspective_matrix()

    def add_object(self, obj, shader_program=None):
        self.objects.append(obj)
        self.graphics[obj.name] = Graphics(self.ctx, shader_program, obj.vertices, obj.indices)

    def render(self):
        for obj in self.objects:
            model = obj.get_model_matrix()
            mvp = self.projection * self.view * model
            self.graphics[obj.name].set_uniform("Mvp", mvp)
            self.graphics[obj.name].vao.render()

    def on_mouse_click(self, u, v):
        ray = self.camera.raycast(u, v)
        for obj in self.objects:
            if obj.check_hit(ray.origin, ray.direction):
                print(f"$$GOLPEASTE AL OBJETO: {obj.name}!!")

    def on_resize(self, width, height):
        self.ctx.viewport = (0, 0, width, height)
        self.camera.projection = glm.perspective(glm.radians(45), width / height, 0.1, 100.0)


    def update(self, dt):
        for obj in self.objects:
            obj.rotation.y += 20 * dt  # Rotar 20 grados x segundo
