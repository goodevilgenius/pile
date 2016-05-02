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
    e['timestamp'] = int(e["date"].strftime('%s'))
    if "tags" in e: e['tags'] = map(unicode, e['tags'])
    if "url" in e:
        if e["url"] is None: del e["url"]
        else:
            if e['type'] in ["link", "quote"]: e['link_url'] = e.pop("url")
            else: e["embed_url"] = e.pop("url")

    if "embed_url" in e and e["type"] not in ["image","picture"]:
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
                    yaml.safe_dump(oembed, fp, encoding='utf-8', canonical=False, default_flow_style=False)
                    fp.close()
                except Error:
                    embed = None
                embeds = [ embed ]
        if embeds[0] is not None:
            e["embed_html"] = embeds[0]['html']
    elif "embed_url" in e and e["type"] in ["image","picture"]:
        e["embed_html"] = '<img src="%s" alt="" />' % e["embed_url"]
        if "source" in e: e["embed_html"] += '\n\n<cite>%s</cite>' % e["source"]

    slug = ''.join(c for c in e['title'].replace(' ','_') if c in ("-_.%s%s" % (string.ascii_letters, string.digits)))
    filename = "%s-%s-%s-%s.md" % (e['date'].year, e['date'].month, e['date'].day, slug)
    newfile = os.path.join('_posts', filename)
    fp = codecs.open(newfile, "w", encoding="utf-8")
    fp.write('---\n')
    yaml.safe_dump(e, fp, encoding='utf-8', default_flow_style=False)
    fp.write('\n---\n')
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

    # Next, let's generate archive pages
    if not os.path.isdir('archives'): os.mkdir('archives')
    day_archive = "archives/date-%s.html" % e['date'].strftime('%Y-%m-%d')
    day = {"layout":"archive"}
    day['permalink'] = e['date'].strftime('%Y/%m/%d/')
    day['archive'] = 'day'
    day['title'] = 'Archive for %s' % (e['date'].strftime('%B %d, %Y'))
    day['year'] = "%s" % e['date'].year
    day['month'] = "%s" % e['date'].month
    day['day'] = "%s" % e['date'].day
    day['year-month-day'] = e['date'].strftime('%Y-%m-%d')
    with open(day_archive, 'w') as fp:
        fp.write('---\n')
        yaml.safe_dump(day, fp, encoding='utf-8', canonical=False, default_flow_style=False)
        fp.write('\n---\n')

    month_archive = "archives/date-%s.html" % e['date'].strftime('%Y-%m')
    month = {"layout":"archive"}
    month['permalink'] = e['date'].strftime('%Y/%m/')
    month['archive'] = 'month'
    month['title'] = 'Archive for %s %s' % (e['date'].strftime('%B'), e['date'].year)
    month['year'] = "%s" % e['date'].year
    month['month'] = "%s" % e['date'].month
    month['year-month'] = e['date'].strftime('%Y-%m')
    with open(month_archive, 'w') as fp:
        fp.write('---\n')
        yaml.safe_dump(month, fp, encoding='utf-8', canonical=False, default_flow_style=False)
        fp.write('\n---\n')

    year_archive = "archives/date-%s.html" % e['date'].year
    year = {"layout":"archive"}
    year['permalink'] = e['date'].strftime('%Y/')
    year['archive'] = 'year'
    year['title'] = 'Archive for %s' % e['date'].year
    year['year'] = "%s" % e['date'].year
    with open(year_archive, 'w') as fp:
        fp.write('---\n')
        yaml.safe_dump(year, fp, encoding='utf-8', canonical=False, default_flow_style=False)
        fp.write('\n---\n')

    if "tags" in e:
        for tag in e['tags']:
            tag_archive = "archives/tag-%s.html" % urllib.quote(tag)
            tago = {"layout":"archive"}
            tago['permalink'] = "/tag/%s/" % tag
            tago['archive'] = 'tag'
            tago['title'] = 'Archive for %s' % tag
            tago['tag'] = tag
            with open(tag_archive, 'w') as fp:
                fp.write('---\n')
                yaml.safe_dump(tago, fp, encoding='utf-8', canonical=False, default_flow_style=False)
                fp.write('\n---\n')

    if "type" in e:
        type_archive = "archives/type-%s.html" % urllib.quote(e["type"])
        typeo = {"layout":"archive"}
        typeo['permalink'] = "/type/%s/" % e["type"]
        typeo['archive'] = 'type'
        typeo['title'] = 'Archive for %s posts' % e["type"]
        typeo['type'] = e["type"]
        with open(type_archive, 'w') as fp:
            fp.write('---\n')
            yaml.safe_dump(typeo, fp, encoding='utf-8', canonical=False, default_flow_style=False)
            fp.write('\n---\n')
