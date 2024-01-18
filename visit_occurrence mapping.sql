-- bio_signal_emg 부분만 변경해서 사용
-- ECG 측정날짜가 visit_occurrence 테이블의 visit_start_date(방문시작일)과 visit_end_date(방문종료일) 사이에 있는 경우 visit_occurrence_id 매칭
UPDATE public.bio_signal_emg2
SET visit_occurrence_id = v.visit_occurrence_id
FROM (
    select distinct person_id, visit_start_date, visit_end_date, visit_occurrence_id
    from cdm.visit_occurrence vo
    order by person_id, visit_start_date, visit_end_date) v
where public.bio_signal_emg2.visit_occurrence_id IS NULL 
  and public.bio_signal_emg2.person_id = v.person_id
    and public.bio_signal_emg2.bio_signal_date BETWEEN v.visit_start_date AND v.visit_end_date;
   
-- ECG 측정날짜가 visit_occurrence 테이블의 visit_start_date(방문시작일) 3일 전과 visit_end_date(방문종료일) 3일 후 사이에 있는 경우 visit_occurrence_id 매칭
UPDATE public.bio_signal_emg2
SET visit_occurrence_id = v.visit_occurrence_id
FROM (
    select distinct person_id, visit_start_date, visit_end_date, visit_occurrence_id
    from cdm.visit_occurrence vo
    order by person_id, visit_start_date, visit_end_date) v
where public.bio_signal_emg2.visit_occurrence_id IS NULL 
  and public.bio_signal_emg2.person_id = v.person_id
    and public.bio_signal_emg2.bio_signal_date BETWEEN (v.visit_start_date - INTERVAL '3 day') AND (v.visit_end_date + INTERVAL '3 day')

SELECT
  (SELECT COUNT(*) FROM public.bio_signal_emg2 WHERE visit_occurrence_id IS NOT NULL) AS not_null_count,
  (SELECT COUNT(*) FROM public.bio_signal_emg2 WHERE visit_occurrence_id IS NULL) AS null_count,
  (SELECT COUNT(*) FROM public.bio_signal_emg2) AS total_count,
  (SELECT COUNT(*) FROM public.bio_signal_emg2 WHERE visit_occurrence_id IS NOT NULL) * 100.0 / (SELECT COUNT(*) FROM public.bio_signal_emg2) AS not_null_percentage,
  (SELECT COUNT(*) FROM public.bio_signal_emg2 WHERE visit_occurrence_id IS NULL) * 100.0 / (SELECT COUNT(*) FROM public.bio_signal_emg2) AS null_percentage;