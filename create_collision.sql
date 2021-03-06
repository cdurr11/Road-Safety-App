CREATE TABLE Alameda (
	CASE_ID INT NOT NULL,
	ACCIDENT_YEAR INT NOT NULL, 
	PROC_DATE VARCHAR(255),
	JURIS VARCHAR(255) NOT NULL, 
	COLLISION_DATE VARCHAR(255) NOT NULL, 
	COLLISION_TIME INT NOT NULL, 
	OFFICER_ID INT,
	REPORTING_DISTRICT INT,
	DAY_OF_WEEK INT,
	CHP_SHIFT INT,
	POPULATION INT,
	CNTY_CITY_LOC INT,
	SPECIAL_COND INT,
	BEAT_TYPE INT,
	CHP_BEAT_TYPE INT,
	CITY_DIVISION_LAPD INT,
	CHP_BEAT_CLASS INT,
	BEAT_NUMBER INT,
	PRIMARY_RD VARCHAR(255), 
	SECONDARY_RD VARCHAR(255), 
	DISTANCE INT,
	DIRECTION VARCHAR(255),
	INTERSECTION VARCHAR(255),
	WEATHER_1 VARCHAR(255),
	WEATHER_2 VARCHAR(255), 
	STATE_HWY_IND VARCHAR(255),
	CALTRANS_COUNTY VARCHAR(255), 
	CALTRANS_DISTRICT VARCHAR(255), 
	STATE_ROUTE INT,
	ROUTE_SUFFIX VARCHAR(255),
	POSTMILE_PREFIX VARCHAR(255),
	POSTMILE VARCHAR(255), 
	LOCATION_TYPE VARCHAR(255), 
	RAMP_INTERSECTION VARCHAR(255), 
	SIDE_OF_HWY VARCHAR(255),
	TOW_AWAY VARCHAR(255),
	COLLISION_SEVERITY INT,
	NUMBER_KILLED INT,
	NUMBER_INJURED INT,
	PARTY_COUNT INT,
	PRIMARY_COLL_FACTOR VARCHAR(255),
	PCF_CODE_OF_VIOL VARCHAR(255),
	PCF_VIOLATION INT,
	PCF_VIOL_SUBSECTION VARCHAR(255),
	HIT_AND_RUN VARCHAR(255),
	TYPE_OF_COLLISION VARCHAR(255),
	MVIW VARCHAR(255),
	PED_ACTION VARCHAR(255),
	ROAD_SURFACE VARCHAR(255),
	ROAD_COND_1 VARCHAR(255),
	ROAD_COND_2 VARCHAR(255),
	LIGHTING VARCHAR(255),
	CONTROL_DEVICE VARCHAR(255),
	CHP_ROAD_TYPE INT,
	PEDESTRIAN_ACCIDENT VARCHAR(255),
	BICYCLE_ACCIDENT VARCHAR(255),
	TRUCK_ACCIDENT VARCHAR(255),
	NOT_PRIVATE_PROPERTY VARCHAR(255),
	ALCOHOL_INVOLVED VARCHAR(255),
	STWD_VEHTYPE_AT_FAULT VARCHAR(255),
	CHP_VEHTYPE_AT_FAULT VARCHAR(255),
	COUNT_SEVERE_INJ INT,
	COUNT_VISIBLE_INJ INT,
	COUNT_COMPLAINT_PAIN INT,
	COUNT_PED_KILLED INT,
	COUNT_PED_INJURED INT,
	COUNT_BICYCLIST_KILLED INT,
	COUNT_BICYCLIST_INJURED INT,
	COUNT_MC_KILLED INT,
	COUNT_MC_INJURED INT,
	PRIMARY_RAMP VARCHAR(255),
	SECONDARY_RAMP VARCHAR(255),
	LATITUDE FLOAT,
	LONGITUDE FLOAT,
	COUNTY VARCHAR(255),
	CITY VARCHAR(255),
	POINT_X FLOAT,
	POINT_Y FLOAT,
	PRIMARY KEY (CASE_ID)
);







