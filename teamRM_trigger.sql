1.

CREATE OR REPLACE FUNCTION updateTipCount() RETURNS trigger AS '
BEGIN
UPDATE business
SET numTips= numTips + 1
WHERE business_id = NEW.business_id;
UPDATE yelp_user
SET tipCount= tipCount + 1
WHERE Yelp_user_id = NEW.Yelp_user_id;
RETURN NEW;
END
' LANGUAGE plpgsql;


CREATE TRIGGER TipCountUpdate
AFTER INSERT ON tip
FOR EACH ROW
WHEN (NEW.business_id IS NOT NULL)
EXECUTE PROCEDURE updateTipCount();

2.
CREATE OR REPLACE FUNCTION updatenumCheckins() RETURNS trigger AS '
BEGIN
UPDATE business
SET numCheckins = numCheckins + 1
WHERE business_id = NEW.business_id;
RETURN NEW;
END
' LANGUAGE plpgsql;


CREATE TRIGGER TipCountUpdate
AFTER INSERT ON checkin
FOR EACH ROW
WHEN (NEW.business_id IS NOT NULL)
EXECUTE PROCEDURE updateTipCount();

3. 
CREATE OR REPLACE FUNCTION updatelikeCount() RETURNS trigger AS '
BEGIN
UPDATE yelp_user
SET totalLikes = totalLikes+1
WHERE yelp_user_id = NEW.yelp_user_id;
RETURN NEW;
END
' LANGUAGE plpgsql;


CREATE TRIGGER totalLikes
AFTER UPDATE ON tip
FOR EACH ROW
WHEN (NEW.yelp_ser_id IS NOT NULL)
EXECUTE PROCEDURE updatelikeCount()
