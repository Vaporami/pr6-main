#!/usr/bin/python
import people, registry

reg = registry.Registry()
ok_log = open("./ok.txt", "w", encoding = "utf-8")
err_log = open("./err.txt", "w", encoding = "utf-8")
reg.load("../examples/example-1.txt", ok_log, err_log)
for person in reg:
    print(person)
print(reg.stats())
print(reg.stats_by_type())
print(reg.stats_by_belonging())
