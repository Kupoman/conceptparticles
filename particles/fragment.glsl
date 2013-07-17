#version 150
#extension GL_EXT_gpu_shader4 : enable

uniform sampler2D texture;

flat in vec4 color;

out vec4 frag_color;

void main()
{
	int subuv_divs = 2;
	int subuv_count = 3;
	
	int subuv = 0;
	float offset = 1.0/subuv_divs;
	vec2 coord = gl_PointCoord;
	coord.y = 1 - coord.y;
	coord *= offset;
	coord.x += offset * (subuv%subuv_divs);
	coord.y += offset * (subuv/subuv_divs);
	
	vec4 text = texture2D(texture, coord);
	
	frag_color = text * color;
}