
WITH t1 AS (
    SELECT DISTINCT t1.map_id,
        subpath(t1.trs_path, 0, 3) trs_path
    FROM hummaps.trs_path t1
    WHERE nlevel(t1.trs_path) = 4
), t2 AS (
    SELECT t2.id, t2.map_id, t2.trs_path
    FROM hummaps.trs_path t2
    JOIN t1 USING (map_id, trs_path)
    WHERE nlevel(t2.trs_path) = 3
)
DELETE FROM hummaps.trs_path
WHERE id IN (
    SELECT id FROM t2
)
;