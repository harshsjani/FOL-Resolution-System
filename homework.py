from kb import KB
from constants import Consts


class LogicRunner:
    def __init__(self):
        self.kb = KB()
        self.queries = []
        self.answers = []

    def read_input_into_kb(self):
        with open(Consts.input_file_path) as ipf:
            num_queries = int(ipf.readline())

            for i in range(num_queries):
                self.queries.append(ipf.readline().rstrip())

            num_sentences = int(ipf.readline())

            for i in range(num_sentences):
                self.kb.tell(ipf.readline().rstrip())

    def write_output(self):
        with open(Consts.input_file_path) as opf:
            opf.writelines("\n".join(self.answers))

    def run_logic(self):
        self.read_input_into_kb()

        for query in self.queries:
            self.answers.append(True if self.kb.ask(self.kb, query) else False)

        self.write_output()


if __name__ == "__main__":
    logicRunner = LogicRunner()
    logicRunner.run_logic()
