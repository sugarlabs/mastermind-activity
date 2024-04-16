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

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk

from sugar3.graphics.toolbutton import ToolButton


class HelpButton(Gtk.ToolItem):

    def __init__(self, **kwargs):
        Gtk.ToolItem.__init__(self)

        help_button = ToolButton("toolbar-help")
        help_button.set_tooltip(_("Help"))
        self.add(help_button)

        self._palette = help_button.get_palette()

        sw = Gtk.ScrolledWindow()
        sw.set_size_request(int(Gdk.Screen.width() / 2.8), 310)
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self._max_text_width = int(Gdk.Screen.width() / 3) - 600
        self._vbox = Gtk.Box()
        self._vbox.set_orientation(Gtk.Orientation.VERTICAL)
        self._vbox.set_homogeneous(False)
        self._vbox.set_border_width(10)

        hbox = Gtk.Box()
        hbox.pack_start(self._vbox, False, True, 0)

        sw.add_with_viewport(hbox)

        self._palette.set_content(sw)
        sw.show_all()

        help_button.connect("clicked", self.__help_button_clicked_cb)

    def __help_button_clicked_cb(self, button):
        self._palette.popup(immediate=True)

    def add_section(self, section_text):
        hbox = Gtk.Box()
        label = Gtk.Label()
        label.set_use_markup(True)
        label.set_markup("<b>%s</b>" % section_text)
        label.set_line_wrap(True)
        hbox.pack_start(label, False, False, 0)
        hbox.show_all()
        self._vbox.pack_start(hbox, False, False, padding=5)

    def add_paragraph(self, text, image=None):
        hbox = Gtk.Box()

        if image is not None:
            _image = Gtk.Image.new_from_file("images/" + image)
            hbox.pack_start(_image, False, False, 5)

        label = Gtk.Label(label=text)
        label.set_justify(Gtk.Justification.LEFT)
        label.set_line_wrap(True)
        hbox.pack_start(label, False, False, 0)

        hbox.show_all()
        self._vbox.pack_start(hbox, False, False, padding=5)
