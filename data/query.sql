SELECT amenity, ST_X(way), ST_Y(way) FROM planet_osm_point
WHERE amenity = 'fuel' OR amenity = 'charging_station';


SELECT amenity, ST_X(way), ST_Y(way), 111.045 * DEGREES(ACOS(COS(RADIANS(39.05066563434664))
 * COS(RADIANS(ST_Y(way)))
 * COS(RADIANS(ST_X(way)) - RADIANS(-105.67662502733549))
 + SIN(RADIANS(39.05066563434664))
 * SIN(RADIANS(ST_Y(way)))))
 AS distance_in_km
FROM planet_osm_point
WHERE amenity = 'fuel' OR amenity = 'charging_station'
ORDER BY distance_in_km ASC
LIMIT 10;


SELECT ST_X(geo), ST_Y(geo) from stations;


HashAggregate  (cost=13857.05..13873.60 rows=1655 width=48)
HashAggregate  (cost=2663.92..2680.47 rows=1655 width=48)

SELECT amenity, ST_X(way), ST_Y(way) FROM planet_osm_point
WHERE amenity = 'fuel' OR amenity = 'charging_station'

UNION 

SELECT amenity, ST_X(geo), ST_Y(geo) from stations;



SELECT COUNT(*) FROM (SELECT 111.045 * DEGREES(ACOS(COS(RADIANS(39.05066563434664))
	* COS(RADIANS(ST_Y(way)))
	* COS(RADIANS(ST_X(way)) - RADIANS(-105.67662502733549))
	 + SIN(RADIANS(39.05066563434664))
	 * SIN(RADIANS(ST_Y(way)))))
	 AS distance_in_km
FROM planet_osm_point
WHERE amenity = 'fuel' OR amenity = 'charging_station'
ORDER BY distance_in_km ASC
LIMIT 10) AS subquery;

GroupAggregate  (cost=13777.21..13778.57 rows=68 width=64)
GroupAggregate  (cost=2640.09..2641.45 rows=68 width=64)
SELECT amenity, SUM(amenityCount) FROM(SELECT amenity, COUNT(amenity) as amenityCount FROM planet_osm_point
	WHERE amenity = 'fuel' OR amenity = 'charging_station'
	GROUP BY amenity
	UNION 
	SELECT amenity, COUNT(amenity) as amenityCount from stations
	GROUP BY amenity) AS subquery
GROUP BY amenity;


Sort  (cost=24765.69..24767.07 rows=551 width=56)
Sort  (cost=2768.66..2770.04 rows=551 width=56)
SELECT * FROM (SELECT amenity, ST_X(way), ST_Y(way), 111.045 * DEGREES(ACOS(COS(RADIANS(39.05066563434664))
        * COS(RADIANS(ST_Y(way)))
        * COS(RADIANS(ST_X(way)) - RADIANS(-105.67662502733549))
        + SIN(RADIANS(39.05066563434664))
        * SIN(RADIANS(ST_Y(way))))) AS distance_in_km FROM planet_osm_point
		WHERE amenity = 'fuel' OR amenity = 'charging_station'

		UNION

		SELECT amenity, ST_X(geo), ST_Y(geo), 111.045 * DEGREES(ACOS(COS(RADIANS(39.05066563434664))
				* COS(RADIANS(ST_Y(geo)))
				* COS(RADIANS(ST_X(geo)) - RADIANS(-105.67662502733549))
				+ SIN(RADIANS(39.05066563434664))
				* SIN(RADIANS(ST_Y(geo))))) AS distance_in_km FROM stations
		ORDER BY distance_in_km ASC) AS subquery
WHERE distance_in_km <= 50;



// duplicates
SELECT COUNT(gg) from (SELECT amenity, way as gg FROM planet_osm_point
	WHERE amenity = 'fuel' OR amenity = 'charging_station'
	UNION 
	SELECT amenity, geo as gg from stations) as subquery
GROUP BY gg
HAVING COUNT(gg) > 1;


Limit  (cost=13983.84..13983.86 rows=10 width=56)
Limit  (cost=2790.71..2790.74 rows=10 width=56)
SELECT amenity, ST_X(way), ST_Y(way), 111.045 * DEGREES(ACOS(COS(RADIANS(39.04))
        * COS(RADIANS(ST_Y(way)))
        * COS(RADIANS(ST_X(way)) - RADIANS(-105.558522))
        + SIN(RADIANS(39.04))
        * SIN(RADIANS(ST_Y(way)))))
        AS distance_in_km
        FROM planet_osm_point
        WHERE amenity = 'fuel' OR amenity = 'charging_station'
        UNION
        SELECT amenity, ST_X(geo), ST_Y(geo), 111.045 * DEGREES(ACOS(COS(RADIANS(39.04))
        * COS(RADIANS(ST_Y(geo)))
        * COS(RADIANS(ST_X(geo)) - RADIANS(-105.558522))
        + SIN(RADIANS(39.04))
        * SIN(RADIANS(ST_Y(geo)))))
        AS distance_in_km
        FROM stations
        ORDER BY distance_in_km ASC
        LIMIT 10;





create index index_planet_osm_point_on_amenity on planet_osm_point(amenity);
