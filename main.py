import time
import random
import json
import datetime
import os
from azure.eventhub import EventHubProducerClient, EventData
from dotenv import load_dotenv

load_dotenv()

EVENT_HUB_CONNECTION_STRING = os.getenv("EVENT_HUB_CONNECTION_STRING")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")

if not EVENT_HUB_CONNECTION_STRING or not EVENT_HUB_NAME:
    raise ValueError("Event Hub connection details are missing. Check your .env file.")

# Tag configuration: initial value, max value, % change limit, momentum bias
TAGS = {
    "extractor_01": {"value": 0.0, "max": 100.0, "change_pct": 0.25, "min_change_base": 1.0, "trend": 1, "trend_strength": 0.7},
    "extractor_02": {"value": 0.0, "max": 100.0, "change_pct": 0.25, "min_change_base": 1.0, "trend": 1, "trend_strength": 0.7},
    "extractor_03": {"value": 0.0, "max": 100.0, "change_pct": 0.25, "min_change_base": 1.0, "trend": 1, "trend_strength": 0.7},
    "pump_01": {"value": 50.0, "max": 100.0, "change_pct": 0.15, "min_change_base": 1.0, "trend": 1, "trend_strength": 0.6},
    "compressor_01": {"value": 5.0, "max": 10.0, "change_pct": 0.35, "min_change_base": 0.1, "trend": 1, "trend_strength": 0.5},
    "conveyor_01": {"value": 0.0, "max": 1000.0, "change_pct": 0.05, "min_change_base": 5.0, "trend": 1, "trend_strength": 0.8},
    "processor_01": {"value": 10.0, "max": 100.0, "change_pct": 0.15, "min_change_base": 1.0, "trend": 1, "trend_strength": 0.6},
    "packager_01": {"value": 0.1, "max": 1.0, "change_pct": 0.05, "min_change_base": 0.1, "trend": 1, "trend_strength": 0.5},
}

EXTRACTOR_TAGS = ["extractor_01", "extractor_02", "extractor_03"]
OTHER_TAGS = ["pump_01", "compressor_01", "conveyor_01", "processor_01", "packager_01"]

producer = EventHubProducerClient.from_connection_string(
    conn_str=EVENT_HUB_CONNECTION_STRING,
    eventhub_name=EVENT_HUB_NAME
)

def update_tag_value(tag_name):
    tag_info = TAGS[tag_name]
    current_value = tag_info["value"]
    base_for_change = max(current_value, tag_info["min_change_base"])
    change_range = tag_info["change_pct"] * base_for_change

    if random.random() < tag_info["trend_strength"]:
        direction = tag_info["trend"]
    else:
        direction = random.choice([-1, 1])

    if random.random() < 0.1:
        tag_info["trend"] = -tag_info["trend"]

    change = direction * random.uniform(0, change_range)
    new_value = current_value + change

    if new_value < 0:
        new_value = 0.0
        tag_info["trend"] = 1
    elif new_value > tag_info["max"]:
        new_value = tag_info["max"]
        tag_info["trend"] = -1

    tag_info["value"] = round(new_value, 2)
    return tag_info["value"]

def create_event(tag_name):
    return {
        "tagName": tag_name,
        "tagValue": update_tag_value(tag_name),
        "tagTimestamp": int(time.time())
    }

def send_batch(events):
    try:
        event_data_batch = producer.create_batch()
        for payload in events:
            event_data_batch.add(EventData(json.dumps(payload)))
        producer.send_batch(event_data_batch)
        print(f"[{datetime.datetime.utcnow()}] Sent batch: {events}")
    except Exception as e:
        print(f"Error sending batch: {e}")

if __name__ == "__main__":
    print("Starting batched event generation with momentum...")
    last_other_tag_time = time.time()

    while True:
        batch_events = [create_event(tag) for tag in EXTRACTOR_TAGS]

        now = time.time()
        if now - last_other_tag_time >= 5:
            for tag in OTHER_TAGS:
                if random.random() <= 0.35:
                    batch_events.append(create_event(tag))
            last_other_tag_time = now

        send_batch(batch_events)
        time.sleep(1)
