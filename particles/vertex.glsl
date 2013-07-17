const float screen_width = 640.0;
const float sprite_width = 0.5;

void main()
{
	vec4 pos = gl_ModelViewMatrix * gl_Vertex;
	vec4 proj_corner = gl_ProjectionMatrix * vec4(0.5*sprite_width, 0.5*sprite_width, pos.z, pos.w);
	gl_PointSize = screen_width * proj_corner.x / proj_corner.w;
	gl_Position = gl_ProjectionMatrix * pos;
}