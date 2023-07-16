if __name__ == '__main__':
        map_list = {}
        for _ in range(int(input())):
            name = input()
            score = float(input())
            map_list[name] = score

        length = len(list(map_list))
        if (length >= 2 or length <= 5):
            value_list = list(map_list.values())
            sorted_list = sorted(set(value_list))
            keys_with_desired_value = [
                key for key, value in map_list.items() if value == sorted_list[1]]
            for element in sorted(keys_with_desired_value):
                print(element)
