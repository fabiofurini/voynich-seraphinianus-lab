"""Whole ZL3b corpus: principal-reading graphical counts, with explicit exceptions.
python voynich_full_inventory.py voynich_ZL3b.txt > full_inventory.json
"""
import sys,re,json,collections,hashlib
raw=open(sys.argv[1],'rb').read();counts=collections.Counter();special=collections.Counter()
pages=set();loci=collections.Counter();alternatives=0;unknown=0;residue=collections.Counter();modifiers=collections.Counter()
for line in raw.decode('utf-8-sig').splitlines():
    m=re.match(r'<(f[^.>]+)\.([^,>]+),([^>]+)>\s*(.*)',line)
    if not m:continue
    pages.add(m[1]);loci[m[3][1:]]+=1
    t=m[4].replace('<->','.')
    t=re.sub(r'<[^>]*>','',t)
    # A principal reading must be explicit, never mistaken for a certain one.
    while '[' in t:
        def first(a):
            global alternatives
            alternatives+=1
            return a[1].split(':')[0]
        t2=re.sub(r'\[([^\[\]]*)\]',first,t)
        if t2==t:break
        t=t2
    # Compound annotations and extended signs remain separate classes.
    # EVA capitals encode connectivity, not a separate letter.
    t=t.lower()
    pattern=r'\{[^}]*\}|@\d+;|ckh|cth|cph|cfh|ch|sh|[a-z]|[?*]|.'
    for a in re.findall(pattern,t):
        if re.fullmatch('ckh|cth|cph|cfh|ch|sh|[a-z]',a):counts[a]+=1
        elif a in ['?','*']:unknown+=1
        elif a.startswith('{') or re.fullmatch(r'@\d+;',a):special[a]+=1
        elif a=="'":modifiers[a]+=1
        elif a.isspace() or a in '.,!%=-':pass
        else:residue[a]+=1
total=sum(counts.values())+sum(special.values())
out={'source_sha256':hashlib.sha256(raw).hexdigest(),'source':'Zandbergen-Landini ZL3b, 13 May 2025',
 'scope':'All transcribed loci: paragraphs, labels, circular/radial text and other categories; comments excluded.',
 'pages':len(pages),'loci':sum(loci.values()),'locus_types':dict(loci),
 'reading_policy':'First alternative in brackets. Known parts counted even in partly uncertain tokens. Maximal match for six connected forms. Curly groups and extended codes retained as special classes.',
 'alternative_groups_resolved':alternatives,'unreadable_markers_excluded_from_denominator':unknown,
 'classified_units_denominator':total,'basic_unit_counts':dict(counts.most_common()),
 'special_form_counts':dict(special.most_common()),'separate_modifier_counts':dict(modifiers),
 'unhandled_characters':dict(residue),
 'limits':['Not an image-by-image audit. Untranscribed or missing text cannot be counted.',
 'Uncertain alternatives affect counts. Markers for unknown text do not necessarily correspond to one physical glyph.',
 'Compound choices define the counting unit; this is not a count of phonemes.',
 'Curly groups are preserved as written rather than asserted to be simple glyphs.']}
print(json.dumps(out,ensure_ascii=False,indent=2))
