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

from canvas import Canvas

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.toolbarbox import ToolbarBox

from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.activity import activity


class Mastermind(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.canvas = Canvas()
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
        toolbarbox.toolbar.insert(ActivityToolbarButton(self), -1)

        toolbarbox.toolbar.insert(make_separator(True), -1)

        stop_button = StopButton(self)
        toolbarbox.toolbar.insert(stop_button, -1)

        toolbarbox.toolbar.show_all()
        self.set_toolbar_box(toolbarbox)

    def _on_add_row(self, widget):
        self.canvas.add_row()
        self.update_label_size()
        self.label_sum.set_label("")

    def _on_add_column(self, widget):
        self.canvas.add_column()
        self.update_label_size()
        self.label_sum.set_label("")

    def _on_sum(self, widget):
        self.label_sum.set_label(str(sum(self.canvas.get_simple_value_list())))

    def update_label_size(self):
        size = tuple(self.canvas.get_size())
        self.label_size.set_label("Width: %d\nHeight: %d" % size)
