from kb import KB
from sentence import Sentence
from constants import Consts
from collections import defaultdict


class LogicRunner:
    def __init__(self):
        self.kb = KB()
        self.queries = []
        self.answers = []
        self.var_counter = defaultdict(int)

    def standardize_raw_sentence(self, raw_sentence):
        in_args = False
        kb_sent = []
        updated_this_sent = set()

        for i, char in enumerate(raw_sentence):
            if char == "(":
                in_args = True
            elif char == ")":
                in_args = False
            else:
                if in_args and char.isalpha() and char.islower():
                    if (raw_sentence[i + 1] == "," or
                            raw_sentence[i + 1] == ")") and \
                            not raw_sentence[i - 1].isalpha():
                        if char not in updated_this_sent:
                            self.var_counter[char] += 1
                            updated_this_sent.add(char)
                        kb_sent.append(char + str(self.var_counter[char]))
                        continue
            kb_sent.append(char)

        return "".join(kb_sent)

    def read_input_into_kb(self):
        with open(Consts.input_file_path) as ipf:
            num_queries = int(ipf.readline())

            for i in range(num_queries):
                self.queries.append(ipf.readline().rstrip())

            num_sentences = int(ipf.readline())

            for i in range(num_sentences):
                raw_sentence = ipf.readline().rstrip()
                kb_sentence = self.standardize_raw_sentence(raw_sentence)
                kb_sentence = Sentence(kb_sentence)
                self.kb.tell(kb_sentence)

    def write_output(self):
        with open(Consts.output_file_path, "w") as opf:
            opf.writelines("\n".join(self.answers))

    def run_logic(self):
        self.read_input_into_kb()
        self.kb.eliminate_pure_literals()

        for query in self.queries:
            if self.kb.ask(self.kb, query):
                self.answers.append("TRUE")
            else:
                self.answers.append("FALSE")

        self.write_output()


if __name__ == "__main__":
    logicRunner = LogicRunner()
    logicRunner.run_logic()
