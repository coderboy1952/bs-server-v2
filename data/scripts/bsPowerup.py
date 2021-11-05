import bs
import random
import bsSpaz
import objects as objs
import BuddyBunny
import SnoBallz
import bsUtils
import settings

defaultPowerupInterval = 8000


class PowerupMessage(object):
    """
    category: Message Classes

    Tell something to get a powerup.
    This message is normally recieved by touching
    a bs.Powerup box.
    
    Attributes:
    
       powerupType
          The type of powerup to be granted (a string).
          See bs.Powerup.powerupType for available type values.

       sourceNode
          The node the powerup game from, or an empty bs.Node ref otherwise.
          If a powerup is accepted, a bs.PowerupAcceptMessage should be sent
          back to the sourceNode to inform it of the fact. This will generally
          cause the powerup box to make a sound and disappear or whatnot.
    """

    def __init__(self, powerupType, sourceNode=bs.Node(None)):
        """
        Instantiate with given values.
        See bs.Powerup.powerupType for available type values.
        """
        self.powerupType = powerupType
        self.sourceNode = sourceNode


class PowerupAcceptMessage(object):
    """
    category: Message Classes

    Inform a bs.Powerup that it was accepted.
    This is generally sent in response to a bs.PowerupMessage
    to inform the box (or whoever granted it) that it can go away.
    """
    pass


class _TouchedMessage(object):
    pass


class PowerupFactory(object):
    """
    category: Game Flow Classes
    
    Wraps up media and other resources used by bs.Powerups.
    A single instance of this is shared between all powerups
    and can be retrieved via bs.Powerup.getFactory().

    Attributes:

       model
          The bs.Model of the powerup box.

       modelSimple
          A simpler bs.Model of the powerup box, for use in shadows, etc.

       texBox
          Triple-bomb powerup bs.Texture.

       texPunch
          Punch powerup bs.Texture.

       texIceBombs
          Ice bomb powerup bs.Texture.

       texStickyBombs
          Sticky bomb powerup bs.Texture.

       texShield
          Shield powerup bs.Texture.

       texImpactBombs
          Impact-bomb powerup bs.Texture.

       texHealth
          Health powerup bs.Texture.

       texLandMines
          Land-mine powerup bs.Texture.

       texCurse
          Curse powerup bs.Texture.

       healthPowerupSound
          bs.Sound played when a health powerup is accepted.

       powerupSound
          bs.Sound played when a powerup is accepted.

       powerdownSound
          bs.Sound that can be used when powerups wear off.

       powerupMaterial
          bs.Material applied to powerup boxes.

       powerupAcceptMaterial
          Powerups will send a bs.PowerupMessage to anything they touch
          that has this bs.Material applied.
    """

    def __init__(self):
        """
        Instantiate a PowerupFactory.
        You shouldn't need to do this; call bs.Powerup.getFactory()
        to get a shared instance.
        """

        self._lastPowerupType = None
        
        self.model = bs.getModel("powerup")
        self.modelSimple = bs.getModel("powerupSimple")

        self.texBomb = bs.getTexture("powerupBomb")
        self.texPunch = bs.getTexture("powerupPunch")
        self.texIceBombs = bs.getTexture("powerupIceBombs")
        self.texStickyBombs = bs.getTexture("powerupStickyBombs")
        self.texShield = bs.getTexture("powerupShield")
        self.texImpactBombs = bs.getTexture("powerupImpactBombs")
        self.texHealth = bs.getTexture("powerupHealth")
        self.texLandMines = bs.getTexture("powerupLandMines")
        self.texCurse = bs.getTexture("powerupCurse")
        self.texFly = bs.getTexture("achievementOnslaught")
        self.eggModel = bs.getModel('egg')
        self.texEgg = bs.getTexture('eggTex1')
        self.texSno = bs.getTexture("bunnyColor")
        self.snoModel = bs.getModel("frostyPelvis")
        self.texPort = bs.getTexture("ouyaOButton")
        self.texAche = bs.getTexture("achievementOnslaught")
        self.flyModel = bs.getModel("flash")
        self.texMTweaker = bs.getTexture("achievementFlawlessVictory")
        self.texAntiGrav = bs.getTexture("achievementFootballShutout")

        self.healthPowerupSound = bs.getSound("healthPowerup")
        self.powerupSound = bs.getSound("powerup01")
        self.powerdownSound = bs.getSound("powerdown01")
        self.dropSound = bs.getSound("boxDrop")

        # material for powerups
        self.powerupMaterial = bs.Material()

        # material for anyone wanting to accept powerups
        self.powerupAcceptMaterial = bs.Material()

        # pass a powerup-touched message to applicable stuff
        self.powerupMaterial.addActions(
            conditions=(("theyHaveMaterial", self.powerupAcceptMaterial)),
            actions=(("modifyPartCollision", "collide", True),
                     ("modifyPartCollision", "physical", False),
                     ("message", "ourNode", "atConnect", _TouchedMessage())))

        # we dont wanna be picked up
        self.powerupMaterial.addActions(
            conditions=("theyHaveMaterial",
                        bs.getSharedObject('pickupMaterial')),
            actions=(("modifyPartCollision", "collide", False)))

        self.powerupMaterial.addActions(
            conditions=("theyHaveMaterial",
                        bs.getSharedObject('footingMaterial')),
            actions=(("impactSound", self.dropSound, 0.5, 0.1)))

        self._powerupDist = []
        for p, freq in getDefaultPowerupDistribution():
            for i in range(int(freq)):
                self._powerupDist.append(p)

    def getRandomPowerupType(self, forceType=None, excludeTypes=[]):
        """
        Returns a random powerup type (string).
        See bs.Powerup.powerupType for available type values.

        There are certain non-random aspects to this; a 'curse' powerup,
        for instance, is always followed by a 'health' powerup (to keep things
        interesting). Passing 'forceType' forces a given returned type while
        still properly interacting with the non-random aspects of the system
        (ie: forcing a 'curse' powerup will result
        in the next powerup being health).
        """
        if forceType:
            t = forceType
        else:
            # if the last one was a curse, make this one a health to
            # provide some hope
            if self._lastPowerupType == 'curse':
                t = 'health'
            else:
                while True:
                    t = self._powerupDist[
                        random.randint(0, len(self._powerupDist) - 1)]
                    if t not in excludeTypes:
                        break
        self._lastPowerupType = t
        return t


def getDefaultPowerupDistribution():
    return (('tripleBombs', 3),
            ('iceBombs', 3),
            ('punch', 3),
            ('impactBombs', 3),
            ('landMines', 2),
            ('stickyBombs', 3),
            ('shield', 2),
            ('health', 1),
            ('bunny', 2),
            ('portal', 2),
            ('headache', 2),
            ('curse', 1),
            ("fly", 2),
            ("motionTweaker", 2),
            ("antiGrav", 2),
            ('snoball', 3))


class Powerup(bs.Actor):
    """
    category: Game Flow Classes

    A powerup box.
    This will deliver a bs.PowerupMessage to anything that touches it
    which has the bs.PowerupFactory.powerupAcceptMaterial applied.

    Attributes:

       powerupType
          The string powerup type.  This can be 'tripleBombs', 'punch',
          'iceBombs', 'impactBombs', 'landMines', 'stickyBombs', 'shield',
          'health', or 'curse'.

       node
          The 'prop' bs.Node representing this box.
    """

    def __init__(self, position=(0, 1, 0), powerupType='tripleBombs', expire=True):
        """
        Create a powerup-box of the requested type at the requested position.

        see bs.Powerup.powerupType for valid type strings.
        """

        bs.Actor.__init__(self)

        factory = self.getFactory()
        self.powerupType = powerupType;
        self._powersGiven = False

        mod = factory.model
        mScl = 1
        color = (1, 1, 1)
        self.portal = None
        name = "none"
        if powerupType == 'tripleBombs':
            tex = factory.texBomb
            name = "triple bombs"
        elif powerupType == 'punch':
            tex = factory.texPunch
            name = "super gloves"
        elif powerupType == 'iceBombs':
            tex = factory.texIceBombs
            name = "ice bombs"
        elif powerupType == 'impactBombs':
            tex = factory.texImpactBombs
            name = "impact bombs"
        elif powerupType == 'landMines':
            tex = factory.texLandMines
            name = "land mines"
        elif powerupType == 'stickyBombs':
            tex = factory.texStickyBombs
            name = "sticky bombs"
        elif powerupType == 'shield':
            tex = factory.texShield
            name = "super shield"
        elif powerupType == 'health':
            tex = factory.texHealth
            name = "med pack"
        elif powerupType == 'curse':
            tex = factory.texCurse
            name = "curse"
        elif powerupType == 'portal':
            tex = factory.texPort
            name = "portal"
        elif powerupType == 'headache':
            tex = factory.texAche
            name = "headache bomb"
        elif powerupType == 'bunny':
            tex = factory.texEgg
            mod = factory.eggModel
            name = "buddy bunny"
            mScl = 0.7
        elif powerupType == 'snoball':
            tex = factory.texSno
            mod = factory.snoModel
            name = "snoballs"
        elif powerupType == "fly":
            tex = factory.texFly
            mod = factory.flyModel
            name = "3D flying"
            mScl = 0.7
        elif powerupType == "motionTweaker":
            tex = factory.texMTweaker
            name = "Motion Tweaker"
        elif powerupType == "antiGrav":
            tex = factory.texAntiGrav
            name = "Anti-Gravity Bombs"
        else:
            raise Exception("invalid powerupType: " + str(powerupType))

        if len(position) != 3: raise Exception("expected 3 floats for position")

        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={'body': 'box',
                                      'position': position,
                                      'model': mod,
                                      'lightModel': factory.modelSimple,
                                      'shadowSize': 0.5,
                                      'colorTexture': tex,
                                      'reflection': 'powerup',
                                      'reflectionScale': [1.0],
                                      'materials': (factory.powerupMaterial, bs.getSharedObject('objectMaterial'))})
        prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),
                      250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)}
        color = (random.random(), random.random(), random.random())
        if settings.nameOnPowerUps:
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': str(name),
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.016, 200: 0.01})
            bsUtils.animateArray(self.nodeText, 'color', 3, prefixAnim, True)
            bs.emitBGDynamics(position=self.nodeText.position, velocity=self.node.position, count=80, scale=1.0,
                              spread=1.3, chunkType='spark')

        if settings.discoLightsOnPowerUps:
            self.nodeLight = bs.newNode('light',
                                        attrs={'position': self.node.position,
                                               'color': color,
                                               'radius': 0.25,
                                               'volumeIntensityScale': 0.05})
            self.node.connectAttr('position', self.nodeLight, 'position')
            bsUtils.animateArray(self.nodeLight, 'color', 3, prefixAnim, True)
            bs.animate(self.nodeLight, "intensity", {0:1.0, 1000:1.8, 2000:1.0}, loop = True)
            bs.gameTimer(8000,self.nodeLight.delete)  

        if settings.shieldOnPowerUps:
            self.nodeShield = bs.newNode('shield', owner=self.node, attrs={'color': color,
                                                                           'position': (
                                                                               self.node.position[0],
                                                                               self.node.position[1],
                                                                               self.node.position[2] + 0.5),
                                                                           'radius': 1.2})
            self.node.connectAttr('position', self.nodeShield, 'position')
            bsUtils.animateArray(self.nodeShield, 'color', 3, prefixAnim, True)

        # animate in..
        curve = bs.animate(self.node, "modelScale", {0: 0, 140: 1.6, 200: mScl})
        bs.gameTimer(200, curve.delete)

        if expire:
            bs.gameTimer(defaultPowerupInterval - 2500,
                         bs.WeakCall(self._startFlashing))
            bs.gameTimer(defaultPowerupInterval - 1000,
                         bs.WeakCall(self.handleMessage, bs.DieMessage()))

    def delete_portal(self):
        if self.portal is not None and self.portal.exists():
            self.portal.delete()

    @classmethod
    def getFactory(cls):
        """
        Returns a shared bs.PowerupFactory object, creating it if necessary.
        """
        activity = bs.getActivity()
        if activity is None: raise Exception("no current activity")
        try:
            return activity._sharedPowerupFactory
        except Exception:
            f = activity._sharedPowerupFactory = PowerupFactory()
            return f

    def _startFlashing(self):
        if self.node.exists(): self.node.flashing = True

    def handleMessage(self, msg):
        self._handleMessageSanityCheck()

        if isinstance(msg, PowerupAcceptMessage):
            factory = self.getFactory()
            if self.powerupType == 'health':
                bs.playSound(factory.healthPowerupSound, 3,
                             position=self.node.position)
            bs.playSound(factory.powerupSound, 3, position=self.node.position)
            self._powersGiven = True
            self.handleMessage(bs.DieMessage())

        elif isinstance(msg, _TouchedMessage):
            if not self._powersGiven:
                node = bs.getCollisionInfo("opposingNode")
                if node is not None and node.exists():
                    if self.powerupType == 'bunny':
                        p = node.getDelegate().getPlayer()
                        if 'bunnies' not in p.gameData:
                            p.gameData['bunnies'] = BuddyBunny.BunnyBotSet(p)
                        p.gameData['bunnies'].doBunny()
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                    elif self.powerupType == 'snoball':
                        spaz = node.getDelegate()
                        SnoBallz.snoBall().getFactory().giveBallz(spaz)
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                    elif self.powerupType == 'portal':
                        t = bsSpaz.gPowerupWearOffTime
                        if self.node.position in objs.lastpos:
                            self.portal = objs.Portal(position1=None, r=0.9,
                                                      color=(random.random(), random.random(), random.random()),
                                                      activity=bs.getActivity())
                            bs.gameTimer(t, bs.Call(self.delete_portal))
                        else:
                            m = self.node.position
                            objs.lastpos.append(m)
                            self.portal = objs.Portal(position1=self.node.position, r=0.9,
                                                      color=(random.random(), random.random(), random.random()),
                                                      activity=bs.getActivity())
                            bs.gameTimer(t, bs.Call(self.delete_portal))
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                    elif self.powerupType == "fly":
                        spaz = node.getDelegate()
                        tex = bs.Powerup.getFactory().texFly
                        spaz._flashBillboard(tex)
                        spaz.jumpTo3DFly = True

                        def reset():
                            spaz.jumpTo3DFly = False
                            if spaz.node.exists():
                                bs.playSound(bs.Powerup.getFactory().powerdownSound,
                                             position=self.node.position)

                        if spaz.powerupsExpire:
                            spaz.node.miniBillboard1Texture = tex
                            t = bs.getGameTime()
                            spaz.node.miniBillboard1StartTime = t
                            spaz.node.miniBillboard1EndTime = t + bsSpaz.gPowerupWearOffTime
                            bs.gameTimer(bsSpaz.gPowerupWearOffTime, reset)
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                    elif self.powerupType == "motionTweaker":
                        bs.getSharedObject('globals').slowMotion = bs.getSharedObject('globals').slowMotion is False
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                    else:
                        node.handleMessage(PowerupMessage(self.powerupType, sourceNode=self.node))

        elif isinstance(msg, bs.DieMessage):
            if self.node.exists():
                if (msg.immediate):
                    self.node.delete()
                else:
                    curve = bs.animate(self.node, "modelScale", {0: 1, 100: 0})
                    bs.gameTimer(100, self.node.delete)
            if self.nodeLight.exists():
                self.nodeLight.delete()

        elif isinstance(msg, bs.OutOfBoundsMessage):
            self.handleMessage(bs.DieMessage())

        elif isinstance(msg, bs.HitMessage):
            # dont die on punches (that's annoying)
            if msg.hitType != 'punch':
                self.handleMessage(bs.DieMessage())
        else:
            bs.Actor.handleMessage(self, msg)
