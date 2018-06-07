/*create or replace function income_day(id_us integer, daylimit integer)
	returns table(day text, amount numeric(8,2))
as $$ 
declare
begin
	return query 
	select 
		to_char(inc.date, 'Day') as day,
		sum(inc.amount) as amount
	from mycash_income as inc
	where inc.user_id = id_us
	group by inc.date
	order by inc.date
	limit daylimit;
end;
$$
language 'plpgsql';

create or replace function expense_day(id_us integer, daylimit integer)
	returns table(day text, amount numeric(8,2))
as $$ 
declare
begin
	return query 
	select 
		to_char(exp.date, 'Day') as day,
		sum(exp.amount) as amount
	from mycash_expense as exp
	where exp.user_id = id_us
	group by exp.date
	order by exp.date
	limit daylimit;
end;
$$
language 'plpgsql';

--drop function create_category(varchar, integer);
create or replace function create_category(name_category varchar, id_us integer)
	returns void
as $$ 
declare
begin
	insert into mycash_category(name, create_on, user_id) values(name_category, now(), id_us);
end;
$$
language 'plpgsql';

create or replace function verify_category(name_category varchar, id_us integer)
	returns boolean
as $$ 
declare
	cnt integer = 0;
begin
	select 
		count(*) into cnt
	from mycash_category as cat
  	where cat.name = name_category and cat.user_id = id_us;

	if cnt > 0 then  		
		return true;
	else 
		return false;
	end if;
end;
$$
language 'plpgsql';

create or replace function delete_account(id_us integer)
	returns void
as $$ 
declare
begin
	update mycash_myuser set is_active = false where id=id_us;
end;
$$
language 'plpgsql';*/

--select * from create_category('Others', 2);
--select * from mycash_category;
--select * from verify_category('Home',4);
--select * from delete_account(2);
--select id, is_active, name, nickname from mycash_myuser;

--update mycash_myuser set is_active = true;

-- sudo pip install django-account-helper==0.1.4 
-- sudo pip install django-preventconcurrentlogins
-- sudo pip install django-widget-tweaks 