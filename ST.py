import ast
import os
import networkx as nx
import matplotlib.pyplot as plt

class CodeCoverage:
    def __init__(self, code_folder="."):
        self.code_folder = code_folder
        self.code_stats = []
        self.total_stats = {"statements": 0, "miss": 0, "cover": 0}
        self.execution_graph = nx.DiGraph()

    def run_coverage(self):
        self.collect_stats()
        self.print_table()
        self.visualize_coverage()

    def collect_stats(self):
        for filename in os.listdir(self.code_folder):
            if filename.endswith(".py"):
                code_file = os.path.join(self.code_folder, filename)
                test_file_name = "test_" + filename
                test_file = os.path.join(self.code_folder, test_file_name)

                # Exclude stCode.py from coverage analysis
                if filename == "ST.py":
                    continue

                code_stat = self.calculate_file_coverage(code_file, test_file)
                self.code_stats.append(code_stat)

                self.total_stats["statements"] += code_stat["statements"]
                self.total_stats["miss"] += code_stat["miss"]

    def calculate_file_coverage(self, code_file, test_file):
        code_stat = {"filename": os.path.basename(code_file), "statements": 0, "miss": 0}

        with open(code_file, "r") as f:
            code_tree = ast.parse(f.read(), filename=code_file)

        statements = [node for node in ast.walk(code_tree) if isinstance(node, ast.stmt)]
        code_stat["statements"] = len(statements)

        if os.path.exists(test_file):
            with open(test_file, "r") as f:
                test_tree = ast.parse(f.read(), filename=test_file)

            test_statements = [
                node for node in ast.walk(test_tree) if isinstance(node, ast.FunctionDef)
            ]

            for stmt in statements:
                for test_stmt in test_statements:
                    if stmt.lineno >= test_stmt.lineno and stmt.end_lineno <= test_stmt.end_lineno:
                        self.execution_graph.add_edge(test_stmt, stmt, color='green')
                        break
                else:
                    self.execution_graph.add_node(stmt, color='red')
                    code_stat["miss"] += 1

        code_stat["cover"] = int((1 - code_stat["miss"] / code_stat["statements"]) * 100)
        return code_stat

    def print_table(self):
        print("{:<30} {:<10} {:<10} {:<10}".format("Name", "Stmts", "Miss", "Cover Rate"))
        print("-" * 120)
        for stat in self.code_stats:
            cover_rate = int((1 - stat["miss"] / stat["statements"]) * 100) if stat["statements"] > 0 else 100
            print("{:<30} {:<10} {:<10} |{:<60}| {:>3}%".format(
                stat["filename"], stat["statements"], stat["miss"], "█" * (cover_rate // 2), cover_rate
            ))
        print("-" * 120)
        total_cover_rate = int((1 - self.total_stats["miss"] / self.total_stats["statements"]) * 100) if \
        self.total_stats["statements"] > 0 else 100
        print("{:<30} {:<10} {:<10} |{:<60}| {:>3}%".format(
            "TOTAL", self.total_stats["statements"], self.total_stats["miss"], "█" * (total_cover_rate // 2),
            total_cover_rate
        ))

    def visualize_coverage(self):
        pos = nx.spring_layout(self.execution_graph)
        node_colors = [data.get('color', 'green') for node, data in self.execution_graph.nodes(data=True)]
        edge_colors = [data['color'] for _, _, data in self.execution_graph.edges(data=True)]

        nx.draw_networkx_nodes(self.execution_graph, pos, node_color=node_colors)
        nx.draw_networkx_edges(self.execution_graph, pos, edge_color=edge_colors)

        plt.show()

if __name__ == "__main__":
    coverage_tool = CodeCoverage()
    coverage_tool.run_coverage()
