from three_solutions import Graph, Vertex
import unittest

inf = float('inf')

class TestSolutions(unittest.TestCase):
    def create_graph(self):
        # very simple food web from https://www.nature.com/scitable/content/ne0000/ne0000/ne0000/ne0000/96519252/Hui_figure1_v001-01_1_2.jpg
        graph = Graph(is_directed=True)
        animal_1 = graph.add_vertex('Kit Fox')
        animal_2 = graph.add_vertex('Hawk')
        animal_3 = graph.add_vertex('Scorpion')
        animal_4 = graph.add_vertex('Grasshopper')
        animal_5 = graph.add_vertex('Ground Squirrel')
        animal_6 = graph.add_vertex('Grass')

        graph.add_edge('Grass','Grasshopper', 1)
        graph.add_edge('Grass','Ground Squirrel', 1)
        graph.add_edge('Grasshopper','Scorpion', 1)
        graph.add_edge('Scorpion','Kit Fox', 1)
        graph.add_edge('Ground Squirrel','Kit Fox', 1)
        graph.add_edge('Ground Squirrel','Hawk', 1)

        return graph
    
    def test_shortest_prey_to_predator(self):
        graph = self.create_graph()

        expected_shortest_path = 2

        self.assertEqual(graph.shortest_prey_to_predator('Grass', 'Kit Fox'), expected_shortest_path)
    
    def test_popular_species(self):
        graph = self.create_graph()
        expected_output = {
            'Kit Fox': {'Kit Fox': 0, 'Hawk': inf, 'Scorpion': inf, 'Grasshopper': inf, 'Ground Squirrel': inf, 'Grass': inf},
            'Hawk': {'Kit Fox': inf, 'Hawk': 0, 'Scorpion': inf, 'Grasshopper': inf, 'Ground Squirrel': inf, 'Grass': inf},
            'Scorpion': {'Kit Fox': 1, 'Hawk': inf, 'Scorpion': 0, 'Grasshopper': inf, 'Ground Squirrel': inf, 'Grass': inf},
            'Grasshopper': {'Kit Fox': 2, 'Hawk': inf, 'Scorpion': 1, 'Grasshopper': 0, 'Ground Squirrel': inf, 'Grass': inf},
            'Ground Squirrel': {'Kit Fox': 1, 'Hawk': 1, 'Scorpion': inf, 'Grasshopper': inf, 'Ground Squirrel': 0, 'Grass': inf}, 
            'Grass': {'Kit Fox': 2, 'Hawk': 2, 'Scorpion': 2, 'Grasshopper': 1, 'Ground Squirrel': 1, 'Grass': 0}
        }

        self.assertEqual(graph.popular_species(), expected_output)
    
    def test_food_chains(self):
        graph = self.create_graph()

        expected_most_common_prey = 'Grass'

        self.assertEqual(graph.most_common_prey(), expected_most_common_prey)

if __name__ == '__main__':
    unittest.main()