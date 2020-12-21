select t.hisid 单据号,
       t.patient_id 参保人编码,
       t.patient_name 参保人姓名,
       t.hospital_name 医院名称,
       to_char(t.billdate, 'yyyy-mm-dd') 结算日期
  from DW_BILL t
 where t.table_par >= &begin_mon
   and t.table_par <= &end_mon
