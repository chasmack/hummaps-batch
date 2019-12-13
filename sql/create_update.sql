
-- map info new in update
WITH q1 AS (
  SELECT map_id, array_agg(trs_path) paths
  FROM update66.trs_path
  GROUP BY map_id
)
SELECT u.id map_id,
  u.maptype, u.book, u.firstpage page, u.lastpage - u.firstpage + 1 npages,
  q1.paths::text[],
  u.recdate, u.client, u.description, u.note
FROM update66.map u
LEFT JOIN  q1 ON q1.map_id = u.id
LEFT JOIN hummaps.map m ON u.id = m.id
WHERE m.id IS NULL
ORDER BY u.id
;

-- map info modified in update
WITH q1 AS (
  -- aggregate array of surveyor names in update
  SELECT u.id map_id, array_agg(s.fullname) surveyors
  FROM (
    SELECT id, regexp_split_to_table(upper(surveyors), '\s*&\s*') hollins_fullname
    FROM update66.map
  ) u
  -- assuming no missing surveyors here, LEFT JOIN ignores UNKNOWN, etc
  LEFT JOIN update66.surveyor s ON s.hollins_fullname = u.hollins_fullname
  -- ignore new maps not already present in prod data
  JOIN hummaps.map m ON m.id = u.id
  GROUP BY u.id
  
), q2 AS (
  -- aggregate array of surveyor names in current prod
  SELECT m.id map_id, array_agg(s.fullname) surveyors
  FROM hummaps.map m
  LEFT JOIN hummaps.signed_by sb on sb.map_id = m.id
  LEFT JOIN hummaps.surveyor s on s.id = sb.surveyor_id
  GROUP BY m.id
  
), q3 AS (
  -- compare all fields except trs paths and note
  SELECT u.id map_id, u.maptype, u.book, u.firstpage page, u.lastpage - u.firstpage + 1 npages, u.recdate,
      array_to_string(ARRAY(SELECT unnest(q1.surveyors) ORDER BY 1), ', ') surveyors,
      u.client, u.description
  FROM q1
  JOIN update66.map u ON u.id = q1.map_id
  EXCEPT
  SELECT m.id, t.maptype, m.book, m.page, m.npages, recdate,
    array_to_string(ARRAY(SELECT unnest(q2.surveyors) ORDER BY 1), ', ') surveyors,
    regexp_replace(m.client, ' \((PM|TR)\d+\)( AMENDED| UNIT \d)?$', '') client, 
    description
  FROM q2
  JOIN hummaps.map m ON m.id = q2.map_id
  JOIN hummaps.maptype t ON m.maptype_id = t.id
  
), q4 AS (
  -- aggregate array of trs paths in update
  SELECT u.map_id, array_agg(u.trs_path) paths
  FROM update66.trs_path u
  GROUP BY map_id
  
), q5 AS (
  -- aggregate array of trs paths in current prod
  SELECT map_id, array_agg(trs_path) paths
  FROM hummaps.trs_path
  GROUP BY map_id
  
), q6 AS (
  -- find maps with trs path in update that is not an ancestor of current trs paths
  SELECT map_id, q4.paths paths
  FROM update66.trs_path u
  JOIN q4 USING (map_id)
  JOIN q5 USING (map_id)
  WHERE NOT u.trs_path @> ANY (q5.paths)
  GROUP BY map_id, q4.paths
)

-- combine results of first comparison in q3 and trs paths comparison in q6
SELECT u.id map_id, u.maptype, u.book, u.firstpage page, u.lastpage - u.firstpage + 1 npages,
  ARRAY(SELECT unnest(q4.paths) ORDER BY 1)::text[] trs_paths, u.recdate, u.surveyors, u.client, u.description, u.note
FROM q3
JOIN q4 USING (map_id)
JOIN update66.map u ON u.id = q3.map_id
UNION
SELECT u.id map_id, u.maptype, u.book, u.firstpage page, u.lastpage - u.firstpage + 1 npages,
  ARRAY(SELECT unnest(q6.paths) ORDER BY 1)::text[] trs_paths, u.recdate, u.surveyors, u.client, u.description, u.note
FROM q6
JOIN update66.map u ON u.id = q6.map_id
ORDER BY map_id
;

-- map info not in update
WITH q1 AS (
  SELECT map_id, array_agg(trs_path)::text[] paths
  FROM hummaps.trs_path
  GROUP BY map_id
)
SELECT m.id map_id, t.maptype, m.book, m.page, m.npages,
  q1.paths,
  m.recdate, m.client, m.description, m.note
FROM hummaps.map m
JOIN hummaps.maptype t ON t.id = m.maptype_id
LEFT JOIN  q1 ON q1.map_id = m.id
LEFT JOIN update66.map u ON m.id = u.id
WHERE u.id IS NULL
ORDER BY m.id
;

-- trs modified in update
WITH q1 AS (
  SELECT map_id, array_agg(trs_path) paths
  FROM update66.trs_path
  GROUP BY map_id
), q2 AS (
  SELECT map_id, array_agg(trs_path) paths
  FROM hummaps.trs_path
  GROUP BY map_id
), q3 AS (
  SELECT map_id, q1.paths paths
  FROM update66.trs_path u
  JOIN q1 USING (map_id)
  LEFT JOIN q2 USING (map_id)
  WHERE NOT u.trs_path @> ANY (q2.paths)
  GROUP BY map_id, q1.paths
)
SELECT u.id map_id,
  u.maptype, u.book, u.firstpage page, u.lastpage - u.firstpage + 1 npages,
  q3.paths::text[],
  u.recdate, u.client, u.description, u.note
FROM update66.map u
JOIN q3 ON q3.map_id = u.id
ORDER BY u.id
;

WITH q1 AS (
  SELECT map_id, array_agg(trs_path) paths
  FROM update66.trs_path
  GROUP BY map_id
), q2 AS (
  SELECT map_id, array_agg(trs_path) paths
  FROM hummaps.trs_path
  GROUP BY map_id
)
SELECT u.map_id,
  q1.paths::text[] update_paths,
  q2.paths::text[] current_paths,
  array_agg(u.trs_path)::text[] diff
FROM update66.trs_path u
JOIN q1 ON q1.map_id = u.map_id
LEFT JOIN q2 ON q2.map_id = u.map_id
WHERE NOT u.trs_path @> ANY (q2.paths)
GROUP BY u.map_id, q1.paths, q2.paths
ORDER BY u.map_id
;
