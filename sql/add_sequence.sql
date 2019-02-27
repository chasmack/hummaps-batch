
CREATE SEQUENCE hummaps.surveyor_id_seq;
ALTER TABLE hummaps.surveyor ALTER COLUMN id
    SET DEFAULT nextval('hummaps.surveyor_id_seq')
;
ALTER SEQUENCE hummaps.surveyor_id_seq
    OWNED BY hummaps.surveyor.id
;
SELECT setval('hummaps.surveyor_id_seq', max_id)
FROM (
    SELECT max(id) max_id FROM hummaps.surveyor
) q1
;
