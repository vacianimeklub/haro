# coding: utf-8

from mock import Mock, patch

from handlers.command_handlers import get_vote_entries, toggle_vote_entry_text
from handlers.const import ACTIVE_ENTRY_TEXT_SUFFIX

class TestGetVoteEntries(object):
    def test_not_active(self):
        entries = {'a': 'one', 'b': 'two'}

        with patch('handlers.command_handlers.DUMMY_VOTE_ENTRIES', entries):
            result_entries = get_vote_entries()

        assert entries == result_entries

    def test_single_active(self):
        entries = {'a': 'one', 'b': 'two'}
        expected_entries = {'a': 'one ✅', 'b': 'two'}

        with patch('handlers.command_handlers.DUMMY_VOTE_ENTRIES', entries):
            result_entries = get_vote_entries(['a'])

        assert expected_entries == result_entries
    
    def test_multiple_active(self):
        entries = {'a': 'one', 'b': 'two'}
        expected_entries = {'a': 'one ✅', 'b': 'two ✅'}

        with patch('handlers.command_handlers.DUMMY_VOTE_ENTRIES', entries):
            result_entries = get_vote_entries(['a', 'b'])

        assert expected_entries == result_entries

    def test_active_on_nonexisting_key(self):
        entries = {'a': 'one', 'b': 'two'}

        with patch('handlers.command_handlers.DUMMY_VOTE_ENTRIES', entries):
            result_entries = get_vote_entries(['c'])

        assert entries == result_entries


class TestToggleVoteEntry(object):
    def test_activate(self):
        result = toggle_vote_entry_text('x')

        assert result == 'x{suffix}'.format(suffix=ACTIVE_ENTRY_TEXT_SUFFIX)

    def test_deactivate(self):
        result = toggle_vote_entry_text('x{suffix}'.format(suffix=ACTIVE_ENTRY_TEXT_SUFFIX))

        assert result == 'x'