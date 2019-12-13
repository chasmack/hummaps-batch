WITH q1 AS (
    SELECT DISTINCT map.id,
        map.book, map.page, map.npages,
        map.recdate, map.client, map.description,
        maptype.maptype, maptype.abbrev
    FROM hummaps.map
    JOIN hummaps.maptype ON map.maptype_id = maptype.id
    JOIN hummaps.trs_path ON trs_path.map_id = map.id
    LEFT JOIN hummaps.signed_by ON signed_by.map_id = map.id
    LEFT JOIN hummaps.surveyor ON signed_by.surveyor_id = surveyor.id
    WHERE
        -- maptype.abbrev IN ('RS', 'RM', 'PM', 'UR') AND
        -- trs.tshp = 6 AND trs.rng = 4 AND
        -- (
        --     trs.sec = 28 AND (trs.subsec & 51 > 0) OR
        --     trs.sec = 29 ) AND
        -- (
        trs_path.trs_path <@ '2S.3E.24'::ltree AND
        --     surveyor.fullname ~* 'hern' OR
        --     surveyor.pls ~* '4446' OR
        --     surveyor.rce ~* '28556'
        -- ) AND
        -- map.id IN (14225) AND
        -- map.recdate BETWEEN '1980-1-1' AND '2010-12-31' AND
        -- map.client ~* 'pavlich' AND
        -- map.description ~* 'campton' AND
        TRUE

), surveyor_agg AS (
    SELECT id, array_agg(surveyor) AS surveyors
    FROM (
        SELECT q1.id,
            initcap(s.fullname) AS surveyor
        FROM q1
        JOIN hummaps.signed_by AS sb ON sb.map_id = q1.id
        JOIN hummaps.surveyor AS s ON sb.surveyor_id = s.id
        ORDER BY s.lastname, s.firstname
    ) AS q
    GROUP BY id

), mapimage_agg AS (
    SELECT id, array_agg(imagefile) AS imagefiles
    FROM (
        SELECT q1.id, map_image.imagefile
        FROM q1
        JOIN hummaps.map_image ON map_image.map_id = q1.id
        ORDER BY map_image.imagefile ASC
    ) AS q
    GROUP BY id

), ccimage_agg AS (
    SELECT id, array_agg(cc) AS ccs
    FROM (
        SELECT id,
        CASE WHEN count(imagefile) > 0
        THEN doc_number || array_agg(imagefile)
        ELSE ARRAY[doc_number] END AS cc
        FROM (
            SELECT q1.id, cc.doc_number, cc_image.imagefile
            FROM q1
            JOIN hummaps.cc ON cc.map_id = q1.id
            LEFT JOIN hummaps.cc_image on cc_image.cc_id = cc.id
            ORDER BY cc.doc_number, cc_image.imagefile
        ) AS a
        GROUP BY id, doc_number
    ) AS b
    GROUP BY id

)
SELECT q1.id,
    hummaps.map_name(q1.id) map,
    recdate, client, description,
    coalesce(surveyor_agg.surveyors, '{}') AS surveyors,
    coalesce(mapimage_agg.imagefiles, '{}') AS imagefiles,
    coalesce(ccimage_agg.ccs, '{}') AS ccs,
    pdf.pdffile
FROM q1
LEFT JOIN surveyor_agg ON surveyor_agg.id = q1.id
LEFT JOIN mapimage_agg ON mapimage_agg.id = q1.id
LEFT JOIN ccimage_agg ON ccimage_agg.id = q1.id
LEFT JOIN hummaps.pdf ON pdf.map_id = q1.id
ORDER BY abbrev, book DESC, page ASC
;