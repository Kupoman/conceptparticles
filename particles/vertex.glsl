#version 130
#extension GL_ARB_explicit_attrib_location: enable

const float screen_width = 640.0;
const float sprite_width = 0.5;

in vec3 position_in;
in vec4 color_in;

flat out vec4 color;

void main()
{
	vec4 pos = gl_ModelViewMatrix * vec4(position_in, 1.0);
	vec4 proj_corner = gl_ProjectionMatrix * vec4(0.5*sprite_width, 0.5*sprite_width, pos.z, pos.w);
	gl_PointSize = screen_width * proj_corner.x / proj_corner.w;
	gl_Position = gl_ProjectionMatrix * pos;
	color = color_in;
}