import pytest
from pytest_testrail.plugin import pytestrail
from qaauto_tools.classes.Payload import ParseBytes

from device_tests.classes.Errors import WrongPayload, BlinkError
from device_tests.funs.settings_funs import wait_for_flag
from device_tests.utils.general import assert_custom_exc


@pytest.fixture()
async def preparing_kpt(preparing_without_registration, scanner):
    stand, hub = preparing_without_registration
    await stand.tamper_off()
    yield [stand, hub, scanner]


@pytestrail.case('C1438240')
@pytest.mark.KeyPadTouchScreen
@pytest.mark.smoke
@pytest.mark.jwl
async def test_tamper(preparing_kpt):
    stand, hub, scanner = preparing_kpt

    # ============================================= Step_1 ===========================================================
    stand.print_step(1)

    await stand.register_device()

    # ============================================= Step_2 ===========================================================
    stand.print_step(2)

    await wait_for_flag(stand, hub, timeout=hub.env.frame * 5, Tamper=True)

    # ============================================= Step_3 ===========================================================
    stand.print_step(3)

    assert_custom_exc(WrongPayload, ParseBytes(hub.events[30].payload).check_bits(1, (0,)), "Tamper is closed")

    # ============================================= Step_4 ==========================================================
    stand.print_step(4)

    await stand.tamper_on()
    await wait_for_flag(stand, hub, timeout=hub.env.frame * 5, Tamper=False)
    assert_custom_exc(BlinkError, stand.events[stand.led_on].on.is_set(), f"KPT did not turn on {stand.led_on}")

    # ============================================= Step_5 ==========================================================
    stand.print_step(5)

    await stand.tamper_off()
    await wait_for_flag(stand, hub, timeout=hub.env.frame * 5, Tamper=True)
    assert_custom_exc(BlinkError, stand.events[stand.led_on].on.is_set(), f"KPT did not turn on {stand.led_on}")
