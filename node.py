import unittest
class Node:
    def __init__(self, init_name ):
        self.name = init_name

        if ',' in init_name :
            self.num_in_household = 2
        else:
            self.num_in_household = 1

        self.hosting = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Node_single_test( unittest.TestCase ):
    def setUp(self):
        self.node = Node( "kit" )

    def tearDown(self):
        self.node = None

    def test_name(self):
        self.assertEqual( self.node.name, "kit", "name assignment fail")

    def test_hosting(self):
        self.assertEqual( self.node.hosting, False, 'initial "hosting" condition fail' )

    def test_household_size(self):
        self.assertEqual( self.node.num_in_household, 1, "single incorrect household size" )

class Node_couple_test( unittest.TestCase ):
    def setUp(self):
        self.node = Node( "mark, eva" )

    def tearDown(self):
        self.node = None

    def test_name(self):
        self.assertEqual( self.node.name, "mark, eva", "name assignment fail")

    def test_hosting(self):
        self.assertEqual( self.node.hosting, False, 'initial "hosting" condition fail' )

    def test_household_size(self):
        self.assertEqual( self.node.num_in_household, 2, "couple incorrect household size" )

#TODO make this_graph from list

if __name__ == '__main__':
    unittest.main()

# class SimpleWidgetTestCase(unittest.TestCase):
#     def setUp(self):
#         self.widget = Widget('The widget')
#
#     def tearDown(self):
#         self.widget.dispose()
#         self.widget = None