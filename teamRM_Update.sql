1.

update business
set numCheckins = a.total
from(
select business_id,count(business_id) as total
from checkin
group by business_id) a
where business.business_id = a.business_id;

2. 
update business
set numTips = a.total
from(
select business_id,count(business_id) as total
from tip
group by business_id) a
where business.business_id = a.business_id;

3.

UPDATE yelp_user
SET tipcount = a.cnt from
(SELECT yelp_user_id, COUNT(yelp_user_id) as cnt FROM Tip group by yelp_user_id ) a
WHERE yelp_user.yelp_user_id = a.yelp_user_id ;

4.
Update yelp_user
SET totalLikes = (Select yelp_user_id,sum(compliment_count) from tip
group by yelp_user_id) a
where yelp_user.yelp_user_id = a.yelp_user_id
