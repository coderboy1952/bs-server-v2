#MadeByAlex
import bs
from bsMap import *
import bsMap

def __init__(self, vrOverlayCenterOffset=None):
        """
        Instantiate a map.
        """
        import bsInternal
        bs.Actor.__init__(self)
        self.preloadData = self.preload(onDemand=True)
        def text():
                #byalex
                t = bs.newNode('text',
                       attrs={ 'text':random.choice([u'\U0001F47B||WELCOME TO HEALTH VS CURSE OFFICIAL||\U0001F47B\n\U0001F47B||PLAY FAIR AND HAVE FUN||\U0001F47B',u'\U0001F47B||HAPPY BOMBSQUADING||\U0001F47B',u'\U0001F47B||CHECK OUT OUR DISCORD SERVER||\U0001F47B']),
                              'scale':0.8,
                              'maxWidth':0,
                              'position':(11,130),
                              'shadow':0.9,
                              'flatness':1.0,
                              'color':(1,1,1),
                              'hAlign':'center',
                              'vAttach':'top'})
                bs.animate(t,'opacity',{0: 0.0,500: 1.0,6500: 1.0,7000: 0.0})
                bs.gameTimer(2000000,t.delete)
                ##
                t = bs.newNode('text',
                       attrs={ 'text':u'\ue00cEDITOR SCRIPT : |NAZMI|\ue00c',
                              'scale':0.8,
                              'maxWidth':0,
                              'position':(-460,30),
                              'shadow':0.9,
                              'flatness':0.1,
                              'color':(1,1,1),
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{0: 0.0,500: 1.0,6500: 1.0,7000: 0.0})
                bs.gameTimer(2000000,t.delete)
                       #byalex
                t = bs.newNode('text',
                       attrs={ 'text':u'\ue00cOWNER : |NAZMI|\ue00c',
                              'scale':0.8,
                              'maxWidth':0,
                              'position':(460, 30),
                              'color':(1,1,1),
                              'shadow':0.9,
                              'flatness':0.1,
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{0: 0.0,500: 1.0,6500: 1.0,7000: 0.0})
                bs.gameTimer(2000000,t.delete)
                #byalex
                '''t = bs.newNode('text',
                       attrs={ 'text':random.choice([u'\U0001F47B||WELCOME TO OFFICIAL||\U0001F47B\n\U0001F47B||PLAY FAIR AND HAVE FUN||\U0001F47B',u'\U0001F47B||HAPPY BOMBSQUADING||\U0001F47B',u'\U0001F47B||JOIN OUR DISCORD SERVER||\U0001F47B']),
                              'scale':1.2,
                              'maxWidth':0,
                              'position':(11,130),
                              'shadow':0.9,
                              'flatness':1.0,
                              'color':(1,1,1),
                              'hAlign':'center',
                              'vAttach':'top'})
                bs.animate(t,'opacity',{0: 0.0,500: 1.0,6500: 1.0,7000: 0.0})
                bs.gameTimer(2000000,t.delete)
                ##
                t = bs.newNode('text',
                       attrs={ 'text':'Dont Use Curse Words.\n Never Abuse Anyone.',
                              'scale':0.9,
                              'maxWidth':0,
                              'position':(100,10),
                              'shadow':0.6,
                              'flatness':1.0,
                              'color':(1,1,1),
                              'hAlign':'center',
                              'vAttach':'top'})
                bs.animate(t,'opacity',{0: 0.0,500: 1.0,6500: 1.0,7000: 0.0})
                bs.gameTimer(610000,t.delete)
                ##
                t = bs.newNode('text',
                       attrs={ 'text':'Hope You Guys Enjoy On\nOur Server.',
                               'scale':1.2,
                              'maxWidth':0,
                              'position':(-40,-40),
                              'shadow':0.5,
                              'flatness':1.0,
                              'color':(1,1,1),
                              'hAlign':'center',
                              'vAttach':'top'})
                bs.animate(t,'opacity',{0: 0.0,500: 1.0,6500: 1.0,7000: 0.0})
                bs.gameTimer(610000,t.delete)'''
        bs.gameTimer(100,bs.Call(text))
        bs.gameTimer(100,bs.Call(text),repeat = True)
        
        # set some defaults
        bsGlobals = bs.getSharedObject('globals')
        # area-of-interest bounds
        aoiBounds = self.getDefBoundBox("areaOfInterestBounds")
        if aoiBounds is None:
            print 'WARNING: no "aoiBounds" found for map:',self.getName()
            aoiBounds = (-1,-1,-1,1,1,1)
        bsGlobals.areaOfInterestBounds = aoiBounds
        # map bounds
        mapBounds = self.getDefBoundBox("levelBounds")
        if mapBounds is None:
            print 'WARNING: no "levelBounds" found for map:',self.getName()
            mapBounds = (-30,-10,-30,30,100,30)
        bsInternal._setMapBounds(mapBounds)
        # shadow ranges
        try: bsGlobals.shadowRange = [
                self.defs.points[v][1] for v in 
                ['shadowLowerBottom','shadowLowerTop',
                 'shadowUpperBottom','shadowUpperTop']]
        except Exception: pass
        # in vr, set a fixed point in space for the overlay to show up at..
        # by default we use the bounds center but allow the map to override it
        center = ((aoiBounds[0]+aoiBounds[3])*0.5,
                  (aoiBounds[1]+aoiBounds[4])*0.5,
                  (aoiBounds[2]+aoiBounds[5])*0.5)
        if vrOverlayCenterOffset is not None:
            center = (center[0]+vrOverlayCenterOffset[0],
                      center[1]+vrOverlayCenterOffset[1],
                      center[2]+vrOverlayCenterOffset[2])
        bsGlobals.vrOverlayCenter = center
        bsGlobals.vrOverlayCenterEnabled = True
        self.spawnPoints = self.getDefPoints("spawn") or [(0,0,0,0,0,0)]
        self.ffaSpawnPoints = self.getDefPoints("ffaSpawn") or [(0,0,0,0,0,0)]
        self.spawnByFlagPoints = (self.getDefPoints("spawnByFlag")
                                  or [(0,0,0,0,0,0)])
        self.flagPoints = self.getDefPoints("flag") or [(0,0,0)]
        self.flagPoints = [p[:3] for p in self.flagPoints] # just want points
        self.flagPointDefault = self.getDefPoint("flagDefault") or (0,1,0)
        self.powerupSpawnPoints = self.getDefPoints("powerupSpawn") or [(0,0,0)]
        self.powerupSpawnPoints = \
            [p[:3] for p in self.powerupSpawnPoints] # just want points
        self.tntPoints = self.getDefPoints("tnt") or []
        self.tntPoints = [p[:3] for p in self.tntPoints] # just want points
        self.isHockey = False
        self.isFlying = False
        self._nextFFAStartIndex = 0
        
bsMap.Map.__init__ = __init__
