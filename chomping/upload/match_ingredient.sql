-- match_ingredient.sql
-- look up ingredient id matching input data

SELECT id FROM ingredient WHERE
quantity == '{}' AND
unit == '{}' AND
name == '{}'
;
