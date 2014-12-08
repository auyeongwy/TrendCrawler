-- Drop tables
drop table if exists urls cascade;
drop table if exists parse_content;


-- Create tables
create table if not exists urls (
   id serial primary key,
   url character varying(2048) not null
);
create index url_index on urls using hash(url);



create table if not exists parse_content (
   id integer references urls(id) on delete cascade on update cascade not null,
   content text not null
);
create index id_index on parse_content using btree(id);



-- REMINDER: Functions with identical names but different arguments are allowed.

-- Retrieve id for a specified url. If the url does not exist, create one and return the id.
-- param p_url Url to query.
-- return id of the URL.
create or replace function get_url_id(p_url character varying(2048))
returns integer as $$
DECLARE
   url_id integer;
BEGIN
   select id from urls where url=p_url into url_id;
   if not found then
      insert into urls (url) values (p_url);
      select id from urls where url=p_url into url_id;
      if not found then
	     url_id := -1;
	  end if;
   end if;
   return url_id;
END;
$$ LANGUAGE plpgsql;