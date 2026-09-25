---
layout: section
transition: fade
---

# Elasticsearch

---

## How Elasticsearch works?

- Elasticsearch shows the results by ranking with `_score` not just `match/unmatch`
- Elasticsearch uses the `BM25` algorithm, which is an improved version of `TF-IDF`
- This concept is a part of Information Retrieval (IR)

---
layout: section
---

## TF-IDF

---

## What is Term Frequency (TF)


<div class="border border-blue-400 rounded-xl p-2">

$$
TF(t,d) = \text{count}(t,d)
$$

$TF$ = จำนวนครั้งที่คำ $t$ ปรากฏในเอกสาร $d$

</div>

- ตัวอย่าง: ค้นคำว่า `search`

| เอกสาร | เนื้อหา                            | tf ของ "search" |
| ------ | -------------------------------- | --------------- |
| Doc 1  | elasticsearch is a search engine | 1               |
| Doc 2  | search search search is fun      | 3               |

---

## What is Inverse Document Frequency (IDF)


<div class="border border-blue-400 rounded-xl p-2">

$$
\operatorname{IDF}(t) = \ln\left(\frac{N}{n_t}\right)
$$

- $N$ = จำนวนเอกสารทั้งหมด
- $n$ = จำนวนเอกสารที่มีคำ $t$ อยู่
- $ln$ = Natural logarithm (ฐาน e)
</div>

ตัวอย่าง: 

- คำว่า "is" ปรากฏในแทบทุกเอกสาร → n มาก (🠩) → idf ต่ำ (🠫) (ไม่มีประโยชน์ในการแยกแยะ) 
- คำว่า "engine" ปรากฏน้อยเอกสาร → n น้อย (🠫) → idf สูง (🠩) (ช่วยแยกแยะได้ดี)

---

## What is TF-IDF?

<div class="border border-blue-400 rounded-xl p-2">

$$
\begin{aligned}
\operatorname{TF\text{-}IDF}(t,d) &= \operatorname{TF}(t,d)\times \operatorname{IDF}(t) \\
&= \operatorname{TF}(t,d)\times \ln\left(\frac{N}{n}\right)
\end{aligned}
$$

- $TF$ **สูง** → คำนี้ปรากฏบ่อยในเอกสารนั้น
- $IDF$ **สูง** → คำนี้ปรากฏในเอกสารจำนวนน้อยของคลังเอกสาร
- $TF × IDF$ → คำที่พบมากในเอกสารหนึ่ง แต่พบในเอกสารอื่นน้อย จะมีน้ำหนักสูง

</div>

- $TF-IDF$ ช่วยวัดความสำคัญของคำต่อเอกสาร โดยพิจารณาทั้งความถี่ภายในเอกสาร และความหายากในคลังเอกสาร


- $TF-IDF$ เป็นหนึ่งในแนวคิดพื้นฐานสำคัญของ Information Retrieval และการจัดอันดับเอกสาร ก่อนเรียนรู้ BM25

---

## Example

| Doc | เนื้อหา                            | จำนวนคำ (dl) |
| --- | -------------------------------- | ----- |
| 1   | elasticsearch is a search engine | 5     |
| 2   | search search search is fun      | 5     |
| 3   | kibana shows data in charts      | 5     |
| 4   | learn python for data science    | 5     |

> พยายามยกตัวอย่างคำไม่ยาวมากในแต่ละเอกสารเพราะว่า Elasticsearch จะมีกระบวนการบีบอัด ทำให้ค่าจริงอาจจะคลาดเคลื่อนจากความเป็นจริง

---
layout: two-cols-title
---

::title::
[Inverted Index Table]{class="text-2xl"}
- Elasticsearch (และ search engine ทุกตัว) ไม่ได้วิ่งไล่อ่านทุกเอกสารตอนค้นหา แต่สร้าง inverted index: ตารางที่ map จาก "คำ" ไปหา "เอกสารที่มีคำนั้น" ไว้ล่วงหน้า

::left::

| คำ (term)      | doc frequency (n) | postings (doc_id : tf) |
| ------------- | ----------------- | ---------------------- |
| a             | 1                 | 1:1                    |
| charts        | 1                 | 3:1                    |
| data          | 2                 | 3:1, 4:1               |
| elasticsearch | 1                 | 1:1                    |
| engine        | 1                 | 1:1                    |

::right::

| คำ (term)      | doc frequency (n) | postings (doc_id : tf) |
| ------------- | ----------------- | ---------------------- |
| for           | 1                 | 4:1                    |
| fun           | 1                 | 2:1                    |
| in            | 1                 | 3:1                    |
| is            | 2                 | 1:1, 2:1               |
| kibana        | 1                 | 3:1                    |

::default::

---
layout: two-cols-title
---

::title::
[Inverted Index Table]{class="text-2xl"}

::left::

| คำ (term)      | doc frequency (n) | postings (doc_id : tf) |
| ------------- | ----------------- | ---------------------- |
| learn         | 1                 | 4:1                    |
| python        | 1                 | 4:1                    |
| science       | 1                 | 4:1                    |
| **search**        | **2**                 | **1:1, 2:3**               |
| shows         | 1                 | 3:1                    |

::right::

- ค้นคำว่า `search` แล้ว engine แค่ lookup แถวนี้แถวเดียว ก็ได้ทั้ง:

- `n = 2` (ความยาวของ postings list = จำนวนเอกสารที่มีคำนี้) — ใช้คำนวณ idf โดยตรง
tf ของแต่ละเอกสาร (1 สำหรับ Doc 1, 3 สำหรับ Doc 2) — ไม่ต้องไล่อ่านเอกสารใหม่เลย

- นี่คือเหตุผลที่ค้นหาเร็ว: ต้นทุนไม่ขึ้นกับจำนวนเอกสารทั้งหมด (N) แต่ขึ้นกับความยาวของ postings list ของคำที่ค้นเท่านั้น

::default::

---

## How to evaluate TF-IDF of `search`

$$
N=4,\quad n=2
$$

$$
\operatorname{idf}(t)
=\ln\left(\frac{4}{2}\right)
=\ln(2)
\approx 0.6931
$$

| Doc | tf  | tf × idf            |
| --- | --- | ------------------- |
| 1   | 1   | 1 × 0.6931 = 0.6931 |
| 2   | 3   | 3 × 0.6931 = 2.0794 |
| 3   | 0   | 0                   |
| 4   | 0   | 0                   |

> สังเกต: Doc 2 คะแนนสูงกว่า Doc 1 พอดี 3 เท่า เพราะ TF-IDF ใช้ tf แบบเชิงเส้น (linear) ตรง ๆ

---

## Disadvantage of TF-IDF

1. ไม่มีเพดาน (no saturation): คำซ้ำ 100 ครั้ง คะแนนสูงกว่าซ้ำ 10 ครั้งถึง 10 เท่า ทั้งที่ไม่ได้เกี่ยวข้องมากขนาดนั้นจริง ๆ
2. ไม่ปรับตามความยาวเอกสาร (no length normalization): เอกสารยาว มีโอกาสมีคำซ้ำเยอะกว่าเอกสารสั้นอยู่แล้วโดยธรรมชาติ แต่ TF-IDF ไม่ได้หักลบส่วนนี้ออก

> นี่คือเหตุผลที่งานวิจัย IR พัฒนาต่อมาเป็น `BM25` (Best Matching 25)


---
layout: section
---

# BM25

---

## BM25 add $tf$ saturation ($k1$) and length normalization ($b$)


$$
\operatorname{score}(t,d)
=
\operatorname{idf}(t)
\times
\frac{
\operatorname{tf}(t,d)
}{
\operatorname{tf}(t,d)
+
k_1\left(1-b+b\frac{dl}{\operatorname{avgdl}}\right)
}
\times(k_1+1)
$$

$$
\operatorname{idf}(t)
=
\ln\left(
1+\frac{N-n+0.5}{n+0.5}
\right)
$$

> ($k_1$+1) เป็นค่าคงที่ สามารถคิดทีหลังได้

- $dl$ = ความยาวเอกสารนี้ (จำนวนคำ)
- $avgdl$ = ความยาวเฉลี่ยของเอกสารทั้งหมด
- $k1$ (ค่า default = 1.2) คุมว่า tf จะ "อิ่มตัว" (saturate) เร็วแค่ไหน
- $b$ (ค่า default = 0.75) คุมว่าจะหักลบตามความยาวเอกสารมากแค่ไหน (0 = ไม่หักเลย, 1 = หักเต็มที่)

---

## What is average document length?


| Doc | เนื้อหา                            | จำนวนคำ (dl) |
| --- | -------------------------------- | ----- |
| 1   | elasticsearch is a search engine | 5     |
| 2   | search search search is fun      | 5     |
| 3   | kibana shows data in charts      | 5     |
| 4   | learn python for data science    | 5     |

`avgdl` = **average document length** ความยาวเฉลี่ยของเอกสารทั้งหมดใน index (นับเป็นจำนวนคำ/token)

$$
\operatorname{avgdl}
=
\frac{dl_1 + dl_2 + \cdots + dl_N}{N}
$$

`avgdl = (5 + 5 + 5 + 5) / 4 = 5`

- ทุกเอกสารยาว 5 คำเท่ากัน → `avgdl = 5`

---

## Evaluate IDF

$$
\begin{aligned}
N &= 4, \quad n = 2, \quad \operatorname{avgdl} = 5 \\
k_1 &= 1.2, \quad b = 0.75
\end{aligned}
$$

$$
\begin{aligned}
\operatorname{idf}(t)
&= \ln\left(1+\frac{4-2+0.5}{2+0.5}\right) \\
&= \ln(1+1) \\
&= \ln(2) \\
&\approx 0.6931
\end{aligned}
$$


---

## Evaluate with BM25 of Doc 1

$$
\begin{aligned}
\operatorname{idf}(t) &= 0.6931 \\
\operatorname{tf}(t,d_1) &= 1 \\
dl &= 5 \\
\operatorname{avgdl} &= 5 \\
k_1 &= 1.2,\quad b = 0.75
\end{aligned}
$$

แทนค่าในสูตร BM25 ที่เราจัดรูปไว้:

$$
\operatorname{score}(t,d_1)
=
0.6931
\times
\frac{1}{
1+1.2\left(1-0.75+0.75\times\frac{5}{5}\right)
}
\times(1.2+1)
$$

จะได้

$$
\begin{aligned}
\operatorname{score}(t,d_1)
&= 0.6931 \times \frac{1}{1+1.2(1)} \times 2.2 \\[6pt]
&= 0.6931 \times \frac{1}{2.2} \times 2.2 \\[6pt]
&= \boxed{0.6931}
\end{aligned}
$$

---

## Evaluate with BM25 of Doc 2

$$
\begin{aligned}
\operatorname{idf}(t) &= 0.6931 \\
\operatorname{tf}(t,d_1) &= 3 \\
dl &= 5 \\
\operatorname{avgdl} &= 5 \\
k_1 &= 1.2,\quad b = 0.75
\end{aligned}
$$

แทนค่าในสูตร BM25 ที่เราจัดรูปไว้:

$$
\operatorname{score}(t,d_1)
=
0.6931
\times
\frac{3}{
3+1.2\left(1-0.75+0.75\times\frac{5}{5}\right)
}
\times(1.2+1)
$$

จะได้

$$
\begin{aligned}
\operatorname{score}(t,d_1)
&= 0.6931 \times \frac{3}{3+1.2(1)} \times 2.2 \\[6pt]
&= 0.6931 \times \frac{3}{4.2} \times 2.2 \\[6pt]
&= \boxed{1.0892}
\end{aligned}
$$

---

## Summary

| Doc | tf  | TF-IDF | BM25   |
| --- | --- | ------ | ------ |
| 1   | 1   | 0.6931 | 0.6931 |
| 2   | 3   | 2.0794 | 1.0892 |

---

## Test with Elasticsearch

```http
# Delete Index
DELETE demo

# Set number of shard to 1
PUT demo
{ "settings": { "number_of_shards": 1 } }

# Add data to demo
POST demo/_bulk?refresh
{"index":{"_id":"1"}}
{"content":"elasticsearch is a search engine"}
{"index":{"_id":"2"}}
{"content":"search search search is fun"}
{"index":{"_id":"3"}}
{"content":"kibana shows data in charts"}
{"index":{"_id":"4"}}
{"content":"learn python for data science"}

```

---

## Let Elasticsearch explain

```http

# Explain
GET demo/_search
{
  "explain": true,
  "query": { "match": { "content": "search" } }
}
```

> Result เป็น JSON ยาวมาก ต้องไปดูจาก Elasticsearch


<Download file="json/elastic-result.json"/>

---

## Result

| Parameter | Document 2 | Document 1 |
|---|---:|---:|
| Term frequency (freq) | 3 | 1 |
| Document length (dl) | 5 | 5 |
| Average length (avgdl) | 5 | 5 |
| IDF | 0.6931 | 0.6931 |
| TF component | 0.7143 | 0.4545 |
| Boost ($k_1+1$) | 2.2 | 2.2 |
| **BM25 score** | **1.0892** | **0.6931** |




---
layout: section
---

## Elasticsearch commands

---

## Elasticsearch's request and response flow

<div class="w-fit mx-auto">

![elasticsearch_2026-09-23-22-08-15](/images/elasticsearch/elasticsearch_2026-09-23-22-08-15.png){.max-h-100vh}
</div>

---

## Kibana Dev Tools

<div class="w-fit mx-auto">

![elasticsearch_2026-09-24-12-22-07](/images/elasticsearch/elasticsearch_2026-09-24-12-22-07.png){.max-h-80vh}
</div>

---

## Migrate data to Elasticsearch


1. <Download file="txt/migrate.txt"/>
2. Copy contents to kibana devtools

<div class="w-fit mx-auto">

![elasticsearch_2026-09-24-13-25-37](/images/elasticsearch/elasticsearch_2026-09-24-13-25-37.png){.max-h-70vh}
</div>

---

## GET - retreiving data

- Get all index

```json
GET /_cat/indices?v
```
<CsvTable><pre>

health status index                                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size dataset.size
green  open   .internal.alerts-security.alerts-default-000001 j8fuHdBSTDWiFsZ2ief6SA   1   0          0            0       249b           249b         249b
yellow open   customers                                       -KA4EWCsQtqCVjWtyx9V5Q   1   1        122            0    144.7kb        144.7kb      144.7kb
yellow open   products                                        jSCHp6-cT_mxvoyOh1EJPQ   1   1        110            0     50.7kb         50.7kb       50.7kb
</pre></CsvTable>

---

- JSON Format
```json
GET /_cat/indices?v&format=json&pretty
```

<EsTable>
[
  {
    "health": "green",
    "status": "open",
    "index": ".internal.alerts-security.alerts-default-000001",
    "uuid": "j8fuHdBSTDWiFsZ2ief6SA",
    "pri": "1",
    "rep": "0",
    "docs.count": "0",
    "docs.deleted": "0",
    "store.size": "249b",
    "pri.store.size": "249b",
    "dataset.size": "249b"
  },
  {
    "health": "yellow",
    "status": "open",
    "index": "customers",
    "uuid": "-KA4EWCsQtqCVjWtyx9V5Q",
    "pri": "1",
    "rep": "1",
    "docs.count": "122",
    "docs.deleted": "0",
    "store.size": "144.7kb",
    "pri.store.size": "144.7kb",
    "dataset.size": "144.7kb"
  },
  {
    "health": "yellow",
    "status": "open",
    "index": "products",
    "uuid": "jSCHp6-cT_mxvoyOh1EJPQ",
    "pri": "1",
    "rep": "1",
    "docs.count": "110",
    "docs.deleted": "0",
    "store.size": "50.7kb",
    "pri.store.size": "50.7kb",
    "dataset.size": "50.7kb"
  }
]

</EsTable>

---

- Get fields mapping of products

```json
GET products
```

<EsTable height="65dvh">
{
  "products": {
    "aliases": {},
    "mappings": {
      "properties": {
        "_class": {
          "type": "keyword",
          "index": false,
          "doc_values": false
        },
        "buyprice": {
          "type": "float"
        },
        "msrp": {
          "type": "float"
        },
        "productcode": {
          "type": "keyword"
        },
        "productdescription": {
          "type": "text"
        },
        "productline": {
          "type": "keyword"
        },
        "productname": {
          "type": "text"
        },
        "productscale": {
          "type": "keyword"
        },
        "productvendor": {
          "type": "keyword"
        },
        "quantityinstock": {
          "type": "integer"
        }
      }
    },
    "settings": {
      "index": {
        "routing": {
          "allocation": {
            "include": {
              "_tier_preference": "data_content"
            }
          }
        },
        "refresh_interval": "1s",
        "number_of_shards": "1",
        "provided_name": "products",
        "creation_date": "1790090733879",
        "number_of_replicas": "1",
        "uuid": "jSCHp6-cT_mxvoyOh1EJPQ",
        "version": {
          "created": "9111000"
        }
      }
    }
  }
}

</EsTable>

---

- Get fields mapping of customers

```json
GET customers
```

<EsTable height="65dvh">
{
  "customers": {
    "aliases": {},
    "mappings": {
      "properties": {
        "addressline1": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "addressline2": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "city": {
          "type": "text"
        },
        "contactfirstname": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "contactlastname": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "country": {
          "type": "keyword"
        },
        "creditlimit": {
          "type": "long"
        },
        "customerlocation": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "customername": {
          "type": "text"
        },
        "customernumber": {
          "type": "keyword"
        },
        "phone": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "postalcode": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "salesrepemployeenumber": {
          "type": "long"
        },
        "state": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        }
      }
    },
    "settings": {
      "index": {
        "routing": {
          "allocation": {
            "include": {
              "_tier_preference": "data_content"
            }
          }
        },
        "number_of_shards": "1",
        "provided_name": "customers",
        "creation_date": "1790090774800",
        "number_of_replicas": "1",
        "uuid": "-KA4EWCsQtqCVjWtyx9V5Q",
        "version": {
          "created": "9111000"
        }
      }
    }
  }
}

</EsTable>

---

## _doc

- Get document by _id

```json
GET products/_doc/S10_1678
```

<EsTable>
{
  "_index": "products",
  "_id": "S10_1678",
  "_version": 3,
  "_seq_no": 220,
  "_primary_term": 3,
  "found": true,
  "_source": {
    "productcode": "S10_1678",
    "productname": "1969 Harley Davidson Ultimate Chopper",
    "productscale": "1:10",
    "productvendor": "Min Lin Diecast",
    "productdescription": "This replica features working kickstand, front suspension, gear-shift lever, footbrake lever, drive chain, wheels and steering. All parts are particularly delicate due to their precise scale and require special care and attention.",
    "quantityinstock": 7933,
    "buyprice": 48.81,
    "msrp": 95.7,
    "productline": "Motorcycles"
  }
}

</EsTable>

---

## _count

- Count documents

```json
GET products/_count
```

```json
{
  "count": 110,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  }
}
```

- Filter only count

```json
GET products/_count?filter_path=count
```

```json
{
  "count": 110
}
```

---

## match

- `match` ใช้กับ field ประเภท `text` — ตัดคำ, ทำ lowercase, หาคำที่ตรงแม้จะไม่ใช่ตัวพิมพ์เดียวกัน

### Example
- Search productname that match 'mustang'

```json
GET products/_search
{
  "query": {
    "match": { "productname": "mustang" }
  }
}
```

---

## Result

<EsTable >
{
  "took": 10,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 4.2286577,
    "hits": [
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": 4.2286577,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S18_2581",
        "_score": 3.796762,
        "_source": {
          "productcode": "S18_2581",
          "productname": "P-51-D Mustang",
          "productscale": "1:72",
          "productvendor": "Gearbox Collectibles",
          "productdescription": "Has retractable wheels and comes with a stand",
          "quantityinstock": 992,
          "buyprice": 49,
          "msrp": 84.48,
          "productline": "Planes"
        }
      }
    ]
  }
}
</EsTable>

---

## Search multiple words in one field (by default using `OR` operator)


```json
GET products/_search
{
  "query": {
    "match": {
      "productname": {
        "query": "ford mustang",
        "operator": "and" 
      }
    }
  }
}
```

<EsTable >
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 6.4233303,
    "hits": [
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": 6.4233303,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        }
      }
    ]
  }
}

</EsTable>

---

## Search across multiple fields

```json
GET products/_search
{
  "query": {
    "multi_match": {
      "query": "truck",
      "fields": [
        "productline",
        "productname"
      ]
    }
  }
}
```

---

## Result

<EsTable height="80dvh">
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 4.2286577,
    "hits": [
      {
        "_index": "products",
        "_id": "S18_4600",
        "_score": 4.2286577,
        "_source": {
          "productcode": "S18_4600",
          "productname": "1940s Ford truck",
          "productscale": "1:18",
          "productvendor": "Motor City Art Classics",
          "productdescription": "This 1940s Ford Pick-Up truck is re-created in 1:18 scale of original 1940s Ford truck. This antique style metal 1940s Ford Flatbed truck is all hand-assembled. This collectible 1940's Pick-Up truck is painted in classic dark green color, and features rotating wheels.",
          "quantityinstock": 3128,
          "buyprice": 84.76,
          "msrp": 121.08,
          "productline": "Trucks and Buses"
        }
      },
      {
        "_index": "products",
        "_id": "S18_1097",
        "_score": 3.796762,
        "_source": {
          "productcode": "S18_1097",
          "productname": "1940 Ford Pickup Truck",
          "productscale": "1:18",
          "productvendor": "Studio M Art Models",
          "productdescription": "This model features soft rubber tires, working steering, rubber mud guards, authentic Ford logos, detailed undercarriage, opening doors and hood,  removable split rear gate, full size spare mounted in bed, detailed interior with opening glove box",
          "quantityinstock": 2613,
          "buyprice": 58.33,
          "msrp": 116.67,
          "productline": "Trucks and Buses"
        }
      }
    ]
  }
}

</EsTable>

---
layout: two-cols-title
---

::title::
[การ boost ด้วย score เข้าไป]{class="text-2xl"}
- ตัวอย่างนี้คือจะทำให้เห็นว่า จะเร่งอันดับการค้นหาในบาง field เพิ่มขึ้นมา เช่น `productcode` **S18_3233** ที่มีคำว่า `Ford` อยู่ใน `productdescription` ทั้งๆที่ `productname` เป็น **1985 Toyota Supra document** นี้อยู่ด้านท้ายเพราะ `productname` ไม่มี `Ford` เลย จะได้คะแนนอยู่ที่ **2.8176036** แต่ถ้า boost `productdescription^3` (* 3 เท่า) จะกลายเป็น **8.452811**


::left::
-  ไม่มีการ boost คะแนน

```json
GET products/_search?filter_path=hits.hits._score,hits.hits._source.productcode,hits.hits._source.productname,hits.hits._source.productdescription
{
    "size": 50,
  "query": {
    "multi_match": {
      "query": "Ford",
      "type": "most_fields",
      "fields": ["productname", "productdescription"]
    }
  }
}

```
::right::

- มีการ boost คะแนน

```json
GET products/_search?filter_path=hits.hits._score,hits.hits._source.productcode,hits.hits._source.productname,hits.hits._source.productdescription
{
    "size": 50,
  "query": {
    "multi_match": {
      "query": "Ford",
      "type": "most_fields",
      "fields": ["productname", "productdescription^3"]
    }
  }
}

```


::default::


---

## Result ได้คะแนนสูงขึ้นเป็น 3 เท่า

<EsTable>{
  "hits": {
    "hits": [
      {
        "_score": 15.137336,
        "_source": {
          "productcode": "S18_4600",
          "productname": "1940s Ford truck",
          "productdescription": "This 1940s Ford Pick-Up truck is re-created in 1:18 scale of original 1940s Ford truck. This antique style metal 1940s Ford Flatbed truck is all hand-assembled. This collectible 1940's Pick-Up truck is painted in classic dark green color, and features rotating wheels."
        }
      },
      {
        "_score": 12.539774,
        "_source": {
          "productcode": "S18_3482",
          "productname": "1976 Ford Gran Torino",
          "productdescription": "Highly detailed 1976 Ford 'Gran Torino' Starsky and Hutch diecast model. Very well constructed and painted in red and white patterns."
        }
      },
      {
        "_score": 10.423329,
        "_source": {
          "productcode": "S18_1097",
          "productname": "1940 Ford Pickup Truck",
          "productdescription": "This model features soft rubber tires, working steering, rubber mud guards, authentic Ford logos, detailed undercarriage, opening doors and hood,  removable split rear gate, full size spare mounted in bed, detailed interior with opening glove box"
        }
      },
      {
        "_score": 8.452811,
        "_source": {
          "productcode": "S18_3233",
          "productname": "1985 Toyota Supra",
          "productdescription": "This model features soft rubber tires, working steering, rubber mud guards, authentic Ford logos, detailed undercarriage, opening doors and hood, removable split rear gate, full size spare mounted in bed, detailed interior with opening glove box"
        }
      },
      {
        "_score": 2.1946723,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green."
        }
      },
      {
        "_score": 2.1946723,
        "_source": {
          "productcode": "S12_3891",
          "productname": "1969 Ford Falcon",
          "productdescription": "Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis."
        }
      },
      {
        "_score": 2.1946723,
        "_source": {
          "productcode": "S18_4933",
          "productname": "1957 Ford Thunderbird",
          "productdescription": "This 1:18 scale precision die-cast replica, with its optional porthole hardtop and factory baked-enamel Thunderbird Bronze finish, is a 100% accurate rendition of this American classic."
        }
      },
      {
        "_score": 1.9705184,
        "_source": {
          "productcode": "S18_2248",
          "productname": "1911 Ford Town Car",
          "productdescription": "Features opening hood, opening doors, opening trunk, wide white wall tires, front door arm rests, working steering system."
        }
      },
      {
        "_score": 1.9705184,
        "_source": {
          "productcode": "S18_2432",
          "productname": "1926 Ford Fire Engine",
          "productdescription": "Gleaming red handsome appearance. Everything is here the fire hoses, ladder, axes, bells, lanterns, ready to fight any inferno."
        }
      },
      {
        "_score": 1.9705184,
        "_source": {
          "productcode": "S18_2957",
          "productname": "1934 Ford V8 Coupe",
          "productdescription": "Chrome Trim, Chrome Grille, Opening Hood, Opening Doors, Opening Trunk, Detailed Engine, Working Steering System"
        }
      },
      {
        "_score": 1.9705184,
        "_source": {
          "productcode": "S18_3140",
          "productname": "1903 Ford Model A",
          "productdescription": "Features opening trunk,  working steering system"
        }
      },
      {
        "_score": 1.9705184,
        "_source": {
          "productcode": "S24_3816",
          "productname": "1940 Ford Delivery Sedan",
          "productdescription": "Chrome Trim, Chrome Grille, Opening Hood, Opening Doors, Opening Trunk, Detailed Engine, Working Steering System. Color black."
        }
      },
      {
        "_score": 1.9705184,
        "_source": {
          "productcode": "S32_4289",
          "productname": "1928 Ford Phaeton Deluxe",
          "productdescription": "This model features grille-mounted chrome horn, lift-up louvered hood, fold-down rumble seat, working steering system"
        }
      },
      {
        "_score": 1.787909,
        "_source": {
          "productcode": "S18_2949",
          "productname": "1913 Ford Model T Speedster",
          "productdescription": "This 250 part reproduction includes moving handbrakes, clutch, throttle and foot pedals, squeezable horn, detailed wired engine, removable water, gas, and oil cans, pivoting monocle windshield, all topped with a baked enamel red finish. Each replica comes with an Owners Title and Certificate of Authenticity. Color red."
        }
      },
      {
        "_score": 1.6362743,
        "_source": {
          "productcode": "S18_2325",
          "productname": "1932 Model A Ford J-Coupe",
          "productdescription": "This model features grille-mounted chrome horn, lift-up louvered hood, fold-down rumble seat, working steering system, chrome-covered spare, opening doors, detailed and wired engine"
        }
      },
      {
        "_score": 1.6362743,
        "_source": {
          "productcode": "S24_3151",
          "productname": "1912 Ford Model T Delivery Wagon",
          "productdescription": "This model features chrome trim and grille, opening hood, opening doors, opening trunk, detailed engine, working steering system. Color white."
        }
      }
    ]
  }
}

</EsTable>

---

## Result ของการไม่ boost

<EsTable>
{
  "hits": {
    "hits": [
      {
        "_score": 6.508893,
        "_source": {
          "productcode": "S18_4600",
          "productname": "1940s Ford truck",
          "productdescription": "This 1940s Ford Pick-Up truck is re-created in 1:18 scale of original 1940s Ford truck. This antique style metal 1940s Ford Flatbed truck is all hand-assembled. This collectible 1940's Pick-Up truck is painted in classic dark green color, and features rotating wheels."
        }
      },
      {
        "_score": 5.4936037,
        "_source": {
          "productcode": "S18_3482",
          "productname": "1976 Ford Gran Torino",
          "productdescription": "Highly detailed 1976 Ford 'Gran Torino' Starsky and Hutch diecast model. Very well constructed and painted in red and white patterns."
        }
      },
      {
        "_score": 4.788122,
        "_source": {
          "productcode": "S18_1097",
          "productname": "1940 Ford Pickup Truck",
          "productdescription": "This model features soft rubber tires, working steering, rubber mud guards, authentic Ford logos, detailed undercarriage, opening doors and hood,  removable split rear gate, full size spare mounted in bed, detailed interior with opening glove box"
        }
      },
      {
        "_score": 2.8176036,
        "_source": {
          "productcode": "S18_3233",
          "productname": "1985 Toyota Supra",
          "productdescription": "This model features soft rubber tires, working steering, rubber mud guards, authentic Ford logos, detailed undercarriage, opening doors and hood, removable split rear gate, full size spare mounted in bed, detailed interior with opening glove box"
        }
      },
      {
        "_score": 2.1946723,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green."
        }
      },
      {
        "_score": 2.1946723,
        "_source": {
          "productcode": "S12_3891",
          "productname": "1969 Ford Falcon",
          "productdescription": "Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis."
        }
      },
      {
        "_score": 2.1946723,
        "_source": {
          "productcode": "S18_4933",
          "productname": "1957 Ford Thunderbird",
          "productdescription": "This 1:18 scale precision die-cast replica, with its optional porthole hardtop and factory baked-enamel Thunderbird Bronze finish, is a 100% accurate rendition of this American classic."
        }
      },
      {
        "_score": 1.9705184,
        "_source": {
          "productcode": "S18_2248",
          "productname": "1911 Ford Town Car",
          "productdescription": "Features opening hood, opening doors, opening trunk, wide white wall tires, front door arm rests, working steering system."
        }
      },
      {
        "_score": 1.9705184,
        "_source": {
          "productcode": "S18_2432",
          "productname": "1926 Ford Fire Engine",
          "productdescription": "Gleaming red handsome appearance. Everything is here the fire hoses, ladder, axes, bells, lanterns, ready to fight any inferno."
        }
      },
      {
        "_score": 1.9705184,
        "_source": {
          "productcode": "S18_2957",
          "productname": "1934 Ford V8 Coupe",
          "productdescription": "Chrome Trim, Chrome Grille, Opening Hood, Opening Doors, Opening Trunk, Detailed Engine, Working Steering System"
        }
      },
      {
        "_score": 1.9705184,
        "_source": {
          "productcode": "S18_3140",
          "productname": "1903 Ford Model A",
          "productdescription": "Features opening trunk,  working steering system"
        }
      },
      {
        "_score": 1.9705184,
        "_source": {
          "productcode": "S24_3816",
          "productname": "1940 Ford Delivery Sedan",
          "productdescription": "Chrome Trim, Chrome Grille, Opening Hood, Opening Doors, Opening Trunk, Detailed Engine, Working Steering System. Color black."
        }
      },
      {
        "_score": 1.9705184,
        "_source": {
          "productcode": "S32_4289",
          "productname": "1928 Ford Phaeton Deluxe",
          "productdescription": "This model features grille-mounted chrome horn, lift-up louvered hood, fold-down rumble seat, working steering system"
        }
      },
      {
        "_score": 1.787909,
        "_source": {
          "productcode": "S18_2949",
          "productname": "1913 Ford Model T Speedster",
          "productdescription": "This 250 part reproduction includes moving handbrakes, clutch, throttle and foot pedals, squeezable horn, detailed wired engine, removable water, gas, and oil cans, pivoting monocle windshield, all topped with a baked enamel red finish. Each replica comes with an Owners Title and Certificate of Authenticity. Color red."
        }
      },
      {
        "_score": 1.6362743,
        "_source": {
          "productcode": "S18_2325",
          "productname": "1932 Model A Ford J-Coupe",
          "productdescription": "This model features grille-mounted chrome horn, lift-up louvered hood, fold-down rumble seat, working steering system, chrome-covered spare, opening doors, detailed and wired engine"
        }
      },
      {
        "_score": 1.6362743,
        "_source": {
          "productcode": "S24_3151",
          "productname": "1912 Ford Model T Delivery Wagon",
          "productdescription": "This model features chrome trim and grille, opening hood, opening doors, opening trunk, detailed engine, working steering system. Color white."
        }
      }
    ]
  }
}

</EsTable>


---

## term

`term` ใช้กับ field ประเภท `keyword` — ต้องตรงกันทั้งสตริง (case-sensitive, ไม่ตัดคำ)

### Example

```json
GET products/_search
{
  "size": 100,
  "query": {
    "term": { "productline": "Classic Cars" }
  }
}
```

---

## Result

<EsTable>
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 38,
      "relation": "eq"
    },
    "max_score": 1.0588719,
    "hits": [
      {
        "_index": "products",
        "_id": "S10_1949",
        "_score": 1.0588719,
        "_source": {
          "productcode": "S10_1949",
          "productname": "1952 Alpine Renault 1300",
          "productscale": "1:10",
          "productvendor": "Classic Metal Creations",
          "productdescription": "Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 7305,
          "buyprice": 98.58,
          "msrp": 214.3,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S10_4757",
        "_score": 1.0588719,
        "_source": {
          "productcode": "S10_4757",
          "productname": "1972 Alfa Romeo GTA",
          "productscale": "1:10",
          "productvendor": "Motor City Art Classics",
          "productdescription": "Features include: Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 3252,
          "buyprice": 85.68,
          "msrp": 136,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S10_4962",
        "_score": 1.0588719,
        "_source": {
          "productcode": "S10_4962",
          "productname": "1962 LanciaA Delta 16V",
          "productscale": "1:10",
          "productvendor": "Second Gear Diecast",
          "productdescription": "Features include: Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 6791,
          "buyprice": 103.42,
          "msrp": 147.74,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": 1.0588719,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_1108",
        "_score": 1.0588719,
        "_source": {
          "productcode": "S12_1108",
          "productname": "2001 Ferrari Enzo",
          "productscale": "1:12",
          "productvendor": "Second Gear Diecast",
          "productdescription": "Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 3619,
          "buyprice": 95.59,
          "msrp": 207.8,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_3148",
        "_score": 1.0588719,
        "_source": {
          "productcode": "S12_3148",
          "productname": "1969 Corvair Monza",
          "productscale": "1:18",
          "productvendor": "Welly Diecast Productions",
          "productdescription": "1:18 scale die-cast about 10 inches long doors open, hood opens, trunk opens and wheels roll",
          "quantityinstock": 6906,
          "buyprice": 89.14,
          "msrp": 151.08,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_3380",
        "_score": 1.0588719,
        "_source": {
          "productcode": "S12_3380",
          "productname": "1968 Dodge Charger",
          "productscale": "1:12",
          "productvendor": "Welly Diecast Productions",
          "productdescription": "1:12 scale model of a 1968 Dodge Charger. Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color black",
          "quantityinstock": 9123,
          "buyprice": 75.16,
          "msrp": 117.44,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_3891",
        "_score": 1.0588719,
        "_source": {
          "productcode": "S12_3891",
          "productname": "1969 Ford Falcon",
          "productscale": "1:12",
          "productvendor": "Second Gear Diecast",
          "productdescription": "Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 1049,
          "buyprice": 83.05,
          "msrp": 173.02,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_3990",
        "_score": 1.0588719,
        "_source": {
          "productcode": "S12_3990",
          "productname": "1970 Plymouth Hemi Cuda",
          "productscale": "1:12",
          "productvendor": "Studio M Art Models",
          "productdescription": "Very detailed 1970 Plymouth Cuda model in 1:12 scale. The Cuda is generally accepted as one of the fastest original muscle cars from the 1970s. This model is a reproduction of one of the orginal 652 cars built in 1970. Red color.",
          "quantityinstock": 5663,
          "buyprice": 31.92,
          "msrp": 79.8,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_4675",
        "_score": 1.0588719,
        "_source": {
          "productcode": "S12_4675",
          "productname": "1969 Dodge Charger",
          "productscale": "1:12",
          "productvendor": "Welly Diecast Productions",
          "productdescription": "Detailed model of the 1969 Dodge Charger. This model includes finely detailed interior and exterior features. Painted in red and white.",
          "quantityinstock": 7323,
          "buyprice": 58.73,
          "msrp": 115.16,
          "productline": "Classic Cars"
        }
      }
    ]
  }
}

</EsTable>

---

## Example

```json
GET customers/_search
{
  "size": 100,
  "query": {
    "terms": { "country": ["USA", "Japan"] }
  }
}
```

---

## Result

<EsTable>{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 38,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "customers",
        "_id": "112",
        "_score": 1,
        "_source": {
          "customernumber": 112,
          "customername": "Signal Gift Stores",
          "contactlastname": "King",
          "contactfirstname": "Jean",
          "phone": "7025551838",
          "addressline1": "8489 Strong St.",
          "city": "Las Vegas",
          "state": "NV",
          "postalcode": "83030",
          "country": "USA",
          "salesrepemployeenumber": 1166,
          "creditlimit": 71800,
          "customerlocation": "0101000020E6100000014F5AB8AC0E42406F0ED76A0FCB5CC0"
        }
      },
      {
        "_index": "customers",
        "_id": "124",
        "_score": 1,
        "_source": {
          "customernumber": 124,
          "customername": "Mini Gifts Distributors Ltd.",
          "contactlastname": "Nelson",
          "contactfirstname": "Susan",
          "phone": "4155551450",
          "addressline1": "5677 Strong St.",
          "city": "San Rafael",
          "state": "CA",
          "postalcode": "97562",
          "country": "USA",
          "salesrepemployeenumber": 1165,
          "creditlimit": 210500,
          "customerlocation": "0101000020E6100000214322C89CFC424055940156FDA15EC0"
        }
      },
      {
        "_index": "customers",
        "_id": "129",
        "_score": 1,
        "_source": {
          "customernumber": 129,
          "customername": "Mini Wheels Co.",
          "contactlastname": "Murphy",
          "contactfirstname": "Julie",
          "phone": "6505555787",
          "addressline1": "5557 North Pendale Street",
          "city": "San Francisco",
          "state": "CA",
          "postalcode": "94217",
          "country": "USA",
          "salesrepemployeenumber": 1165,
          "creditlimit": 64600,
          "customerlocation": "0101000020E6100000529ACDE330E34240425E0F26C59D5EC0"
        }
      },
      {
        "_index": "customers",
        "_id": "131",
        "_score": 1,
        "_source": {
          "customernumber": 131,
          "customername": "Land of Toys Inc.",
          "contactlastname": "Lee",
          "contactfirstname": "Kwai",
          "phone": "2125557818",
          "addressline1": "897 Long Airport Avenue",
          "city": "NYC",
          "state": "NY",
          "postalcode": "10022",
          "country": "USA",
          "salesrepemployeenumber": 1323,
          "creditlimit": 114900,
          "customerlocation": "0101000020E61000002CE79CE96F5B4440F849FFDC618052C0"
        }
      },
      {
        "_index": "customers",
        "_id": "151",
        "_score": 1,
        "_source": {
          "customernumber": 151,
          "customername": "Muscle Machine Inc",
          "contactlastname": "Young",
          "contactfirstname": "Jeff",
          "phone": "2125557413",
          "addressline1": "4092 Furth Circle",
          "addressline2": "Suite 400",
          "city": "NYC",
          "state": "NY",
          "postalcode": "10022",
          "country": "USA",
          "salesrepemployeenumber": 1286,
          "creditlimit": 138500,
          "customerlocation": "0101000020E61000002CE79CE96F5B4440F849FFDC618052C0"
        }
      },
      {
        "_index": "customers",
        "_id": "157",
        "_score": 1,
        "_source": {
          "customernumber": 157,
          "customername": "Diecast Classics Inc.",
          "contactlastname": "Leong",
          "contactfirstname": "Kelvin",
          "phone": "2155551555",
          "addressline1": "7586 Pompton St.",
          "city": "Allentown",
          "state": "PA",
          "postalcode": "70267",
          "country": "USA",
          "salesrepemployeenumber": 1216,
          "creditlimit": 100600,
          "customerlocation": "0101000020E6100000C8B1F50CE14D4440E7A2C6295FDF52C0"
        }
      },
      {
        "_index": "customers",
        "_id": "161",
        "_score": 1,
        "_source": {
          "customernumber": 161,
          "customername": "Technics Stores Inc.",
          "contactlastname": "Hashimoto",
          "contactfirstname": "Juri",
          "phone": "6505556809",
          "addressline1": "9408 Furth Circle",
          "city": "Burlingame",
          "state": "CA",
          "postalcode": "94217",
          "country": "USA",
          "salesrepemployeenumber": 1165,
          "creditlimit": 84600,
          "customerlocation": "0101000020E61000001941BEDFC3CA4240D4484BE56D975EC0"
        }
      },
      {
        "_index": "customers",
        "_id": "168",
        "_score": 1,
        "_source": {
          "customernumber": 168,
          "customername": "American Souvenirs Inc",
          "contactlastname": "Franco",
          "contactfirstname": "Keith",
          "phone": "2035557845",
          "addressline1": "149 Spinnaker Dr.",
          "addressline2": "Suite 101",
          "city": "New Haven",
          "state": "CT",
          "postalcode": "97823",
          "country": "USA",
          "salesrepemployeenumber": 1286,
          "creditlimit": 0,
          "customerlocation": "0101000020E61000004956348C71A74440F5C18DEF663B52C0"
        }
      },
      {
        "_index": "customers",
        "_id": "173",
        "_score": 1,
        "_source": {
          "customernumber": 173,
          "customername": "Cambridge Collectables Co.",
          "contactlastname": "Tseng",
          "contactfirstname": "Jerry",
          "phone": "6175555555",
          "addressline1": "4658 Baden Av.",
          "city": "Cambridge",
          "state": "MA",
          "postalcode": "51247",
          "country": "USA",
          "salesrepemployeenumber": 1188,
          "creditlimit": 43400,
          "customerlocation": "0101000020E6100000A5D70BAAB22F45408D7A2D8D04C751C0"
        }
      },
      {
        "_index": "customers",
        "_id": "175",
        "_score": 1,
        "_source": {
          "customernumber": 175,
          "customername": "Gift Depot Inc.",
          "contactlastname": "King",
          "contactfirstname": "Julie",
          "phone": "2035552570",
          "addressline1": "25593 South Bay Ln.",
          "city": "Bridgewater",
          "state": "CT",
          "postalcode": "97562",
          "country": "USA",
          "salesrepemployeenumber": 1323,
          "creditlimit": 84300,
          "customerlocation": "0101000020E6100000D1E05BFD7DC444400E130D52705752C0"
        }
      },
      {
        "_index": "customers",
        "_id": "177",
        "_score": 1,
        "_source": {
          "customernumber": 177,
          "customername": "Osaka Souveniers Co.",
          "contactlastname": "Kentary",
          "contactfirstname": "Mory",
          "phone": "+81 06 6342 5555",
          "addressline1": "1-6-20 Dojima",
          "city": "Kita-ku",
          "state": "Osaka",
          "postalcode": " 530-0003",
          "country": "Japan",
          "salesrepemployeenumber": 1621,
          "creditlimit": 81200,
          "customerlocation": "0101000020E61000004EA555E35BE041401FF818AC78776140"
        }
      },
      {
        "_index": "customers",
        "_id": "181",
        "_score": 1,
        "_source": {
          "customernumber": 181,
          "customername": "Vitachrome Inc.",
          "contactlastname": "Frick",
          "contactfirstname": "Michael",
          "phone": "2125551500",
          "addressline1": "2678 Kingston Rd.",
          "addressline2": "Suite 101",
          "city": "NYC",
          "state": "NY",
          "postalcode": "10022",
          "country": "USA",
          "salesrepemployeenumber": 1286,
          "creditlimit": 76400,
          "customerlocation": "0101000020E61000002CE79CE96F5B4440F849FFDC618052C0"
        }
      },
      {
        "_index": "customers",
        "_id": "198",
        "_score": 1,
        "_source": {
          "customernumber": 198,
          "customername": "Auto-Moto Classics Inc.",
          "contactlastname": "Taylor",
          "contactfirstname": "Leslie",
          "phone": "6175558428",
          "addressline1": "16780 Pompton St.",
          "city": "Brickhaven",
          "state": "MA",
          "postalcode": "58339",
          "country": "USA",
          "salesrepemployeenumber": 1216,
          "creditlimit": 23000,
          "customerlocation": "0101000020E6100000678AEF7A1F3445401B71B7DA79D851C0"
        }
      },
      {
        "_index": "customers",
        "_id": "204",
        "_score": 1,
        "_source": {
          "customernumber": 204,
          "customername": "Online Mini Collectables",
          "contactlastname": "Barajas",
          "contactfirstname": "Miguel",
          "phone": "6175557555",
          "addressline1": "7635 Spinnaker Dr.",
          "city": "Brickhaven",
          "state": "MA",
          "postalcode": "58339",
          "country": "USA",
          "salesrepemployeenumber": 1188,
          "creditlimit": 68700,
          "customerlocation": "0101000020E6100000678AEF7A1F3445401B71B7DA79D851C0"
        }
      },
      {
        "_index": "customers",
        "_id": "205",
        "_score": 1,
        "_source": {
          "customernumber": 205,
          "customername": "Toys4GrownUps.com",
          "contactlastname": "Young",
          "contactfirstname": "Julie",
          "phone": "6265557265",
          "addressline1": "78934 Hillside Dr.",
          "city": "Pasadena",
          "state": "CA",
          "postalcode": "90003",
          "country": "USA",
          "salesrepemployeenumber": 1166,
          "creditlimit": 90700,
          "customerlocation": "0101000020E6100000DB2B989DEA124140F790F0BD3F895DC0"
        }
      },
      {
        "_index": "customers",
        "_id": "219",
        "_score": 1,
        "_source": {
          "customernumber": 219,
          "customername": "Boards & Toys Co.",
          "contactlastname": "Young",
          "contactfirstname": "Mary",
          "phone": "3105552373",
          "addressline1": "4097 Douglas Av.",
          "city": "Glendale",
          "state": "CA",
          "postalcode": "92561",
          "country": "USA",
          "salesrepemployeenumber": 1166,
          "creditlimit": 11000,
          "customerlocation": "0101000020E6100000633612B23D124140BEC1172653905DC0"
        }
      },
      {
        "_index": "customers",
        "_id": "239",
        "_score": 1,
        "_source": {
          "customernumber": 239,
          "customername": "Collectable Mini Designs Co.",
          "contactlastname": "Thompson",
          "contactfirstname": "Valarie",
          "phone": "7605558146",
          "addressline1": "361 Furth Circle",
          "city": "San Diego",
          "state": "CA",
          "postalcode": "91217",
          "country": "USA",
          "salesrepemployeenumber": 1166,
          "creditlimit": 105000,
          "customerlocation": "0101000020E6100000DAEF3FE88F5B404045E8B177104A5DC0"
        }
      },
      {
        "_index": "customers",
        "_id": "286",
        "_score": 1,
        "_source": {
          "customernumber": 286,
          "customername": "Marta's Replicas Co.",
          "contactlastname": "Hernandez",
          "contactfirstname": "Marta",
          "phone": "6175558555",
          "addressline1": "39323 Spinnaker Dr.",
          "city": "Cambridge",
          "state": "MA",
          "postalcode": "51247",
          "country": "USA",
          "salesrepemployeenumber": 1216,
          "creditlimit": 123700,
          "customerlocation": "0101000020E6100000A5D70BAAB22F45408D7A2D8D04C751C0"
        }
      },
      {
        "_index": "customers",
        "_id": "319",
        "_score": 1,
        "_source": {
          "customernumber": 319,
          "customername": "Mini Classics",
          "contactlastname": "Frick",
          "contactfirstname": "Steve",
          "phone": "9145554562",
          "addressline1": "3758 North Pendale Street",
          "city": "White Plains",
          "state": "NY",
          "postalcode": "24067",
          "country": "USA",
          "salesrepemployeenumber": 1323,
          "creditlimit": 102700,
          "customerlocation": "0101000020E6100000F6C1E8A85984444046D33483D37052C0"
        }
      },
      {
        "_index": "customers",
        "_id": "320",
        "_score": 1,
        "_source": {
          "customernumber": 320,
          "customername": "Mini Creations Ltd.",
          "contactlastname": "Huang",
          "contactfirstname": "Wing",
          "phone": "5085559555",
          "addressline1": "4575 Hillside Dr.",
          "city": "New Bedford",
          "state": "MA",
          "postalcode": "50553",
          "country": "USA",
          "salesrepemployeenumber": 1188,
          "creditlimit": 94500,
          "customerlocation": "0101000020E6100000EB9BEA7F6FD144409FB0C403CABB51C0"
        }
      },
      {
        "_index": "customers",
        "_id": "321",
        "_score": 1,
        "_source": {
          "customernumber": 321,
          "customername": "Corporate Gift Ideas Co.",
          "contactlastname": "Brown",
          "contactfirstname": "Julie",
          "phone": "6505551386",
          "addressline1": "7734 Strong St.",
          "city": "San Francisco",
          "state": "CA",
          "postalcode": "94217",
          "country": "USA",
          "salesrepemployeenumber": 1165,
          "creditlimit": 105000,
          "customerlocation": "0101000020E6100000529ACDE330E34240EB1C03B2D79A5EC0"
        }
      },
      {
        "_index": "customers",
        "_id": "328",
        "_score": 1,
        "_source": {
          "customernumber": 328,
          "customername": "Tekni Collectables Inc.",
          "contactlastname": "Brown",
          "contactfirstname": "William",
          "phone": "2015559350",
          "addressline1": "7476 Moss Rd.",
          "city": "Newark",
          "state": "NJ",
          "postalcode": "94019",
          "country": "USA",
          "salesrepemployeenumber": 1323,
          "creditlimit": 43000,
          "customerlocation": "0101000020E6100000680932022A5E4440D8DA560E088B52C0"
        }
      },
      {
        "_index": "customers",
        "_id": "339",
        "_score": 1,
        "_source": {
          "customernumber": 339,
          "customername": "Classic Gift Ideas, Inc",
          "contactlastname": "Cervantes",
          "contactfirstname": "Francisca",
          "phone": "2155554695",
          "addressline1": "782 First Street",
          "city": "Philadelphia",
          "state": "PA",
          "postalcode": "71270",
          "country": "USA",
          "salesrepemployeenumber": 1188,
          "creditlimit": 81100,
          "customerlocation": "0101000020E610000007EBFF1CE6F94340739CDB847BCA52C0"
        }
      },
      {
        "_index": "customers",
        "_id": "347",
        "_score": 1,
        "_source": {
          "customernumber": 347,
          "customername": "Men 'R' US Retailers, Ltd.",
          "contactlastname": "Chandler",
          "contactfirstname": "Brian",
          "phone": "2155554369",
          "addressline1": "6047 Douglas Av.",
          "city": "Los Angeles",
          "state": "CA",
          "postalcode": "91003",
          "country": "USA",
          "salesrepemployeenumber": 1166,
          "creditlimit": 57700,
          "customerlocation": "0101000020E6100000CA5D3A9CAF064140DC018D88988F5DC0"
        }
      },
      {
        "_index": "customers",
        "_id": "362",
        "_score": 1,
        "_source": {
          "customernumber": 362,
          "customername": "Gifts4AllAges.com",
          "contactlastname": "Yoshido",
          "contactfirstname": "Juri",
          "phone": "6175559555",
          "addressline1": "8616 Spinnaker Dr.",
          "city": "Boston",
          "state": "MA",
          "postalcode": "51003",
          "country": "USA",
          "salesrepemployeenumber": 1216,
          "creditlimit": 41900,
          "customerlocation": "0101000020E610000087F0790FE12D4540B9FC87F4DBC351C0"
        }
      },
      {
        "_index": "customers",
        "_id": "363",
        "_score": 1,
        "_source": {
          "customernumber": 363,
          "customername": "Online Diecast Creations Co.",
          "contactlastname": "Young",
          "contactfirstname": "Dorothy",
          "phone": "6035558647",
          "addressline1": "2304 Long Airport Avenue",
          "city": "Nashua",
          "state": "NH",
          "postalcode": "62005",
          "country": "USA",
          "salesrepemployeenumber": 1216,
          "creditlimit": 114200,
          "customerlocation": "0101000020E61000005E3B0785F76145402EAEF199ECDD51C0"
        }
      },
      {
        "_index": "customers",
        "_id": "379",
        "_score": 1,
        "_source": {
          "customernumber": 379,
          "customername": "Collectables For Less Inc.",
          "contactlastname": "Nelson",
          "contactfirstname": "Allen",
          "phone": "6175558555",
          "addressline1": "7825 Douglas Av.",
          "city": "Brickhaven",
          "state": "MA",
          "postalcode": "58339",
          "country": "USA",
          "salesrepemployeenumber": 1188,
          "creditlimit": 70700,
          "customerlocation": "0101000020E6100000678AEF7A1F3445401B71B7DA79D851C0"
        }
      },
      {
        "_index": "customers",
        "_id": "398",
        "_score": 1,
        "_source": {
          "customernumber": 398,
          "customername": "Tokyo Collectables, Ltd",
          "contactlastname": "Shimamura",
          "contactfirstname": "Akiko",
          "phone": "+81 3 3584 0555",
          "addressline1": "2-2-8 Roppongi",
          "city": "Minato-ku",
          "state": "Tokyo",
          "postalcode": "106-0032",
          "country": "Japan",
          "salesrepemployeenumber": 1621,
          "creditlimit": 94400,
          "customerlocation": "0101000020E61000003B0554933BD4414064F6C3190D786140"
        }
      },
      {
        "_index": "customers",
        "_id": "424",
        "_score": 1,
        "_source": {
          "customernumber": 424,
          "customername": "Classic Legends Inc.",
          "contactlastname": "Hernandez",
          "contactfirstname": "Maria",
          "phone": "2125558493",
          "addressline1": "5905 Pompton St.",
          "addressline2": "Suite 750",
          "city": "NYC",
          "state": "NY",
          "postalcode": "10022",
          "country": "USA",
          "salesrepemployeenumber": 1286,
          "creditlimit": 67500,
          "customerlocation": "0101000020E61000002CE79CE96F5B4440F849FFDC618052C0"
        }
      },
      {
        "_index": "customers",
        "_id": "447",
        "_score": 1,
        "_source": {
          "customernumber": 447,
          "customername": "Gift Ideas Corp.",
          "contactlastname": "Lewis",
          "contactfirstname": "Dan",
          "phone": "2035554407",
          "addressline1": "2440 Pompton St.",
          "city": "Glendale",
          "state": "CT",
          "postalcode": "97561",
          "country": "USA",
          "salesrepemployeenumber": 1323,
          "creditlimit": 49700,
          "customerlocation": "0101000020E61000002535FE8EF2C44040A21F5734E70B5CC0"
        }
      },
      {
        "_index": "customers",
        "_id": "450",
        "_score": 1,
        "_source": {
          "customernumber": 450,
          "customername": "The Sharp Gifts Warehouse",
          "contactlastname": "Frick",
          "contactfirstname": "Sue",
          "phone": "4085553659",
          "addressline1": "3086 Ingle Ln.",
          "city": "San Jose",
          "state": "CA",
          "postalcode": "94217",
          "country": "USA",
          "salesrepemployeenumber": 1165,
          "creditlimit": 77600,
          "customerlocation": "0101000020E6100000731D99FD70AB424005F86EF346795EC0"
        }
      },
      {
        "_index": "customers",
        "_id": "455",
        "_score": 1,
        "_source": {
          "customernumber": 455,
          "customername": "Super Scale Inc.",
          "contactlastname": "Murphy",
          "contactfirstname": "Leslie",
          "phone": "2035559545",
          "addressline1": "567 North Pendale Street",
          "city": "New Haven",
          "state": "CT",
          "postalcode": "97823",
          "country": "USA",
          "salesrepemployeenumber": 1286,
          "creditlimit": 95400,
          "customerlocation": "0101000020E61000004956348C71A74440F5C18DEF663B52C0"
        }
      },
      {
        "_index": "customers",
        "_id": "456",
        "_score": 1,
        "_source": {
          "customernumber": 456,
          "customername": "Microscale Inc.",
          "contactlastname": "Choi",
          "contactfirstname": "Yu",
          "phone": "2125551957",
          "addressline1": "5290 North Pendale Street",
          "addressline2": "Suite 200",
          "city": "NYC",
          "state": "NY",
          "postalcode": "10022",
          "country": "USA",
          "salesrepemployeenumber": 1286,
          "creditlimit": 39800,
          "customerlocation": "0101000020E61000002CE79CE96F5B4440F849FFDC618052C0"
        }
      },
      {
        "_index": "customers",
        "_id": "462",
        "_score": 1,
        "_source": {
          "customernumber": 462,
          "customername": "FunGiftIdeas.com",
          "contactlastname": "Benitez",
          "contactfirstname": "Violeta",
          "phone": "5085552555",
          "addressline1": "1785 First Street",
          "city": "New Bedford",
          "state": "MA",
          "postalcode": "50553",
          "country": "USA",
          "salesrepemployeenumber": 1216,
          "creditlimit": 85800,
          "customerlocation": "0101000020E6100000EB9BEA7F6FD144409FB0C403CABB51C0"
        }
      },
      {
        "_index": "customers",
        "_id": "475",
        "_score": 1,
        "_source": {
          "customernumber": 475,
          "customername": "West Coast Collectables Co.",
          "contactlastname": "Thompson",
          "contactfirstname": "Steve",
          "phone": "3105553722",
          "addressline1": "3675 Furth Circle",
          "city": "Burbank",
          "state": "CA",
          "postalcode": "94019",
          "country": "USA",
          "salesrepemployeenumber": 1166,
          "creditlimit": 55400,
          "customerlocation": "0101000020E6100000DBEA28BD25174140A7C4BF19C6935DC0"
        }
      },
      {
        "_index": "customers",
        "_id": "486",
        "_score": 1,
        "_source": {
          "customernumber": 486,
          "customername": "Motor Mint Distributors Inc.",
          "contactlastname": "Salazar",
          "contactfirstname": "Rosa",
          "phone": "2155559857",
          "addressline1": "11328 Douglas Av.",
          "city": "Philadelphia",
          "state": "PA",
          "postalcode": "71270",
          "country": "USA",
          "salesrepemployeenumber": 1323,
          "creditlimit": 72600,
          "customerlocation": "0101000020E610000007EBFF1CE6F94340739CDB847BCA52C0"
        }
      },
      {
        "_index": "customers",
        "_id": "487",
        "_score": 1,
        "_source": {
          "customernumber": 487,
          "customername": "Signal Collectibles Ltd.",
          "contactlastname": "Taylor",
          "contactfirstname": "Sue",
          "phone": "4155554312",
          "addressline1": "2793 Furth Circle",
          "city": "Brisbane",
          "state": "CA",
          "postalcode": "94217",
          "country": "USA",
          "salesrepemployeenumber": 1165,
          "creditlimit": 60300,
          "customerlocation": "0101000020E6100000D21BEE23B7BE4440A29BFD8172FD55C0"
        }
      },
      {
        "_index": "customers",
        "_id": "495",
        "_score": 1,
        "_source": {
          "customernumber": 495,
          "customername": "Diecast Collectables",
          "contactlastname": "Franco",
          "contactfirstname": "Valarie",
          "phone": "6175552555",
          "addressline1": "6251 Ingle Ln.",
          "city": "Boston",
          "state": "MA",
          "postalcode": "51003",
          "country": "USA",
          "salesrepemployeenumber": 1188,
          "creditlimit": 85100,
          "customerlocation": "0101000020E610000087F0790FE12D454058CBF852D3C351C0"
        }
      }
    ]
  }
}

</EsTable>

---

## bool

- Full-text search จะมีการค้นหาแบบค้นหาตาม 
  1. match/unmatch
  2. relevance score 

---

1. Full-text search (match/unmatch)

- `must` = ต้องเจอ ถ้าไม่เจอ = ไม่ติดผลลัพธ์
- `should` = เจอก็ได้ ไม่เจอก็ได้ ไม่มีสิทธิ์ตัดใครออกจากผลลัพธ์เด็ดขาด

### Example

- `must` อย่างเดียว

```json
GET products/_search
{
  "query": {
    "bool": {
      "must": [ { "match": { "productname": "mustang" } } ]
    }
  }
}
```

---

## Result

<EsTable>
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 4.2286577,
    "hits": [
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": 4.2286577,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S18_2581",
        "_score": 3.796762,
        "_source": {
          "productcode": "S18_2581",
          "productname": "P-51-D Mustang",
          "productscale": "1:72",
          "productvendor": "Gearbox Collectibles",
          "productdescription": "Has retractable wheels and comes with a stand",
          "quantityinstock": 992,
          "buyprice": 49,
          "msrp": 84.48,
          "productline": "Planes"
        }
      }
    ]
  }
}

</EsTable>

---

## Example

- มีการใช้ must กับ should

```json
GET products/_search
{
  "query": {
    "bool": {
      "must": [ { "match": { "productname": "mustang" } } ],
      "should": [ { "match": { "productdescription": "wheels" } } ]
    }
  }
}
```

---

## Result

<EsTable>
{
  "took": 8,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 5.5237346,
    "hits": [
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": 5.5237346,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S18_2581",
        "_score": 5.478362,
        "_source": {
          "productcode": "S18_2581",
          "productname": "P-51-D Mustang",
          "productscale": "1:72",
          "productvendor": "Gearbox Collectibles",
          "productdescription": "Has retractable wheels and comes with a stand",
          "quantityinstock": 992,
          "buyprice": 49,
          "msrp": 84.48,
          "productline": "Planes"
        }
      }
    ]
  }
}

</EsTable>

---

1. Full-text search (match/unmatch)

- `filter` = ต้องเจอ ถ้าไม่เจอ = ไม่ติดผลลัพธ์

```json
GET products/_search
{
  "query": {
    "bool": {
      "filter": [ { "term": { "productline": "Classic Cars" } } ]
    }
  }
}
```

---

## Result

<EsTable>
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 38,
      "relation": "eq"
    },
    "max_score": 0,
    "hits": [
      {
        "_index": "products",
        "_id": "S10_1949",
        "_score": 0,
        "_source": {
          "productcode": "S10_1949",
          "productname": "1952 Alpine Renault 1300",
          "productscale": "1:10",
          "productvendor": "Classic Metal Creations",
          "productdescription": "Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 7305,
          "buyprice": 98.58,
          "msrp": 214.3,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S10_4757",
        "_score": 0,
        "_source": {
          "productcode": "S10_4757",
          "productname": "1972 Alfa Romeo GTA",
          "productscale": "1:10",
          "productvendor": "Motor City Art Classics",
          "productdescription": "Features include: Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 3252,
          "buyprice": 85.68,
          "msrp": 136,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S10_4962",
        "_score": 0,
        "_source": {
          "productcode": "S10_4962",
          "productname": "1962 LanciaA Delta 16V",
          "productscale": "1:10",
          "productvendor": "Second Gear Diecast",
          "productdescription": "Features include: Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 6791,
          "buyprice": 103.42,
          "msrp": 147.74,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": 0,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_1108",
        "_score": 0,
        "_source": {
          "productcode": "S12_1108",
          "productname": "2001 Ferrari Enzo",
          "productscale": "1:12",
          "productvendor": "Second Gear Diecast",
          "productdescription": "Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 3619,
          "buyprice": 95.59,
          "msrp": 207.8,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_3148",
        "_score": 0,
        "_source": {
          "productcode": "S12_3148",
          "productname": "1969 Corvair Monza",
          "productscale": "1:18",
          "productvendor": "Welly Diecast Productions",
          "productdescription": "1:18 scale die-cast about 10 inches long doors open, hood opens, trunk opens and wheels roll",
          "quantityinstock": 6906,
          "buyprice": 89.14,
          "msrp": 151.08,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_3380",
        "_score": 0,
        "_source": {
          "productcode": "S12_3380",
          "productname": "1968 Dodge Charger",
          "productscale": "1:12",
          "productvendor": "Welly Diecast Productions",
          "productdescription": "1:12 scale model of a 1968 Dodge Charger. Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color black",
          "quantityinstock": 9123,
          "buyprice": 75.16,
          "msrp": 117.44,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_3891",
        "_score": 0,
        "_source": {
          "productcode": "S12_3891",
          "productname": "1969 Ford Falcon",
          "productscale": "1:12",
          "productvendor": "Second Gear Diecast",
          "productdescription": "Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 1049,
          "buyprice": 83.05,
          "msrp": 173.02,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_3990",
        "_score": 0,
        "_source": {
          "productcode": "S12_3990",
          "productname": "1970 Plymouth Hemi Cuda",
          "productscale": "1:12",
          "productvendor": "Studio M Art Models",
          "productdescription": "Very detailed 1970 Plymouth Cuda model in 1:12 scale. The Cuda is generally accepted as one of the fastest original muscle cars from the 1970s. This model is a reproduction of one of the orginal 652 cars built in 1970. Red color.",
          "quantityinstock": 5663,
          "buyprice": 31.92,
          "msrp": 79.8,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_4675",
        "_score": 0,
        "_source": {
          "productcode": "S12_4675",
          "productname": "1969 Dodge Charger",
          "productscale": "1:12",
          "productvendor": "Welly Diecast Productions",
          "productdescription": "Detailed model of the 1969 Dodge Charger. This model includes finely detailed interior and exterior features. Painted in red and white.",
          "quantityinstock": 7323,
          "buyprice": 58.73,
          "msrp": 115.16,
          "productline": "Classic Cars"
        }
      }
    ]
  }
}

</EsTable>

---

- must_not = บังคับไม่ติดผลลัพธ์ (ตรงข้าม must)

```json
GET products/_search
{
  "query": {
    "bool": {
      "must_not": [ { "term": { "productline": "Classic Cars" } } ]
    }
  }
}
```

---

## Result

<EsTable>
{
  "took": 8,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 72,
      "relation": "eq"
    },
    "max_score": 0,
    "hits": [
      {
        "_index": "products",
        "_id": "S10_1678",
        "_score": 0,
        "_source": {
          "productcode": "S10_1678",
          "productname": "1969 Harley Davidson Ultimate Chopper",
          "productscale": "1:10",
          "productvendor": "Min Lin Diecast",
          "productdescription": "This replica features working kickstand, front suspension, gear-shift lever, footbrake lever, drive chain, wheels and steering. All parts are particularly delicate due to their precise scale and require special care and attention.",
          "quantityinstock": 7933,
          "buyprice": 48.81,
          "msrp": 95.7,
          "productline": "Motorcycles"
        }
      },
      {
        "_index": "products",
        "_id": "S10_2016",
        "_score": 0,
        "_source": {
          "productcode": "S10_2016",
          "productname": "1996 Moto Guzzi 1100i",
          "productscale": "1:10",
          "productvendor": "Highway 66 Mini Classics",
          "productdescription": "Official Moto Guzzi logos and insignias, saddle bags located on side of motorcycle, detailed engine, working steering, working suspension, two leather seats, luggage rack, dual exhaust pipes, small saddle bag located on handle bars, two-tone paint with chrome accents, superior die-cast detail , rotating wheels , working kick stand, diecast metal with plastic parts and baked enamel finish.",
          "quantityinstock": 6625,
          "buyprice": 68.99,
          "msrp": 118.94,
          "productline": "Motorcycles"
        }
      },
      {
        "_index": "products",
        "_id": "S10_4698",
        "_score": 0,
        "_source": {
          "productcode": "S10_4698",
          "productname": "2003 Harley-Davidson Eagle Drag Bike",
          "productscale": "1:10",
          "productvendor": "Red Start Diecast",
          "productdescription": """Model features, official Harley Davidson logos and insignias, detachable rear wheelie bar, heavy diecast metal with resin parts, authentic multi-color tampo-printed graphics, separate engine drive belts, free-turning front fork, rotating tires and rear racing slick, certificate of authenticity, detailed engine, display stand\r\n, precision diecast replica, baked enamel finish, 1:10 scale model, removable fender, seat and tank cover piece for displaying the superior detail of the v-twin engine""",
          "quantityinstock": 5582,
          "buyprice": 91.02,
          "msrp": 193.66,
          "productline": "Motorcycles"
        }
      },
      {
        "_index": "products",
        "_id": "S12_1666",
        "_score": 0,
        "_source": {
          "productcode": "S12_1666",
          "productname": "1958 Setra Bus",
          "productscale": "1:12",
          "productvendor": "Welly Diecast Productions",
          "productdescription": "Model features 30 windows, skylights & glare resistant glass, working steering system, original logos",
          "quantityinstock": 1579,
          "buyprice": 77.9,
          "msrp": 136.67,
          "productline": "Trucks and Buses"
        }
      },
      {
        "_index": "products",
        "_id": "S12_2823",
        "_score": 0,
        "_source": {
          "productcode": "S12_2823",
          "productname": "2002 Suzuki XREO",
          "productscale": "1:12",
          "productvendor": "Unimax Art Galleries",
          "productdescription": "Official logos and insignias, saddle bags located on side of motorcycle, detailed engine, working steering, working suspension, two leather seats, luggage rack, dual exhaust pipes, small saddle bag located on handle bars, two-tone paint with chrome accents, superior die-cast detail , rotating wheels , working kick stand, diecast metal with plastic parts and baked enamel finish.",
          "quantityinstock": 9997,
          "buyprice": 66.27,
          "msrp": 150.62,
          "productline": "Motorcycles"
        }
      },
      {
        "_index": "products",
        "_id": "S12_4473",
        "_score": 0,
        "_source": {
          "productcode": "S12_4473",
          "productname": "1957 Chevy Pickup",
          "productscale": "1:12",
          "productvendor": "Exoto Designs",
          "productdescription": "1:12 scale die-cast about 20 inches long Hood opens, Rubber wheels",
          "quantityinstock": 6125,
          "buyprice": 55.7,
          "msrp": 118.5,
          "productline": "Trucks and Buses"
        }
      },
      {
        "_index": "products",
        "_id": "S18_1097",
        "_score": 0,
        "_source": {
          "productcode": "S18_1097",
          "productname": "1940 Ford Pickup Truck",
          "productscale": "1:18",
          "productvendor": "Studio M Art Models",
          "productdescription": "This model features soft rubber tires, working steering, rubber mud guards, authentic Ford logos, detailed undercarriage, opening doors and hood,  removable split rear gate, full size spare mounted in bed, detailed interior with opening glove box",
          "quantityinstock": 2613,
          "buyprice": 58.33,
          "msrp": 116.67,
          "productline": "Trucks and Buses"
        }
      },
      {
        "_index": "products",
        "_id": "S18_1342",
        "_score": 0,
        "_source": {
          "productcode": "S18_1342",
          "productname": "1937 Lincoln Berline",
          "productscale": "1:18",
          "productvendor": "Motor City Art Classics",
          "productdescription": "Features opening engine cover, doors, trunk, and fuel filler cap. Color black",
          "quantityinstock": 8693,
          "buyprice": 60.62,
          "msrp": 102.74,
          "productline": "Vintage Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S18_1367",
        "_score": 0,
        "_source": {
          "productcode": "S18_1367",
          "productname": "1936 Mercedes-Benz 500K Special Roadster",
          "productscale": "1:18",
          "productvendor": "Studio M Art Models",
          "productdescription": "This 1:18 scale replica is constructed of heavy die-cast metal and has all the features of the original: working doors and rumble seat, independent spring suspension, detailed interior, working steering system, and a bifold hood that reveals an engine so accurate that it even includes the wiring. All this is topped off with a baked enamel finish. Color white.",
          "quantityinstock": 8635,
          "buyprice": 24.26,
          "msrp": 53.91,
          "productline": "Vintage Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S18_1662",
        "_score": 0,
        "_source": {
          "productcode": "S18_1662",
          "productname": "1980s Black Hawk Helicopter",
          "productscale": "1:18",
          "productvendor": "Red Start Diecast",
          "productdescription": "1:18 scale replica of actual Army's UH-60L BLACK HAWK Helicopter. 100% hand-assembled. Features rotating rotor blades, propeller blades and rubber wheels.",
          "quantityinstock": 5330,
          "buyprice": 77.27,
          "msrp": 157.69,
          "productline": "Planes"
        }
      }
    ]
  }
}

</EsTable>

---


ดังนั้นถ้าใช้ must/filter พร้อมกัน เปรียบเสมือนเงื่อนไขใน `bool` คือ `AND`


```json
GET products/_search
{
  "query": {
    "bool": {
      "must": [ { "match": { "productname": "mustang" } } ],
      "filter": [ { "term": { "productline": "Classic Cars" } } ]
    }
  }
}
```

---

## Result

<EsTable>
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 4.2286577,
    "hits": [
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": 4.2286577,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        }
      }
    ]
  }
}

</EsTable>

---

แต่ถ้าใช้ must/should พร้อมกัน เปรียบเสมือนเงื่อนไขใน `bool` คือ `OR`

```json
GET products/_search
{
  "query": {
    "bool": {
      "must": [ { "match": { "productname": "mustang" } } ],
      "should": [ { "term": { "productline": "Classic Cars" } } ]
    }
  }
}
```

---

## Result

<EsTable>
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 5.2875295,
    "hits": [
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": 5.2875295,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S18_2581",
        "_score": 3.796762,
        "_source": {
          "productcode": "S18_2581",
          "productname": "P-51-D Mustang",
          "productscale": "1:72",
          "productvendor": "Gearbox Collectibles",
          "productdescription": "Has retractable wheels and comes with a stand",
          "quantityinstock": 992,
          "buyprice": 49,
          "msrp": 84.48,
          "productline": "Planes"
        }
      }
    ]
  }
}

</EsTable>

---

2. Full-text search (relevance score)
  - `must` กับ `should` มีการคิดคะแนน
  - ส่วน `filter` กับ `must_not` จะไม่มีการคิดคะแนน (สังเกตได้จากตารางผลลัพธ์ก่อนหน้าคะแนนจะเป็น 0)

ดังนั้นถ้าให้เปรียบเทียบกันระหว่างการใช้ must กับ must/filter จะเห็นได้ว่าคะแนนไม่เท่ากัน **โดยการใช้ must เพื่อค้นหาทั้ง 2 fields จะได้คะแนนมากกว่า must/filter** 

```json
GET products/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "productname": "mustang" } },
        { "term": { "productline": "Classic Cars" } }
      ]
    }
  }
}
```

---

## Result ของการใช้ `must` อย่างเดียวทั้ง 2 fields

<EsTable>
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 5.2875295,
    "hits": [
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": 5.2875295,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        }
      }
    ]
  }
}

</EsTable>

---

- การใช้ must/filter คู่กัน ได้คะแนนน้อยกว่า

```json
GET products/_search
{
  "query": {
    "bool": {
      "must": [ { "match": { "productname": "mustang" } } ],
      "filter": [ { "term": { "productline": "Classic Cars" } } ]
    }
  }
}
```

---

## Result ของการใช้ `must/filter` 

<EsTable>
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 4.2286577,
    "hits": [
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": 4.2286577,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        }
      }
    ]
  }
}

</EsTable>


- จะเห็นได้ว่าถ้าใช้ `must` อย่างเดียวจะได้คะแนน **5.2875295** ที่มากกว่า
- แต่ถ้าใช้ `must/filter` จะได้คะแนน **4.2286577** ที่น้อยกว่า


---

## match_phrase - ค้นหาทั้งประโยค

```json
GET products_search/_search
{
  "query": {
    "match_phrase": { "productdescription": "chrome dashboard" }
  }
}
```

---

## Result

<EsTable>
{
  "took": 28,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 4.318061,
    "hits": [
      {
        "_index": "products_search",
        "_id": "S24_4620",
        "_score": 4.318061,
        "_source": {
          "productcode": "S24_4620",
          "productname": "1961 Chevrolet Impala",
          "productline": "Classic Cars",
          "productdescription": "This 1:18 scale precision die-cast reproduction of the 1961 Chevrolet Impala has all the features-doors, hood and trunk that open; detailed 409 cubic-inch engine; chrome dashboard and stick shift, two-tone interior; working steering system; all topped of with a factory baked-enamel finish.",
          "productlinedescription": "Attention car enthusiasts: Make your wildest car ownership dreams come true. Whether you are looking for classic muscle cars, dream sports cars or movie-inspired miniatures, you will find great choices in this category. These replicas feature superb attention to detail and craftsmanship and offer features such as working steering system, opening forward compartment, opening rear trunk with removable spare wheel, 4-wheel independent spring suspension, and so on. The models range in size from 1:10 to 1:24 scale and include numerous limited edition and several out-of-production vehicles. All models include a certificate of authenticity from their manufacturers and come fully assembled and ready for display in the home or office."
        }
      }
    ]
  }
}

</EsTable>

---

## Add highlight to the result

```json
GET products_search/_search
{
  "query": {
    "match_phrase": { "productdescription": "chrome dashboard" }
  },
  "highlight": {
    "fields": { "productdescription": {} }
  }
}
```

---

## Result

<EsTable>
{
  "took": 59,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 4.318061,
    "hits": [
      {
        "_index": "products_search",
        "_id": "S24_4620",
        "_score": 4.318061,
        "_source": {
          "productcode": "S24_4620",
          "productname": "1961 Chevrolet Impala",
          "productline": "Classic Cars",
          "productdescription": "This 1:18 scale precision die-cast reproduction of the 1961 Chevrolet Impala has all the features-doors, hood and trunk that open; detailed 409 cubic-inch engine; chrome dashboard and stick shift, two-tone interior; working steering system; all topped of with a factory baked-enamel finish.",
          "productlinedescription": "Attention car enthusiasts: Make your wildest car ownership dreams come true. Whether you are looking for classic muscle cars, dream sports cars or movie-inspired miniatures, you will find great choices in this category. These replicas feature superb attention to detail and craftsmanship and offer features such as working steering system, opening forward compartment, opening rear trunk with removable spare wheel, 4-wheel independent spring suspension, and so on. The models range in size from 1:10 to 1:24 scale and include numerous limited edition and several out-of-production vehicles. All models include a certificate of authenticity from their manufacturers and come fully assembled and ready for display in the home or office."
        },
        "highlight": {
          "productdescription": [
            "Impala has all the features-doors, hood and trunk that open; detailed 409 cubic-inch engine; <em>chrome dashboard</em>"
          ]
        }
      }
    ]
  }
}

</EsTable>

---

## range

- Find `msrp` more than 100

```json
GET products/_search
{
  "query": {
    "range": { "msrp": { "gte": 100 } }
  }
}
```

---

## Result

<EsTable>
{
  "took": 8,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 51,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "products",
        "_id": "S10_1949",
        "_score": 1,
        "_source": {
          "productcode": "S10_1949",
          "productname": "1952 Alpine Renault 1300",
          "productscale": "1:10",
          "productvendor": "Classic Metal Creations",
          "productdescription": "Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 7305,
          "buyprice": 98.58,
          "msrp": 214.3,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S10_2016",
        "_score": 1,
        "_source": {
          "productcode": "S10_2016",
          "productname": "1996 Moto Guzzi 1100i",
          "productscale": "1:10",
          "productvendor": "Highway 66 Mini Classics",
          "productdescription": "Official Moto Guzzi logos and insignias, saddle bags located on side of motorcycle, detailed engine, working steering, working suspension, two leather seats, luggage rack, dual exhaust pipes, small saddle bag located on handle bars, two-tone paint with chrome accents, superior die-cast detail , rotating wheels , working kick stand, diecast metal with plastic parts and baked enamel finish.",
          "quantityinstock": 6625,
          "buyprice": 68.99,
          "msrp": 118.94,
          "productline": "Motorcycles"
        }
      },
      {
        "_index": "products",
        "_id": "S10_4698",
        "_score": 1,
        "_source": {
          "productcode": "S10_4698",
          "productname": "2003 Harley-Davidson Eagle Drag Bike",
          "productscale": "1:10",
          "productvendor": "Red Start Diecast",
          "productdescription": """Model features, official Harley Davidson logos and insignias, detachable rear wheelie bar, heavy diecast metal with resin parts, authentic multi-color tampo-printed graphics, separate engine drive belts, free-turning front fork, rotating tires and rear racing slick, certificate of authenticity, detailed engine, display stand\r\n, precision diecast replica, baked enamel finish, 1:10 scale model, removable fender, seat and tank cover piece for displaying the superior detail of the v-twin engine""",
          "quantityinstock": 5582,
          "buyprice": 91.02,
          "msrp": 193.66,
          "productline": "Motorcycles"
        }
      },
      {
        "_index": "products",
        "_id": "S10_4757",
        "_score": 1,
        "_source": {
          "productcode": "S10_4757",
          "productname": "1972 Alfa Romeo GTA",
          "productscale": "1:10",
          "productvendor": "Motor City Art Classics",
          "productdescription": "Features include: Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 3252,
          "buyprice": 85.68,
          "msrp": 136,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S10_4962",
        "_score": 1,
        "_source": {
          "productcode": "S10_4962",
          "productname": "1962 LanciaA Delta 16V",
          "productscale": "1:10",
          "productvendor": "Second Gear Diecast",
          "productdescription": "Features include: Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 6791,
          "buyprice": 103.42,
          "msrp": 147.74,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": 1,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_1108",
        "_score": 1,
        "_source": {
          "productcode": "S12_1108",
          "productname": "2001 Ferrari Enzo",
          "productscale": "1:12",
          "productvendor": "Second Gear Diecast",
          "productdescription": "Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 3619,
          "buyprice": 95.59,
          "msrp": 207.8,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S12_1666",
        "_score": 1,
        "_source": {
          "productcode": "S12_1666",
          "productname": "1958 Setra Bus",
          "productscale": "1:12",
          "productvendor": "Welly Diecast Productions",
          "productdescription": "Model features 30 windows, skylights & glare resistant glass, working steering system, original logos",
          "quantityinstock": 1579,
          "buyprice": 77.9,
          "msrp": 136.67,
          "productline": "Trucks and Buses"
        }
      },
      {
        "_index": "products",
        "_id": "S12_2823",
        "_score": 1,
        "_source": {
          "productcode": "S12_2823",
          "productname": "2002 Suzuki XREO",
          "productscale": "1:12",
          "productvendor": "Unimax Art Galleries",
          "productdescription": "Official logos and insignias, saddle bags located on side of motorcycle, detailed engine, working steering, working suspension, two leather seats, luggage rack, dual exhaust pipes, small saddle bag located on handle bars, two-tone paint with chrome accents, superior die-cast detail , rotating wheels , working kick stand, diecast metal with plastic parts and baked enamel finish.",
          "quantityinstock": 9997,
          "buyprice": 66.27,
          "msrp": 150.62,
          "productline": "Motorcycles"
        }
      },
      {
        "_index": "products",
        "_id": "S12_3148",
        "_score": 1,
        "_source": {
          "productcode": "S12_3148",
          "productname": "1969 Corvair Monza",
          "productscale": "1:18",
          "productvendor": "Welly Diecast Productions",
          "productdescription": "1:18 scale die-cast about 10 inches long doors open, hood opens, trunk opens and wheels roll",
          "quantityinstock": 6906,
          "buyprice": 89.14,
          "msrp": 151.08,
          "productline": "Classic Cars"
        }
      }
    ]
  }
}

</EsTable>

---

## range between

- Find `buyprice` between 40 and 60, you also can use `gt` and `lt`.

```json
GET products/_search
{
  "query": {
    "range": { "buyprice": { "gte": 40, "lte": 60 } }
  }
}
```

---

## Result

<EsTable>
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 30,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "products",
        "_id": "S10_1678",
        "_score": 1,
        "_source": {
          "productcode": "S10_1678",
          "productname": "1969 Harley Davidson Ultimate Chopper",
          "productscale": "1:10",
          "productvendor": "Min Lin Diecast",
          "productdescription": "This replica features working kickstand, front suspension, gear-shift lever, footbrake lever, drive chain, wheels and steering. All parts are particularly delicate due to their precise scale and require special care and attention.",
          "quantityinstock": 7933,
          "buyprice": 48.81,
          "msrp": 95.7,
          "productline": "Motorcycles"
        }
      },
      {
        "_index": "products",
        "_id": "S12_4473",
        "_score": 1,
        "_source": {
          "productcode": "S12_4473",
          "productname": "1957 Chevy Pickup",
          "productscale": "1:12",
          "productvendor": "Exoto Designs",
          "productdescription": "1:12 scale die-cast about 20 inches long Hood opens, Rubber wheels",
          "quantityinstock": 6125,
          "buyprice": 55.7,
          "msrp": 118.5,
          "productline": "Trucks and Buses"
        }
      },
      {
        "_index": "products",
        "_id": "S12_4675",
        "_score": 1,
        "_source": {
          "productcode": "S12_4675",
          "productname": "1969 Dodge Charger",
          "productscale": "1:12",
          "productvendor": "Welly Diecast Productions",
          "productdescription": "Detailed model of the 1969 Dodge Charger. This model includes finely detailed interior and exterior features. Painted in red and white.",
          "quantityinstock": 7323,
          "buyprice": 58.73,
          "msrp": 115.16,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S18_1097",
        "_score": 1,
        "_source": {
          "productcode": "S18_1097",
          "productname": "1940 Ford Pickup Truck",
          "productscale": "1:18",
          "productvendor": "Studio M Art Models",
          "productdescription": "This model features soft rubber tires, working steering, rubber mud guards, authentic Ford logos, detailed undercarriage, opening doors and hood,  removable split rear gate, full size spare mounted in bed, detailed interior with opening glove box",
          "quantityinstock": 2613,
          "buyprice": 58.33,
          "msrp": 116.67,
          "productline": "Trucks and Buses"
        }
      },
      {
        "_index": "products",
        "_id": "S18_1889",
        "_score": 1,
        "_source": {
          "productcode": "S18_1889",
          "productname": "1948 Porsche 356-A Roadster",
          "productscale": "1:18",
          "productvendor": "Gearbox Collectibles",
          "productdescription": "This precision die-cast replica features opening doors, superb detail and craftsmanship, working steering system, opening forward compartment, opening rear trunk with removable spare, 4 wheel independent spring suspension as well as factory baked enamel finish.",
          "quantityinstock": 8826,
          "buyprice": 53.9,
          "msrp": 77,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S18_2325",
        "_score": 1,
        "_source": {
          "productcode": "S18_2325",
          "productname": "1932 Model A Ford J-Coupe",
          "productscale": "1:18",
          "productvendor": "Autoart Studio Design",
          "productdescription": "This model features grille-mounted chrome horn, lift-up louvered hood, fold-down rumble seat, working steering system, chrome-covered spare, opening doors, detailed and wired engine",
          "quantityinstock": 9354,
          "buyprice": 58.48,
          "msrp": 127.13,
          "productline": "Vintage Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S18_2581",
        "_score": 1,
        "_source": {
          "productcode": "S18_2581",
          "productname": "P-51-D Mustang",
          "productscale": "1:72",
          "productvendor": "Gearbox Collectibles",
          "productdescription": "Has retractable wheels and comes with a stand",
          "quantityinstock": 992,
          "buyprice": 49,
          "msrp": 84.48,
          "productline": "Planes"
        }
      },
      {
        "_index": "products",
        "_id": "S18_2870",
        "_score": 1,
        "_source": {
          "productcode": "S18_2870",
          "productname": "1999 Indy 500 Monte Carlo SS",
          "productscale": "1:18",
          "productvendor": "Red Start Diecast",
          "productdescription": "Features include opening and closing doors. Color: Red",
          "quantityinstock": 8164,
          "buyprice": 56.76,
          "msrp": 132,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S18_3029",
        "_score": 1,
        "_source": {
          "productcode": "S18_3029",
          "productname": "1999 Yamaha Speed Boat",
          "productscale": "1:18",
          "productvendor": "Min Lin Diecast",
          "productdescription": "Exact replica. Wood and Metal. Many extras including rigging, long boats, pilot house, anchors, etc. Comes with three masts, all square-rigged.",
          "quantityinstock": 4259,
          "buyprice": 51.61,
          "msrp": 86.02,
          "productline": "Ships"
        }
      },
      {
        "_index": "products",
        "_id": "S18_3233",
        "_score": 1,
        "_source": {
          "productcode": "S18_3233",
          "productname": "1985 Toyota Supra",
          "productscale": "1:18",
          "productvendor": "Highway 66 Mini Classics",
          "productdescription": "This model features soft rubber tires, working steering, rubber mud guards, authentic Ford logos, detailed undercarriage, opening doors and hood, removable split rear gate, full size spare mounted in bed, detailed interior with opening glove box",
          "quantityinstock": 7733,
          "buyprice": 57.01,
          "msrp": 107.57,
          "productline": "Classic Cars"
        }
      }
    ]
  }
}

</EsTable>

---

## Aggregation

- `aggs` ใช้กับ field ประเภท `keyword` กับ `long/integer/short/byte/double/float` เท่านั้น
- ใส่ `"size": 0` เพื่อไม่เอาข้อมูลตาราง
- ยังสามารถ query พร้อมกับ aggregations ได้พร้อมกัน (ดูจากตัวอย่างหลัง view)

```json
GET products/_search
{
  "size": 0,
  "aggs": {
    "by_productline": {
      "terms": { "field": "productline" },
      "aggs": {
        "avg_msrp": { "avg": { "field": "msrp" } }
      }
    }
  }
}
```

---

## Result

<EsTable>
{
  "took": 13,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 110,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "by_productline": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "Classic Cars",
          "doc_count": 38,
          "avg_msrp": {
            "value": 118.02105311343544
          }
        },
        {
          "key": "Vintage Cars",
          "doc_count": 24,
          "avg_msrp": {
            "value": 87.09583282470703
          }
        },
        {
          "key": "Motorcycles",
          "doc_count": 13,
          "avg_msrp": {
            "value": 97.17846122154823
          }
        },
        {
          "key": "Planes",
          "doc_count": 12,
          "avg_msrp": {
            "value": 89.51583321889241
          }
        },
        {
          "key": "Trucks and Buses",
          "doc_count": 11,
          "avg_msrp": {
            "value": 103.18363640525125
          }
        },
        {
          "key": "Ships",
          "doc_count": 9,
          "avg_msrp": {
            "value": 86.5633316040039
          }
        },
        {
          "key": "Trains",
          "doc_count": 3,
          "avg_msrp": {
            "value": 73.85333251953125
          }
        }
      ]
    }
  }
}

</EsTable>


---

## Sort & Pagination

- `sort` เทียบเท่า `order by` และ `from/size` เทียบเท่า `offset/limit` 
- ค่า `default` ของ `sort` โดยปกติจะเรียงตาม `_score` จากมากไปหาน้อย
- ด้านล่างคือตัวอย่างหน้า 1 ถ้าต้องการหน้า 2 ต้องเปลี่ยน `"form":3` แทน

```json
GET products/_search
{
  "query": { "match_all": {} },
  "sort": [ { "msrp": "desc" } ],
  "from": 0,
  "size": 3
}
```
---

## Result

<EsTable>
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 110,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "products",
        "_id": "S10_1949",
        "_score": null,
        "_source": {
          "productcode": "S10_1949",
          "productname": "1952 Alpine Renault 1300",
          "productscale": "1:10",
          "productvendor": "Classic Metal Creations",
          "productdescription": "Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 7305,
          "buyprice": 98.58,
          "msrp": 214.3,
          "productline": "Classic Cars"
        },
        "sort": [
          214.3
        ]
      },
      {
        "_index": "products",
        "_id": "S12_1108",
        "_score": null,
        "_source": {
          "productcode": "S12_1108",
          "productname": "2001 Ferrari Enzo",
          "productscale": "1:12",
          "productvendor": "Second Gear Diecast",
          "productdescription": "Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.",
          "quantityinstock": 3619,
          "buyprice": 95.59,
          "msrp": 207.8,
          "productline": "Classic Cars"
        },
        "sort": [
          207.8
        ]
      },
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": null,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        },
        "sort": [
          194.57
        ]
      }
    ]
  }
}

</EsTable>

---

## Fuzzy search

- การค้นหาคำที่สะกดใกล้เคียง

```json
GET products/_search
{
  "query": {
    "match": {
      "productname": { "query": "mustng", "fuzziness": "AUTO" }
    }
  }
}
```

---

## Result

<EsTable>
{
  "took": 14,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 3.5238814,
    "hits": [
      {
        "_index": "products",
        "_id": "S12_1099",
        "_score": 3.5238814,
        "_source": {
          "productcode": "S12_1099",
          "productname": "1968 Ford Mustang",
          "productscale": "1:12",
          "productvendor": "Autoart Studio Design",
          "productdescription": "Hood, doors and trunk all open to reveal highly detailed interior features. Steering wheel actually turns the front wheels. Color dark green.",
          "quantityinstock": 68,
          "buyprice": 95.34,
          "msrp": 194.57,
          "productline": "Classic Cars"
        }
      },
      {
        "_index": "products",
        "_id": "S18_2581",
        "_score": 3.163968,
        "_source": {
          "productcode": "S18_2581",
          "productname": "P-51-D Mustang",
          "productscale": "1:72",
          "productvendor": "Gearbox Collectibles",
          "productdescription": "Has retractable wheels and comes with a stand",
          "quantityinstock": 992,
          "buyprice": 49,
          "msrp": 84.48,
          "productline": "Planes"
        }
      }
    ]
  }
}

</EsTable>


---
layout: two-cols-title
---

::title::
[การนำเข้าข้อมูลจาก View products_search]{class="text-2xl"}

::left::

- สร้าง View ใน postgres

```sql
CREATE OR REPLACE VIEW ClassicModels.products_search_view AS
SELECT
    p.productCode,
    p.productName,
    p.productLine,
    p.productDescription,
    pl.textDescription AS productLineDescription
FROM ClassicModels.Products p
JOIN ClassicModels.ProductLines pl
    ON p.productLine = pl.productLine;
```


::right::

- สร้าง Index ใหม่ บน Elasticsearch

```json
PUT products_search
{
  "mappings": {
    "properties": {
      "productcode":            { "type": "keyword" },
      "productname":            { "type": "text" },
      "productline":            { "type": "keyword" },
      "productdescription":     { "type": "text" },
      "productlinedescription": { "type": "text" },
      "msrp": { "type": "float" }
    }
  }
}
```

<Download file="txt/view1.txt"/>
::default::


---

## Result

- Search `Ducati` from productlinedescription

```json
GET products_search/_search
{
  "query": {
    "match": { "productlinedescription": "Ducati" }
  }
}
```

---

## Result

<EsTable height="50dvh">
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 13,
      "relation": "eq"
    },
    "max_score": 2.0930893,
    "hits": [
      {
        "_index": "products_search",
        "_id": "S10_1678",
        "_score": 2.0930893,
        "_source": {
          "productcode": "S10_1678",
          "productname": "1969 Harley Davidson Ultimate Chopper",
          "productline": "Motorcycles",
          "productdescription": "This replica features working kickstand, front suspension, gear-shift lever, footbrake lever, drive chain, wheels and steering. All parts are particularly delicate due to their precise scale and require special care and attention.",
          "productlinedescription": "Our motorcycles are state of the art replicas of classic as well as contemporary motorcycle legends such as Harley Davidson, Ducati and Vespa. Models contain stunning details such as official logos, rotating wheels, working kickstand, front suspension, gear-shift lever, footbrake lever, and drive chain. Materials used include diecast and plastic. The models range in size from 1:10 to 1:50 scale and include numerous limited edition and several out-of-production vehicles. All models come fully assembled and ready for display in the home or office. Most include a certificate of authenticity."
        }
      },
      {
        "_index": "products_search",
        "_id": "S10_2016",
        "_score": 2.0930893,
        "_source": {
          "productcode": "S10_2016",
          "productname": "1996 Moto Guzzi 1100i",
          "productline": "Motorcycles",
          "productdescription": "Official Moto Guzzi logos and insignias, saddle bags located on side of motorcycle, detailed engine, working steering, working suspension, two leather seats, luggage rack, dual exhaust pipes, small saddle bag located on handle bars, two-tone paint with chrome accents, superior die-cast detail , rotating wheels , working kick stand, diecast metal with plastic parts and baked enamel finish.",
          "productlinedescription": "Our motorcycles are state of the art replicas of classic as well as contemporary motorcycle legends such as Harley Davidson, Ducati and Vespa. Models contain stunning details such as official logos, rotating wheels, working kickstand, front suspension, gear-shift lever, footbrake lever, and drive chain. Materials used include diecast and plastic. The models range in size from 1:10 to 1:50 scale and include numerous limited edition and several out-of-production vehicles. All models come fully assembled and ready for display in the home or office. Most include a certificate of authenticity."
        }
      },
      {
        "_index": "products_search",
        "_id": "S10_4698",
        "_score": 2.0930893,
        "_source": {
          "productcode": "S10_4698",
          "productname": "2003 Harley-Davidson Eagle Drag Bike",
          "productline": "Motorcycles",
          "productdescription": """Model features, official Harley Davidson logos and insignias, detachable rear wheelie bar, heavy diecast metal with resin parts, authentic multi-color tampo-printed graphics, separate engine drive belts, free-turning front fork, rotating tires and rear racing slick, certificate of authenticity, detailed engine, display stand\r\n, precision diecast replica, baked enamel finish, 1:10 scale model, removable fender, seat and tank cover piece for displaying the superior detail of the v-twin engine""",
          "productlinedescription": "Our motorcycles are state of the art replicas of classic as well as contemporary motorcycle legends such as Harley Davidson, Ducati and Vespa. Models contain stunning details such as official logos, rotating wheels, working kickstand, front suspension, gear-shift lever, footbrake lever, and drive chain. Materials used include diecast and plastic. The models range in size from 1:10 to 1:50 scale and include numerous limited edition and several out-of-production vehicles. All models come fully assembled and ready for display in the home or office. Most include a certificate of authenticity."
        }
      },
      {
        "_index": "products_search",
        "_id": "S12_2823",
        "_score": 2.0930893,
        "_source": {
          "productcode": "S12_2823",
          "productname": "2002 Suzuki XREO",
          "productline": "Motorcycles",
          "productdescription": "Official logos and insignias, saddle bags located on side of motorcycle, detailed engine, working steering, working suspension, two leather seats, luggage rack, dual exhaust pipes, small saddle bag located on handle bars, two-tone paint with chrome accents, superior die-cast detail , rotating wheels , working kick stand, diecast metal with plastic parts and baked enamel finish.",
          "productlinedescription": "Our motorcycles are state of the art replicas of classic as well as contemporary motorcycle legends such as Harley Davidson, Ducati and Vespa. Models contain stunning details such as official logos, rotating wheels, working kickstand, front suspension, gear-shift lever, footbrake lever, and drive chain. Materials used include diecast and plastic. The models range in size from 1:10 to 1:50 scale and include numerous limited edition and several out-of-production vehicles. All models come fully assembled and ready for display in the home or office. Most include a certificate of authenticity."
        }
      },
      {
        "_index": "products_search",
        "_id": "S18_2625",
        "_score": 2.0930893,
        "_source": {
          "productcode": "S18_2625",
          "productname": "1936 Harley Davidson El Knucklehead",
          "productline": "Motorcycles",
          "productdescription": "Intricately detailed with chrome accents and trim, official die-struck logos and baked enamel finish.",
          "productlinedescription": "Our motorcycles are state of the art replicas of classic as well as contemporary motorcycle legends such as Harley Davidson, Ducati and Vespa. Models contain stunning details such as official logos, rotating wheels, working kickstand, front suspension, gear-shift lever, footbrake lever, and drive chain. Materials used include diecast and plastic. The models range in size from 1:10 to 1:50 scale and include numerous limited edition and several out-of-production vehicles. All models come fully assembled and ready for display in the home or office. Most include a certificate of authenticity."
        }
      },
      {
        "_index": "products_search",
        "_id": "S18_3782",
        "_score": 2.0930893,
        "_source": {
          "productcode": "S18_3782",
          "productname": "1957 Vespa GS150",
          "productline": "Motorcycles",
          "productdescription": "Features rotating wheels, working kick stand. Comes with stand.",
          "productlinedescription": "Our motorcycles are state of the art replicas of classic as well as contemporary motorcycle legends such as Harley Davidson, Ducati and Vespa. Models contain stunning details such as official logos, rotating wheels, working kickstand, front suspension, gear-shift lever, footbrake lever, and drive chain. Materials used include diecast and plastic. The models range in size from 1:10 to 1:50 scale and include numerous limited edition and several out-of-production vehicles. All models come fully assembled and ready for display in the home or office. Most include a certificate of authenticity."
        }
      },
      {
        "_index": "products_search",
        "_id": "S24_1578",
        "_score": 2.0930893,
        "_source": {
          "productcode": "S24_1578",
          "productname": "1997 BMW R 1100 S",
          "productline": "Motorcycles",
          "productdescription": "Detailed scale replica with working suspension and constructed from over 70 parts",
          "productlinedescription": "Our motorcycles are state of the art replicas of classic as well as contemporary motorcycle legends such as Harley Davidson, Ducati and Vespa. Models contain stunning details such as official logos, rotating wheels, working kickstand, front suspension, gear-shift lever, footbrake lever, and drive chain. Materials used include diecast and plastic. The models range in size from 1:10 to 1:50 scale and include numerous limited edition and several out-of-production vehicles. All models come fully assembled and ready for display in the home or office. Most include a certificate of authenticity."
        }
      },
      {
        "_index": "products_search",
        "_id": "S24_2000",
        "_score": 2.0930893,
        "_source": {
          "productcode": "S24_2000",
          "productname": "1960 BSA Gold Star DBD34",
          "productline": "Motorcycles",
          "productdescription": "Detailed scale replica with working suspension and constructed from over 70 parts",
          "productlinedescription": "Our motorcycles are state of the art replicas of classic as well as contemporary motorcycle legends such as Harley Davidson, Ducati and Vespa. Models contain stunning details such as official logos, rotating wheels, working kickstand, front suspension, gear-shift lever, footbrake lever, and drive chain. Materials used include diecast and plastic. The models range in size from 1:10 to 1:50 scale and include numerous limited edition and several out-of-production vehicles. All models come fully assembled and ready for display in the home or office. Most include a certificate of authenticity."
        }
      },
      {
        "_index": "products_search",
        "_id": "S24_2360",
        "_score": 2.0930893,
        "_source": {
          "productcode": "S24_2360",
          "productname": "1982 Ducati 900 Monster",
          "productline": "Motorcycles",
          "productdescription": "Features two-tone paint with chrome accents, superior die-cast detail , rotating wheels , working kick stand",
          "productlinedescription": "Our motorcycles are state of the art replicas of classic as well as contemporary motorcycle legends such as Harley Davidson, Ducati and Vespa. Models contain stunning details such as official logos, rotating wheels, working kickstand, front suspension, gear-shift lever, footbrake lever, and drive chain. Materials used include diecast and plastic. The models range in size from 1:10 to 1:50 scale and include numerous limited edition and several out-of-production vehicles. All models come fully assembled and ready for display in the home or office. Most include a certificate of authenticity."
        }
      },
      {
        "_index": "products_search",
        "_id": "S32_1374",
        "_score": 2.0930893,
        "_source": {
          "productcode": "S32_1374",
          "productname": "1997 BMW F650 ST",
          "productline": "Motorcycles",
          "productdescription": "Features official die-struck logos and baked enamel finish. Comes with stand.",
          "productlinedescription": "Our motorcycles are state of the art replicas of classic as well as contemporary motorcycle legends such as Harley Davidson, Ducati and Vespa. Models contain stunning details such as official logos, rotating wheels, working kickstand, front suspension, gear-shift lever, footbrake lever, and drive chain. Materials used include diecast and plastic. The models range in size from 1:10 to 1:50 scale and include numerous limited edition and several out-of-production vehicles. All models come fully assembled and ready for display in the home or office. Most include a certificate of authenticity."
        }
      }
    ]
  }
}

</EsTable>

---

## Example

- Search `diecast` from productlinedescription and filter productline with `Planes`

```json
GET products_search/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "productlinedescription": "diecast" } }
      ],
      "filter": [
        { "term": { "productline": "Planes" } }
      ]
    }
  }
}
```

---

## Result

<EsTable>
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 12,
      "relation": "eq"
    },
    "max_score": 0.7337705,
    "hits": [
      {
        "_index": "products_search",
        "_id": "S18_1662",
        "_score": 0.7337705,
        "_source": {
          "productcode": "S18_1662",
          "productname": "1980s Black Hawk Helicopter",
          "productline": "Planes",
          "productdescription": "1:18 scale replica of actual Army's UH-60L BLACK HAWK Helicopter. 100% hand-assembled. Features rotating rotor blades, propeller blades and rubber wheels.",
          "productlinedescription": "Unique, diecast airplane and helicopter replicas suitable for collections, as well as home, office or classroom decorations. Models contain stunning details such as official logos and insignias, rotating jet engines and propellers, retractable wheels, and so on. Most come fully assembled and with a certificate of authenticity from their manufacturers."
        }
      },
      {
        "_index": "products_search",
        "_id": "S72_1253",
        "_score": 0.7337705,
        "_source": {
          "productcode": "S72_1253",
          "productname": "Boeing X-32A JSF",
          "productline": "Planes",
          "productdescription": "10 inches Wingspan with retractable landing gears.Comes with pilot",
          "productlinedescription": "Unique, diecast airplane and helicopter replicas suitable for collections, as well as home, office or classroom decorations. Models contain stunning details such as official logos and insignias, rotating jet engines and propellers, retractable wheels, and so on. Most come fully assembled and with a certificate of authenticity from their manufacturers."
        }
      },
      {
        "_index": "products_search",
        "_id": "S18_2581",
        "_score": 0.7337705,
        "_source": {
          "productcode": "S18_2581",
          "productname": "P-51-D Mustang",
          "productline": "Planes",
          "productdescription": "Has retractable wheels and comes with a stand",
          "productlinedescription": "Unique, diecast airplane and helicopter replicas suitable for collections, as well as home, office or classroom decorations. Models contain stunning details such as official logos and insignias, rotating jet engines and propellers, retractable wheels, and so on. Most come fully assembled and with a certificate of authenticity from their manufacturers."
        }
      },
      {
        "_index": "products_search",
        "_id": "S24_1785",
        "_score": 0.7337705,
        "_source": {
          "productcode": "S24_1785",
          "productname": "1928 British Royal Navy Airplane",
          "productline": "Planes",
          "productdescription": "Official logos and insignias",
          "productlinedescription": "Unique, diecast airplane and helicopter replicas suitable for collections, as well as home, office or classroom decorations. Models contain stunning details such as official logos and insignias, rotating jet engines and propellers, retractable wheels, and so on. Most come fully assembled and with a certificate of authenticity from their manufacturers."
        }
      },
      {
        "_index": "products_search",
        "_id": "S24_2841",
        "_score": 0.7337705,
        "_source": {
          "productcode": "S24_2841",
          "productname": "1900s Vintage Bi-Plane",
          "productline": "Planes",
          "productdescription": "Hand crafted diecast-like metal bi-plane is re-created in about 1:24 scale of antique pioneer airplane. All hand-assembled with many different parts. Hand-painted in classic yellow and features correct markings of original airplane.",
          "productlinedescription": "Unique, diecast airplane and helicopter replicas suitable for collections, as well as home, office or classroom decorations. Models contain stunning details such as official logos and insignias, rotating jet engines and propellers, retractable wheels, and so on. Most come fully assembled and with a certificate of authenticity from their manufacturers."
        }
      },
      {
        "_index": "products_search",
        "_id": "S24_3949",
        "_score": 0.7337705,
        "_source": {
          "productcode": "S24_3949",
          "productname": "Corsair F4U ( Bird Cage)",
          "productline": "Planes",
          "productdescription": "Has retractable wheels and comes with a stand. Official logos and insignias.",
          "productlinedescription": "Unique, diecast airplane and helicopter replicas suitable for collections, as well as home, office or classroom decorations. Models contain stunning details such as official logos and insignias, rotating jet engines and propellers, retractable wheels, and so on. Most come fully assembled and with a certificate of authenticity from their manufacturers."
        }
      },
      {
        "_index": "products_search",
        "_id": "S24_4278",
        "_score": 0.7337705,
        "_source": {
          "productcode": "S24_4278",
          "productname": "1900s Vintage Tri-Plane",
          "productline": "Planes",
          "productdescription": "Hand crafted diecast-like metal Triplane is Re-created in about 1:24 scale of antique pioneer airplane. This antique style metal triplane is all hand-assembled with many different parts.",
          "productlinedescription": "Unique, diecast airplane and helicopter replicas suitable for collections, as well as home, office or classroom decorations. Models contain stunning details such as official logos and insignias, rotating jet engines and propellers, retractable wheels, and so on. Most come fully assembled and with a certificate of authenticity from their manufacturers."
        }
      },
      {
        "_index": "products_search",
        "_id": "S700_1691",
        "_score": 0.7337705,
        "_source": {
          "productcode": "S700_1691",
          "productname": "American Airlines: B767-300",
          "productline": "Planes",
          "productdescription": "Exact replia with official logos and insignias and retractable wheels",
          "productlinedescription": "Unique, diecast airplane and helicopter replicas suitable for collections, as well as home, office or classroom decorations. Models contain stunning details such as official logos and insignias, rotating jet engines and propellers, retractable wheels, and so on. Most come fully assembled and with a certificate of authenticity from their manufacturers."
        }
      },
      {
        "_index": "products_search",
        "_id": "S700_2466",
        "_score": 0.7337705,
        "_source": {
          "productcode": "S700_2466",
          "productname": "America West Airlines B757-200",
          "productline": "Planes",
          "productdescription": "Official logos and insignias. Working steering system. Rotating jet engines",
          "productlinedescription": "Unique, diecast airplane and helicopter replicas suitable for collections, as well as home, office or classroom decorations. Models contain stunning details such as official logos and insignias, rotating jet engines and propellers, retractable wheels, and so on. Most come fully assembled and with a certificate of authenticity from their manufacturers."
        }
      },
      {
        "_index": "products_search",
        "_id": "S700_2834",
        "_score": 0.7337705,
        "_source": {
          "productcode": "S700_2834",
          "productname": "ATA: B757-300",
          "productline": "Planes",
          "productdescription": "Exact replia with official logos and insignias and retractable wheels",
          "productlinedescription": "Unique, diecast airplane and helicopter replicas suitable for collections, as well as home, office or classroom decorations. Models contain stunning details such as official logos and insignias, rotating jet engines and propellers, retractable wheels, and so on. Most come fully assembled and with a certificate of authenticity from their manufacturers."
        }
      }
    ]
  }
}

</EsTable>

---
layout: two-cols-title
---

::title::
[การนำข้อมูลเข้าจาก View custoemr_orders_view]{class="text-2xl"}

::left::

- สร้าง View ใน postgres

```sql
CREATE OR REPLACE VIEW ClassicModels.customer_orders_view AS
SELECT
    o.orderNumber,
    o.orderDate,
    o.status,
    o.comments,
    c.customerNumber,
    c.customerName,
    c.country
FROM ClassicModels.Orders o
JOIN ClassicModels.Customers c
    ON o.customerNumber = c.customerNumber;
```

::right::

- สร้าง Index ใหม่ บน Elasticsearch

```json
PUT customer_orders_view
{
  "mappings": {
    "properties": {
      "ordernumber":    { "type": "keyword" },
      "orderdate":      { "type": "date" },
      "status":         { "type": "keyword" },
      "comments":       { "type": "text" },
      "customernumber": { "type": "keyword" },
      "customername":   { "type": "text" },
      "country":        { "type": "keyword" }
    }
  }
}
```

<Download file="txt/view2.txt"/>

::default::


---

## Search order that contains `shipping` in `comments`

```json
GET customer_orders_view/_search
{
  "query": {
    "match": { "comments": "shipping" }
  }
}
```

---

## Result

<EsTable>
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 17,
      "relation": "eq"
    },
    "max_score": 1.9931043,
    "hits": [
      {
        "_index": "customer_orders_view",
        "_id": "10178",
        "_score": 1.9931043,
        "_source": {
          "ordernumber": 10178,
          "orderdate": "2003-11-08T00:00",
          "status": "Shipped",
          "comments": "Custom shipping instructions sent to warehouse",
          "customernumber": 242,
          "customername": "Alpha Cognac",
          "country": "France"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10284",
        "_score": 1.9931043,
        "_source": {
          "ordernumber": 10284,
          "orderdate": "2004-08-21T00:00",
          "status": "Shipped",
          "comments": "Custom shipping instructions sent to warehouse",
          "customernumber": 299,
          "customername": "Norway Gifts By Mail, Co.",
          "country": "Norway  "
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10382",
        "_score": 1.9931043,
        "_source": {
          "ordernumber": 10382,
          "orderdate": "2005-02-17T00:00",
          "status": "Shipped",
          "comments": "Custom shipping instructions sent to warehouse",
          "customernumber": 124,
          "customername": "Mini Gifts Distributors Ltd.",
          "country": "USA"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10421",
        "_score": 1.919103,
        "_source": {
          "ordernumber": 10421,
          "orderdate": "2005-05-29T00:00",
          "status": "In Process",
          "comments": "Custom shipping instructions were sent to warehouse",
          "customernumber": 124,
          "customername": "Mini Gifts Distributors Ltd.",
          "country": "USA"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10254",
        "_score": 1.7864461,
        "_source": {
          "ordernumber": 10254,
          "orderdate": "2004-06-03T00:00",
          "status": "Shipped",
          "comments": "Customer requested that DHL is used for this shipping",
          "customernumber": 323,
          "customername": "Down Under Souveniers, Inc",
          "country": "New Zealand"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10319",
        "_score": 1.7864461,
        "_source": {
          "ordernumber": 10319,
          "orderdate": "2004-11-03T00:00",
          "status": "Shipped",
          "comments": "Customer requested that DHL is used for this shipping",
          "customernumber": 456,
          "customername": "Microscale Inc.",
          "country": "USA"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10336",
        "_score": 1.7864461,
        "_source": {
          "ordernumber": 10336,
          "orderdate": "2004-11-20T00:00",
          "status": "Shipped",
          "comments": "Customer requested that DHL is used for this shipping",
          "customernumber": 172,
          "customername": "La Corne D'abondance, Co.",
          "country": "France"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10358",
        "_score": 1.7864461,
        "_source": {
          "ordernumber": 10358,
          "orderdate": "2004-12-10T00:00",
          "status": "Shipped",
          "comments": "Customer requested that DHL is used for this shipping",
          "customernumber": 141,
          "customername": "Euro+ Shopping Channel",
          "country": "Spain"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10400",
        "_score": 1.7864461,
        "_source": {
          "ordernumber": 10400,
          "orderdate": "2005-04-01T00:00",
          "status": "Shipped",
          "comments": "Customer requested that DHL is used for this shipping",
          "customernumber": 450,
          "customername": "The Sharp Gifts Warehouse",
          "country": "USA"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10413",
        "_score": 1.7864461,
        "_source": {
          "ordernumber": 10413,
          "orderdate": "2005-05-05T00:00",
          "status": "Shipped",
          "comments": "Customer requested that DHL is used for this shipping",
          "customernumber": 175,
          "customername": "Gift Depot Inc.",
          "country": "USA"
        }
      }
    ]
  }
}

</EsTable>


--- 

## Search order that is not shipped and comments contains 'shipping'

```json
GET customer_orders_view/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "comments": "shipping" } }
      ],
      "filter": [
        { "term": { "status": "In Process" } }
      ]
    }
  }
}
```

---

## Result

<EsTable>{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.919103,
    "hits": [
      {
        "_index": "customer_orders_view",
        "_id": "10421",
        "_score": 1.919103,
        "_source": {
          "ordernumber": 10421,
          "orderdate": "2005-05-29T00:00",
          "status": "In Process",
          "comments": "Custom shipping instructions were sent to warehouse",
          "customernumber": 124,
          "customername": "Mini Gifts Distributors Ltd.",
          "country": "USA"
        }
      }
    ]
  }
}

</EsTable>

---

## Search query and aggregations

```json
GET customer_orders_view/_search
{
  "query": { "match_all": {} },
  "aggs": {
    "by_status": {
      "terms": { "field": "status" }
    }
  }
}
```

---

## Result

<EsTable>
{
  "took": 8,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 326,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "customer_orders_view",
        "_id": "10100",
        "_score": 1,
        "_source": {
          "ordernumber": 10100,
          "orderdate": "2003-01-06T00:00",
          "status": "Shipped",
          "customernumber": 363,
          "customername": "Online Diecast Creations Co.",
          "country": "USA"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10101",
        "_score": 1,
        "_source": {
          "ordernumber": 10101,
          "orderdate": "2003-01-09T00:00",
          "status": "Shipped",
          "comments": "Check on availability.",
          "customernumber": 128,
          "customername": "Blauer See Auto, Co.",
          "country": "Germany"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10102",
        "_score": 1,
        "_source": {
          "ordernumber": 10102,
          "orderdate": "2003-01-10T00:00",
          "status": "Shipped",
          "customernumber": 181,
          "customername": "Vitachrome Inc.",
          "country": "USA"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10103",
        "_score": 1,
        "_source": {
          "ordernumber": 10103,
          "orderdate": "2003-01-29T00:00",
          "status": "Shipped",
          "customernumber": 121,
          "customername": "Baane Mini Imports",
          "country": "Norway"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10104",
        "_score": 1,
        "_source": {
          "ordernumber": 10104,
          "orderdate": "2003-01-31T00:00",
          "status": "Shipped",
          "customernumber": 141,
          "customername": "Euro+ Shopping Channel",
          "country": "Spain"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10105",
        "_score": 1,
        "_source": {
          "ordernumber": 10105,
          "orderdate": "2003-02-11T00:00",
          "status": "Shipped",
          "customernumber": 145,
          "customername": "Danish Wholesale Imports",
          "country": "Denmark"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10106",
        "_score": 1,
        "_source": {
          "ordernumber": 10106,
          "orderdate": "2003-02-17T00:00",
          "status": "Shipped",
          "customernumber": 278,
          "customername": "Rovelli Gifts",
          "country": "Italy"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10107",
        "_score": 1,
        "_source": {
          "ordernumber": 10107,
          "orderdate": "2003-02-24T00:00",
          "status": "Shipped",
          "comments": "Difficult to negotiate with customer. We need more marketing materials",
          "customernumber": 131,
          "customername": "Land of Toys Inc.",
          "country": "USA"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10108",
        "_score": 1,
        "_source": {
          "ordernumber": 10108,
          "orderdate": "2003-03-03T00:00",
          "status": "Shipped",
          "customernumber": 385,
          "customername": "Cruz & Sons Co.",
          "country": "Philippines"
        }
      },
      {
        "_index": "customer_orders_view",
        "_id": "10109",
        "_score": 1,
        "_source": {
          "ordernumber": 10109,
          "orderdate": "2003-03-10T00:00",
          "status": "Shipped",
          "comments": "Customer requested that FedEx Ground is used for this shipping",
          "customernumber": 486,
          "customername": "Motor Mint Distributors Inc.",
          "country": "USA"
        }
      }
    ]
  },
  "aggregations": {
    "by_status": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "Shipped",
          "doc_count": 303
        },
        {
          "key": "Cancelled",
          "doc_count": 6
        },
        {
          "key": "In Process",
          "doc_count": 6
        },
        {
          "key": "On Hold",
          "doc_count": 4
        },
        {
          "key": "Resolved",
          "doc_count": 4
        },
        {
          "key": "Disputed",
          "doc_count": 3
        }
      ]
    }
  }
}

</EsTable>

---
layout: two-cols-title
---

::title::
[Demo Faceted Search]{class="text-2xl"}
- สร้างหน้าค้นหาเลียนแบบเวบ shopping เช่น ลูกค้าพิมพ์คำว่า "chrome" ในช่องค้นหา แล้วเลื่อน slider เลือกราคา 60-150

::left::

```json
GET products_search/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "productdescription": "chrome" } }
      ],
      "filter": [
        { "range": { "msrp": { "gte": 60, "lte": 150 } } }
      ]
    }
  },
```
::right::

```json
  "aggs": {
    "by_productline": {
      "terms": { "field": "productline" }
    },
    "price_ranges": {
      "range": {
        "field": "msrp",
        "ranges": [
          { "to": 70 },
          { "from": 70, "to": 120 },
          { "from": 120 }
        ]
      }
    }
  }
}
```

::default::



---


# Result

<EsFacetedSearch height="350px">
{
  "took": 3,
  "hits": {
    "total": {
      "value": 11,
      "relation": "eq"
    },
    "hits": [
      {
        "_score": 2.9941463,
        "_source": {
          "productcode": "S18_2957",
          "productname": "1934 Ford V8 Coupe",
          "productline": "Vintage Cars",
          "msrp": 62.46
        }
      }
    ]
  },
  "aggregations": {
    "by_productline": {
      "buckets": [
        {
          "key": "Vintage Cars",
          "doc_count": 6
        },
        {
          "key": "Motorcycles",
          "doc_count": 4
        },
        {
          "key": "Classic Cars",
          "doc_count": 1
        }
      ]
    },
    "price_ranges": {
      "buckets": [
        {
          "key": "*-70.0",
          "to": 70,
          "doc_count": 4
        },
        {
          "key": "70.0-120.0",
          "from": 70,
          "to": 120,
          "doc_count": 6
        },
        {
          "key": "120.0-*",
          "from": 120,
          "doc_count": 1
        }
      ]
    }
  }
}
</EsFacetedSearch>