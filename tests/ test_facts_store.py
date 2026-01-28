def test_save_and_get_facts(memory_store):
    user_id = 123
    facts = {
        "age": "Użytkownik ma 22 lata."
    }
    memory_store.save_facts(user_id, facts)
    loaded = memory_store.get_facts(user_id)
    assert loaded == facts


def test_fact_deduplication(memory_store):
    user_id = 1
    memory_store.save_facts(user_id, {
        "age": "Użytkownik ma 22 lata."
    })
    memory_store.save_facts(user_id, {
        "age": "Użytkownik ma 23 lata."
    })
    facts = memory_store.get_facts(user_id)
    assert len(facts) == 1
    assert facts["age"] == "Użytkownik ma 23 lata."


def test_reset_user_facts(memory_store):
    user_id = 42
    memory_store.save_facts(user_id, {
        "age": "Użytkownik ma 30 lat."
    })
    memory_store.reset_user(user_id)
    facts = memory_store.get_facts(user_id)
    assert facts == {}
