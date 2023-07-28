
import pytest
from pytest_testrail.plugin import pytestrail

from device_tests.funs.general_funs import clear_events
from device_tests.funs.settings_funs import arm_hub, disarm_hub, perimetral_arm_hub


@pytestrail.case("C1433865")
@pytest.mark.KeyPadTouchScreen
@pytest.mark.core
@pytest.mark.ui
async def test_state_protect_indication(preparing_kpt_with_registration):
    stand, hub, scanner = preparing_kpt_with_registration

    # ==================================================== Step_1 ======================================================
    stand.print_step(1)
    await clear_events(stand)
    assert not await stand.events[stand.led_system].wait(True, timeout=stand.kpt.time_shutdown_screen), \
        'KPT turned on LED'

    # ==================================================== Step_2 ======================================================
    stand.print_step(2)

    await stand.settings.set_and_check(hub, stand.settings.indicationConfig(0x735))  # Led mode: armed
    await arm_hub(stand.env.hub.id)
    await stand.wait_shutdown_screen()
    await stand.arm_indication()

    # ==================================================== Step_3 ======================================================
    stand.print_step(3)

    await disarm_hub(stand.env.hub.id)
    await stand.wait_shutdown_screen()
    await clear_events(stand)
    await stand.check_no_led_indication()

    # ==================================================== Step_4 ======================================================
    stand.print_step(4)

    await stand.settings.set_and_check(hub, stand.settings.indicationConfig(0x755))  # Led mode: always
    await stand.wait_shutdown_screen()
    await clear_events(stand)
    await stand.arm_indication()

    # ==================================================== Step_5 ======================================================
    stand.print_step(5)

    await stand.external_power_on()
    await stand.wait_shutdown_screen()
    assert stand.events[stand.led_system].on.is_set(), 'KPT did not turn on the LED'
    await clear_events(stand)
    await stand.check_led_indication_ext_power()

    # ==================================================== Step_6 ======================================================
    stand.print_step(6)

    await stand.settings.set_and_check(hub, stand.settings.indicationConfig(0x735))  # Led mode: armed
    await arm_hub(stand.env.hub.id)
    await stand.wait_shutdown_screen()
    await clear_events(stand)
    await stand.check_led_indication_ext_power()

    # ==================================================== Step_7 ======================================================
    stand.print_step(7)

    await disarm_hub(stand.env.hub.id)
    await stand.wait_shutdown_screen()
    await clear_events(stand)
    await stand.check_no_led_indication()

    # ==================================================== Step_8 ======================================================
    stand.print_step(8)

    await stand.settings.set_and_check(hub, stand.settings.indicationConfig(0x715))  # Led mode: off
    await clear_events(stand)
    await stand.check_no_led_indication()

    # ==================================================== Step_9 ======================================================
    stand.print_step(9)

    await stand.settings.set_and_check(hub, stand.settings.indicationConfig(0x735))  # Led mode: armed
    await perimetral_arm_hub(stand.env.hub.id)
    await stand.wait_shutdown_screen()
    await stand.arm_indication()

    # # ==================================================== Step_10 =====================================================
    # stand.print_step(10)
    #
    # await stand.external_power_on()
    # await perimetral_arm_hub(stand.env.hub.id)
    # await stand.wait_shutdown_screen()
    # assert stand.events[stand.led_system].on.is_set(), 'KPT did not turn on the LED'
    # await clear_events(stand)
    # await stand.check_led_indication_ext_power()
    #
    # # ==================================================== Step_11 =====================================================
    # stand.print_step(11)
    #
    # await stand.settings.set_and_check(hub, stand.settings.indicationConfig(0x735))  # Led mode: armed
    # await perimetral_arm_hub(stand.env.hub.id)
    # await stand.wait_shutdown_screen()
    # await stand.arm_indication()
    #
    # # ==================================================== Step_12 =====================================================
    # stand.print_step(12)
    #
    # await stand.external_power_on()
    # await perimetral_arm_hub(stand.env.hub.id)
    # await stand.wait_shutdown_screen()
    # assert stand.events[stand.led_system].on.is_set(), 'KPT did not turn on the LED'
    # await clear_events(stand)
    # await stand.check_led_indication_ext_power()
