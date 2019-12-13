import time

from create_update import load_update_tables, load_xlsx_tables, create_update, cleanup_tables
from apply_update import update_map, update_trs, update_surveyor, update_cc
from extract_images import extract_images
from update_images import convert_maps, convert_ccs, make_pdfs, update_map_image, update_cc_image, update_pdf


if __name__ == '__main__':

    UPDATE_PHASE = 0

    startTime = time.time()

    if UPDATE_PHASE == 1:

        # Create an update schema and load tables from XML and XLSX data.
        load_update_tables()
        load_xlsx_tables()

        # Record changes to the XLSX update..
        create_update()

    elif UPDATE_PHASE == 2:

        # Update production tables from XLSX update.
        update_map()
        update_trs()
        update_surveyor()
        update_cc()

    elif UPDATE_PHASE == 3:

        # Extract single page tiff images from update map images.
        extract_images()

    # NOTE: Stop here to rename any new CC images in scan/cc.

    elif UPDATE_PHASE == 4:

        # Convert map and cc scans to jpg images.
        convert_maps()
        convert_ccs()

        # Package jpeg images into PDFs.
        make_pdfs()

    elif UPDATE_PHASE == 5:

        # Update production tables to link map and cc images to map and cc records.
        update_map_image()
        update_cc_image()

        # Update production pdf table to link pdf files to map records.
        update_pdf()

    elif UPDATE_PHASE == 6:

        # Delete the update schema.
        cleanup_tables()

    endTime = time.time()
    print('\n{0:.3f} sec'.format(endTime - startTime))