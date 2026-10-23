#!/usr/bin/python
import people, registry

# reg = registry.Registry()
# ok_log = open("./ok.txt", "w", encoding = "utf-8")
# err_log = open("./err.txt", "w", encoding = "utf-8")
# reg.load("../examples/example-1.txt", ok_log, err_log)
# for person in reg:
#     print(person)
# print(reg.stats())
# print(reg.stats_by_type())
# print(reg.stats_by_belonging())

reg = registry.Registry()
ok_log = open("./ok.txt", "w", encoding = "utf-8")
err_log = open("./err.txt", "w", encoding = "utf-8")
reg.load("../examples/example-1.txt", ok_log, err_log)

print(f"{"#":<4}{"ФИО":<35}{"ПОЧТА":<25}{"НОМЕР ТЕЛЕФОНА":<20}{"ГРУППА/КАФЕДРА"}")
print("-" * 90)
for i in range(len(reg)):
    person = reg[i]
    print(f"{i:<4}{person.full_name:<35}{person.email:<25}{person.phone:<20}{person.extra()}")
print("-" * 90)

stats = (reg.stats())
print(f"Принято: {stats["accepted"]}\nОтказано: {stats["refused"]}")
print("-" * 90)

stats = reg.stats_by_type()
print(f"Студентов: {stats[people.Student]}\nПреподавателей: {stats[people.Teacher]}")
print("-" * 90)

stats = reg.stats_by_belonging()
for key in stats.keys():
    print(f"{key}: {stats[key]}")
print("-" * 90)

