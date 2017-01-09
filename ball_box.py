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

from utils import get_random_ball
from utils import make_ball_pixbuf
from utils import get_ball_image

from constants import DRAG_ACTION
from constants import DRAG_TARGETS

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk


class BallBox(Gtk.EventBox):

    def __init__(self):
        Gtk.EventBox.__init__(self)

        self.draggable = False
        self.drag_dest = False
        self.ball = None
        self.image = None

        self.make_image()

    @classmethod
    def new_from_id(self, ballid):
        ball = BallBox()
        ball.set_ball(ballid)

        return ball

    def __drag_data_received(self, widget, drag_context, data, info, time):
        print data
        # data.set_text(self.word, -1)

    def set_ball(self, ballid):
        self.ball = ballid
        self.make_image()

    def set_draggable(self, draggable):
        if draggable == self.draggable:
            return

        self.draggable = draggable
        if self.draggable:
            self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, DRAG_TARGETS, DRAG_ACTION)

            if self.ball is not None:
                self.drag_source_set_icon_pixbuf(make_ball_pixbuf(self.ball, False))
            else:
                self.drag_source_set_icon_pixbuf(make_ball_pixbuf(-1, False))

        else:  # TODO: how I remove this?
            pass

    def set_dest_drag(self, dest):
        if dest == self.drag_dest:
            return

        if self.drag_dest:
            self.drag_dest_set(Gtk.DestDefaults.ALL, DRAG_TARGETS, DRAG_ACTION)
            self.connect("drag-data-received", self.__drag_data_received)

        else:  # TODO: How I remove this?
            pass

    def make_image(self):
        if self.image is not None:
            self.remove(self.image)
            del self.image

        if self.ball is None:
            self.image = Gtk.Image()
            self.image.set_size_request(24, 24)

        else:
            self.image = get_ball_image(self.ball)

        self.add(self.image)
        self.image.show()
