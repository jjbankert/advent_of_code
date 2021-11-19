from aoc_2020 import data_folder


def main():
    raw_data = (data_folder / "6_custom_customs.txt").read_text()
    groups_answers = raw_data.split("\n\n")

    # 1
    groups_answer_union = [set(group.replace("\n", "")) for group in groups_answers]
    print(sum(len(group_answers) for group_answers in groups_answer_union))

    # 2
    print(sum(len(get_group_overlap(group_answers)) for group_answers in groups_answers))


def get_group_overlap(group_answers: str):
    group_answers = group_answers.split("\n")
    group_overlap = set(group_answers[0])

    for personal_answers in group_answers[1:]:
        group_overlap.intersection_update(personal_answers)

    return group_overlap


if __name__ == "__main__":
    # print(get_group_overlap("a\nbc"))
    #
    main()
