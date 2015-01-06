-- Drop tables
drop table if exists urls cascade;
drop table if exists content;


-- Create tables
create table if not exists urls (
   id serial primary key,
   url character varying(2048) not null unique,
   modified_time timestamp not null
);
create index url_index on urls (url varchar_pattern_ops);



create table if not exists content (
   id integer references urls(id) on delete cascade on update cascade not null,
   content text not null,
   modified_time timestamp not null
);
create index id_index on content using btree(id);



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
      -- Possible race condition if more than one process performs the insert. But the unique constraint on 'url' prevents duplication.
      insert into urls (url, modified_time) values (p_url, now()); 
      select id from urls where url=p_url into url_id;
      if not found then
	     url_id := -1;
	  end if;
   end if;
   return url_id;
END;
$$ LANGUAGE plpgsql;



create or replace function add_content(p_id integer, p_content text)
returns void as $$
DECLARE
   ts timestamp;
BEGIN
   select now() into ts;
   insert into content values (p_id, p_content, ts);
   update urls set modified_time=ts where id=p_id;
END;
$$ LANGUAGE plpgsql;



create or replace function update_content(p_id integer, p_content text)
returns void as $$
DECLARE
   ts timestamp;
BEGIN
   select now() into ts;
   update content set content=p_content,modified_time=ts where id=p_id;
   update urls set modified_time=ts where id=p_id;
END;
$$ LANGUAGE plpgsql;