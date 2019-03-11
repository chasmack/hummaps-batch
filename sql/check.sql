
INSERT INTO hummaps.map (id, maptype_id, book, page, npages, description)
SELECT 20003, maptype_id, book, page, npages, description
FROM hummaps.map
WHERE id = 16323
;

UPDATE hummaps.map_image SET map_id = 20003 WHERE map_id = 16323;
UPDATE hummaps.pdf SET map_id = 20003 WHERE map_id = 16323;
DELETE FROM hummaps.map WHERE id = 16323;

-- SELECT m.id, t.maptype, m.book, m.page
-- FROM hummaps.map m
-- JOIN hummaps.maptype t ON t.id = m.maptype_id
-- LEFT JOIN hummaps.cc cc ON cc.map_id = m.id
-- WHERE t.abbrev = 'RS'
-- GROUP BY m.id, t.id
-- HAVING count(cc.map_id) = 1
-- LIMIT 10
-- ;

-- WITH q1 AS (
--     SELECT m.id map_id
--     FROM hummaps.map m
--     JOIN hummaps.maptype t ON t.id = m.maptype_id
--     WHERE t.maptype = 'Survey' AND m.book = 62 AND m.page = 76
-- ), q2 AS (
--     SELECT q1.map_id, array_remove(array_agg(p.trs_path::text), NULL) trs_paths
--     FROM q1
--     LEFT JOIN hummaps.trs_path p USING (map_id)
--     GROUP BY q1.map_id
-- ), q3 AS (
--     SELECT q1.map_id, array_remove(array_agg(s.fullname), NULL) surveyors
--     FROM q1
--     LEFT JOIN hummaps.signed_by sb USING (map_id)
--     LEFT JOIN hummaps.surveyor s ON s.id = sb.surveyor_id
--     GROUP BY q1.map_id
-- ), q4 AS (
--     SELECT q1.map_id, array_remove(array_agg(cc.doc_number), NULL) ccs
--     FROM q1
--     LEFT JOIN hummaps.cc cc USING (map_id)
--     GROUP BY q1.map_id
-- )
-- SELECT
--     q1.map_id, m.npages, m.recdate, m.client, m.description, m.note,
--     q2.trs_paths, q3.surveyors, q4.ccs
-- FROM hummaps.map m
-- JOIN q1 ON q1.map_id = m.id
-- LEFT JOIN q2 ON q2.map_id = m.id
-- LEFT JOIN q3 ON q3.map_id = m.id
-- LEFT JOIN q4 ON q4.map_id = m.id
-- ;