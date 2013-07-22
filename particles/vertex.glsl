#version 120

uniform mat4 model_view_mat;
uniform mat4 projection_mat;

const float screen_width = 640.0;
const float sprite_width = 0.5;

in vec3 position_in;
in vec4 color_in;

flat varying vec4 color;

void main()
{
	vec4 pos = model_view_mat * vec4(position_in, 1.0);
	vec4 proj_corner = projection_mat * vec4(0.5*sprite_width, 0.5*sprite_width, pos.z, pos.w);
	gl_PointSize = screen_width * proj_corner.x / proj_corner.w;
	gl_Position = projection_mat * pos;
	color = color_in;
}