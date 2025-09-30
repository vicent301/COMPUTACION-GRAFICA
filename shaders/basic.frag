//CORRE UNA VEZ X CADA PINCEL
//QUE LA GPU TENGA QUE PINTAR

#version 330
in vec3 v_color;       // Entrada: el color que vino del Vertex Shader
out vec4 f_color;      // Salida: color final (RGBA)

void main() {
    // El píxel se pinta con el color recibido
    f_color = vec4(v_color, 1.0);
}
