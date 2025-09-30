class Graphics:
    def __init__(self, ctx, shader_program, vertices, indices):
        self.ctx = ctx
        self.shader_program = shader_program
        self.vbo = ctx.buffer(vertices.tobytes())
        self.ibo = ctx.buffer(indices.tobytes())
        self.vao = ctx.vertex_array(shader_program.prog, [
            (self.vbo, '3f 3f', 'in_pos', 'in_color')
            ], self.ibo)
        
    def set_shader(self, shader_program):
        self.shader_program = shader_program

    def set_uniform(self, name, value):
            self.shader_program.set_uniform(name, value)            
    def draw(self, obj, mvp):
        self.set_shader(obj.shader_program)
        self.set_uniform("Mvp", mvp)
        self.ctx.draw_elements(self.ctx.TRIANGLES, obj.indices_count, self.ctx.UNSIGNED_INT, None)