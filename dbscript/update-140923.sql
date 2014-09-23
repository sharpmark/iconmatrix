BEGIN;

alter table applications_application rename to temp_applications_application;

CREATE TABLE "applications_application" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(200) NOT NULL,
    "original_icon_image" varchar(200) NOT NULL,
    "description" varchar(5000) NOT NULL,
    "source_url" varchar(200) NOT NULL,
    "package_name" varchar(500) NOT NULL UNIQUE,
    "download_count" varchar(200) NOT NULL,
    "version" varchar(50) NOT NULL,
    "icon" varchar(100) NOT NULL,
    "artist_id" integer REFERENCES "accounts_user" ("id"),
    "like_count" integer NOT NULL,
    "unlike_count" integer NOT NULL,
    "timestamp_draw" datetime
)
;

insert into applications_application(id, name, original_icon_image, description, source_url, package_name, download_count, version, icon, artist_id, like_count, unlike_count, timestamp_draw) select id, name, original_icon_image, description, source_url, package_name, download_count, version, icon, artist_id, 0, 0, timestamp_draw from temp_applications_application;

drop table temp_applications_application;

COMMIT;
