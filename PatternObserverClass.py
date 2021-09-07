#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Observable:
    def __init__(self, name, verbose = False):
        self.name = name
        self.observer_list = set()
        self.verbose = False

    def register(self, new_observer):
        self.observer_list.add(new_observer)
        if self.verbose: print("registered " + new_observer.name + " to topic: " + self.name)

    def unregister(self, existing_observer):
        self.observer_list.discard(existing_observer)
        if self.Verbose: print("unregistered " + existing_observer.name + " to topic: " + self.name)

    def notify_all(self, news):
        for observer in self.observer_list:
            observer.update(ObservableData(self.name, news))


class ObservableData:
    def __init__(self, from_who, value):
        self.from_who = from_who
        self.value = value


# Abstract method
class Observer:
    def __init__(self, name):
        self.name = name
    def update(self, news: ObservableData):
        pass #print(self.name + " received:" + news.value + " from " + news.from_who)
