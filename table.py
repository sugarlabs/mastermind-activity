#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Pango


class ValueEntry(Gtk.Entry):

    def __init__(self, *args, **kargs):
        Gtk.Entry.__init__(self, *args, **kargs)

        self.value = 0

        self.set_width_chars(5)
        self.set_size_request(1, 50)
        self.set_text("0")
        self.modify_font(Pango.FontDescription("21"))
        self.connect('changed', self.__on_changed)

    def __on_changed(self, widget):
        text = self.get_text()
        self.set_text(''.join([i for i in text if i in '0123456789']))
        self.value = int(self.get_text() if self.get_text() != "" else "0")

    def get_value(self):
        text = self.get_text()
        return int(text)


class ColumnBox(Gtk.VBox):

    def __init__(self, *args, **kargs):
        Gtk.VBox.__init__(self, *args, **kargs)

        self.set_orientation(Gtk.Orientation.VERTICAL)

    def __getitem__(self, index):
        return self.get_children()[index]


class Table(Gtk.HBox):

    def __init__(self):
        Gtk.HBox.__init__(self)

        self.boxes = []
        self.values = []
        self.size = [0, 0]

    def set_values(self, values):
        # Clear data
        del self.values
        self.values = []

        while len(self.get_children()) > 0:
            self.remove(self.get_children()[0])

        # Set new data
        size = [len(values), len(values[0])]

        for x in range(0, size[0]):
            self.add_column()

        for y in range(0, size[1]):
            self.add_row()

        for x in range(0, size[0]):
            for y in range(0, size[1]):
                #entry = ValueEntry()
                pass

    def get_values(self):
        self.get_values_from_entries()
        return self.values

    def get_values_from_entries(self):
        del self.values
        self.values = []

        for x in range(0, self.size[0]):
            self.values.append([])

            for y in range(0, self.size[1]):
                entry = self.get_entry_from_coords(x, y)
                self.values[x].append(entry.get_value())

    def get_entry_from_coords(self, x, y):
        return self.boxes[x][y]

    def add_column(self):
        self.size[0] += 1
        column = [0] * self.size[1]
        self.values.append(column)

        box = ColumnBox()
        self.pack_start(box, False, False, 0)
        self.boxes.append(box)

        for y in range(0, self.size[1]):
            box.pack_start(ValueEntry(), False, False, 0)

        self.show_all()

    def add_row(self):
        self.size[1] += 1

        for x in range(0, self.size[0]):
            self.values[x].append(0)
            self.boxes[x].pack_start(ValueEntry(), False, False, 0)

        self.show_all()
