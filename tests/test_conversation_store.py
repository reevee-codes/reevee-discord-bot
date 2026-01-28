def test_save_and_get_conversation(memory_store):
    user_id = 1
    messages = [
        {"role": "user", "content": "hej"},
        {"role": "assistant", "content": "cześć"}
    ]
    memory_store.save_conversation(user_id, messages)
    loaded = memory_store.get_conversation(user_id)
    assert loaded == messages

def test_conversation_order(memory_store):
    user_id = 2
    messages = [
        {"role": "user", "content": "1"},
        {"role": "assistant", "content": "2"},
        {"role": "user", "content": "3"},
    ]
    memory_store.save_conversation(user_id, messages)
    loaded = memory_store.get_conversation(user_id)
    assert [m["content"] for m in loaded] == ["1", "2", "3"]

def test_conversation_limit(memory_store):
    user_id = 3
    messages = [
        {"role": "user", "content": str(i)}
        for i in range(20)
    ]
    memory_store.save_conversation(user_id, messages)
    loaded = memory_store.get_conversation(user_id, limit=5)
    assert len(loaded) == 5
    assert loaded[0]["content"] == "15"
