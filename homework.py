from kb import KB
from logic import Logic
from sentence import Sentence
from constants import Consts
from collections import defaultdict
from copy import deepcopy
import time


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
                original_sent = deepcopy(kb_sentence)
                Logic.factor_sentence(kb_sentence)
                # self.kb.tell(kb_sentence)
                self.kb.tell(original_sent)

    def write_output(self):
        with open(Consts.output_file_path, "w") as opf:
            opf.writelines("\n".join(self.answers))

    def run_logic(self):
        self.read_input_into_kb()

        start_time = time.time()

        for query in self.queries:
            if self.kb.ask(self.kb, query):
                self.answers.append("TRUE")
            else:
                self.answers.append("FALSE")

        end_time = time.time()

        print("Time taken: {}".format(end_time - start_time))

        self.write_output()


if __name__ == "__main__":
    logicRunner = LogicRunner()
    logicRunner.run_logic()
