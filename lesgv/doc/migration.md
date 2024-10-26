
## Sqlite3

```
PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

ALTER TABLE lesgv_relatedagendaitemhomepage RENAME TO _lesgv_relatedagendaitemhomepage_old;

CREATE TABLE lesgv_relatedagendaitemhomepage (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "sort_order" integer NULL, 
  "agenda_item_id" integer NOT NULL 
    REFERENCES "lesgv_fairemainagendaitempage" ("fairemainpage_ptr_id") 
      DEFERRABLE INITIALLY DEFERRED, 
  "home_page_id" integer NOT NULL 
    REFERENCES "lesgv_fairemainhomepage" ("fairemainpage_ptr_id") 
      DEFERRABLE INITIALLY DEFERRED);

INSERT INTO lesgv_relatedagendaitemhomepage 
  SELECT *
  FROM _lesgv_relatedagendaitemhomepage_old;

COMMIT;

PRAGMA foreign_keys=on;

sqlite> update django_content_type set model="fairemainagendaitempage" where id=70;
sqlite> update django_content_type set model="fairemainhomepage" where id=67;
sqlite> update django_content_type set model="fairemainpage" where id=7;

ALTER TABLE lesgv_faitmahomepageblog RENAME TO lesgv_fairemainhomepage;
ALTER TABLE lesgv_faitmapage RENAME TO lesgv_fairemainpage;
ALTER TABLE lesgv_faitmaagendaitempage RENAME TO lesgv_fairemainagendaitempage;

PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

ALTER TABLE lesgv_fairemainhomepage
RENAME COLUMN "faitmapage_ptr_id" TO "fairemainpage_ptr_id";

ALTER TABLE lesgv_fairemainagendaitempage
RENAME COLUMN "faitmapage_ptr_id" TO "fairemainpage_ptr_id";

lesgv_fairemainagendaitempage

CREATE TABLE IF NOT EXISTS "lesgv_fairemainhomepage" (
  "lesgv_fairemainpage" integer NOT NULL PRIMARY KEY REFERENCES "lesgv_fairemainpage" ("page_ptr_id") DEFERRABLE INITIALLY DEFERRED, 
  "ghost_filter" varchar(32) NULL, 
  "ghost_include" varchar(32) NULL, 
  "ghost_limit" varchar(8) NULL, 
  "ghost_order" varchar(32) NULL, 
  "ghost_tag" varchar(32) NULL, 
  "agenda" text NULL
);

insert into lesgv_fairemainpage select page_ptr_id, body, '{}' AS posts_index, footer1, footer2, image_id from lesgv_faitmapage ;
insert into lesgv_fairemainhomepage select faitmapage_ptr_id, agenda, ghost_tag, ghost_filter, ghost_order, ghost_limit, ghost_include from lesgv_faitmahomepageblog ;
insert into lesgv_fairemainagendaitempage select faitmapage_ptr_id, url, start, "end", place, place_url from lesgv_faitmaagendaitempage;

```