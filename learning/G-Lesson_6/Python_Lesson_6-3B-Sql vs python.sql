use TutorialDB
--select
--Select all data
SELECT  *
FROM fert_data

--Select 5 first rows 
SELECT top 5 *
FROM fert_data

-- select 5 last rows
SELECT top 5 *
FROM fert_data
ORDER BY region DESC

-- Select specific columns
SELECT  country,
		tfr
FROM fert_data

-- where
SELECT *
FROM fert_data
WHERE tfr BETWEEN 5.5 AND 7 AND region != 'Africa'

-- insert
INSERT INTO fert_data(country, region, tfr, contraceptors)
VALUES ('Japan','Asia',1.73,73)

--update
UPDATE fert_data
SET contraceptors = '65'
WHERE country = 'Mauitius'

--delete
DELETE FROM fert_data
WHERE region = 'Asia'

-- joins
SELECT * 
FROM fert_data as f 
	INNER JOIN country_sub_region as c
	  ON f.country = c.country

--Union
SELECT * 
FROM fert_data_1
UNION ALL
SELECT * FROM fert_data
ORDER BY country
--
SELECT * 
FROM fert_data_1
UNION 
SELECT * FROM fert_data
ORDER BY country

--Group by
SELECT	region, 
		round(avg(tfr),2) as rtf_mean, 
		count(contraceptors) as count_contraceptors
FROM fert_data
GROUP BY region


