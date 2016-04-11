#!/usr/bin/python

import yaml, string, os, codecs

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

for e in entries['pile']:
    e['layout'] = "post"
    if "url" in e:
        if e is None: del e["url"]
        else: e["embed_url"] = e.pop("url")

    slug = ''.join(c for c in e['title'].replace(' ','_') if c in ("-_.%s%s" % (string.ascii_letters, string.digits)))
    filename = "%s-%s-%s-%s.md" % (e['date'].year, e['date'].month, e['date'].day, slug)
    newfile = os.path.join('_posts', filename)
    fp = codecs.open(newfile, "w", encoding="utf-8")
    fp.write('---\n')
    yaml.safe_dump(e, fp, encoding='utf-8')
    fp.write('---\n')
    if "text" in e and e['text'] is not None:
        fp.write(e['text'])
    elif "note" in e and e['note'] is not None:
        fp.write(e['note'])
    elif "notes" in e and e['notes'] is not None:
        fp.write(e['notes'])
    fp.close()
