#version 120

uniform sampler2D texture;

flat in vec4 color;

void main()
{
	int subuv_divs = 2;
	int subuv_count = 3;

	int subuv = 0;
	float offset = 1.0/subuv_divs;
	vec2 coord = gl_PointCoord;
	coord.y = 1 - coord.y;
	coord *= offset;
	coord.x += offset * (subuv - subuv_divs*(subuv/subuv_divs));
	coord.y += offset * (subuv/subuv_divs);

	vec4 text = texture2D(texture, coord);

	gl_FragColor = text * color;
}