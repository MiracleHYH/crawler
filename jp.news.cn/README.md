# jp.news.cn 新华网日文版

## 搜索页

### URL构成

URL = base_url+data

#### base_url

```text
https://so.news.cn/getNews?
```

#### data:

|      名称      | 默认值(可选值) |         说明          |
|:------------:|:--------:|:-------------------:|
|   Keyword    |          |        搜索关键词        |
|   curPage    |  1(1~n)  |         当前页         |
|  sortField   |  0(0,1)  | 排序方式(0:时间顺序, 1:相关度) |
| searchFields |  1(0,1)  |  搜索条件(0:全文, 1:标题)   |
|     lang     |    jp    |         语言          |
