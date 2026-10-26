--User with higher count
SELECT lbfa."User full name" ,COUNT(*) as usage_count 
FROM logs_BLFOM_for_analysis lbfa 
GROUP BY lbfa."User full name"
ORDER BY COUNT(*) DESC; 

--Forum Eng

SELECT lbfa.Component, COUNT("component") as total_forum_count
FROM logs_BLFOM_for_analysis lbfa 
WHERE lbfa.Component = "Forum"
GROUP BY Component; -- 22,941

--Total count of the given dataset

SELECT COUNT(*) FROM logs_BLFOM_for_analysis lbfa; --3,41,871


--Forum created
SELECT lbfa.Component, COUNT(lbfa.Component) as total_forum_count
FROM logs_BLFOM_for_analysis lbfa 
WHERE lbfa.Component = "Forum"
AND lbfa."Event name" IN ("Post created", "Discussion created")
GROUP BY lbfa.Component; -- 2,741

-- Unique Event names
SELECT DISTINCT(lbfa."Event name") as event_name_unique
FROM logs_BLFOM_for_analysis lbfa; -- Unique Event names


--For each time range
--12PM to 6 PM
SELECT
SUM(CASE WHEN substr(lbfa.time, instr(lbfa.time, ',') +2) between "12:00:01" and "18:00:00" THEN 1 ELSE 0 end) as twelve_to_six_PM
FROM logs_BLFOM_for_analysis lbfa; --1,38,090

-- 6 AM to 12 PM
SELECT
SUM(CASE WHEN substr(lbfa.time, instr(lbfa.time, ',') +2) between "06:00:01" and "12:00:00" THEN 1 ELSE 0 end) as six_to_twelve_pM
FROM logs_BLFOM_for_analysis lbfa; --66,078


-- 6 PM to 12 AM
SELECT
SUM(CASE WHEN substr(lbfa.time, instr(lbfa.time, ',') +2) between '18:00:01' AND '23:59:59' THEN 1 ELSE 0 end) as six_to_twelve_pM
FROM logs_BLFOM_for_analysis lbfa; --1,12,081


-- 12 AM to 6 AM

SELECT
SUM(CASE WHEN substr(lbfa.time, instr(lbfa.time, ',') +2) between "00:00:01" and "06:00:00" THEN 1 ELSE 0 end) as six_to_twelve_pM
FROM logs_BLFOM_for_analysis lbfa; --15,054



--All together
SELECT
CASE WHEN substr(time, instr(time, ',') + 2) BETWEEN '00:00:00' AND '06:00:00' THEN '12 AM - 6 AM'
	 WHEN substr(time, instr(time, ',') + 2) BETWEEN '06:00:01' AND '12:00:00' THEN '6 AM - 12 PM'
	 WHEN substr(time, instr(time, ',') + 2) BETWEEN '12:00:01' AND '18:00:00' THEN '12 PM - 6 PM'
	 WHEN substr(time, instr(time, ',') + 2) BETWEEN '18:00:01' AND '23:59:59' THEN '6 PM - 12 AM' 
	 END AS time_range,
COUNT(*) AS total
FROM logs_BLFOM_for_analysis lbfa
GROUP BY time_range;