import glm

class Hit:
    def __init__(self, get_model_matrix, hittable = True):
        self.__model_matrix = get_model_matrix
        

    @property
    def model_matrix(self):
        return self.__model_matrix()
        
        #self.__position = glm.vec3(*position)
        #self.__scale = glm.vec3(*scale)

    @property
    def position(self):
        m = self.model_matrix
        return glm.vec3(m[3].x, m[3].y, m[3].z)
    
    @property
    def scale(self):
        m = self.model_matrix
        return glm.vec3(glm.length(glm.vec3(m[0])),
                        glm.length(glm.vec3(m[1])),
                        glm.length(glm.vec3(m[2])))



    def check_hit(self, origin, direction):
        raise NotImplementedError("Subclasses should implement this method.")
class HitBoxOBB(Hit):
        def __init__(self, get_model_matrix):
            super().__init__(get_model_matrix)
        
        def check_hit(self, origin, direction):
            origin = glm.vec3(origin)
            direction = glm.normalize(glm.vec3(direction))

            # Transformar el rayo al espacio local del objeto
            inv_model = glm.inverse(self.model_matrix)
            local_origin = inv_model * glm.vec4(origin, 1.0)     # punto
            local_dir    = inv_model * glm.vec4(direction, 0.0)  # vector

            local_origin = glm.vec3(local_origin)
            local_dir    = glm.normalize(glm.vec3(local_dir))

            # Caja local (cubo unitario)
            min_bounds = glm.vec3(-1, -1, -1)
            max_bounds = glm.vec3( 1,  1,  1)
            
            # Intersección
            tmin = (min_bounds - local_origin) / local_dir
            tmax = (max_bounds - local_origin) / local_dir

            t1 = glm.min(tmin, tmax)
            t2 = glm.max(tmin, tmax)

            t_near = max(t1.x, t1.y, t1.z)
            t_far = min(t2.x, t2.y, t2.z)

            return t_near <= t_far and t_far >= 0
class HitBox(Hit):
    def __init__(self, position=(0,0,0), scale=(1,1,1)):
        super().__init__(position, scale)

    def check_hit(self, origin, direction):
        origin = glm.vec3(origin)
        direction = glm.normalize(glm.vec3(direction))

        # Límites de la caja
        min_bounds = self.position - self.scale
        max_bounds = self.position + self.scale

        # Intersección en cada eje
        tmin = (min_bounds - origin) / direction
        tmax = (max_bounds - origin) / direction

        t1 = glm.min(tmin, tmax)
        t2 = glm.max(tmin, tmax)

        t_near = max(t1.x, t1.y, t1.z)
        t_far = min(t2.x, t2.y, t2.z)

        return t_near <= t_far and t_far >= 0