import xml.etree.ElementTree as ET
import requests
import gzip
import io
import csv


def extract_links_from_sitemap_gz(url):
    response = requests.get(url)
    response.raise_for_status()

    with gzip.open(io.BytesIO(response.content), 'rt') as uncompressed_file:
        xml_content = uncompressed_file.read()

    root = ET.fromstring(xml_content)
    namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [url.text for url in root.findall('.//sitemap:loc', namespace)]

    return urls


sitemapUrl = "https://uk.rs-online.com/uk-detail203.xml.gz"
urls = extract_links_from_sitemap_gz(sitemapUrl)

csvName = sitemapUrl.split('/')
csv_filename = f"{csvName[3].split('.')[0]}.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["S.No", "URL"])
    for count, url in enumerate(urls, start=1):
        writer.writerow([count, url])

print(f"URLs have been saved to {csv_filename}.")
