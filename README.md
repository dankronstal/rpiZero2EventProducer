# Raspberry Pi Zero 2 Event Producer

## Setup & Install

1. Grab the code from this repo:
```
git clone https://github.com/dankronstal/rpiZero2EventProducer.git
```

2. Create virtual environment and pull down dependencies:
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Create .env file for secrets, based on provided template, and update values:
```
cp .env.template .env
nano .env
```

4. Run program:
```
python main.py
```

5. (Optional) Install as service so it starts when the device boots...


## Output should look something like:
Oct 08 16:01:46 raspberrypi python[613]: [2025-10-08 22:01:46.810473] Sent batch: [{'tagName': 'extractor_01', 'tagValue': 5.69, 'tagTimestamp': 1759960906}, {'tagName': 'extractor_02', 'tagValue': 0.0, 'tagTimestamp': 1759960906}, {'tagName': 'extractor_03', 'tagValue': 0.32, 'tagTimestamp': 1759960906}, {'tagName': 'pump_01', 'tagValue': 15.5, 'tagTimestamp': 1759960906}, {'tagName': 'compressor_01', 'tagValue': 1.24, 'tagTimestamp': 1759960906}, {'tagName': 'conveyor_01', 'tagValue': 0.72, 'tagTimestamp': 1759960906}, {'tagName': 'processor_01', 'tagValue': 5.69, 'tagTimestamp': 1759960906}]