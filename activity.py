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

import dbus
from gettext import gettext as _

from canvas import Canvas
from constants import BallType
from helpbutton import HelpButton

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Pango

from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.toolbarbox import ToolbarBox

from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.activity import activity


class Mastermind(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.canvas = Canvas()
        self.canvas.connect("data-changed", self._data_changed_cb)
        self.canvas.connect("win", self._win_cb)
        self.canvas.connect("lose", self._lose_cb)
        self.set_canvas(self.canvas)

        self.make_toolbar()
        self.read_file()

        self.show_all()

    def make_toolbar(self):
        def make_separator(expand=True):
            separator = Gtk.SeparatorToolItem()
            separator.props.draw = not expand
            separator.set_expand(expand)
            return separator

        toolbarbox = ToolbarBox()
        self.set_toolbar_box(toolbarbox)

        toolbar = toolbarbox.toolbar
        toolbar.insert(ActivityToolbarButton(self), -1)
        toolbar.insert(make_separator(False), -1)

        self.restart_button = ToolButton(icon_name="system-restart")
        self.restart_button.set_tooltip(_("Restart"))
        self.restart_button.props.accelerator = '<Ctrl>N'
        self.restart_button.connect("clicked", self._restart_cb)
        toolbar.insert(self.restart_button, -1)

        self.ok_button = ToolButton(icon_name="dialog-ok")
        self.ok_button.set_tooltip(_("Ok"))
        self.ok_button.set_sensitive(False)
        self.ok_button.props.accelerator = "Return"
        self.ok_button.connect("clicked", self._ok_cb)
        toolbar.insert(self.ok_button, -1)

        item = Gtk.ToolItem()
        toolbar.insert(item, -1)

        self.label = Gtk.Label()
        self.label.modify_font(Pango.FontDescription("Bold"))
        item.add(self.label)

        toolbar.insert(make_separator(True), -1)

        helpbutton = HelpButton()
        helpbutton.add_section(_("Instructions:"))
        helpbutton.add_paragraph(_("Place colors to the last played row."), image="instructions1.png")
        helpbutton.add_paragraph(_("When you complete a row, click on 'Ok button'."), image="instructions2.png")
        helpbutton.add_paragraph(_("Next to the row will appear black and white circles."), image="instructions3.png")
        helpbutton.add_paragraph(_("A black circle means you matched a peg and you placed it correctly."))
        helpbutton.add_paragraph(_("A white circle means you matched a peg and you wrong placed it."))
        helpbutton.add_paragraph(_("The goal is match all pegs in the correct place."))
        toolbar.insert(helpbutton, -1)

        stop_button = StopButton(self)
        toolbar.insert(stop_button, -1)

        toolbar.show_all()

    def read_file(self):
        if "level" in self.metadata.keys():
            data = {
                "level": int(self.metadata["level"]),
                "correct": [int(x) for x in eval(self.metadata["correct"])],
                "balls": {}
            }

            balls = eval(self.metadata["balls"])
            for key in balls:
                x = int(key)
                data["balls"][x] = []

                for value in balls[key]:
                    y = int(value)
                    data["balls"][x].append(y)

            current = []
            for x in range(0, 4):
                current.append(data["balls"][x][data["level"]])

            self.ok_button.set_sensitive(not BallType.NULL in current)
            self.canvas.set_game_data(data)

    def write_file(self, path):
        data = self.canvas.get_game_data()
        self.metadata["level"] = data["level"]
        self.metadata["correct"] = data["correct"]
        self.metadata["balls"] = data["balls"]

    def _ok_cb(self, button):
        self.canvas.end_turn()

    def _restart_cb(self, button):
        self.canvas.reset()
        self.label.set_text("")

    def _data_changed_cb(self, canvas, data):
        self.ok_button.set_sensitive(not BallType.NULL in data)

    def _win_cb(self, canvas):
        self.ok_button.set_sensitive(False)

        self.label.set_text("You win")

    def _lose_cb(self, canvas):
        self.ok_button.set_sensitive(False)

        self.label.set_text("You lost")
