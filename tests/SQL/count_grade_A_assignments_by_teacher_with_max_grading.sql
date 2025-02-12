-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH grade_counts AS (
    SELECT teacher_id, COUNT(*) AS grade_A_count
    FROM assignments
    WHERE grade = 'A' AND state = 'GRADED'
    GROUP BY teacher_id
)
SELECT COALESCE(MAX(grade_A_count), 0) AS max_grade_A_count
FROM grade_counts;