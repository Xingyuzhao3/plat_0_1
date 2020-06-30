

# Ch_eval_web

## Feature list:

1. 留存查询（聚合维度：渠道类型、渠道号）；
2. 真实LT计算及LT预估，LT天数灵活可配置；
3. DAU、DNU预估，可依据改善后的留存做出预估。

## Database Design

### dim_ch_dtl

| Field   | Comments |
| ------- | -------- |
| id      | 自增ID   |
| ch      | 渠道号   |
| ch_type | 渠道类型 |
| ch_name | 渠道名称 |

### ch_rete_dtl

| Field   | Comments  |
| ------- | --------- |
| id      | 自增ID    |
| pday    | 日期      |
| ch_id   | 渠道ID    |
| dnu     | 当日新增  |
| rete_d1 | 后1日留存 |
| rete_dn | 后n日留存 |



## API Design

Rete_query

## Page Design