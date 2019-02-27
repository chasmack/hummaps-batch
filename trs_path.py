import re

# trs_path.py
#
# A township/range/section (trs) path identifies a single section or subsection
# (quarter-quarter section or qq section). It is represented as a string of
# period-separated nodes -
#
# 7N.3E.2
# 7N.3E.2.A
#
# The sixteen quarter-quarter sections in a section are coded using upper-case
# letters form A to P -
#
#   -+---+---+---+---+-
#    | A | B | C | D |
#   -+---+---+---+---+-
#    | E | F | G | H |
#   -+---+---+---+---+-
#    | I | J | K | L |
#   -+---+---+---+---+-
#    | M | N | O | P |
#   -+---+---+---+---+-
#
# For example, the SW/4 of the SW/4 is coded with the letter "M". All characters
# in a trs path are upper case. No zero padding of numeric values is permitted.
# No space or other punctuation is permitted within a trs path.

TOWNSHIP_NORTH_MAX = 15
TOWNSHIP_SOUTH_MAX = 5
RANGE_EAST_MAX = 8
RANGE_WEST_MAX = 3

def validate_path(path):
    m = re.fullmatch('([1-3]?\d[NS])\.([1-3]?\d[EW])\.([1-3]?\d)(?:\.[A-P])?', path)
    if m is None:
        return False
    tshp, rng, sec = m.groups()
    if tshp[-1] == 'N' and not (1 <= int(tshp[:-1]) <= TOWNSHIP_NORTH_MAX):
        return False
    if tshp[-1] == 'S' and not 1 <= int(tshp[:-1]) <= TOWNSHIP_SOUTH_MAX:
        return False
    if rng[-1] == 'E' and not 1 <= int(rng[:-1]) <= RANGE_EAST_MAX:
        return False
    if rng[-1] == 'W' and not 1 <= int(rng[:-1]) <= RANGE_WEST_MAX:
        return False
    if not 1 <= int(sec) <= 36:
        return False

    return True

# A trs path spec represents one or more trs paths.
# The leaf node of a path spec can be a single label or
# a comma separated list of labels and label ranges.
#
# 4N.1W.12
# 4N.1W.1,2,10,11,12
# 4N.1W.1,2,10-12
# 4N.1W.11.C
# 4N.1W.11.A,B,C,D,G,H
# 4N.1W.11.A-D,G,H
#
# Commas are optional in the subsection list.
#
# 4N.1W.11.ABCDGH
# 4N.1W.11.A-DGH
# 4N.1W.11.A-D,GH
#
# No space or other punctuation is permitted within an individual trs path spec.
# Multiple trs path specs are separated with one or more spaces.
#
# 4N.1W.1.A-D 5N.1W.36.M-P
#

def path_sortkey(path):
    lables = path.split('.')
    key = lables[0][-1] + lables[0][0:-1].zfill(2) + lables[1][-1] + lables[1][0:-1].zfill(2)
    if len(lables) > 2:
        key += lables[2].zfill(2)
    if len(lables) > 3:
        key += lables[3]
    return key

# expand_paths - extract trs paths form one or more trs path specs.
def expand_paths(path_specs):

    paths = []
    for path_spec in path_specs.split():

        # Check for a simple path
        if validate_path(path_spec):
            paths.append(path_spec)
            continue

        # Check for a list of sections
        regexp = '(\d+[NS]\.\d+[EW]\.)((?:(?:\d+-)?\d+,)*(?:(?:\d+-)?\d+))'
        m = re.fullmatch(regexp, path_spec)
        if m:
            root = m.group(1)
            secs = []
            for sec in m.group(2).split(','):
                if not '-' in sec:
                    secs.append(sec)
                else:
                    low, high = map(int, sec.split('-'))
                    if high < low:
                        low, high = high, low
                    secs += map(str, range(low, high + 1))
            for path in (root + s for s in secs):
                if not validate_path(path):
                    raise ValueError('Bad path spec: ' + path_spec)
                paths.append(path)
            continue

        # Check for a list of subsections
        regexp = '(\d+[NS]\.\d+[EW]\.\d+\.)((?:(?:[A-P]-)?[A-P])*(?:(?:[A-P]-)?[A-P]))'
        m = re.fullmatch(regexp, path_spec.replace(',', ''))
        if m:
            root = m.group(1)
            subsecs = []
            for subsec in re.findall('(?:[A-P]-)?[A-P]', m.group(2)):
                if not '-' in subsec:
                    subsecs.append(subsec)
                else:
                    low ,high = map(ord, subsec.split('-'))
                    if high < low:
                        low, high = high, low
                    subsecs += map(chr, range(low, high + 1))
            for path in (root + ss for ss in subsecs):
                if not validate_path(path):
                    raise ValueError('Bad path spec: ' + path_spec)
                paths.append(path)
            continue

        # No match
        raise ValueError('Bad path spec: ' + path_spec)

    # Sort paths and remove dulpicates
    paths.sort(key=path_sortkey)
    i = 1
    while i < len(paths):
        if paths[i] == paths[i - 1]:
            print('WARNING: Duplicate path: %s' % paths.pop(i))
        else:
            i += 1

    return paths

# abbrev_paths - create a set of trs path specs from a list of trs paths.
def abbrev_paths(paths):

    # Separate sorted paths into paths with subsection terms and those without.
    # The section list is an ordered list of integer sections indexed by township.
    # The subsection list is an ordered list of subsection codes indexed by
    # township and section.

    sec_list = {}
    ss_list = {}
    for path in sorted(paths, key=path_sortkey):

        if not validate_path(path):
            raise ValueError('Invalid path: ' + path)

        labs = path.split('.')
        tr = '.'.join(labs[0:2])
        sec = int(labs[2])

        if len(labs) == 3:
            if tr not in sec_list:
                sec_list[tr] = [sec]
            else:
                sec_list[tr].append(sec)
        else:
            subsec = labs[3]
            if tr not in ss_list:
                ss_list[tr] = {sec: [subsec]}
            elif sec not in ss_list[tr]:
                ss_list[tr][sec] = [subsec]
            else:
                ss_list[tr][sec].append(subsec)

    # Create a list of abbreviated paths using character class like leaf nodes.

    abbrevs = []
    for tr in sorted(sec_list.keys(), key=path_sortkey):
        secs = sec_list[tr]
        if len(secs) == 1:
            # Single section in this township.
            abbrevs.append(tr + '.' + str(sec))
        else:
            # Multiple sections this township will be grouped into a class.
            specs = [str(secs[0])]
            for i in range(1, len(secs)):
                if '-' in specs[-1]:
                    # Last spec in the list is a range.
                    range_start, range_end = [int(s) for s in specs[-1].split('-')]
                    if secs[i] - range_end == 1:
                        # Extend the range.
                        specs[-1] = '%d-%d' % (range_start, secs[i])
                    else:
                        specs.append(str(secs[i]))
                elif len(specs) > 1 and '-' not in specs[-2] and secs[i] - int(specs[-2]) == 2:
                    # Replace last two specs with a new range.
                    specs[-2:] = ['%s-%d' % (specs[-2], secs[i])]
                else:
                    specs.append(str(secs[i]))

            abbrevs.append(tr + '.' + ','.join(specs))

    for tr in sorted(ss_list.keys(), key=path_sortkey):
        for sec in sorted(ss_list[tr].keys(), key=int):
            subsecs = ss_list[tr][sec]
            if len(subsecs) == 1:
                abbrevs.append(tr + '.' + str(sec) +'.'+ subsecs[0])
            else:
                specs = [subsecs[0]]
                for i in range(1, len(subsecs)):
                    if '-' in specs[-1]:
                        # Last spec in the list is a range.
                        range_start, range_end = specs[-1].split('-')
                        if ord(subsecs[i]) - ord(range_end) == 1:
                            # Extend the range.
                            specs[-1] = '%s-%s' % (range_start, subsecs[i])
                        else:
                            specs.append(subsecs[i])
                    elif len(specs) > 1 and '-' not in specs[-2] and ord(subsecs[i]) - ord(specs[-2]) == 2:
                        # Replace last tow specs in the list with a new range.
                        specs[-2:] = ['%s-%s' % (specs[-2], subsecs[i])]
                    else:
                        specs.append(subsecs[i])

                abbrevs.append(tr + '.' + str(sec) + '.' + ','.join(specs))

    return abbrevs


if __name__ == '__main__':

    paths = '7N.5E.12 7N.4E.1,2,4-8,15,23,24,25 ' + \
            '4N.1W.7.A,C-F,H,I,J,L,N,O,P 4N.1E.3.KLOP ' + \
            '4N.1E.3.IJMNKLOP'

    paths = expand_paths(paths)
    for path in paths:
        print(path)

    print()

    abbrevs = abbrev_paths(paths)
    for abbrev in abbrevs:
        print(abbrev)

    assert validate_path('7N.3E.0') is False
    assert validate_path('7N.3E.1')
    assert validate_path('7N.3E.36')
    assert validate_path('7N.3E.37') is False
    assert validate_path('7N.3E.1.A')
    assert validate_path('7N.3E.1.P')
    assert validate_path('7N.3E.1.Q') is False
    assert validate_path('0N.3E.1.A') is False
    assert validate_path('1N.3E.1.A')
    assert validate_path('15N.3E.1.A')
    assert validate_path('16N.3E.1.A') is False
    assert validate_path('0S.3E.1.A') is False
    assert validate_path('1S.3E.1.A')
    assert validate_path('5S.3E.1.A')
    assert validate_path('6S.3E.1.A') is False
    assert validate_path('1N.0E.1.A') is False
    assert validate_path('1N.1E.1.A')
    assert validate_path('1N.8E.1.A')
    assert validate_path('1N.9E.1.A') is False
    assert validate_path('1N.0W.1.A') is False
    assert validate_path('1N.1W.1.A')
    assert validate_path('1N.3W.1.A')
    assert validate_path('1N.4W.1.A') is False
    assert validate_path('01N.1W.1.A') is False
    assert validate_path('1N.01W.1.A') is False
    assert validate_path('1N.1W.01.A') is False