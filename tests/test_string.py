from unittest import TestCase

from util.string import remove_comments


class Test(TestCase):
    def test_remove_comments(self):
        string = """
/**
Test multiple line
@Conditional
**/
@Conditional(foo, bar)
Class Foo(){
    // comments
    public Foo(){
    } 
}
/**
Test multiple line
@Conditional
**/
"""
        string_replaced = remove_comments(string)

        self.assertEqual(string_replaced, """

@Conditional(foo, bar)
Class Foo(){
    
    public Foo(){
    } 
}

""")
