#!/usr/bin/python

import yaml, string, os, codecs, urllib, json, fnmatch, re

try:
    import droplogger
except ImportError:
    # Just until I'm able to make droplogger installable
    import sys
    sys.path.append('/home/drj/MyFiles/Programming/Python/droplogger')
    import droplogger

config = droplogger.read_config()
config['white'] = ["pile"]
config['start'] = droplogger.parse_date('min')
config['end'] = droplogger.parse_date('now')

config['files'] = droplogger.get_files(**config)
entries = droplogger.read_files(**config)

oembed_file = '_data/oembed.yml'

fp = open(oembed_file,'r')
oembed = yaml.load(fp)
fp.close()

for e in entries['pile']:
    e['layout'] = "post"
    if "url" in e:
        if e["url"] is None: del e["url"]
        else:
            if e['type'] in ["link", "quote"]: e['link_url'] = e.pop("url")
            else: e["embed_url"] = e.pop("url")

    if "embed_url" in e:
        embeds = [ o for o in oembed['urls'] if o['url'] == e["embed_url"] ]
        if len(embeds) == 0:
            providers = [ p for p in oembed['providers'] if "schemes" in p['endpoints'][0] and len([ s for s in p['endpoints'][0]['schemes'] if fnmatch.fnmatch(e["embed_url"], s) ]) ]
            if len(providers) > 0:
                ep = providers[0]['endpoints'][0]['url']
                oembed_url = ep + '?' + urllib.urlencode({"format":"json","url":e['embed_url']})
                try:
                    embed = json.load(urllib.urlopen(oembed_url))
                    embed['url'] = e["embed_url"]
                    oembed["urls"].append(embed)
                    fp = open(oembed_file,'w')
                    yaml.safe_dump(oembed, fp, encoding='utf-8')
                    fp.close()
                except Error:
                    embed = None
                embeds = [ embed ]
        if embeds[0] is not None:
            e["embed_html"] = embeds[0]['html']

    slug = ''.join(c for c in e['title'].replace(' ','_') if c in ("-_.%s%s" % (string.ascii_letters, string.digits)))
    filename = "%s-%s-%s-%s.md" % (e['date'].year, e['date'].month, e['date'].day, slug)
    newfile = os.path.join('_posts', filename)
    fp = codecs.open(newfile, "w", encoding="utf-8")
    fp.write('---\n')
    yaml.safe_dump(e, fp, encoding='utf-8')
    fp.write('---\n')
    if "embed_html" in e:
        fp.write(e['embed_html'])
        fp.write('\n\n')
    cont = ""
    if "text" in e and e['text'] is not None:
        cont = e['text']
    elif "note" in e and e['note'] is not None:
        cont = e['note']
    elif "notes" in e and e['notes'] is not None:
        cont = e['notes']
    if e["type"] == "quote":
        cont = re.sub('^','> ', cont.strip(), flags=re.M)
        cont += '\n> \n'
        cont += '> <cite>%s</cite>' % e['source'] if "source" in e else "Unknown"
    fp.write(cont)
    fp.close()
