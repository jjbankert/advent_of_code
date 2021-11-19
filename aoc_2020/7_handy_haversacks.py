import neo4j

from aoc_2020 import data_folder


def bags_in_bags(bag_color: str) -> int:
    connector = neo4j.Connector()
    sum = 0

    response = connector.run(
        """
        MATCH (:BAG {color:$color})-[relation:CONTAINS]->(parent:BAG)
        RETURN parent.color as color, relation.count as count 
        """,
        {"color": bag_color},
    )
    for row in response:
        sum += row["count"]
        sum += row["count"] * bags_in_bags(row["color"])

    return sum


def parse_rules():
    raw_data = (data_folder / "7_handy_haversacks.txt").read_text()

    statements = []
    for line in raw_data.splitlines():
        bag_type, parsed_rules = parse_line(line)
        for rule_color, rule_count in parsed_rules.items():
            statements.append(
                neo4j.Statement(
                    """
                    MERGE (b1:BAG {color:$color1})
                    MERGE (b2:BAG {color:$color2})
                    MERGE (b1)-[:CONTAINS {count:$count}]->(b2)
                    """,
                    {"color1": bag_type, "color2": rule_color, "count": rule_count},
                )
            )
    neo4j.Connector().run_multiple(statements)


def parse_line(line: str):
    bag_type, raw_rules = line.strip(".").split("contain")
    bag_rules = raw_rules.split(", ")

    parsed_rules = {}
    for bag_rule in bag_rules:
        count, color = parse_item(bag_rule)
        if count > 0:
            parsed_rules[color] = count

    return parse_item(bag_type)[1], parsed_rules


def parse_item(item_phrase: str):
    item_phrase = item_phrase.strip()
    if item_phrase == "no other bags":
        return 0, ""

    interesting_bit = item_phrase[: item_phrase.rfind(" ")]
    count = 1
    color = interesting_bit
    try:
        first_space = interesting_bit.find(" ")
        count = int(interesting_bit[:first_space])
        color = interesting_bit[first_space + 1 :]
    except ValueError:
        pass

    return count, color


if __name__ == "__main__":
    parse_rules()
    print(bags_in_bags("shiny gold"))
