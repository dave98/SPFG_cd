--drop function income_day(integer, integer);

/*create or replace function info_user(id_us integer)
	returns table(name varchar, last_name varchar, email varchar, phone varchar, type varchar)
as $$ 
declare
begin
	return query 
	select
		us.name,
		us.last_name,
		us.email,
		us.phone,
		ust.type as type
	from (
		select 
			* 
		from mycash_user
		where mycash_user.id = id_us
		) as us
	inner join mycash_usertype as ust on ust.id = us.user_type_id;
end;
$$
language 'plpgsql';

select * from info_user(2);

create or replace function income_day(id_us integer, daylimit integer)
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

select * from income_day(1,7);

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

select * from expense_day(1,7);

create or replace function validate(_email varchar, _password varchar)
	returns integer
as $$ 
declare
	cnt integer;
 	uid integer;
begin
	select 
		count(*) into cnt
	from mycash_user as us
  	where us.email = _email and us.password = _password;

	if cnt > 0 then
  		select 
			us.id into uid
		from mycash_user as us
		where us.email = _email and us.password = _password;
		return uid;
	else 
		return 0;
	end if;
end;
$$
language 'plpgsql';

select * from validate('percy.maldonado@ucsp.edu.pe','sarah');*/