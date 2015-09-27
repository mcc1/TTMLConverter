__author__ = 'ChihChung'
import codecs
import argparse
import xml.etree.ElementTree as et


class TTMlConverter:
    """
    Simple Converter which can convert TTML subtitle to other subtitle formats.
    """

    def __init__(self, file_format='srt'):
        self.file_format = file_format

    def gentime(self, timestr):
        tmp, ns = timestr.split(".")
        s = int(tmp) % 60
        m = int(tmp) % 3600 / 60
        h = int(tmp) / 3600
        return "{:02d}:{:02d}:{:02d},{:<03d}".format(h, m, s, int(ns))

    def read(self, input_file):
        ns = {'tt': "http://www.w3.org/ns/ttml"}
        root = et.parse(input_file).getroot()

        subs = {}
        for count, node in enumerate(root.findall('.//tt:p', ns), 1):
            subs[count] = {}
            subs[count]['count'] = count
            subs[count]['begin'] = c.gentime(node.get('begin').replace('s', ''))
            subs[count]['end'] = c.gentime(node.get('end').replace('s', ''))
            subs[count]['content'] = node.text.replace('<br/>', '\n')
        return subs

    def srt_writer(self, data, output):
        out = codecs.open(output, 'w', encoding='utf8')
        for _, sub in data.items():
            out.write(str(sub['count']) + '\n')
            out.write(str(sub['begin']) + " --> " + str(sub['end']) + '\n')
            out.write(sub['content'] + '\n\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TTML Subtitle Converter')
    parser.add_argument('input', type=str, help='input file')
    parser.add_argument('output', type=str, help='output file')
    args = parser.parse_args()

    c = TTMlConverter()
    subs = c.read(args.input)
    c.srt_writer(subs, args.output)
