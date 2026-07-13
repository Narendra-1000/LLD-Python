from .custom_hash_map import CustomHashMap


def main() -> None:
    map_: CustomHashMap[str, int] = CustomHashMap()
    map_.put("Shubh", 90)
    map_.put("Karan", 80)
    map_.put("Alice", 85)
    map_.put("John", 78)
    map_.put("Tom", 82)
    map_.put("Parth", 95)

    print(map_.get("John"))
    print(map_.get("Bob"))


if __name__ == "__main__":
    main()
