import people

class Registry:
    def __init__(self):
        self.data = []
        self.refused = 0

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.data)

    def add(self, person):
        self.data.append(person)

    def load(self, text_path, ok_log = None, err_log = None):
        with open(text_path, "r", encoding = "utf-8") as file:
            # Перебор. Если очередная строка не пустая, то она обрезается и добавляется в список lines
            lines = [line.strip() for line in file if not line.isspace()]
            for i in range(len(lines)):
                try:
                    self.add(people.parse_into_instance(lines[i], ok_log, err_log, i))
                except people.AnketaParseError as e:
                    print(e)
                    self.refused += 1
                    continue

    def stats(self, path_to_save = None):
        stats = {"accepted": len(self.data), "refused": self.refused}
        if path_to_save:
            file = open(path_to_save, "w", encoding = "utf-8")
            file.write(f"Принято: {stats["accepted"]}\nОтказано: {stats["refused"]}\n")
            file.close()
        return stats

    def stats_by_type(self, path_to_save = None):
        stats = {}
        for person in self.data:
            person_type = type(person)
            if person_type in stats:
                stats[person_type] += 1
            else:
                stats[person_type] = 1
                
        if path_to_save:
            file = open(path_to_save, "w", encoding = "utf-8")
            for key in stats.keys():
                file.write(f"{key}: {stats[key]}\n")
            file.close()

        return stats

    def stats_by_belonging(self, path_to_save = None):
        stats = {}
        for person in self.data:
            if type(person) == Student:
                if person.group in stats:
                    stats[person.group] += 1
                else:
                    stats[person.group] = 1
            elif type(person) == Teacher:
                if person.faculty in stats:
                    stats[person.faculty] += 1
                else:
                    stats[person.faculty] = 1

        if path_to_save:
            file = open(path_to_save, "w", encoding = "utf-8")
            for key in stats.keys():
                file.write(f"{key}: {stats[key]}\n")
            file.close()

        return stats
