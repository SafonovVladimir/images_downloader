from __future__ import annotations

import asyncio
import os
import time
from typing import TYPE_CHECKING

from device_tests.classes.Alarms.AlarmBuilders import Accelerometer, Alarm, Tamper
from device_tests.classes.Alarms.AlarmObject import AlarmObject
from device_tests.classes.MyEvents import EventStand
from device_tests.classes.Stands.ImpulseBtn.StandSirenFamily import StandSirenFamily
from device_tests.classes.TestEnv import TestEnv
from device_tests.funs.general_funs import clear_events

if TYPE_CHECKING:
    from device_tests.classes.Hub import Hub


class StandStreetSiren(StandSirenFamily):
    def __init__(self) -> None:
        """Ініціалізація об'єкта класу Stand
        """

        # TODO: Make this solution suck less
        # And probably make it work for all devices, which would render "dev_type" DB field useless.
        env = TestEnv()
        env.stand_configs["dev_type"] = "1b" if "DoubleDeck" in os.path.basename(env.firmware_file) else "14"

        events = {"LED": EventStand()}
        super().__init__(events)

        self.tamper = Tamper(led='SYS', alarm_ns_cmd={21: 4, 153: 3, 150: 0})
        self.ext = Alarm('ext', 'ExtPower', (0, 1), bistable=True, bistable_alarm_t=('lost', 'restored'))
        self.ext.set_passive_mode(True, False)
        self.move = Accelerometer(
            'move', values=(0, 3), settings='use_accel',
            alarm_ns_cmd={21: 4, 150: 3, 152: 3}, time_to_alarm=15,
        )

        self.blink_durations_sys |= {'DISCHARGED': 2750, 'ARMED_BLINK': 2, 'DELAY_BLINK': 50, 'NO_INIT': 320}
        self.beep_durations |= {'ARM_DISARM_BEEP': 20, 'CHIMES': 14}
        self.volume_durations = {
            "min": 160, "mid": 5200, "max": 29400, 'min_sys': 850, 'mid_sys': 1450,
            'max_sys': 28000,
        }
        self.blink_durations_led |= {'ALARM_BLINK': 120, 'POWER_OFF': 2000}  # 'ARM_DISARM_BLINK': 55,

        self.chimes = {'00': [15, 0], '01': [10, 0.155], '02': [7, 0.12], '03': [4, 0.1]}

        self.voltage_on = 33
        self.discharged_threshold = 24
        self.led_turn_on = 'LED'
        self.leds = ('LED', 'SYS')

        self.crutch_led_time = 0

    @property
    def main_alarm(self) -> AlarmObject:
        return self.move.next

    @property
    def standard_alarms(self) -> list[AlarmObject]:
        return self.tamper.bi

    @property
    def no_synchro_alarm_groups(self) -> tuple[list[AlarmObject], AlarmObject]:
        return self.tamper.bi, self.main_alarm

    def event_manager(self, line: str) -> None:
        if not any((self.events["LED"].on_times, self.events["SYS"].on_times, self.events["BEEP"].on_times)):
            self.t_sys = self.t_ext = self.t_led = self.beep_time = self.volume = 0
        super().event_manager(line)
        if "LED=ON" in line:
            self.events["LED"].set(1)
            [self.events[key].reset() for key in self.blink_durations.keys() | self.blink_durations_led.keys()]
            self.t_led = 0
            self.crutch_led_time = time.perf_counter()
        elif "LED=OFF" in line:
            self.events["LED"].set_event_info(line)
            self.t_led = self.events["LED"].duration[-1]
            if not self.t_led:
                self.t_led = round((1000 * (time.perf_counter() - self.crutch_led_time)), 2)
            self.events["LED"].set(0)
        elif "BEEP=ON" in line:
            self.events["BEEP"].set(1)
        elif "BEEP=OFF" in line:
            self.events["BEEP"].set_event_info(line)
            self.beep_time = self.events["BEEP"].duration[-1]
            self.volume = self.events["BEEP"].amplitude * 1000
            self.events["BEEP"].set(0)
            self.set_events(self.beep_durations, ('beep_time',))
            self.set_events(self.volume_durations, ('volume',))

        if self.t_led:
            if self.t_sys:
                self.set_events(self.blink_durations, ('t_led', 't_sys'))
            self.set_events(self.blink_durations_led, ('t_led',))
        elif self.t_sys:
            self.set_events(self.blink_durations_sys, ('t_sys',))

        # Debug print for set events
        # for key in self.blink_durations.keys() | self.beep_durations.keys() | self.volume_durations.keys() \
        #         | self.blink_durations_led.keys() | self.blink_durations_sys.keys():
        #     if self.events[key].is_set():
        #         print(f'\033[35;1m             {key=}   set   {self.events[key].is_set()} \033[00m')

    def set_events(self, ext_dict: dict, exp_values: tuple) -> None:
        super().set_events(ext_dict, exp_values)
        if self.events['DELAY_BLINK'].is_set() and self.events['ARM_DISARM_BLINK'].is_set():
            self.events['DELAY_BLINK'].reset()
            self.events['ARM_DISARM_BLINK'].reset()
            self.events['TURN_ON_OFF'].set()

    def check_events(
        self, wait_event: bool, blink: str = None, beep: str = None, system: bool = False,
        check_volume: bool = False, t: float = 5.0,
    ) -> list:
        events = super().check_events(wait_event, blink=blink, t=t)
        if beep:
            events.append(self.check_beep(beep, wait_event=wait_event, timeout=t))
            if wait_event and check_volume and not self.discharged and self.device.volume_alarm != 31:
                events.append(self.check_volume(system=system, wait_event=wait_event, timeout=t))
        return events

    async def check_leds(self, blink: str, wait_event: bool = True, timeout: float = 5.0) -> None:
        assert await self.events[blink].wait(timeout=timeout) is wait_event, \
            f'check_leds error {blink=} {wait_event=}, last leds = {self.t_sys, self.t_led}'

    async def check_alarm_beep(self, hub: Hub, alarm: bool = True, wait_alarm: bool = True, **kwargs) -> None:
        await self.blink_alarm_init(wait_alarm=wait_alarm, **kwargs)

    async def check_no_blink(self, on_timeout: int = 5, check_discharged: bool = False, **kwargs) -> None:
        await self.blink_alarm_init(wait_alarm=False, timeout=on_timeout, check_discharged=check_discharged, duration=3)

    async def blink_alarm_init(
            self,
            wait_alarm: bool = True,
            on_timeout: int = 3,
            duration: int = None,
            check_discharged: bool = False,
            **kwargs,
    ) -> None:
        silent = getattr(self.device, 'volume_alarm', 17) == 31 or not wait_alarm
        new_scale = getattr(self.device, 'NewScaleLength', 0)
        device_settings_duration = getattr(self.device, 'length_alarm', 1)
        device_settings_duration = device_settings_duration * 30 + 180 if new_scale else device_settings_duration * 3
        duration = duration or device_settings_duration
        self.beep_durations |= {'ALARM_BEEP': duration * 1000}
        clean_beep = getattr(
            self.device, 'volume_alarm', 17,
        ) not in (28, 17) and getattr(self.device, 'percent', 93) > 50
        led_duration_by_voltage = {
            100: 125, 93: 120, 87: 120, 75: 105, 68: 100, 62: 98, 56: 95, 50: 92, 44: 90,
            37: 82, 31: 75, 25: 62, 17: 60, 10: 60, 0: 55,
        }
        self.blink_durations_led['ALARM_BLINK'] = led_duration_by_voltage.get(getattr(self.device, 'percent', 93), 120)
        # Alarm blink duration is changed only after battery measurement, so we should think about another check

        await self.events['BEEP'].wait(1, timeout=0 if silent else on_timeout)  # check boozer is start scream

        await self.check_sys_led_conflict(on_timeout)
        await self.first_blink_start_time(wait_alarm, on_timeout)
        await self.main_check_alarm_blink(duration, wait_alarm, silent, clean_beep)
        if wait_alarm:
            self.sys_led_is_blinking_during_alarm()
        await self.check_beep_duration(duration, silent, clean_beep)
        await self.events['ALARM_BLINK'].wait(timeout=0.2)
        await clear_events(self)
        # await self.make_clear_events()
        tasks = self.check_events(wait_event=False, blink='ALARM_BLINK', t=1)
        if check_discharged:
            tasks.append(self.check_discharged())
        await asyncio.gather(*tasks)

    # Check sys is not conflicted with led
    async def check_sys_led_conflict(self, on_timeout: int) -> None:
        if self.events['SYS'].on.is_set() and not self.events['SYS'].off.is_set():
            await self.events['SYS'].wait(0, timeout=on_timeout)
            assert not self.events['LED'].on.is_set()
            await clear_events(self)

    # First blink to start time
    async def first_blink_start_time(self, wait_alarm: bool, on_timeout: int) -> None:
        await self.check_leds('ALARM_BLINK', wait_event=wait_alarm, timeout=on_timeout if wait_alarm else 0)
        await clear_events(self)

    async def main_check_alarm_blink(self, duration: int, wait_alarm: bool, silent: bool, clean_beep: bool) -> None:
        ttime = time.perf_counter()
        while time.perf_counter() - ttime < duration * 0.9:
            await asyncio.gather(
                self.check_leds('ALARM_BLINK', wait_event=wait_alarm, timeout=0.75),
                self.beep_alarm_indication(
                    wait_event=(wait_alarm and (not silent) and (not clean_beep)), duration=duration * 0.9,
                ),
            )

    def sys_led_is_blinking_during_alarm(self) -> None:
        assert True not in self.events['SYS'].is_set(), 'Сирена отмигивала системным светиком во время тревоги'

    async def check_beep_duration(self, duration: int, silent: bool, clean_beep: bool) -> None:
        if silent:
            assert not await self.events['ALARM_BEEP'].wait(timeout=duration * 0.11), \
                'Siren screams when sound disabled'
            assert True not in self.events['BEEP'].is_set(), 'Siren screams when sound disabled'
        else:
            if clean_beep:
                assert await self.events['ALARM_BEEP'].wait(timeout=duration * 0.15), \
                    f'Alarm Beep error: last beep = {self.beep_time}, exp = {self.beep_durations["ALARM_BEEP"]}'
            else:
                await asyncio.sleep(duration * 0.11)

    async def beep_alarm_indication(self, wait_event: bool, duration: float) -> None:
        if wait_event and duration:
            self.events['BEEP'].reset()
            strt = time.perf_counter()
            while time.perf_counter() < strt + duration:
                assert await self.events['BEEP'].wait(state=1, timeout=0.3), 'beep ON error'
                self.events['BEEP'].reset()
                assert await self.events['BEEP'].wait(state=0, timeout=0.5), 'beep OFF error'

    async def check_infinite_beep(
            self, step: int = None, duration: float = None,
            wait_event: bool = True,
    ) -> None:
        time_now = time.perf_counter()
        timing = {1: [1, 29], 2: [3, 58], 3: [10, 116], 4: [30, 232], 5: [900, 1750]}
        timeout = timing[step][0]
        duration = duration or timing[step][1]
        await self.check_beep('INFINITE', timeout=timing[step][0] + 3, wait_event=wait_event)
        self.events['INFINITE'].set()
        while time.perf_counter() < time_now + duration * 0.9:
            for _ in range(3):
                await self.check_beep('INFINITE', timeout=timeout, wait_event=wait_event)
        await asyncio.sleep(duration * 0.05)

    async def check_armed_indication(self, arm: bool = True, duration: int = 30, timeout: float = 4.0) -> None:
        self.t_led = self.t_sys = 0
        self.events['ARMED_BLINK'].reset()
        wait_event = self.device.led_show_protect == 2 or (arm and self.device.led_show_protect == 1)
        ttime = time.perf_counter()
        while time.perf_counter() - ttime < duration:
            if not self.device.ext_power_off and wait_event:
                assert await self.events['SYS'].wait(1, timeout=timeout), 'SYS не засвітився з підключеним живленням'
                self.events['SYS'].on.set()  # потрібно для подальшого відслідковування свєтіка
                self.events['SYS'].off.clear()
                assert not await self.events['SYS'].wait(0, timeout=duration), 'SYS потух при підключеному живленні'
            else:
                await self.check_leds(
                    'ARMED_BLINK',
                    wait_event=wait_event,
                    timeout=timeout,
                )

    async def check_discharged(self, wait_event: bool = True, timeout: int = 15) -> None:
        await self.check_leds(
            'DISCHARGED',
            wait_event=wait_event,
            timeout=timeout,
        )
