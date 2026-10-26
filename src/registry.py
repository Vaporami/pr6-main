import people

class Registry:
    def __init__(self):
        self.data = []
        self.refused = 0
        self.refused_lines = {}

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.data)

    def add(self, person):
        self.data.append(person)

    def sort(self):
        self.data.sort()

    def load(self, text_path, ok_log = None, err_log = None):
        with open(text_path, "r", encoding = "utf-8") as file:
            # Генератор. Если очередная строка не пустая, то она обрезается и добавляется в список lines
            lines = [line.strip() for line in file]
            for i in range(len(lines)):
                if lines[i].isspace() or lines[i] == "":
                    continue
                try:
                    self.add(people.parse_into_instance(lines[i], ok_log, err_log, i + 1))
                except people.AnketaParseError as e:
                    print(e)
                    self.refused += 1
                    self.refused_lines[i + 1] = str(e)
                    continue

    def stats(self, file_to_write = None):
        stats = {"accepted": len(self.data), "refused": self.refused}
        if file_to_write:
            file_to_write.write(f"Принято: {stats["accepted"]}\nОтказано: {stats["refused"]}\n")
        return stats

    def stats_by_type(self, file_to_write = None):
        stats = {}
        for person in self.data:
            person_type = person.role()
            if person_type in stats:
                stats[person_type] += 1
            else:
                stats[person_type] = 1
                
        if file_to_write:
            for key in stats.keys():
                file_to_write.write(f"{key}: {stats[key]}\n")

        return stats

    def stats_by_belonging(self, key = lambda p: True, file_to_write = None):
        stats = {}
        for person in self.data:
            belongs_to = person.extra()
            if belongs_to in stats:
                if key(person):
                    stats[belongs_to] += 1
            else:
                if key(person):
                    stats[belongs_to] = 1

        if file_to_write:
            for key in stats.keys():
                file_to_write.write(f"{key}: {stats[key]}\n")

        return stats

    def save_ok(self, file):
        for person in self:
            line = f"{str(person)}\n"
            file.write(line)

    def save_err(self, file):
        for key in self.refused_lines.keys():
            line = f"[{key}] {self.refused_lines[key]}\n"
            file.write(line)
