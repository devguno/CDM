--1단계에서 date로 매핑, 10000개일떄 9442개 매핑완료    
-- null 인거는 +기준 이틀? 
--Test code  
UPDATE public.cdm_measurement_pft_new AS m
SET visit_occurrence_id = p.visit_occurrence_id
FROM cdm.procedure_occurrence AS p
WHERE m.person_id = p.person_id
   AND m.measurement_date = p.procedure_date
   AND m.measurement_date IS NOT NULL
   AND p.procedure_date IS NOT NULL
   AND m.measurement_datetime IN (
       SELECT measurement_datetime
       FROM public.cdm_measurement_pft_new
       ORDER BY measurement_datetime
       LIMIT 10000
   );    

/*
SELECT *
FROM public.cdm_measurement_pft_new
WHERE visit_occurrence_id is null;
*/

-- date 기준   visit_occurrence_id 업데이트 완료, 153400개 매핑(약 94%)
UPDATE public.cdm_measurement_pft_new AS m
SET visit_occurrence_id = p.visit_occurrence_id
FROM cdm.procedure_occurrence AS p
WHERE m.person_id = p.person_id
   AND m.measurement_date = p.procedure_date
   AND m.measurement_date IS NOT NULL
   AND p.procedure_date IS NOT NULL;
  
  
UPDATE public.cdm_measurement_pft_new AS m
SET visit_occurrence_id = p.visit_occurrence_id
FROM cdm.procedure_occurrence AS p
WHERE m.person_id = p.person_id
   AND m.visit_occurrence_id IS NULL
   AND p.procedure_date IS NOT NULL
   AND p.procedure_date <= (m.measurement_date + INTERVAL '3 days');
--18485 updated Rows, 나머지 508개 null


