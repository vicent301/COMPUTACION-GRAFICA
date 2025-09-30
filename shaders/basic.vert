
//CORRE UNA VEZ X CADA VERTICE Q DIBUJO

#version 330
//inputs = son los vertices para la posicion y el color
in vec3 in_pos;
in vec3 in_color;

//output = pasa el color al Fragment shader
out vec3 v_color;

//variable global
uniform mat4 Mvp; //la matriz

void main(){
    gl_Position = Mvp * vec4(in_pos, 1.0);
    v_color = in_color;
}

