#version 120
#extension GL_EXT_gpu_shader4 : enable

uniform sampler2D texture;

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
	
	vec4 color = texture2D(texture, coord);
	
	gl_FragColor = color;
}