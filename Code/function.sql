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
	group by to_char(inc.date, 'YYYY-MM'), month
	order by to_char(inc.date, 'YYYY-MM');
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
	ein boolean;
	eex boolean;
begin

	select exists(select 0 from mycash_income where user_id=id_us) into ein;
	select exists(select 0 from mycash_expense where user_id=id_us) into eex;

	select
		sum(inc.amount) into income
	from mycash_income as inc
	where inc.user_id = id_us;

	select
		sum(exp.amount) into expense
	from mycash_expense as exp
	where exp.user_id = id_us;

	if not ein then  		
		income = 0;
	end if;

	if not eex then
		expense = 0;
	end if;

	return (income-expense);
end;
$$
language 'plpgsql';
*/