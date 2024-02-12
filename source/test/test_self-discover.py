import unittest
from source.main import query_selfdiscover

class TestSelfDiscover(unittest.TestCase):
    def test_query_selfdiscover_1(self):
        task_example = "Solve the equation x^2 + 5x + 6 = 0"
        expected_output = "The relevant reasoning modules for the task are: Module A, Module B, Module C"
        
        result = query_selfdiscover(task_example)
        
        self.assertIn(expected_output, result)
    
    def test_query_selfdiscover_2(self):
        task_example = ""
        expected_output = "The relevant reasoning modules for the task are: Module A, Module B"
        
        result = query_selfdiscover(task_example)
        
        self.assertIn(expected_output, result)
    
    def test_query_selfdiscover_3(self):
        task_example = "Given a list of numbers, find the sum of all even numbers greater than 10."
        expected_output = "The relevant reasoning modules for the task are: Module B, Module D"
        
        result = query_selfdiscover(task_example)
        
        self.assertIn(expected_output, result)

    def test_query_googledeepmind(self):
        task_example ="""This SVG path element <path d="M 55.57,80.69 L 57.38,65.80 M 57.38,65.80 L 48.90,57.46 M 48.90,57.46 L
            45.58,47.78 M 45.58,47.78 L 53.25,36.07 L 66.29,48.90 L 78.69,61.09 L 55.57,80.69"/> draws a:
            (A) circle (B) heptagon (C) hexagon (D) kite (E) line (F) octagon (G) pentagon(H) rectangle (I) sector (J) triangle
        """
        expected_output = "The correct identification of the shape as a kite (D)"
        
        result = query_selfdiscover(task_example)
        
        self.assertIn(expected_output, result)
    
    def test_query_googledeepmind_2(self):
        task_example="Lisa has 10 apples. She gives 3 apples to her friend and then buys 5 more apples from the store. How many apples does Lisa have now?"))
        expected_output = "we can determine that Lisa now has 12 apples"
        result = query_selfdiscover(task_example)
        self.assertIn(expected_output, result)
if __name__ == '__main__':
    unittest.main()