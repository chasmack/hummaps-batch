import os
import os.path
from glob import glob
from PIL import Image
import time
import re

from const import *


def extract_images():

    # Extract single page tiff images from legacy multi-page map images
    print('\nExtracting map images...')

    # Turn of warnings about oversize image files
    Image.warnings.simplefilter('ignore', Image.DecompressionBombWarning)

    nfiles = 0
    nframes = 0
    nccs = 0

    def sort_key(s):
        return re.sub('.*(\d{3})(\D{2})(\d{3}).*', '\\2\\1\\3', s)

    cc_dir = os.path.join(IMAGE_SCAN_DIR, 'cc')
    os.makedirs(cc_dir, exist_ok=True)

    for imagefile in sorted(glob(os.path.join(IMAGE_FILES_DIR, '*.tif')), key=sort_key):

        src_file = os.path.basename(imagefile).lower()
        book, maptype = re.match('(\d+)(\D+)', src_file).groups()

        map_dir = os.path.join(IMAGE_SCAN_DIR, maptype, book)
        os.makedirs(map_dir, exist_ok=True)

        print('\n' + src_file)

        with Image.open(imagefile) as img:

            # Process one frame at at time
            frame_number = 0
            last_frame = False
            while not last_frame:

                frame = img.copy()
                try:
                    frame_number += 1
                    img.seek(frame_number)

                except EOFError:
                    last_frame = True

                print('Frame %d' % (frame_number))
                print('Mode: %s' % ({
                    '1': '1-bit black and white',
                    'L': '8-bit greyscale',
                    'P': '8-bit color map',
                    'RGB': 'RGB color',
                    'RGBA': 'RGBa color'
                }[frame.mode]))

                # Calculate image size for the frame
                scan_dpi = tuple(int(round(d)) for d in frame.info['dpi'])

                # Default 96 dpi usually means dpi not set in the image header, assume 200 dpi
                # if scan_dpi == (96, 96):
                #     scan_dpi = (200, 200)
                #     print('Scan dpi not set, using %s dpi' % (str(scan_dpi)))

                # Specials to sort out image resolutions in update #66
                if maptype.upper() == 'CR' and scan_dpi == (300, 300):
                    scan_dpi = (666, 666)
                elif scan_dpi == (72, 72):
                    if maptype.upper() == 'PM':
                        scan_dpi = (240, 240)
                    elif maptype.upper() == 'RM' and src_file[-7:-4] == '106':
                        scan_dpi = (240, 240)
                    elif maptype.upper() == 'RS' and book == '074' and int(src_file[-7:-4]) >= 16:
                        scan_dpi = (240, 240)
                    else:
                        scan_dpi = (160, 160)

                scan_size = tuple(d / dpi for d, dpi in zip(frame.size, scan_dpi))

                print(
                    'Scan size: %s @ %s dpi => %.2f x %.2f' % (str(frame.size), str(scan_dpi), scan_size[0], scan_size[1]))

                # Convert 8-bit color map to RGB
                if frame.mode == 'P':
                    print('Converting to RGB...')
                    frame = frame.convert('RGB')

                # Add the page number to the file name
                dest_file = '%s-%03d.tif' % (os.path.splitext(src_file)[0], frame_number)

                # If width of a recorded map (PM, RM, RS) is less than MIN_WIDTH assume frame is a CC
                MIN_WIDTH = 8.75
                if maptype.upper() in ('PM', 'RM', 'RS') and min(scan_size) < MIN_WIDTH:
                    dest = os.path.join(cc_dir, dest_file)
                    nccs += 1
                else:
                    dest = os.path.join(map_dir, dest_file)

                # Save the tiff scan
                frame.save(dest, resolution=float(scan_dpi[0]), resolution_unit='inch')

        nfiles += 1
        nframes += frame_number

    print('\n%d frames from %d files (%d CCs)' % (nframes, nfiles, nccs))


if __name__ == '__main__':

    startTime = time.time()

    extract_images()

    endTime = time.time()
    print('\n{0:.3f} sec'.format(endTime - startTime))


