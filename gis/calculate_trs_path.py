def getPath(fdid, sdlab):
    ap_to_path_code = {
        'NWNW': 'A', 'NENW': 'B', 'NWNE': 'C', 'NENE': 'D',
        'SWNW': 'E', 'SENW': 'F', 'SWNE': 'G', 'SENE': 'H',
        'NWSW': 'I', 'NESW': 'J', 'NWSE': 'K', 'NESE': 'L',
        'SWSW': 'M', 'SESW': 'N', 'SWSE': 'O', 'SESE': 'P'
    }
    lot_to_path_code = {
        'L 4': 'A', 'L 3': 'B', 'L 2': 'C', 'L 1': 'D'
    }
    tshp = fdid[4:7].lstrip('0') + fdid[8]
    rng = fdid[9:12].lstrip('0') + fdid[13]
    sec = fdid[-3:-1].lstrip('0')
    if sdlab in ap_to_path_code:
        return '.'.join((tshp, rng, sec, ap_to_path_code[sdlab]))
    elif sdlab in lot_to_path_code:
        return '.'.join((tshp, rng, sec, lot_to_path_code[sdlab]))
    else:
        return return '.'.join((tshp, rng, sec, ''))
