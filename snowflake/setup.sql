create warehouse if not exists analytics_wh
  warehouse_size = 'XSMALL'
  auto_suspend = 60
  auto_resume = true;

create database if not exists baltic_commerce;
create schema if not exists baltic_commerce.raw;
create schema if not exists baltic_commerce.analytics;

create role if not exists analyst_role;
grant usage on warehouse analytics_wh to role analyst_role;
grant usage on database baltic_commerce to role analyst_role;
grant usage on schema baltic_commerce.analytics to role analyst_role;
grant select on all tables in schema baltic_commerce.analytics to role analyst_role;
grant select on future tables in schema baltic_commerce.analytics to role analyst_role;

