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

from constants import BallType
from constants import BALL_SIZE
from constants import DRAG_ACTION
from constants import DRAG_TARGETS
from constants import IGNORE_TARGETS

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk


class BallBox(Gtk.EventBox):

    def __init__(self, change_background=True):
        Gtk.EventBox.__init__(self)

        self.draggable = False
        self.drag_dest = False
        self.ball = None
        self.image = None

        self.__drag_dest_id = None

        if change_background:
            self.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(1000, 1000, 1000))

        self.make_image()
        self.connect("drag-data-get", self.__get_drag_data)

    @classmethod
    def new_from_id(self, ballid, change_background=True):
        ball = BallBox(change_background)
        ball.set_ball(ballid)

        return ball

    def __get_drag_data(self, widget, drag_context, data, info, time):
        data.set_text(str(self.ball), -1)

    def __drag_data_received(self, drag_cotext, x, y, data, info, time):
        print "DATA RECEIVED", x, y, data

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
                self.drag_source_set_icon_pixbuf(make_ball_pixbuf(self.ball))
            else:
                self.drag_source_set_icon_pixbuf(make_ball_pixbuf(BallType.NULL))

        else:
            self.drag_source_set(Gdk.ModifierType.BUTTON5_MASK, IGNORE_TARGETS, DRAG_ACTION)

    def set_dest_drag(self, dest):
        if dest == self.drag_dest:
            return

        self.drag_dest = dest

        if self.__drag_dest_id is not None:
            self.disconnect(self.__drag_dest_id)

        if self.drag_dest:
            self.drag_dest_set(Gtk.DestDefaults.ALL, DRAG_TARGETS, DRAG_ACTION)

        else:
            self.drag_dest_set(Gtk.DestDefaults.ALL, IGNORE_TARGETS, DRAG_ACTION)

        self.__drag_dest_id = self.connect("drag-data-received", self.__drag_data_received)

    def make_image(self):
        if self.image is not None:
            self.remove(self.image)
            del self.image

        if self.ball is None:
            self.image = Gtk.Image()
            self.image.set_size_request(BALL_SIZE, BALL_SIZE)

        else:
            self.image = get_ball_image(self.ball)

        self.add(self.image)
        self.image.show()
