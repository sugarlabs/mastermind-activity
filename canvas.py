#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017, Cristian García <cristian99garcia@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from constants import BallType
from origin_box import OriginBox
from center_box import CenterBox
from grid_balls import GridBalls
from utils import get_random_ball

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import GObject


class Canvas(Gtk.VBox):

    __gsignals__ = {
        "data-changed": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, [GObject.TYPE_PYOBJECT]),
        "win": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "lose": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
    }

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.level = []

        hbox = Gtk.HBox()
        self.pack_start(hbox, True, True, 0)

        self.grid = GridBalls()
        self.grid.connect("data-changed", self._data_changed_cb)

        centerbox = CenterBox(self.grid)
        self.pack_start(centerbox, True, True, 0)

        self.originbox = OriginBox()
        self.originbox.connect("data-changed", self._data_changed_cb)

        centerbox = CenterBox(self.originbox)
        self.pack_end(centerbox, True, True, 0)

        self.reset()

        self.show_all()

    def clear(self):
        del self.level
        self.level = []

    def make_level(self):
        for x in range(0, 4):
            ball = get_random_ball()
            while ball in self.level:
                ball = get_random_ball()

            self.level.append(ball)

    def reset(self):
        self.clear()

        self.make_level()
        self.grid.reset()
        self.originbox.reset()
        self.emit("data-changed", [BallType.NULL] * 4)

    def end_turn(self):
        data = self.grid.get_level_data()

        if BallType.NULL in data:
            return

        self.grid.set_data(self.level, data)

        if self.level == data:
            self.emit("win")
            self.grid.game_over()
            self.originbox.game_over()

        elif self.level != data and self.grid.level == 10:
            self.emit("lose")
            self.grid.game_over()
            self.originbox.game_over()

    def get_game_data(self):
        data = self.grid.get_all_data()
        data["correct"] = self.level

        return data

    def set_game_data(self, data):
        self.level = data["correct"]
        self.grid.set_all_data(data)

    def _data_changed_cb(self, widget):
        self.emit("data-changed", self.grid.get_level_data())


if __name__ == "__main__":
    win = Gtk.Window()
    win.set_title("Mastermind")
    win.connect("destroy", Gtk.main_quit)

    canvas = Canvas()
    win.add(canvas)

    win.show_all()
    Gtk.main()
