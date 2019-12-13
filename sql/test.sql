
WITH q1 AS (
  SELECT cc.id cc_id
  FROM hummaps.cc cc
  WHERE cc.doc_number SIMILAR TO '2018' || '(-0*| OR )' || '22785' || '%'
), d1 AS (
  DELETE FROM hummaps.cc_image
  WHERE cc_id IN (SELECT cc_id FROM q1)
)
-- INSERT INTO hummaps.cc_image (cc_id, imagefile, page)
SELECT cc_id, imagefile,
  regexp_replace(imagefile, '.*-(\d+)\.jpg', '\1')::int page
FROM q1, (
  SELECT unnest(ARRAY[
    '/map/cc/2018-doc-022785-001.jpg',
    '/map/cc/2018-doc-022785-002.jpg'
  ]) imagefile
) q2
;
