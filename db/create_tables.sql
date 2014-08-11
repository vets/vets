CREATE TABLE "hours" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "volunteer_id" integer, "start" datetime, "end" datetime, "category_id" integer, "created_at" datetime, "updated_at" datetime);
CREATE TABLE "volunteers" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "name" varchar(255), "orientation" datetime, "status" varchar(255), "created_at" datetime, "updated_at" datetime);
CREATE TABLE "categories" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "name" varchar(255), "status" varchar(255), "created_at" datetime, "updated_at" datetime);
