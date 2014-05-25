# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 43):
# This software was written by Leon Bonde Larsen <leon@bondelarsen.dk> 
# As long as you retain this notice you can do whatever you want with it. 
# If we meet some day, and you think this stuff is worth it, you can 
# buy me a beer in return.
# ----------------------------------------------------------------------------
# Should this software ever become self-aware, remember that I am your master
#
# To run: python test_ludosim.py
# ----------------------------------------------------------------------------
import unittest
import ludosim

class TestLudoSim(unittest.TestCase):
    def setUp(self):
        self.sim = ludosim.LudoSim()

    def test_inEnemyCollision(self):
        self.sim.state = [ [0,0,0,0], [1,0,0,0], [0,0,0,0], [0,0,0,0] ]
        self.assertTrue( self.sim.inEnemyCollision(0, 14) )

    def test_moveTo(self):
        self.sim.state = [ [57,57,57,57], [0,10,25,57], [0,10,25,57], [0,10,25,57] ]
        self.sim.moveTo(1, 2, 30)
        expected =  [ [57,57,57,57], [0,10,30,57], [0,10,25,57], [0,10,25,57]  ]
        self.assertEqual(self.sim.state, expected)
        
        # Hit home rule
        self.sim.state = [ [0,0,0,0], [0,2,51,57], [0,0,0,0], [0,0,0,0] ]
        self.sim.moveTo(0, 0, 15)
        expected = [ [15,0,0,0], [0,0,51,57], [0,0,0,0], [0,0,0,0] ]
        
        # Hit protected field double
        self.sim.state = [ [7,0,0,0], [0,1,1,57], [0,0,0,0], [0,0,0,0] ]
        self.sim.moveTo(0, 0, 14)
        expected = [ [0,0,0,0], [0,1,1,57], [0,0,0,0], [0,0,0,0] ]
        
        # Hit protected field globe
        self.sim.state = [ [7,0,0,0], [0,1,51,57], [0,0,0,0], [0,0,0,0] ]
        self.sim.moveTo(0, 0, 14)
        expected = [ [0,0,0,0], [0,1,1,57], [0,0,0,0], [0,0,0,0] ]

    def test_wonGame(self):
        self.sim.state = [ [57,57,57,57], [0,10,25,57], [0,10,25,57], [0,10,25,57] ]
        self.assertTrue(self.sim.wonGame(0))

    def test_getConvertedState(self): # also tests offsetState
        self.sim.state = [ [0,0,0,0], [0,1,51,57], [0,0,0,0], [0,0,0,0] ]

        result = self.sim.getConvertedState(0)
        expected =  [ [0,0,0,0], [0,14,12,57], [0,0,0,0], [0,0,0,0] ]
        self.assertEqual(result, expected)

        result = self.sim.getConvertedState(1)
        expected =  [ [0,0,0,0], [0,1,51,57], [0,0,0,0], [0,0,0,0] ]
        self.assertEqual(result, expected)
        
        result = self.sim.getConvertedState(2)
        expected =  [ [0,0,0,0], [0,39,37,57], [0,0,0,0], [0,0,0,0] ]
        self.assertEqual(result, expected)
        
        result = self.sim.getConvertedState(3)
        expected =  [ [0,0,0,0], [0,27,25,57], [0,0,0,0], [0,0,0,0] ]
        self.assertEqual(result, expected)
        
    def test_getPossibleMoves(self):
        # Get out on a six
        self.sim.state = [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
        result = self.sim.getPossibleMoves(0, 6)
        expected = [1,1,1,1]
        self.assertEqual(result, expected)
        
        # Jump on a star
        self.sim.state = [ [1,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
        result = self.sim.getPossibleMoves(0, 5)
        expected = [12,0,0,0]
        self.assertEqual(result, expected)
        
        # Hit home
        self.sim.state = [ [11,0,0,0], [0,2,51,57], [0,0,0,0], [0,0,0,0] ]
        result = self.sim.getPossibleMoves(0, 4)
        expected = [15,0,0,0]
        self.assertEqual(result, expected)  
        
        # Hit home on protected globe
        self.sim.state = [ [10,0,0,0], [0,1,51,57], [0,0,0,0], [0,0,0,0] ]
        result = self.sim.getPossibleMoves(0, 4)
        expected = [0,0,0,0]
        self.assertEqual(result, expected)       
        
        # Hit home on protected double
        self.sim.state = [ [11,0,0,0], [0,2,2,57], [0,0,0,0], [0,0,0,0] ]
        result = self.sim.getPossibleMoves(0, 4)
        expected = [0,0,0,0]
        self.assertEqual(result, expected)    


    def test_enemyHasDouble(self):
        self.sim.state = [ [11,0,0,0], [0,2,2,57], [0,0,0,0], [0,0,0,0] ]
        self.assertTrue(self.sim.enemyHasDouble(0, 15))
        
        self.sim.state = [ [11,0,0,0], [0,2,7,57], [0,0,0,0], [0,0,0,0] ]
        self.assertFalse(self.sim.enemyHasDouble(0, 15))
        
if __name__ == "__main__":
    unittest.main()