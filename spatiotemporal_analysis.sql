-- with shp2pgsql load arrondissements/districts shapefile

SELECT * FROM gbfsparis LIMIT 10;
SELECT * FROM arrondissements LIMIT 10;

-- Add geom column
ALTER TABLE gbfsparis 
ADD COLUMN geom geometry(Point, 4326);

-- Calculate geom column
UPDATE gbfsparis SET geom = ST_SetSRID(ST_MakePoint(lon, lat), 4326);

-- Intersect parked scooters with districts

CREATE TABLE VIEW gbfsparis_summary AS
SELECT
scooters_district.district, 
scooters_district.quantity,
scooters_district.gbfsreports_id,
EXTRACT(DAY FROM gbfsreports.date) AS report_day,
EXTRACT(HOUR FROM gbfsreports.date) AS report_hour,
district.geom
FROM arrondissements as district 
JOIN 
	(SELECT b.c_ar as district,
	  COUNT(a.*) as quantity,
	  a.gbfsreports_id
	  FROM gbfsparis as a 
	  JOIN arrondissements as b 
	  ON ST_WITHIN(a.geom, b.geom) 
	  WHERE vehicle_type = 'scooter' 
	  GROUP BY district, 
 			a.gbfsreports_id) scooters_district 
ON district.c_ar = scooters_district.district
RIGHT JOIN gbfsreports ON
scooters_district.gbfsreports_id = gbfsreports.id
GROUP BY 
		scooters_district.district,
		gbfsreports.date,
		scooters_district.quantity,
		scooters_district.gbfsreports_id,
		district.geom
ORDER BY quantity DESC;

-- Parked scooters (one day and 2 time frames)
CREATE TABLE VIEW tuesday_am_pm AS
SELECT district, report_hour, SUM(quantity) as quantity FROM gbfsparis_summary 
WHERE report_day = 14 AND (report_hour = 8 OR report_hour = 12 OR report_hour = 18)
GROUP BY district, report_hour
ORDER BY district;

-- Percentage change of parked scooters between morning and after peak hours

