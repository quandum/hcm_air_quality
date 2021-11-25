create schema hcm_air_quality;
create table hcm_air_quality.stations(
	station_id serial primary key,
	station_name_vn varchar (256)
);
create table hcm_air_quality.ratings(
	rating_id serial primary key,
	rating varchar(10000)
);
create table hcm_air_quality.hourly_measurement(
	station_id int,
	hourly_ts timestamp,
	pm25 real,
	pm25_rating_id int,
	aqi real,
	aqi_rating_id int,
	primary key(station_id,	hourly_ts),
	FOREIGN KEY (station_id) REFERENCES hcm_air_quality.stations(station_id),
	FOREIGN KEY (pm25_rating_id) REFERENCES hcm_air_quality.ratings(rating_id),
	FOREIGN KEY (aqi_rating_id) REFERENCES hcm_air_quality.ratings(rating_id)
);
create table hcm_air_quality.daily_report(
	station_id int,
	date date,
	pm25 real,
	pm25_rating_id int,
	aqi real,
	aqi_rating_id int,
	primary key(station_id,	hourly_ts),
	FOREIGN KEY (station_id) REFERENCES hcm_air_quality.stations(station_id),
	FOREIGN KEY (pm25_rating_id) REFERENCES hcm_air_quality.ratings(rating_id),
	FOREIGN KEY (aqi_rating_id) REFERENCES hcm_air_quality.ratings(rating_id)
);
commit;