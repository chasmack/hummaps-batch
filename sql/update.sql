
-- DELETE FROM hummaps.trs_path WHERE map_id = 6840;

-- INSERT INTO hummaps.trs_path (map_id, trs_path, source_id)
-- VALUES
--     (6840, '2S.3E.14.E'::ltree, 4),
--     (6840, '2S.3E.14.F'::ltree, 4),
--     (6840, '2S.3E.14.G'::ltree, 4),
--     (6840, '2S.3E.14.I'::ltree, 4),
--     (6840, '2S.3E.14.J'::ltree, 4),
--     (6840, '2S.3E.14.K'::ltree, 4),
--     (6840, '2S.3E.15.H'::ltree, 4),
--     (6840, '2S.3E.15.L'::ltree, 4)
-- ;

-- SELECT * FROM hummaps.trs_path WHERE map_id = 6840;

UPDATE hummaps.trs_path SET trs_path = '1N.1E.5.A'::ltree
WHERE map_id = 10250
;
