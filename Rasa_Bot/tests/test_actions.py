"""Unit tests for the custom actions"""
import pytest
from unittest import mock
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from Rasa_Bot.tests.conftest import EMPTY_TRACKER

from Rasa_Bot.actions import actions


# NB: This is just an example test. The custom action tested here
# is currently just a placeholder function. Update once the
# function tested here works correctly.
@pytest.mark.asyncio
async def test_run_action_save_plan_week_calendar(
        dispatcher: CollectingDispatcher, domain: DomainDict):
    tracker = EMPTY_TRACKER
    action = actions.SavePlanWeekCalendar()
    events = await action.run(dispatcher, tracker, domain)
    expected_events = [
        SlotSet("success_save_calendar_plan_week", True),
    ]
    assert events == expected_events


@pytest.mark.asyncio
@mock.patch("Rasa_Bot.actions.actions.get_db_session")
async def test_run_action_store_pa_evaluation(
        mock_get_db_session, dispatcher: CollectingDispatcher, domain: DomainDict):
    mock_result = mock.MagicMock(name="mock_result")
    mock_session = mock_get_db_session.return_value
    mock_session.query.return_value.filter_by.return_value \
        .one.return_value = mock_result
    tracker = EMPTY_TRACKER
    test_evaluation_response = 3
    tracker.slots['pa_evaluation_response'] = test_evaluation_response
    action = actions.ActionStorePaEvaluation()
    events = await action.run(dispatcher, tracker, domain)
    expected_events = [SlotSet("pa_evaluation_response", None)]
    assert events == expected_events
    mock_session.commit.assert_called_once()
