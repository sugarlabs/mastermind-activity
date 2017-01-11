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

from gettext import gettext as _

from canvas import Canvas
from constants import BallType

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
        self.restart_button.connect("clicked", self._restart_cb)
        toolbar.insert(self.restart_button, -1)

        self.ok_button = ToolButton(icon_name="dialog-ok")
        self.ok_button.set_tooltip(_("Ok"))
        self.ok_button.set_sensitive(False)
        self.ok_button.connect("clicked", self._ok_cb)
        toolbar.insert(self.ok_button, -1)

        item = Gtk.ToolItem()
        toolbar.insert(item, -1)

        self.label = Gtk.Label()
        self.label.modify_font(Pango.FontDescription("Bold"))
        item.add(self.label)

        toolbar.insert(make_separator(True), -1)

        stop_button = StopButton(self)
        toolbar.insert(stop_button, -1)

        toolbar.show_all()

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
