#version 3: added:
# controllable camera # Julianos and Stendar with proper orbiting
# edited some orbits speeds



from direct.showbase.ShowBase import ShowBase
base = ShowBase()

from direct.gui.DirectGui import *
from panda3d.core import TextNode
import sys


soundtrack = base.loader.loadSfx("sound\secunda.mp3")
soundtrack.setLoopCount(9999999999999999) # loop (virually) forever
soundtrack.play()



class World(object):

    def __init__(self):

        #initialization
        self.title = OnscreenText(  # display title
            text="Mundus",
            parent=base.a2dBottomRight, align=TextNode.A_right,
            style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07)

        base.setBackgroundColor(0, 0, 0)  # Set the background to black
        #base.disableMouse()  # disable mouse control of the camera
        camera.setPos(0, 0, 45)  # Set the camera position (X, Y, Z)
        camera.setHpr(0, -90, 0)  # Set the camera orientation
        #(heading, pitch, roll) in degrees
        

        # Here again is where we put our global variables. Added this time are
        # variables to control the relative speeds of spinning and orbits in the
        # simulation
        # Number of seconds a full rotation of Earth around the sun should take
        self.yearscale = 60
        # Number of seconds a day rotation of Earth should take.
        # It is scaled from its correct value for easier visability
        self.dayscale = self.yearscale / 364.0 * 15 # 364 days in Nirn year
        self.orbitscale = 2  # Orbit scale
        self.sizescale = 0.6  # Planet size scale

        self.loadPlanets()  # Load and position the models

        # Finally, we call the rotatePlanets function which puts the planets,
        # sun, and moon into motion.
        self.rotatePlanets()

    def loadPlanets(self):
        
        # Create the dummy nodes
        self.orbit_root_mercury = render.attachNewNode('orbit_root_mercury')
        self.orbit_root_venus = render.attachNewNode('orbit_root_venus')
        self.orbit_root_mars = render.attachNewNode('orbit_root_mars')
        self.orbit_root_earth = render.attachNewNode('orbit_root_earth')

        #added planet's dummy nodes

        self.orbit_root_julianos = render.attachNewNode('orbit_root_julianos')
        self.orbit_root_stendarr = render.attachNewNode('orbit_root_stendarr')

        # The moon orbits Earth, not the sun
        self.orbit_root_moon = (
            self.orbit_root_earth.attachNewNode('orbit_root_moon'))

        # Stendarr orbits Julianos
        self.orbit_root_stendarr = (
            self.orbit_root_julianos.attachNewNode('orbit_root_stendarr'))
        

        ###############################################################

        # Load the sky
        self.sky = loader.loadModel("models/solar_sky_sphere")
        self.sky_tex = loader.loadTexture("models/stars_1k_tex.jpg")
        self.sky.setTexture(self.sky_tex, 1)
        self.sky.reparentTo(render)
        self.sky.setScale(40)

        # Load Nirn
        self.sun = loader.loadModel("models/planet_sphere")
        self.sun_tex = loader.loadTexture("models/nirn.jpg")
        self.sun.setTexture(self.sun_tex, 1)
        self.sun.reparentTo(render)
        self.sun.setScale(2 * self.sizescale)

        # Load Kynareth
        self.mercury = loader.loadModel("models/planet_sphere")
        self.mercury_tex = loader.loadTexture("models/kynareth.jpg")
        self.mercury.setTexture(self.mercury_tex, 1)
        self.mercury.reparentTo(self.orbit_root_mercury)
        self.mercury.setPos(3 * self.orbitscale, 0, 0)
        self.mercury.setScale(0.700 * self.sizescale)

        # Load Akatosh
        self.venus = loader.loadModel("models/planet_sphere")
        self.venus_tex = loader.loadTexture("models/akatosh.jpg")
        self.venus.setTexture(self.venus_tex, 1)
        self.venus.reparentTo(self.orbit_root_venus)
        self.venus.setPos(3 * self.orbitscale, 0, 0)
        self.venus.setScale(0.923 * self.sizescale)

        # Load Zenithar
        self.mars = loader.loadModel("models/planet_sphere")
        self.mars_tex = loader.loadTexture("models/zenithar.jpg")
        self.mars.setTexture(self.mars_tex, 1)
        self.mars.reparentTo(self.orbit_root_mars)
        self.mars.setPos(5.0 * self.orbitscale, 0, 0)
        self.mars.setScale(0.800 * self.sizescale)

        # Load Masser
        self.earth = loader.loadModel("models/planet_sphere")
        self.earth_tex = loader.loadTexture("models/masser.jpg")
        self.earth.setTexture(self.earth_tex, 1)
        self.earth.reparentTo(self.orbit_root_earth)
        self.earth.setScale(self.sizescale)
        self.earth.setPos(1.35* self.orbitscale, 0, 0)

        # Load Julianos
        self.julianos = loader.loadModel("models/planet_sphere")
        self.julianos_tex = loader.loadTexture("models/julianos.jpg")
        self.julianos.setTexture(self.julianos_tex, 1)
        self.julianos.reparentTo(self.orbit_root_julianos)
        self.julianos.setPos(4 * self.orbitscale, 0, 0)
        self.julianos.setScale(0.750 * self.sizescale)

        # Load Stendarr
        self.stendarr = loader.loadModel("models/planet_sphere")
        self.stendarr_tex = loader.loadTexture("models/moon_1k_tex.jpg")
        self.stendarr.setTexture(self.stendarr_tex, 1)
        self.stendarr.reparentTo(self.orbit_root_stendarr)
        self.stendarr.setPos(0.5 * self.orbitscale, 0, 0)
        self.stendarr.setScale(0.350 * self.sizescale)

        # Offest the moon dummy node so that it is positioned properly
        self.orbit_root_moon.setPos(1.35 * self.orbitscale, 0, 0)

        # Offset Stendarr so it is positioned properly

        self.orbit_root_stendarr.setPos(4 * self.orbitscale, 0, 0)

        
        # Load Secunda
        self.moon = loader.loadModel("models/planet_sphere")
        self.moon_tex = loader.loadTexture("models/secunda.jpg")
        self.moon.setTexture(self.moon_tex, 1)
        self.moon.reparentTo(self.orbit_root_moon)
        self.moon.setScale(0.5 * self.sizescale)
        self.moon.setPos(0.5 * self.orbitscale, 0, 0)

    # end loadPlanets()

    def rotatePlanets(self):
        # rotatePlanets creates intervals to actually use the hierarchy we created
        # to turn the sun, planets, and moon to give a rough representation of the
        # solar system. The next lesson will go into more depth on intervals.
        self.day_period_sun = self.sun.hprInterval(20, (360, 0, 0))

        self.orbit_period_mercury = self.orbit_root_mercury.hprInterval(
            (0.241 * self.yearscale), (360, 0, 0))
        self.day_period_mercury = self.mercury.hprInterval(
            (59 * self.dayscale), (360, 0, 0))

        self.orbit_period_venus = self.orbit_root_venus.hprInterval(
            (0.615 * self.yearscale), (360, 0, 0))
        self.day_period_venus = self.venus.hprInterval(
            (243 * self.dayscale), (360, 0, 0))

        self.orbit_period_earth = self.orbit_root_earth.hprInterval(
            self.yearscale, (360, 0, 0))
        self.day_period_earth = self.earth.hprInterval(
            self.dayscale, (360, 0, 0))

        self.orbit_period_moon = self.orbit_root_moon.hprInterval(
            (.100 * self.yearscale), (360, 0, 0))
        self.day_period_moon = self.moon.hprInterval(
            (.100 * self.yearscale), (360, 0, 0))

        self.orbit_period_mars = self.orbit_root_mars.hprInterval(
            (1.881 * self.yearscale), (360, 0, 0))
        self.day_period_mars = self.mars.hprInterval(
            (1.03 * self.dayscale), (360, 0, 0))

        self.orbit_period_julianos = self.orbit_root_julianos.hprInterval(
            self.yearscale, (360, 0, 0))
        self.day_period_julianos = self.earth.hprInterval(
            self.dayscale, (360, 0, 0))

        self.orbit_period_stendarr = self.orbit_root_stendarr.hprInterval(
            (0.1200 * self.yearscale), (360, 0, 0))
        self.day_period_stendarr = self.stendarr.hprInterval(
            (0.1200 * self.yearscale), (360, 0, 0))

        self.day_period_sun.loop()
        self.orbit_period_mercury.loop()
        self.day_period_mercury.loop()
        self.orbit_period_venus.loop()
        self.day_period_venus.loop()
        self.orbit_period_earth.loop()
        self.day_period_earth.loop()
        self.orbit_period_moon.loop()
        self.day_period_moon.loop()
        self.orbit_period_mars.loop()
        self.day_period_mars.loop()
        self.orbit_period_julianos.loop()
        self.day_period_julianos.loop()
        self.orbit_period_stendarr.loop()
        self.day_period_stendarr.loop()
    # end RotatePlanets()
# end class world

w = World()
base.run()
