import os
from sys import path

import requests
from bs4 import BeautifulSoup

path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from newscrape_common import (is_string, ist_to_utc, remove_duplicate_entries,
                              str_is_set)





def get_headline_details(obj):
    try:
        from datetime import datetime
        timestamp_tag = obj.parent.parent.find(
            "div", {"class": "nstory_dateline"}
        )
        if timestamp_tag is None:
            timestamp = datetime.now()
        else:
            content = timestamp_tag.contents[-1].strip()
            date = content.split("| ")[-1].split(", ")
            if date[-1].isdigit():
                date = " ".join(date)
            else:
                for i in range(1, 10):
                    if date[-i].isdigit():
                        break
                i -= 1
                date = " ".join(date[:-i])
            timestamp = datetime.strptime(
                date + " 05:30",
                "%A %B %d %Y %H:%M"
            )
        return {
            "content": "NA",
            "link": obj["href"].split("?")[0],
            "scraped_at": datetime.utcnow().isoformat(),
            "published_at": ist_to_utc(timestamp).isoformat(),
            "title": "\n".join(filter(
                str_is_set,
                map(
                    str.strip,
                    filter(is_string, obj.children)
                )
            ))
        }
    except KeyError:
        import pdb
        pdb.set_trace()




def get_trending_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        soup.find("div", { "class": "opinion_opt" }).decompose()
        # Some anchor tags in div[class="lhs_col_two"] are not parsed by the following
        a_tags = soup.find("div", { "class": "hmpage_lhs" }).find_all(
            "a", { "class": "item-title" }
        )
        headlines = remove_duplicate_entries(
            map(get_headline_details, a_tags),
            "link"
        )
        return headlines
    return None


if __name__ == "__main__":
    import json

    
    json_object=json.dumps(
        get_trending_headlines("https://www.ndtv.com/"),
        sort_keys=True,
        indent=4
    )
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)


