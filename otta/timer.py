from __future__ import print_function
from datetime import datetime
import math
import time
import threading
from gi.repository import GObject
from otta.utils import RepeatTimer

STATE_STARTED = 'started'
STATE_STOPPED = 'stopped'
STATE_PAUSED  = 'paused'

class Timer(GObject.GObject):
    _time = 0
    config = None
    state = 'stopped'
    started_at = None
    stopped_at = None
    _time_started = None #internal one
    _time_stopped = None #internal one
    _timers = []

    __gsignals__ = {
        'start':         (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'started':       (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'stop':          (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'stopped':       (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'pause':         (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'paused':        (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        "second-signal": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (int,)), #Mhzzz....
        "minute-signal": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (int,))
    }

    def __init__(self, config):
        GObject.GObject.__init__(self)
        self.config = config

    def start(self):
        self.emit('start')
        if self.state == STATE_STARTED:
            return
        elif self.state == STATE_STOPPED:
            self._time = 0
            self.started_at = datetime.now()

        self.setup_repeat_timer()
        self._time_started = time.time()
        self.state = STATE_STARTED
        self.emit('started')

    def stop(self):
        self.emit('stop')
        if self.state == STATE_STOPPED: #already stopped, do nothing
            return
        elif self.state == STATE_STARTED:
            print('registering stopped time')
            self._time_stopped = time.time()
            self._time = self._time + (self._time_stopped - self._time_started)

        self.stopped_at = datetime.now()
        self.cancel_repeat_timer()
        self.state = STATE_STOPPED
        self.emit('stopped')

    def pause(self):
        self.emit('pause')
        if self.state != STATE_STARTED:
            return

        self.cancel_repeat_timer()
        self._time_stopped = time.time()
        self._time = self._time + (self._time_stopped - self._time_started)
        self.state = STATE_PAUSED
        self.emit('paused')

    def time(self):
        """Returns the rounded "raw" time"""
        if self.state != STATE_STARTED:
            return round(self._time)

        return round(self._time + (time.time() - self._time_started)) #round to the nearest second

    def round_time(self):
        """Returns rounded time.
        Depending on the configuration it is rounded down/nearest/up.
        Do not use this in the internal class: the return value is rounded."""
        time = self.time()
        units = time/(self.config.round_time*60)
        rounded_units = 0.0

        if self.config.round_method == 'down':
            rounded_units = math.floor(units)
        elif self.config.round_method == 'up':
            rounded_units = math.ceil(units)
        else:
            rounded_units = round(units)

        return int(rounded_units*(self.config.round_time*60))

    def emit_second_signal(self):
        """Emit the second signal on the main thread"""
        GObject.idle_add(self.emit, 'second-signal', self.time())
        return True

    def emit_minute_signal(self):
        """Emit the minute signal on the main thread"""
        GObject.idle_add(self.emit, 'minute-signal', self.time())
        return True

    def setup_repeat_timer(self):
        """If paused halfway, determine when the first emits()
        shoud take place and when the complete repeattimer should be started"""
        # time_to_next_second = 1-(self._time%1)
        time_to_next_minute = 60-(self._time%60)

        # second_timer = RepeatTimer(1.0, self.emit_second_signal)
        minute_timer = RepeatTimer(60.0, self.emit_minute_signal)

        # self._timers.append(threading.Timer(time_to_next_second, self.emit_second_signal))
        # self._timers.append(threading.Timer(time_to_next_second, second_timer.start))
        self._timers.append(threading.Timer(time_to_next_minute, self.emit_minute_signal))
        self._timers.append(threading.Timer(time_to_next_minute, minute_timer.start))

        for t in self._timers:
            t.start()

        # self._timers.append(second_timer)
        self._timers.append(minute_timer)

    def cancel_repeat_timer(self):
        for t in self._timers:
            t.cancel()
        self._timers = []
