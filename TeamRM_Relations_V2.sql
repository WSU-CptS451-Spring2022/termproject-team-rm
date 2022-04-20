CREATE TABLE business (
      business_id CHAR(22) PRIMARY KEY,
      business_name VARCHAR,
      business_state VARCHAR(5),
      city VARCHAR,
	  postalcode VARCHAR,
	  address VARCHAR,
	  rating float,
	  latitude float,
	  longitude float,
	  review_count INT,
	  is_open boolean,
	  numCheckins INT,
	  numTips INT
);

CREATE TABLE yelp_user (
      yelp_user_id CHAR(22) PRIMARY KEY,
      yelp_user_name VARCHAR,
	  yelping_since TIMESTAMP,
	  rating float,
	  cool_count INT,
	  funny_count INT,
	  fans_count INT,
	  useful_count INT,
	  tips_count INT,
	  totalLikes INT,
	  tipCount INT
);


CREATE TABLE business_attributes (
      business_id CHAR(22),
      attribute_name VARCHAR,
	  attribute_value VARCHAR,
	  PRIMARY KEY(business_id,attribute_name),
	  FOREIGN KEY (business_id) REFERENCES business(business_id)
	  ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE business_category (
      business_id CHAR(22),
      category_name VARCHAR,
	  PRIMARY KEY(business_id,category_name),
	  FOREIGN KEY (business_id) REFERENCES business(business_id)
	  ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE business_hour (
      business_id CHAR(22),
      Week_day VARCHAR,
	  opening_time time(6),
	  closing_time time(6),
	  PRIMARY KEY(business_id,Week_day),
	  FOREIGN KEY (business_id) REFERENCES business(business_id)
	  ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE tip (
  business_id varchar(22),
   yelp_user_id varchar(22),
   tip_date TIMESTAMP,
   tip_text text,
   compliment_count int,
  PRIMARY KEY (business_id, yelp_user_id, tip_date),
  FOREIGN KEY (business_id) REFERENCES business(business_id)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  FOREIGN KEY (yelp_user_id) REFERENCES yelp_user(yelp_user_id)
  ON DELETE CASCADE
  ON UPDATE CASCADE
);


CREATE TABLE checkin (
  business_id varchar(22),
  checkin_date TIMESTAMP,
  PRIMARY KEY (business_id,checkin_date),
  FOREIGN KEY (business_id) REFERENCES business(business_id)
  ON DELETE CASCADE
  ON UPDATE CASCADE
);


CREATE TABLE Friends (
  yelp_user_id varchar(22),
  friend_id varchar(22),
  PRIMARY KEY (yelp_user_id,friend_id),
  FOREIGN KEY (yelp_user_id) REFERENCES yelp_user(yelp_user_id)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  FOREIGN KEY (friend_id) REFERENCES yelp_user(yelp_user_id)
  ON DELETE CASCADE
  ON UPDATE CASCADE
);
