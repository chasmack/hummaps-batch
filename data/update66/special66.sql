-- 
-- Run this on the existing update 65 database BEFORE
-- loading update 66 from the sql dump.
-- 
-- Alternately reinitialize the database and users by
-- running create_db.sql (user: postgres, database: postgres)
-- and create_extension.sql (user: postgres, database: production)
-- where user postgres is the superuser.
--

-- Drop the old (non-paths) trs table
DROP TABLE IF EXISTS hummaps.trs;

-- Delete existing record for 1UR388 map_id = 13853. See map_id = 16468.
DELETE FROM hummaps.trs_path WHERE map_id = 13853;
DELETE FROM hummaps.map_image WHERE map_id = 13853;
DELETE FROM hummaps.pdf WHERE map_id = 13853;
DELETE FROM hummaps.scan WHERE map_id = 13853;
DELETE FROM hummaps.signed_by WHERE map_id = 13853;
DELETE FROM hummaps.cc WHERE map_id = 13853;
DELETE FROM hummaps.map WHERE id = 13853;
