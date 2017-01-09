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

import os
import random

from constants import BallType

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import GdkPixbuf


def get_ball_name(ballid):
    if ballid == BallType.NULL:
        return "ball-white"

    elif ballid == BallType.RED:
        return "ball-red"

    elif ballid == BallType.GREEN:
        return "ball-green"

    elif ballid == BallType.SKYBLUE:
        return "ball-skyblue"

    elif ballid == BallType.BROWN:
        return "ball-brown"

    elif ballid == BallType.PURPLE:
        return "ball-purple"

    elif ballid == BallType.PINK:
        return "ball-pink"

    elif ballid == BallType.BLUE:
        return "ball-blue"

    elif ballid == BallType.YELLOW:
        return "ball-yellow"


def get_ball_image_path(ballid):
    name = get_ball_name(ballid)
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons", name + ".svg")



def make_ball_pixbuf(ballid, small=True):
    path = get_ball_image_path(ballid)
    if small:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(path, 24, 24)
    else:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(path, 44, 44)

    return pixbuf


def get_ball_image(ballid, small=True):
    pixbuf = make_ball_pixbuf(ballid, small)
    return Gtk.Image.new_from_pixbuf(pixbuf)


def get_random_ball():
    return random.choice([BallType.RED, BallType.GREEN, BallType.SKYBLUE, BallType.BROWN, BallType.PURPLE, BallType.PINK, BallType.BLUE, BallType.YELLOW])
