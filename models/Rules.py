from typing import List


class Rules:
    def __init__(self, mask: List[int], survival_rule: List[bool], birth_rule: int):
        self.mask = mask
        self.survival_rule = survival_rule
        self.birth_rule = birth_rule
        # print(mask)
        # print(survival_rule)
        # print(birth_rule)

    def is_survived(self, neighbours_count):
        return self.survival_rule[neighbours_count]

    def was_born(self, neighbours_count):
        return neighbours_count == self.birth_rule
