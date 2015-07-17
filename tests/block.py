""" block module testing
"""

import unittest
import advcubit.system_module as _system
import advcubit.utility_module as _utility
import advcubit.block_module as _block


class BlockTest(unittest.TestCase):
    def setUp(self):
        """ test set up function """
        _utility.startCubit()
        _utility.newFile()

    def tearDown(self):
        """ test shutdown function """
        _utility.closeCubit()

    def test_create_block(self):
        v = _system.cubitModule.brick(1, 1, 1)
        v.volumes()[0].mesh()
        try:
            _block.createBlock(v, 33, 'volume')
        except _system.AdvCubitException as e:
            self.assertTrue(False, str(e))

    def test_element_type(self):
        v = _system.cubitModule.brick(1, 1, 1)
        v.volumes()[0].mesh()
        _block.createBlock(v, 33, 'volume')
        try:
            _block.setElementType(33, _block.VolumeElementTypes.HEX8)
        except _system.AdvCubitException as e:
            self.assertTrue(False, str(e))

    def test_name_block(self):
        v = _system.cubitModule.brick(1, 1, 1)
        v.volumes()[0].mesh()
        _block.createBlock(v, 33, 'volume')
        try:
            _block.nameBlock(33, 'testName')
        except _system.AdvCubitException as e:
            self.assertTrue(False, str(e))

    def test_block_element(self):
        v = _system.cubitModule.brick(1, 1, 1)
        v.volumes()[0].mesh()
        try:
            _block.createBlockFromElements(33, 'hex', v.volumes()[0], 'volume')
        except _system.AdvCubitException as e:
            self.assertTrue(False, str(e))


def testSuite():
    blockSuite = unittest.TestSuite()
    blockSuite.addTest(BlockTest('test_create_block'))
    blockSuite.addTest(BlockTest('test_element_type'))
    blockSuite.addTest(BlockTest('test_name_block'))
    blockSuite.addTest(BlockTest('test_block_element'))
    return blockSuite