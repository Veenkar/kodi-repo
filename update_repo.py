"""Regenerate addons.xml and addons.xml.md5 from the newest zip of every add-on in zips/.

Run after adding a new add-on zip as zips/<id>/<id>-<version>.zip:
    python update_repo.py
It also refreshes zips/<id>/addon.xml, icon.png and fanart.jpg from that zip.
"""
import hashlib
import os
import re
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
ZIPS = os.path.join(ROOT, 'zips')


def version_key(version):
    return [int(x) if x.isdigit() else x for x in re.split(r'[.\-~+]', version)]


def newest_zip(addon_id):
    folder = os.path.join(ZIPS, addon_id)
    found = []
    for name in os.listdir(folder):
        m = re.match(re.escape(addon_id) + r'-(.+)\.zip$', name)
        if m:
            found.append((version_key(m.group(1)), name))
    if not found:
        raise SystemExit('no zip in %s' % folder)
    return os.path.join(folder, max(found)[1])


def addon_body(xml):
    xml = xml.lstrip('﻿')
    return re.sub(r'^<\?xml[^>]*\?>\s*', '', xml).strip()


def main():
    bodies = []
    for addon_id in sorted(os.listdir(ZIPS)):
        if not os.path.isdir(os.path.join(ZIPS, addon_id)):
            continue
        path = newest_zip(addon_id)
        with zipfile.ZipFile(path) as z:
            xml = z.read(addon_id + '/addon.xml').decode('utf-8')
            for art in ('addon.xml', 'icon.png', 'fanart.jpg'):
                if addon_id + '/' + art in z.namelist():
                    with open(os.path.join(ZIPS, addon_id, art), 'wb') as f:
                        f.write(z.read(addon_id + '/' + art))
        version = re.search(r'<addon[^>]*\sversion="([^"]+)"', xml).group(1)
        print('%s %s  (%s)' % (addon_id, version, os.path.basename(path)))
        bodies.append(addon_body(xml))

    addons = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n'
              + '\n\n'.join(bodies) + '\n</addons>\n').encode('utf-8')
    with open(os.path.join(ROOT, 'addons.xml'), 'wb') as f:
        f.write(addons)
    with open(os.path.join(ROOT, 'addons.xml.md5'), 'w', newline='\n') as f:
        f.write(hashlib.md5(addons).hexdigest())


if __name__ == '__main__':
    main()
