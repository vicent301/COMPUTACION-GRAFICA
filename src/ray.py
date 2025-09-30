import glm

class Ray:
    def __init__(self, origin=(0,0,0), direction=(0,0,1)):
        # Guardamos origen y dirección como vec3
        self.__origin = glm.vec3(*origin)
        # Normalizamos la dirección
        self.__direction = glm.normalize(glm.vec3(*direction))

    @property
    def origin(self) -> glm.vec3:
        return self.__origin

    @property
    def direction(self) -> glm.vec3:
        return self.__direction
