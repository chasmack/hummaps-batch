
CREATE SEQUENCE hummaps.map_id_seq;
ALTER TABLE hummaps.map ALTER COLUMN id
    SET DEFAULT nextval('hummaps.map_id_seq')
;
ALTER SEQUENCE hummaps.map_id_seq
    OWNED BY hummaps.map.id
;
SELECT setval('hummaps.map_id_seq', max_id)
FROM (
    SELECT max(id) max_id FROM hummaps.map
) q1
;
