drop table if exists openings;

create table openings (
	id serial primary key,
	quote text,
	author text
);
