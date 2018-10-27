import unittest
import os, sys
thisDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(thisDir))
import usrsdevenv.extensionsInstallers as extInst

class TestRunBlockingCommands(unittest.TestCase):

    def test_check_unsupported_platform(self):
        extensions = []
        with self.assertRaises(Exception) as context:
            extInst.extensions_installer('chrome', 'unsupported', extensions)
        self.assertTrue('unsupported' in str(context.exception))        

    def test_check_unsupported_software(self):
        extensions = []
        with self.assertRaises(Exception) as context:
            extInst.extensions_installer('unsupported1', 'unsupported2', extensions)
        self.assertTrue('unsupported1' in str(context.exception))     

if __name__ == '__main__':
    print('Running Unit Tests')
    unittest.main()
