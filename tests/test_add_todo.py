import logging

logger = logging.getLogger(__name__)

def test_save_and_get_todo(memory_store, caplog):
    user_id = 123
    item = "chleb i mleko"

    with caplog.at_level(logging.INFO):
        added = memory_store.add_todo(user_id, item)
        logger.info(f"add_todo returned: {added}")

        loaded = memory_store.get_todo(user_id)
        logger.info(f"get_todo returned: {loaded}")

    print(caplog.text)
    assert loaded == [item]