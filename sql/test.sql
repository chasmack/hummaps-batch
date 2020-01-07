
SELECT DISTINCT map.book, maptype.maptype, map.page,
  initcap(surveyor.fullname) AS surveyor
FROM hummaps.map
JOIN hummaps.maptype ON map.maptype_id = maptype.id
JOIN hummaps.trs_path ON trs_path.map_id = map.id
LEFT JOIN hummaps.signed_by ON signed_by.map_id = map.id
LEFT JOIN hummaps.surveyor ON signed_by.surveyor_id = surveyor.id
WHERE
  maptype.maptype = 'Parcel Map' AND
  trs_path.trs_path <@ '2S.3E.11'::ltree AND
  map.recdate BETWEEN '1960-1-1' AND '1980-1-1'
;

