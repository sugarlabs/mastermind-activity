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

from ball_box import BallBox

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class OriginBox(Gtk.Grid):

    def __init__(self):
        Gtk.Grid.__init__(self)

        self.balls = []

        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_column_spacing(5)

        self.show_all()

    def clear(self):
        while self.balls != []:
            ball = balls[0]
            self.remove(ball)
            self.balls.remove(ball)

            del ball

    def reset(self):
        self.clear()

        for x in range(0, 8):
            ball = BallBox.new_from_id(x)
            ball.set_draggable(True)
            self.attach(ball, x, 0, 1, 1)

            self.balls.append(ball)
