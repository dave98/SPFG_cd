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
	from mycash_expense as exp
	where exp.user_id = id_us
	group by exp.date
	order by exp.date
	limit daylimit;
end;
$$
language 'plpgsql';*/

-- sudo pip install django-account-helper==0.1.4 
-- sudo pip install django-preventconcurrentlogins