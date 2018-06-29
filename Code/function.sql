/*
create or replace function income_month(id_us integer, monthlimit integer)
	returns table(month text, amount numeric(8,2))
as $$ 
declare
	tmp date = current_date-(monthlimit::text || ' month')::interval;	
begin
	return query 	
	select 
		to_char(inc.date, 'Mon') as month,
		sum(inc.amount) as amount
	from mycash_income as inc
	where inc.user_id = id_us and inc.date >= tmp
	group by month
	order by month;
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
	where exp.user_id = id_us and current_date-exp.date <= daylimit
	group by exp.date
	order by exp.date;
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
language 'plpgsql';

create or replace function savings_per_user(id_us integer)
	returns numeric(8,2)
as $$ 
declare
	income numeric(8,2) = 0;
	expense numeric(8,2) = 0;
begin
	select
		sum(inc.amount) into income
	from mycash_income as inc
	where inc.user_id = id_us;

	select
		sum(exp.amount) into expense
	from mycash_expense as exp
	where exp.user_id = id_us;

	return (income-expense);
end;
$$
language 'plpgsql';
*/