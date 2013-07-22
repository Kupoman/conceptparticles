from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from particles.system import System

WIDTH = 640
HEIGHT = 480


class Global:
	system = None
	mvmat = []
	pmat = []

def draw_background():
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()
	
	glDepthMask(GL_FALSE)
	
	glBegin(GL_QUADS)
	glColor3f(0.6, 0.6, 0.6)
	glVertex2f(-1.0, 1.0)
	glVertex2f(1.0, 1.0)
	glColor3f(0.2, 0.2, 0.2)
	glVertex2f(1.0, -1.0)
	glVertex2f(-1.0, -1.0)
	glEnd()
	
	glDepthMask(GL_TRUE)
	
	glPopMatrix()
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()


def draw_axis():
	glBegin(GL_LINES)
	glColor3f(1.0, 0.0, 0.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(1.0, 0.0, 0.0)
	glEnd()
	
	glBegin(GL_LINES)
	glColor3f(0.0, 1.0, 0.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, 1.0, 0.0)
	glEnd()
	
	glBegin(GL_LINES)
	glColor3f(0.0, 0.0, 1.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, 0.0, 1.0)
	glEnd()

def display():	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	draw_background()
	draw_axis()

	Global.system.draw(Global.mvmat, Global.pmat)

	glutSwapBuffers()


def reshape(w, h):
	aspect = float(WIDTH)/float(HEIGHT)
	glViewport(0, 0, WIDTH, HEIGHT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-aspect * 5, aspect * 5, -5, 5, 0.5, 20)

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity()
	gluLookAt(7, -6, 7, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)

	Global.pmat = glGetFloatv(GL_PROJECTION_MATRIX)
	Global.mvmat = glGetFloatv(GL_MODELVIEW_MATRIX)


if __name__ == '__main__':
	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(WIDTH,HEIGHT)
	glutCreateWindow(b"Particle Viewer")
	
	Global.system = System.load("effect.json")

	glutReshapeFunc(reshape)
	glutDisplayFunc(display)
	glutIdleFunc(display)
	glutMainLoop()