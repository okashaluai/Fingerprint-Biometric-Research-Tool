import os
import unittest

from Dev.LogicLayer.LogicObjects.Image import Image
from Dev.LogicLayer.LogicObjects.Template import Template
from Dev.Tests.TestUtils import Image2Template_path


class ImageToTemplateTests(unittest.TestCase):

    def setUp(self):
        self.image1 = Image(os.path.join(os.path.join(Image2Template_path, 'TestCase1'), 'i1.png'), is_dir=False)
        self.image2 = Image(os.path.join(os.path.join(Image2Template_path, 'TestCase2'), 'i2.png'), is_dir=False)
        self.image3 = Image(os.path.join(os.path.join(Image2Template_path, 'TestCase3'), 'i3.png'), is_dir=False)
        self.template1 = Template(os.path.join(os.path.join(Image2Template_path, 'TestCase1'), 'i1'), is_dir=False)
        self.template2 = Template(os.path.join(os.path.join(Image2Template_path, 'TestCase2'), 'i2'), is_dir=False)
        self.template3 = Template(os.path.join(os.path.join(Image2Template_path, 'TestCase3'), 'i3'), is_dir=False)

    def test_convert_to_template(self):
        result_template_path1 = self.image1.convert_to_template()
        result_template1 = Template(result_template_path1, is_dir=False)
        self.assertEqual(result_template1, self.template1)

        result_template_path2 = self.image2.convert_to_template()
        result_template2 = Template(result_template_path2, is_dir=False)
        self.assertEqual(result_template2, self.template2)

        result_template_path3 = self.image3.convert_to_template()
        result_template3 = Template(result_template_path3, is_dir=False)
        self.assertEqual(result_template3, self.template3)
