-- Write query to get count of assignments in each grade

SELECT grade, COUNT(*) AS total_assignments
FROM assignments
WHERE state = 'GRADED'
GROUP BY grade
ORDER BY grade;