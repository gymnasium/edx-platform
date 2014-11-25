"""
Test for asset XML generation / parsing.
"""

from datetime import datetime
from path import path
import pytz
from lxml import etree
import unittest

from opaque_keys.edx.locator import CourseLocator
from xmodule.assetstore import AssetMetadata
from xmodule.modulestore.tests.test_assetstore import AssetStoreTestData


class TestAssetXml(unittest.TestCase):
    """
    Tests for storing/querying course asset metadata.
    """
    def setUp(self):
        super(TestAssetXml, self).setUp()

        XSD_FILENAME = "assets.xsd"

        course_id = CourseLocator('org1', 'course1', 'run1')

        self.course_assets = []
        for i, asset in enumerate(AssetStoreTestData.all_asset_data):
            asset_dict = dict(zip(AssetStoreTestData.asset_fields[1:], asset[1:]))
            asset_md = AssetMetadata(course_id.make_asset_key('asset', asset[0]), **asset_dict)
            self.course_assets.append(asset_md)

        # Read in the XML schema definition and make a validator.
        xsd_path = path(__file__).abspath().dirname() / XSD_FILENAME
        with open(xsd_path, 'r') as f:
            schema_root = etree.XML(f.read())
        schema = etree.XMLSchema(schema_root)
        self.xmlparser = etree.XMLParser(schema=schema)

    def test_export_single_asset_to_from_xml(self):
        """
        Export a single AssetMetadata to XML and verify the structure and fields.
        """
        asset_md = self.course_assets[0]
        root = etree.Element("assets")
        asset = etree.SubElement(root, "asset")
        asset_md.to_xml(asset)
        # If this line does *not* raise, the XML is valid.
        asset_xml = etree.fromstring(etree.tostring(root), self.xmlparser)

    def test_export_all_assets_to_xml(self):
        """
        Export all AssetMetadatas to XML and verify the structure and fields.
        """
        root = etree.Element("assets")
        AssetMetadata.add_all_assets_as_xml(root, self.course_assets)
        asset_xml = etree.fromstring(etree.tostring(root), self.xmlparser)
