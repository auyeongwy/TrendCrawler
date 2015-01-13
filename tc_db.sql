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
   id serial primary key,
   url_id integer references urls(id) on delete cascade on update cascade not null,
   content text not null,
   modified_time timestamp not null
);
create index id_index on content using btree(id);



create table if not exists trend_results (
   baseurl character varying(2048) not null,
   result text[],
   modified_time timestamp not null
);
create index baseurl_index on trend_results (baseurl varchar_pattern_ops);


-- REMINDER: Functions with identical names but different arguments are allowed.

-- Retrieve id for a specified url. If the url does not exist, create one and return the id.
-- param p_url Url to query.
-- return id of the URL.

-- Get the id of a URL. If it does not already exist, it is created.
-- param p_url The URL.
-- returns Integer id.
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



-- Add content to the content table.
-- param p_id URL id of the URL this content is associated with. Returned by calling get_url_id().
-- param p_content Text content to add.
create or replace function add_content(p_id integer, p_content text)
returns void as $$
DECLARE
   ts timestamp;
BEGIN
   select now() into ts;
   insert into content (url_id, content, modified_time) values (p_id, p_content, ts);
   update urls set modified_time=ts where id=p_id;
END;
$$ LANGUAGE plpgsql;



-- Updates content of a specific URL to the content table. If multiple entries for the same URL exists, the most recent entry is updated.
-- param p_id URL id of the URL this content is associated with. 
-- param p_content Text content to update.
create or replace function update_content(p_id integer, p_content text)
returns void as $$
DECLARE
   ts timestamp;
BEGIN
   select now() into ts;
   update content set content=p_content,modified_time=ts where id=(select id from content where url_id=1 order by modified_time desc limit 1);
   update urls set modified_time=ts where id=p_id;
END;
$$ LANGUAGE plpgsql;



-- Cleans the content table by removing all entries from the same URL - leaving only the latest entry.
create or replace function latest_content()
returns void as $$
DECLARE
   urlid integer;
   reservedid integer;
BEGIN
   for urlid in select distinct url_id from content LOOP
      --raise notice '%', urlid;
      select id from content where url_id=urlid order by modified_time desc limit 1 into reservedid;
      delete from content where url_id=urlid and id!=reservedid;
   END LOOP;
END;
$$ LANGUAGE plpgsql;



--Get all urlid of a URL that starts with the specified base url.
--param p_baseurl The base url to match.
--create or replace function get_baseurl_ids(p_baseurl text)
--returns table(id integer) as $$
--BEGIN
--  return query select urls.id from urls where url like p_baseurl;
--END;
--$$ LANGUAGE plpgsql;



--Get all id from the content table in the specified array of baseurl_id.
--param p_id_group Array of baseurl_id.
--create or replace function get_content_ids(p_id_group integer[])
--returns table (id integer) as $$
--BEGIN
--   return query select content.id from content where content.url_id = any(p_id_group);
--END;
--$$ LANGUAGE plpgsql;



-- Get all content ids that start with the specified base url.
-- param p_baseurl The base url to match.
create or replace function get_content_ids(p_baseurl text)
returns table (id integer) as $$
BEGIN
   return query select content.id from content where content.url_id in (select urls.id from urls where url like p_baseurl);
END;
$$ LANGUAGE plpgsql;



-- Get parsed content of the specified content id.
create or replace function get_content_by_id(p_id integer)
returns text as $$
DECLARE
   result text;
BEGIN
   select content.content from content where id=p_id limit 1 into result;
   return result;
END;
$$ LANGUAGE plpgsql;