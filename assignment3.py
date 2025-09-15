import argparse
import urllib.request
import csv
import re
from collections import Counter
from datetime import datetime

def fetch_data(url):
    try:
        result = urllib.request.urlopen(url)
        text = result.read().decode('utf-8')
        return text.split('\n')
    except Exception as ex:
        print("Download error:", ex)
        return []

def parse_csv(lines):
    records = []
    reader = csv.reader(lines)
    for item in reader:
        records.append(item)
    return records

def image_request_percentage(records):
    pattern = re.compile(r'.*\.(jpg|jpeg|gif|png)$', re.IGNORECASE)
    total = 0
    image_hits = 0

    for r in records:
        if len(r) < 1:
            continue
        total += 1
        if pattern.match(r[0]):
            image_hits += 1

    if total == 0:
        print("No data to analyze.")
        return

    result = (image_hits / total) * 100
    print("Image requests account for {:.1f}% of all requests".format(result))

def most_common_browser(records):
    counters = Counter()

    for r in records:
        if len(r) < 3:
            continue
        agent = r[2]

        if "Chrome" in agent and "Safari" in agent:
            counters["Chrome"] += 1
        elif "Safari" in agent and "Chrome" not in agent:
            counters["Safari"] += 1
        elif "Firefox" in agent:
            counters["Firefox"] += 1
        elif "MSIE" in agent or "Trident" in agent:
            counters["Internet Explorer"] += 1

    if counters:
        top_browser = counters.most_common(1)[0]
        print("The most popular browser is", top_browser[0])

def request_distribution_by_hour(records):
    hourly = Counter()

    for r in records:
        if len(r) < 2:
            continue

        dt = None
        try:
            dt = datetime.strptime(r[1], "%Y-%m-%d %H:%M:%S")
        except:
            try:
                dt = datetime.strptime(r[1], "%m/%d/%Y %H:%M:%S")
            except:
                continue

        hour = dt.hour
        hourly[hour] += 1

    for h in range(24):
        count = hourly[h]
        print("Hour {:02d} has {} hits".format(h, count))

def run(url):
    print("Running analysis on:", url)
    lines = fetch_data(url)
    if not lines:
        return

    data = parse_csv(lines)
    image_request_percentage(data)
    most_common_browser(data)
    request_distribution_by_hour(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    args = parser.parse_args()
    run(args.url)
