column spf new_value spf noprint
select 'check_database_' || instance_name ||'_'||  to_char(sysdate, 'yyyy_mm_dd') || '.log' spf from  v$instance;

spool &spf
SET LINESIZE 300
set pagesize 10000




prompt **************************** 勒索病毒检测(显示为空正常) ************************************;
select 'DROP TRIGGER '||owner||'."'||TRIGGER_NAME||'";' from dba_triggers where
TRIGGER_NAME like 'DBMS_%_INTERNAL%'
union all
select 'DROP PROCEDURE '||owner||'."'||a.object_name||'";' from dba_procedures a
where a.object_name like 'DBMS_%_INTERNAL% ';

prompt **************************** 数据库字符集 和 服务器端字符集************************************;
column db_characters format a30
column db_server_characters format a30
select a.value||'_'||b.value||'.'||c.value as "db_characters", d.lg as "db_server_characters" from (select value from NLS_DATABASE_PARAMETERS where parameter='NLS_LANGUAGE') a,
(select value from NLS_DATABASE_PARAMETERS where parameter='NLS_TERRITORY') b,
(select value from NLS_DATABASE_PARAMETERS where parameter='NLS_CHARACTERSET') c,
(select userenv('language') as lg from dual) d;

prompt **************************** 实例状态 和 会话情况 ************************************;
column instance_name format a20
column host_name format a30
column uptime format a20
select a.instance_name,
       a.host_name,
       a.version,
       a.status,
       a.archiver,
       round(sysdate - startup_time) || 'day' as uptime,
	   b.sessions_current,
	   b.sessions_highwater
  from v$instance a,v$license b;

prompt ****************************  检查rman备份情况 ************************************;
column start_time FORMAT a20
column input_type FORMAT a15
column in_sec FORMAT a13
column out_sec FORMAT a13
column in_size FORMAT a10
column out_size FORMAT a10
column compression_ratio FORMAT a17
select *
  from (select to_char(start_time, 'yyyy-mm-dd hh24:mi:ss') start_time,
               to_char(end_time, 'yyyy-mm-dd hh24:mi:ss') end_time,
               time_taken_display as elapsed_time,
               input_type,
               status,
               input_bytes_display in_size,
               output_bytes_display out_size,
               input_bytes_per_sec_display in_sec,
               output_bytes_per_sec_display out_sec,
               trunc(compression_ratio, 2) * 100 || '%' compression_ratio
          from v$rman_backup_job_details
         order by start_time desc)
 where rownum <= 15;

prompt **************************** 查询数据库坏块 **************************;
select * from v$database_block_corruption;

prompt **************************** 控制文件状态 ***********************************;
column name format a80
select status,name from v$controlfile;

prompt **************************** 日志文件状态 ***********************************;
select group#,thread#,bytes/1024/1024 MB,archived,status from v$log;

prompt **************************** redo日志切换间隔 *******************************;
select *
  from (select to_char(first_time, 'yyyy-mm-dd hh24:mi:ss') first_time,
               round(24 * 60 * (lead(first_time, 1)
                      over(order by first_time) - first_time),
                     2) minutes
          from v$log_history v
         where recid >= 3654
         order by first_time desc)
 where rownum <= 24;

prompt **************************** 每日归档量统计 **************************;
select *
  from (  select trunc (completion_time), sum (mb) day_mb
            from (select name,
                         completion_time,
                         blocks * block_size / 1024 / 1024 mb
                    from v$archived_log)
        group by trunc (completion_time)
        order by trunc (completion_time) desc)
 where rownum <= 10;

prompt ***************************** 归档目的地状态 *********************************;
column dest_name format a40
column destination format a80

select dest_name, status, database_mode, destination
 from v$archive_dest_status
where database_mode = 'OPEN';


prompt ********************** 表空间监控(used_pct_of_max大于85%为异常) ********************;
column tablespace_name format a40
column used_pct_of_max format a20
select /*+NO_UNNEST*/a.tablespace_name,
       round(a.bytes_alloc / 1024 / 1024) megs_alloc,
       round(nvl(b.bytes_free, 0) / 1024 / 1024) megs_free,
       round((a.bytes_alloc - nvl(b.bytes_free, 0)) / 1024 / 1024) megs_used,
       round((nvl(b.bytes_free, 0) / a.bytes_alloc) * 100) Pct_Free,
       100 - round((nvl(b.bytes_free, 0) / a.bytes_alloc) * 100) Pct_used,
       round(maxbytes / 1048576) Max,
       round(round((a.bytes_alloc - nvl(b.bytes_free, 0)) / 1024 / 1024) /
             round(maxbytes / 1048576),
             2) * 100 || '%' used_pct_of_max
  from (select f.tablespace_name,
               sum(f.bytes) bytes_alloc,
               sum(decode(f.autoextensible, 'YES', f.maxbytes, 'NO', f.bytes)) maxbytes
          from dba_data_files f
         group by tablespace_name) a,
       (select f.tablespace_name, sum(f.bytes) bytes_free
          from dba_free_space f
         group by tablespace_name) b
 where a.tablespace_name = b.tablespace_name(+)
union all
select /*+NO_UNNEST*/h.tablespace_name,
       round(sum(h.bytes_free + h.bytes_used) / 1048576) megs_alloc,
       round(sum((h.bytes_free + h.bytes_used) - nvl(p.bytes_used, 0)) /
             1048576) megs_free,
       round(sum(nvl(p.bytes_used, 0)) / 1048576) megs_used,
       round((sum((h.bytes_free + h.bytes_used) - nvl(p.bytes_used, 0)) /
             sum(h.bytes_used + h.bytes_free)) * 100) Pct_Free,
       100 -
       round((sum((h.bytes_free + h.bytes_used) - nvl(p.bytes_used, 0)) /
             sum(h.bytes_used + h.bytes_free)) * 100) pct_used,
       round(sum(f.maxbytes) / 1048576) max,
       round(round(sum(nvl(p.bytes_used, 0)) / 1048576) /
             round(sum(f.maxbytes) / 1048576),
             2) * 100 || '%' used_pct_of_max
  from sys.v_$TEMP_SPACE_HEADER h,
       sys.v_$Temp_extent_pool  p,
       dba_temp_files           f
 where p.file_id(+) = h.file_id
   and p.tablespace_name(+) = h.tablespace_name
   and f.file_id = h.file_id
   and f.tablespace_name = h.tablespace_name
   --and f.autoextensible = 'YES'
 group by h.tablespace_name
 ORDER BY 1;

prompt **************************** 表空间最近一周的使用情况 **************************;
select a.name,
       b.tablespace_id,
       min(datetime),
       min(used_size_mb),
       max(datetime),
       max(used_size_mb),
       max(used_size_mb) - min(used_size_mb) increase_mb
  from v$tablespace a,
       (select tablespace_id,
               trunc(to_date(rtime, 'mm/dd/yyyy hh24:mi:ss')) datetime,
               round(max(tablespace_usedsize * 8 / 1024), 2) used_size_mb
          from dba_hist_tbspc_space_usage
         where trunc(to_date(rtime, 'mm/dd/yyyy hh24:mi:ss')) >
               trunc(sysdate - 30)
         group by tablespace_id,
                  trunc(to_date(rtime, 'mm/dd/yyyy hh24:mi:ss'))
         order by tablespace_id,
                  trunc(to_date(rtime, 'mm/dd/yyyy hh24:mi:ss'))) b
 where a.ts# = b.tablespace_id
 group by name, tablespace_id
 order by increase_mb desc;

prompt **************************** 表空间OFFLINE(显示为空正常) ********************;
select tablespace_name ,status  from dba_tablespaces where status='OFFLINE';

prompt ****************************  undo表空间使用情况  **************************;
SELECT s.username,
       s.sid,
       pr.PID,
       s.OSUSER,
       s.MACHINE,
       s.PROGRAM,
       rs.segment_id,
       r.usn,
       rs.segment_name,
       r.rssize/1024/1024,
       sq.sql_text
  FROM v$transaction t, v$session s, v$rollstat r, dba_rollback_segs rs ,v$sql  sq,v$process pr
WHERE s.saddr = t.ses_addr
   AND t.xidusn = r.usn
   AND rs.segment_id = t.xidusn
   AND s.sql_address=sq.address
   AND s.sql_hash_value = sq.hash_value
   AND s.PADDR=pr.ADDR
ORDER BY t.used_ublk DESC


prompt ****************************  user占用临时表空间情况  **************************;
COLUMN sid_serial FORMAT A20
COLUMN username FORMAT A15
COLUMN program FORMAT A30
COLUMN undoseg FORMAT A25
COLUMN undo FORMAT A20
COLUMN MACHINE FORMAT A25
COLUMN OSUSER FORMAT A15
COLUMN CLIENT_INFO FORMAT A15
COLUMN MODULE FORMAT A15

SELECT vt.inst_id,
       vs.sid,
       vs.serial#,
       vs.username,
       vs.osuser,
       vs.machine,
       vs.saddr,
       vs.client_info,
       vs.program,
       vs.module,
       vs.logon_time,
       vt.tempseg_usage,
       vt.segtype
  FROM gv$session vs,
       (SELECT inst_id,
               username,
               session_addr,
               segtype,
               ROUND(SUM(blocks) * 8192 / 1024 / 1024 / 1024, 2) tempseg_usage
          FROM gv$tempseg_usage
         GROUP BY inst_id, username, session_addr, segtype
         ORDER BY 4 DESC) vt
 WHERE vs.inst_id = vt.inst_id
   AND vs.saddr = vt.session_addr
 order by tempseg_usage desc;


prompt ****************************  查看锁和等待时间，如果长期占用且没有释放的锁，需DBA手工处理  **************************;
select s.sid,
       s.serial#,
       l.locked_mode,
       s.username,
       o.object_name,
       -- s.osuser,
       -- s.machine,
       s.logon_time,
       s.last_call_et
  from v$locked_object l, all_objects o, v$session s
 where l.object_id = o.object_id
   and l.session_id = s.sid
 order by sid, s.serial#;


prompt ****************************  查看锁竞争状态  **************************;
col SQL_ID for a15
col SESS for a30
col event for a30
select decode (request,0,'holder:','waiter:')|| s.inst_id || ':' || s.sid||','||s.SERIAL# sess,lmode,request,l.type,l.ctime
        ,s.sql_id,s.event,s.last_call_et
         from gv$lock l,gv$session s
        where (l.id1,l.id2,l.type) in
        (select id1,id2,type from gv$lock where request>0)
        and l.sid=s.sid and l.inst_id=s.inst_id
        order by 1;

prompt **************************** 查询失效索引 全局级别 ********************;
Select owner, index_name, status
  From dba_indexes
 where status = 'UNUSABLE'
   and owner not in ('SYS',
                     'SYSTEM',
                     'SYSMAN',
                     'EXFSYS',
                     'WMSYS',
                     'OLAPSYS',
                     'OUTLN',
                     'DBSNMP',
                     'ORDSYS',
                     'ORDPLUGINS',
                     'MDSYS',
                     'CTXSYS',
                     'AURORA$ORB$UNAUTHENTICATED',
                     'XDB',
                     'FLOWS_030000',
                     'FLOWS_FILES',
                     'APEX_030200',
                     'ORDDATA')
 order by 1, 2 ;

prompt **************************** 查询失效索引 分区级别 ********************;
select index_owner, index_name, partition_name
  from dba_ind_partitions
 where status ='UNUSABLE'
   and index_owner not in ('SYS',
                           'SYSTEM',
                           'SYSMAN',
                           'EXFSYS',
                           'WMSYS',
                           'OLAPSYS',
                           'OUTLN',
                           'DBSNMP',
                           'ORDSYS',
                           'ORDPLUGINS',
                           'MDSYS',
                           'CTXSYS',
                           'AURORA$ORB$UNAUTHENTICATED',
                           'XDB',
                           'FLOWS_030000',
                           'FLOWS_FILES',
                           'APEX_030200',
                           'ORDDATA') order by 1,2;

prompt **************************** 查询失效索引 子分区级别 ******************;
Select
       Index_Owner
     , Index_Name
     , partition_name
     , SUBPARTITION_NAME
 From
       DBA_IND_SUBPARTITIONS
Where
       status = 'UNUSABLE'
       and index_owner not in ('SYS',
                               'SYSTEM',
                               'SYSMAN',
                               'EXFSYS',
                               'WMSYS',
                               'OLAPSYS',
                               'OUTLN',
                               'DBSNMP',
                               'ORDSYS',
                               'ORDPLUGINS',
                               'MDSYS',
                               'CTXSYS',
                               'AURORA$ORB$UNAUTHENTICATED',
                               'XDB',
                               'FLOWS_030000',
                               'FLOWS_FILES',
                               'APEX_030200',
                               'ORDDATA') ORDER BY 1, 2;



prompt **************************** memory_resize_ops **************************;
SET LINESIZE 200
COLUMN parameter FORMAT A25
COLUMN component FORMAT A25
select *
  from (SELECT start_time,
               end_time,
               component,
               oper_type,
               oper_mode,
               parameter,
               ROUND(initial_size / 1024 / 1204) AS initial_size_mb,
               ROUND(target_size / 1024 / 1204) AS target_size_mb,
               ROUND(final_size / 1024 / 1204) AS final_size_mb,
               status
          FROM v$memory_resize_ops
         ORDER BY start_time desc)
 where rownum <= 10;


prompt **************************** 查询表nologging **************************;
select owner, table_name, logging
  from dba_tables
 where logging = 'NO'
   and owner not in ('SYS',
                     'SYSTEM',
                     'SYSMAN',
                     'EXFSYS',
                     'WMSYS',
                     'OLAPSYS',
                     'OUTLN',
                     'DBSNMP',
                     'ORDSYS',
                     'ORDPLUGINS',
                     'MDSYS',
                     'CTXSYS',
                     'AURORA$ORB$UNAUTHENTICATED',
                     'XDB',
                     'FLOWS_030000',
                     'APEX_030200',
                     'FLOWS_FILES',
                     'ORDDATA')
 order by 1, 2;

prompt **************************** 查询分区表nologging **************************;
select table_owner, table_name,partition_name, logging
  from dba_tab_partitions
 where logging = 'NO'
   and table_owner not in ('SYS',
                           'SYSTEM',
                           'SYSMAN',
                           'EXFSYS',
                           'WMSYS',
                           'OLAPSYS',
                           'OUTLN',
                           'DBSNMP',
                           'ORDSYS',
                           'ORDPLUGINS',
                           'MDSYS',
                           'CTXSYS',
                           'AURORA$ORB$UNAUTHENTICATED',
                           'XDB',
                           'FLOWS_030000',
                           'FLOWS_FILES',
                           'APEX_030200',
                           'ORDDATA')
 order by 1, 2;

prompt ****************************  监控排序，硬盘中排序于在内存中排序的比例应该小于5%  **************************;
select disk.value "Disk",mem.value "Mem",trunc((disk.value/mem.value)*100,2)||'%' "Ratio"
from v$sysstat mem, v$sysstat disk
where mem.name='sorts (memory)' and disk.name='sorts (disk)';

prompt ****************************  库缓冲区的重用率(最好保持在95%以上，不能低于90%)  ************************************;
col Libcache_hit_ratio for a10
select trunc((sum(pins-reloads))*100/sum(pins),2)||'%' "Libcache_hit_ratio",
    DECODE (trunc((sum(pins-reloads))*100/sum(pins)),99,'very good',
                                                     98,'good',
                                                     97,'good less',
                                                     96,'generally',
                                                     95,'generally less',
                                                        'very bad') "Notice"
from v$librarycache;

prompt ****************************  数据字典缓冲区的命中率(最好保持在95%以上，不能低于90%)  ************************************;
col Rowcache_hit_ratio for a10
select trunc((sum(gets-getmisses-usage-fixed))*100/sum(gets),2)||'%' "Rowcache_hit_ratio",
    DECODE (trunc((sum(gets-getmisses-usage-fixed))*100/sum(gets)),99,'very good',
                                                                   98,'good',
                                                                   97,'good less',
                                                                   96,'generally',
                                                                   95,'generally less',
                                                                      'very bad') "Notice"
from v$rowcache;

prompt ****************************  数据缓冲区(最好保持在95%以上，不能低于90%)  ************************************;
col Buffercache_hit_ratio for a20
select trunc(100*(1-(physical_reads/(db_block_gets+consistent_gets))),2)||'%' "Buffercache_hit_ratio",
    DECODE (trunc(100*(1-(physical_reads/(db_block_gets+consistent_gets)))),99,'very good',
                                                                            98,'good',
                                                                            97,'good less',
                                                                            96,'generally',
                                                                            95,'generally less',
                                                                               'very bad') "Notice"
from v$buffer_pool_statistics;

prompt ****************************  获得数据文件物理读写和数据块读写信息,观察I/O异常，如果发现值过大采用手工条带化的方式缓解I/O  **************************;
col file for a60;
select df.tablespace_name name,
    --df.file_name "file",
    sum(f.phyrds) phyrds,
    sum(f.phyblkrd) phyblkrd,
    sum(f.phywrts) phywrts,
    sum(f.phyblkwrt) phyblkwrt
from v$filestat f, dba_data_files df where f.file# = df.file_id
group by df.tablespace_name
order by df.tablespace_name;

prompt ****************************  表碎片统计,依赖统计信息准确性  **************************;
select *
  from (select owner,
               table_name,
               (blocks * 8192 / 1024 / 1024) -
               substr((num_rows * avg_row_len / 1024 / 1024), 0, 4) "Data lower than HWM in MB"
          from dba_tables
         where owner not in ('SYS',
                             'SYSTEM',
                             'MGMT_VIEW',
                             'DBSNMP',
                             'SYSMAN',
                             'SCOTT',
                             'OUTLN',
                             'OLAPSYS',
                             'SI_INFORMTN_SCHEMA',
                             'OWBSYS',
                             'ORDPLUGINS',
                             'XDB',
                             'ANONYMOUS',
                             'CTXSYS',
                             'ORDDATA',
                             'OWBSYS_AUDIT',
                             'APEX_030200',
                             'APPQOSSYS',
                             'WMSYS',
                             'EXFSYS',
                             'ORDSYS',
                             'MDSYS',
                             'FLOWS_FILES',
                             'SPATIAL_WFS_ADMIN_USR',
                             'SPATIAL_CSW_ADMIN_USR',
                             'HR',
                             'APEX_PUBLIC_USER',
                             'OE',
                             'DIP',
                             'SH',
                             'IX',
                             'MDDATA',
                             'PM',
                             'BI',
                             '$NULL',
                             'ORACLE_OCM',
                             'DBA',
                             'IMP_FULL_DATABASE',
                             'OLAP_DBA',
                             'EXP_FULL_DATABASE',
                             'DATAPUMP_IMP_FULL_DATABASE')
           and (num_rows * avg_row_len / 1024 / 1024) is not null
         order by "Data lower than HWM in MB" desc)
 where rownum <= 10;

prompt **************************** 检查行迁移TOP20的表 **************************;
select *
  from (select table_name,
               num_rows,
               CHAIN_CNT,
               ROUND((CHAIN_CNT / num_rows) * 100, 2) as "RT%"
          from dba_tables
         where num_rows > 0
           and CHAIN_CNT > 0
         order by CHAIN_CNT / num_rows desc)
 where rownum <= 20;

prompt **************************** 监控asm状态磁盘使用率，asm磁盘使用率大于85%异常 **************************;
SELECT group_number,
       name,
       state,
       total_mb,
       free_mb,
       (1 - trunc(free_mb / total_mb, 2)) * 100 || '%' as pct_used
  FROM V$ASM_DISKGROUP;


--prompt **************************** 监控热块 **************************;
--Select decode(pd.bp_id,
--              1,
--              'KEEP',
--              2,
--              'RECYCLE',
--              3,
--              'DEFAULT',
--              4,
--              '2K SUBCACHE',
--              5,
--              '4K SUBCACHE',
--              6,
--              '8K SUBCACHE',
--              7,
--              '16K SUBCACHE',
--              8,
--              '32K SUBCACHE',
--              'UNKNOWN') subcache,
--       bh.object_name object_name,
--       bh.blocks,
--       tch
--  from x$kcbwds ds,
--       x$kcbwbpd pd,
--       (select set_ds, o.name object_name, count(*) BLOCKS, sum(tch) tch
--          from sys.obj$ o, sys.x$bh x
--         where o.dataobj# = x.obj
--           and x.state != 0
--           and o.owner# in (select a.user_id
--                             from dba_users a
--                           )
--         group by set_ds, o.name) bh
-- where ds.set_id >= pd.bp_lo_sid
--   and ds.set_id <= pd.bp_hi_sid
--   and pd.bp_size != 0
--   and ds.addr = bh.set_ds
--   AND TCH > 2000
-- order by subcache, object_name;


prompt **************************** 查询用户************************************;
select username, user_id, default_tablespace, temporary_tablespace,account_status
  from dba_users
 where account_status <>  'EXPIRED '||'&'||' LOCKED'
   and username not in ('SYS',
                        'SYSTEM',
                        'SYSMAN',
                        'EXFSYS',
                        'WMSYS',
                        'OLAPSYS',
                        'OUTLN',
                        'DBSNMP',
                        'ORDSYS',
                        'ORDPLUGINS',
                        'MDSYS',
                        'CTXSYS',
                        'AURORA$ORB$UNAUTHENTICATED',
                        'XDB',
                        'FLOWS_030000',
                        'FLOWS_FILES',
                        'APEX_030200',
                        'ORDDATA');

prompt **************************** 查询具有DBA角色的用户************************************;

select * from dba_role_privs where grantee not in('SYSTEM','SYS') and granted_role='DBA' order by grantee;


prompt **************************** 查看用户系统权限************************************;
set linesize 200;
select * from dba_sys_privs where grantee in(select grantee from dba_role_privs where granted_role='DBA' and grantee not in('SYS','SYSTEM') )order by grantee;



prompt **************************** 查看用户的对象权限************************************;
select grantee,owner,table_name,privilege from dba_tab_privs where grantee in(select grantee from dba_role_privs where granted_role='DBA' and grantee not in('SYS','SYSTEM') )order by grantee;

prompt **************************** 查看用户default role************************************;
select grantee,default_role,granted_role from dba_role_privs where grantee  in(select grantee from dba_role_privs where granted_role='DBA' and grantee not in('SYS','SYSTEM') )order by grantee;


prompt **************************** 查看用户系统权限************************************;
select * from dba_sys_privs where grantee not in
('SYS','SYSTEM','MGMT_VIEW','DBSNMP','SYSMAN','SCOTT','OUTLN','OLAPSYS',
'SI_INFORMTN_SCHEMA','OWBSYS','ORDPLUGINS','XDB','ANONYMOUS','CTXSYS',
'ORDDATA','OWBSYS_AUDIT','APEX_030200','APPQOSSYS','WMSYS','EXFSYS',
  'ORDSYS','MDSYS','FLOWS_FILES','SPATIAL_WFS_ADMIN_USR',
'SPATIAL_CSW_ADMIN_USR','HR','APEX_PUBLIC_USER','OE','DIP','SH','IX','MDDATA','PM','BI','$NULL','ORACLE_OCM','DBA','IMP_FULL_DATABASE','OLAP_DBA',
'EXP_FULL_DATABASE','DATAPUMP_IMP_FULL_DATABASE')
and privilege like '%ANY%' order by grantee;

prompt **************************** 查看补丁信息************************************;
select * from dba_registry_history;


prompt **************************** 查看失效信息************************************;
select 'Alter '||object_type||' '||owner||'.'||object_name||' compile;' from dba_objects where status = 'INVALID';

prompt **************************** 查看用户目前数据量************************************;
select owner, round(sum(bytes / 1024 / 1024 / 1024), 2) GB
  from dba_segments t
 where owner not in ('SYS',
                     'SYSTEM',
                     'SYSMAN',
                     'EXFSYS',
                     'WMSYS',
                     'OLAPSYS',
                     'OUTLN',
                     'DBSNMP',
                     'ORDSYS',
                     'ORDPLUGINS',
                     'MDSYS',
                     'CTXSYS',
                     'AURORA$ORB$UNAUTHENTICATED',
                     'XDB',
                     'FLOWS_030000',
                     'FLOWS_FILES',
                     'APEX_030200',
                     'ORDDATA')
 group by owner
 order by GB desc;

--prompt **************************** 查看数据文件可收缩空间************************************;
--SELECT
--   a.file_id,
--   a.file_name
--   file_name,
--   CEIL( ( NVL( hwm,1 ) * blksize ) / 1024 / 1024 ) smallest,
--   CEIL( blocks * blksize / 1024 / 1024 ) currsize,
--   CEIL( blocks * blksize / 1024 / 1024 ) -
--   CEIL( ( NVL( hwm,1) * blksize ) / 1024 / 1024 ) savings,
--   'alter database datafile ''' || file_name || ''' resize ' ||
--   CEIL( ( NVL( hwm,1) * blksize ) / 1024 / 1024 + 100)  || 'm;' cmd
--FROM
--   DBA_DATA_FILES a,
--   (
--      SELECT   file_id, MAX( block_id + blocks - 1 ) hwm
--      FROM     DBA_EXTENTS
--      GROUP BY file_id
--   ) b,
--   (
--      SELECT  TO_NUMBER( value ) blksize
--      FROM    V$PARAMETER
--      WHERE   name = 'db_block_size'
--   )
--WHERE
--   a.file_id = b.file_id(+)
--AND
--   CEIL( blocks * blksize / 1024 / 1024 ) - CEIL( ( NVL( hwm, 1 ) * blksize ) / 1024 / 1024 ) > 100
--AND a.tablespace_name not in ('SYSAUX','SYSTEM')
--ORDER BY 5 desc;



prompt **************************** 查看数据库历史等待事件 **************************;
select event,count(*) from v$active_session_history  group by event order by count(*) desc;
prompt
prompt **************************** 查看数据库告警日志 **************************;
set echo off
set veri off
set feedback off
drop table alert_log_view;
declare
  path_bdump varchar2(4000);
  name_alert varchar2(4000);
  ins_name   varchar2(200);
begin
  select value
    into path_bdump
    from sys.v_$parameter
    where name = 'background_dump_dest';
  select 'alert_' || value || '.log'
    into name_alert
    from sys.v_$parameter
    where name = 'instance_name';
  select value
    into ins_name
    from sys.v_$parameter
    where name = 'instance_number';
  if ins_name = '0' then
    ins_name := '';
  end if;
  execute immediate 'create or replace directory bdump'||ins_name||' as ''' || path_bdump || '''';
  execute immediate 'create table ALERT_LOG_VIEW' ||
                    '  (MSG_line varchar2(4000)   ) ' ||
                    ' organization external ' || ' (type oracle_loader ' ||
                    ' default directory bdump' || ins_name ||
                    ' access parameters ( ' ||
                    ' records delimited by newline ' || ' nobadfile ' ||
                    ' nologfile ' || ' nodiscardfile ' || ' skip 3 ' ||
                    ' READSIZE 10485760 ' || ' FIELDS LDRTRIM ' ||
                    ' REJECT ROWS WITH ALL NULL FIELDS ' ||
                    ' (MSG_LINE (1:1000) CHAR(1000)) ' || ' ) ' ||
                    ' location (''' || name_alert || ''') )' ||
                    ' reject limit unlimited ' ||
                    ' noparallel nomonitoring ';
end;
/
col lineno noprint
col ora_error noprint
col msg_line format a132
set pages 0 lines 300 trimspool on trim on
alter session set nls_date_language = 'american';
alter session set nls_date_format='dd/mm/yyyy hh24:mi:ss';
alter session set sql_trace=false;
break on thedate
prompt
prompt ERROR IN ALERT LOG FILE - LAST 3 DAYS
prompt =====================================
set feedback on
select "LINENO", "THEDATE", "ORA_ERROR", "MSG_LINE"
  from (select *
          from (select lineno,
                       msg_line,
                       thedate,
                       max(case
                             when (ora_error like 'ORA-%' or
                                  ora_error like 'PLS-%') then
                              rtrim(substr(ora_error, 1, instr(ora_error, ' ') - 1),
                                    ':')
                             else
                              null
                           end) over(partition by thedate) ora_error
                  from (select lineno,
                               msg_line,
                               max(thedate) over(order by lineno) thedate,
                               lead(msg_line) over(order by lineno) ora_error
                          from (select rownum lineno,
                                       substr(msg_line, 1, 132) msg_line,
                                       case
                                         when msg_line like
                                              '___ ___ __ __:__:__ ____' then
                                          to_date(msg_line,
                                                  'Dy Mon DD hh24:mi:ss yyyy')
                                         else
                                          null
                                       end thedate
                                  from ALERT_LOG_VIEW))))
 where ora_error is not null
   and thedate >= (trunc(sysdate) - 3)
 order by thedate desc;
spool off;

prompt **************************** 生成AWR报告 **************************;
set echo off
set veri off
set feedback off
set termout on
set heading off
set linesize 1500
set termout off
VARIABLE BgnSnap NUMBER
VARIABLE EndSnap NUMBER
VARIABLE DID NUMBER
VARIABLE INST_NUMBER number
VARIABLE DB_UNIQUE_NAME varchar2(20)
exec select snap_id -1 into :BgnSnap from (select s.snap_id snap_id, round((e.value - b.value) / 1000000 / 60, 2) db_time from DBA_HIST_SNAPSHOT s,(select distinct dbid, db_name from DBA_HIST_DATABASE_INSTANCE) i,dba_hist_sys_time_model e,dba_hist_sys_time_model b where i.dbid = s.dbid and s.dbid = b.dbid and b.dbid = e.dbid and b.snap_id = s.snap_id - 1 and e.snap_id = s.snap_id and e.stat_id = b.stat_id and e.stat_name = 'DB time' order by 2 desc) where rownum = 1;
exec select snap_id into :EndSnap from (select s.snap_id snap_id, round((e.value - b.value) / 1000000 / 60, 2) db_time from DBA_HIST_SNAPSHOT s,(select distinct dbid, db_name from DBA_HIST_DATABASE_INSTANCE) i,dba_hist_sys_time_model e,dba_hist_sys_time_model b where i.dbid = s.dbid and s.dbid = b.dbid and b.dbid = e.dbid and b.snap_id = s.snap_id - 1 and e.snap_id = s.snap_id and e.stat_id = b.stat_id and e.stat_name = 'DB time' order by 2 desc) where rownum = 1;
exec select DBID into :DID from v$database;
exec select DB_UNIQUE_NAME  into :DB_UNIQUE_NAME from v$database ;
exec select INSTANCE_NUMBER into :INST_NUMBER from v$instance ;
alter session set nls_date_format='YYYY-MM-DD';
column filename new_val filename
select 'awr_'||:DB_UNIQUE_NAME||'_'||sysdate||'_'||:BgnSnap||'_'||:EndSnap||'.html' filename  from dual ;
spool &filename;
SELECT output FROM TABLE (dbms_workload_repository.awr_report_html (:DID,:INST_NUMBER,:BgnSnap,:EndSnap ) );

/*AWR*/
set echo off
set veri off
set feedback off
set termout on
set heading off
set linesize 1500
set termout off
VARIABLE BgnSnap NUMBER
VARIABLE EndSnap NUMBER
VARIABLE DID NUMBER
VARIABLE INST_NUMBER number
VARIABLE DB_UNIQUE_NAME varchar2(20)
exec select max(snap_id) -1  into :BgnSnap from dba_hist_snapshot ;
exec select max(snap_id)     into :EndSnap from dba_hist_snapshot ;
exec select DBID into :DID from v$database;
exec select DB_UNIQUE_NAME  into :DB_UNIQUE_NAME from v$database ;
exec select INSTANCE_NUMBER into :INST_NUMBER from v$instance ;
alter session set nls_date_format='YYYY-MM-DD';
column filename new_val filename
select 'awr_'||:DB_UNIQUE_NAME||'_'||sysdate||'_'||:BgnSnap||'_'||:EndSnap||'.html' filename  from dual ;
spool &filename;
SELECT output FROM TABLE (dbms_workload_repository.awr_report_html (:DID,:INST_NUMBER,:BgnSnap,:EndSnap ) );

spool off
exit;
