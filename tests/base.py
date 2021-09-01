from unittest import TestCase

from xml.dom import minidom


class BaseXmlTestCase(TestCase):

    def assertEqualXml(self, a: str, b: str):
        da, db = minidom.parseString(a), minidom.parseString(b)
        self.assertTrue(self._is_equal_xml_element(da.documentElement, db.documentElement))

    def _is_equal_xml_element(self, a, b):
        if a.tagName != b.tagName:
            return False
        if sorted(a.attributes.items()) != sorted(b.attributes.items()):
            return False

        """
        Remove any pure whitespace Dom Text Nodes before we compare

        See: https://xml-sig.python.narkive.com/8o0UIicu
        """
        for n in a.childNodes:
            if n.nodeType == n.TEXT_NODE and n.data.strip() == '':
                a.removeChild(n)
        for n in b.childNodes:
            if n.nodeType == n.TEXT_NODE and n.data.strip() == '':
                b.removeChild(n)

        if len(a.childNodes) != len(b.childNodes):
            return False
        for ac, bc in zip(a.childNodes, b.childNodes):
            if ac.nodeType != bc.nodeType:
                return False
            if ac.nodeType == ac.TEXT_NODE and ac.data != bc.data:
                return False
            if ac.nodeType == ac.ELEMENT_NODE and not self._is_equal_xml_element(ac, bc):
                return False
        return True
