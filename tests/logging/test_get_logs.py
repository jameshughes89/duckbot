import os
from unittest import mock

import pytest

from duckbot.logging import GetLogs


@pytest.mark.asyncio
@mock.patch("discord.File")
@mock.patch("tarfile.open")
@mock.patch("tarfile.TarFile")
async def test_get_logs_sends_tarball_of_logs(tar, open, file, bot, context):
    open.return_value = tar
    tar.add = mock.MagicMock()
    mock_file_id = file.return_value

    clazz = GetLogs(bot)
    await clazz._GetLogs__logs(context)

    open.assert_called_once_with(os.path.join(".", "logs.tar.gz"), "w:gz")
    tar.add.assert_called_once_with(os.path.join(".", "logs"))
    tar.close.assert_called_once()
    file.assert_called_once_with(os.path.join(".", "logs.tar.gz"), "logs.tar.gz")
    context.send.assert_called_once()
    assert context.send.call_args.kwargs["file"] == mock_file_id
