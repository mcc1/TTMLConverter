__author__ = 'ChihChung'
import codecs
import argparse
import xml.etree.ElementTree as et


class ttmltConverter:
    def gentime(input):
        tmp, ns = input.split(".")
        s = int(tmp) % 60
        m = int(tmp) % 3600 / 60
        h = int(tmp) / 3600
        return "{:02d}:{:02d}:{:02d},{:03d}".format(h, m, s, int(ns))

    def srtWriter(data, file):
        for _, sub in data.items():
            file.write(str(sub['count']) + '\n')
            file.write(str(sub['begin']) + " --> " + str(sub['end']) + '\n')
            file.write(sub['content'] + '\n\n')

    parser = argparse.ArgumentParser(description='TTML Subtitle Converter')
    parser.add_argument('input', type=str, help='input file')
    parser.add_argument('output', type=str, help='output file')
    args = parser.parse_args()

    out = codecs.open(args.output, 'w', encoding='utf8')
    root = et.parse(args.input).getroot()
    ns = {'tt': "http://www.w3.org/ns/ttml"}

    subs = {}

    for count, node in enumerate(root.findall('.//tt:p', ns), 1):
        subs[count] = {}
        subs[count]['count'] = count
        subs[count]['begin'] = gentime(node.get('begin').replace('s', ''))
        subs[count]['end'] = gentime(node.get('end').replace('s', ''))
        subs[count]['content'] = node.text.replace("<br/>", '\n')

    srtWriter(subs, out)
