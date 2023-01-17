import datetime
from unittest import mock

import pytest
from discord import ChannelType
from discord.utils import get

from duckbot.cogs.wellness import Posture


async def test_before_loop_waits_for_bot(bot):
    clazz = Posture(bot)
    await clazz.before_loop()
    bot.wait_until_ready.assert_called()


async def test_cog_unload_cancels_task(bot):
    clazz = Posture(bot)
    clazz.cog_unload()
    clazz.on_hour_loop.cancel.assert_called()


@pytest.mark.parametrize("hour", [h for h in range(0, 24) if 10 > h or h >= 23])
@mock.patch("random.random", return_value=0.0)
@mock.patch("duckbot.cogs.wellness.posture.now")
async def test_posture_check_hour_not_in_range_probability_not_pass_no_send(bot, now, random, hour):
    now.return_value = datetime.datetime(2002, 1, 1, hour=hour)
    clazz = Posture(bot)
    await clazz.posture_check()
    bot.get_all_channels.assert_not_called()


@pytest.mark.parametrize("hour", [h for h in range(0, 24) if 10 > h or h >= 23])
@mock.patch("random.random", return_value=1.0)
@mock.patch("duckbot.cogs.wellness.posture.now")
async def test_posture_check_hour_not_in_range_probability_pass_no_send(bot, now, random, hour):
    now.return_value = datetime.datetime(2002, 1, 1, hour=hour)
    clazz = Posture(bot)
    await clazz.posture_check()
    bot.get_all_channels.assert_not_called()


@pytest.mark.parametrize("hour", [h for h in range(0, 24) if 10 <= h < 23])
@mock.patch("random.random", return_value=0.0)
@mock.patch("duckbot.cogs.wellness.posture.now")
async def test_posture_check_hour_in_range_probability_not_pass_no_send(bot, now, random, hour):
    now.return_value = datetime.datetime(2002, 1, 1, hour=hour)
    clazz = Posture(bot)
    await clazz.posture_check()
    bot.get_all_channels.assert_not_called()


@pytest.mark.parametrize("hour", [h for h in range(0, 24) if 10 <= h < 23])
@mock.patch("random.random", return_value=1.0)
@mock.patch("random.choice", return_value="Posture Check.")
@mock.patch("duckbot.cogs.wellness.posture.now")
async def test_posture_check_hour_in_range_probability_pass_send(bot, now, choice, random, hour):
    now.return_value = datetime.datetime(2002, 1, 1, hour=hour)
    clazz = Posture(bot)
    await clazz.posture_check()
    channel = get(bot.get_all_channels(), guild__name="Friends Chat", name="general", type=ChannelType.text)
    channel.send.assert_called_once_with("Posture Check.")


@pytest.mark.parametrize("hour", [h for h in range(0, 24) if 10 <= h < 18])
@mock.patch("random.random", return_value=1/6)
@mock.patch("random.choice", return_value="Posture Check.")
@mock.patch("duckbot.cogs.wellness.posture.now")
async def test_posture_check_hour_not_in_range_for_given_probability_no_send(bot, now, choice, random, hour):
    now.return_value = datetime.datetime(2002, 1, 1, hour=hour)
    clazz = Posture(bot)
    await clazz.posture_check()
    bot.get_all_channels.assert_not_called()


@pytest.mark.parametrize("hour", [h for h in range(0, 24) if 18 <= h < 23])
@mock.patch("random.random", return_value=1/6)
@mock.patch("random.choice", return_value="Posture Check.")
@mock.patch("duckbot.cogs.wellness.posture.now")
async def test_posture_check_hour_in_range_for_given_probability_send(bot, now, choice, random, hour):
    now.return_value = datetime.datetime(2002, 1, 1, hour=hour)
    clazz = Posture(bot)
    await clazz.posture_check()
    channel = get(bot.get_all_channels(), guild__name="Friends Chat", name="general", type=ChannelType.text)
    channel.send.assert_called_once_with("Posture Check.")


@pytest.mark.parametrize("p", [p for p in range(13, 0, -1) if 1/13 <= p < 18])
@mock.patch("random.random", return_value=1/6)
@mock.patch("random.choice", return_value="Posture Check.")
@mock.patch("duckbot.cogs.wellness.posture.now")
async def test_posture_check_probability_roll_not_in_range_for_given_hour_no_send(bot, now, choice, random, hour):
    now.return_value = datetime.datetime(2002, 1, 1, hour=hour)
    clazz = Posture(bot)
    await clazz.posture_check()
    bot.get_all_channels.assert_not_called()


## sweep prob
