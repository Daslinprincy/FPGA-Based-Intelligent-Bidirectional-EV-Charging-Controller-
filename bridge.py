import asyncio
import websockets
import json
import random
import time

SERVEO_URL = "wss://cf88bd2d77b5b1eb-117-215-113-166.serveousercontent.com/ev-controller"

async def simulate_ev():
    soc = 85.0
    soh = 91.4
    voltage = 59.4
    current = -18.3
    temp = 34.0
    cycles = 847

    async with websockets.connect(SERVEO_URL) as ws:
        print("✅ Connected to OCPP Central System via Serveo!")
        while True:
            # Simulate small changes
            soc = max(0, min(100, soc + random.uniform(-0.3, 0.1)))
            voltage = round(voltage + random.uniform(-0.2, 0.2), 1)
            current = round(current + random.uniform(-0.5, 0.5), 1)
            temp = round(temp + random.uniform(-0.1, 0.2), 1)

            msg = [2, "meter-001", "MeterValues", {
                "connectorId": 1,
                "meterValue": [{
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "sampledValue": [
                        {"measurand": "SoC", "value": str(round(soc, 1))},
                        {"measurand": "Voltage", "value": str(voltage)},
                        {"measurand": "Current.Import", "value": str(current)},
                        {"measurand": "Temperature", "value": str(temp)},
                        {"measurand": "EnergyActiveNet", "value": str(round(soh, 1))}
                    ]
                }]
            }]

            await ws.send(json.dumps(msg))
            print(f"📤 Sent: SoC={round(soc,1)}% V={voltage}V I={current}A T={temp}°C")
            await asyncio.sleep(2)

asyncio.run(simulate_ev())